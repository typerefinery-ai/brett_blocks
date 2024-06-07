
################################################################################
## header start                                                               ##
################################################################################
# allow importing og service local packages
import os
import sys
import os.path

where_am_i = os.path.dirname(os.path.abspath(__file__))
# sys.path.insert(0, os.environ["APP_SERVICE_PACKAGES_PATH"])
# sys.path.append(where_am_i)
# end of local package imports
################################################################################
## header end                                                                 ##
################################################################################


################################################################################
## body start                                                                 ##
################################################################################

##############################################################################
# Title: When Impact tab selected, get data
# Author: OS-Threat
# Organisation Repo: https://github.com/typerefinery-ai/brett_blocks
# Contact Email: denis@cloudaccelerator.co
# Date: 07/08/2023
#
# Description: This script is designed to take in a Stix Object ID
#       and return a Stix object
#
# No Input:
# 1.
# One Output
# 1. Sighting Hierarchy
#
# This code is licensed under the terms of the BSD.
##############################################################################

from stixorm.module.definitions.os_threat import (
    StateChangeObject, EventCoreExt, Event, ImpactCoreExt,
    Availability, Confidentiality, External, Integrity, Monetary, Physical,
    Traceability, Impact, IncidentScoreObject, IncidentCoreExt, TaskCoreExt,
    Task, SightingEvidence, Sequence, SequenceExt, ContactNumber, EmailContact,
    SocialMediaContact, IdentityContact, AnecdoteExt, Anecdote,
    SightingAnecdote, SightingAlert, SightingContext, SightingExclusion,
    SightingEnrichment, SightingHunt, SightingFramework, SightingExternal
)
from stixorm.module.authorise import import_type_factory
from posixpath import basename
import json
import os
import copy
from Block_Families.General._library.convert_n_and_e import convert_relns, convert_sighting, convert_node, \
    refine_edges, generate_legend

import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

from datetime import datetime
from stixorm.module.typedb_lib.factories.auth_factory import get_auth_factory_instance
import_type = import_type_factory.get_all_imports()

TR_Context_Memory_Dir = "./Context_Mem"
local = {
    "global": "/global_variables_dict.json",
    "me" : "/cache_me.json",
    "team" : "/cache_team.json",
    "users": "/company_1/users.json",
    "company" : "/company_1/company.json",
    "assets" : "/company_1/assets.json",
    "systems" : "/company_1/systems.json",
    "relations" : "/company_1/relations.json",
    "edges" : "/company_1/edges.json",
    "relation_edges" : "/company_1/relation_edges.json",
    "relation_replacement_edges" : "/company_1/relation_replacement_edges.json"
}
refs = {
    "incident" : "/incident_1/incident.json",
    "start" : "/incident_1/sequence_start_refs.json",
    "sequence" : "/incident_1/sequence_refs.json",
    "impact" : "/incident_1/impact_refs.json",
    "event" : "/incident_1/event_refs.json",
    "task" : "/incident_1/task_refs.json",
    "other" : "/incident_1/other_object_refs.json",
    "unattached" : "/incident_1/unattached_objs.json",
    "relations" : "/incident_1/incident_relations.json",
    "edges" : "/incident_1/incident_edges.json",
    "relation_edges" : "/incident_1/relation_edges.json",
    "relation_replacement_edges" : "/incident_1/relation_replacement_edges.json"
}
key_list = ["start", "impact", "other", "task", "relations"]


def get_impact_index():
    show_sro = True
    impact_index = {}
    # 1. Setup variables
    impacts = []
    possible = []
    relations = []
    stix_incident_id = ""
    auth_factory = get_auth_factory_instance()
    auth = auth_factory.get_auth_for_import(import_type)
    auth_types = copy.deepcopy(auth["types"])
    # 2. open "others" list file, and split it into chunks
    if os.path.exists(TR_Context_Memory_Dir + refs["incident"]):
        with open(TR_Context_Memory_Dir + refs["incident"], "r") as mem_input:
            stix_incident_obj = json.load(mem_input)
            stix_incident_id = stix_incident_obj[0]["id"]
    if os.path.exists(TR_Context_Memory_Dir + refs["impact"]):
        with open(TR_Context_Memory_Dir + refs["impact"], "r") as mem_input:
            stix_impact_list = json.load(mem_input)
            for stix_obj in stix_impact_list:
                if stix_obj["type"] == "impact":
                    impacts.append(stix_obj)
                else:
                    return {"result": "error, type is not impact"}
    for key in key_list:
        if os.path.exists(TR_Context_Memory_Dir + refs[key]):
            with open(TR_Context_Memory_Dir + refs[key], "r") as mem_input:
                stix_obj_list = json.load(mem_input)
                if key == "relations":
                    relations = stix_obj_list
                else:
                    possible = possible + stix_obj_list
    # 3. sort sightings by time
    if impacts != []:
        sorted_list = sorted(impacts, key=lambda t: datetime.strptime(t["original"]["created"], "%Y-%m-%dT%H:%M:%S.%fZ"))
        impact_index["name"] = "Impact List"
        impact_index["icon"] = "impact"
        impact_index["type"] = ""
        impact_index["heading"] = "Impact List"
        impact_index["description"] = "List of Impacts for this Incident"
        impact_index["edge"] = ""
        impact_index["id"] = ""
        impact_index["children"] = []
        children = impact_index["children"]
        # 4. Process each sighting and place them into the children
        for sorted_obj in sorted_list:
            # 4A. First setup the sighting object
            level1 = {}
            level1 = sorted_obj
            level1["edge"] = "impact_refs"
            temp_list = []
            created_by_ref = ""
            impacted_refs = []
            superseded_by_ref = ""
            if "impacted_refs" in sorted_obj["original"]:
                impacted_refs = sorted_obj["original"]["impacted_refs"]
            if "created_by_ref" in sorted_obj["original"]:
                created_by_ref = sorted_obj["original"]["created_by_ref"]
            if "superseded_by_ref" in sorted_obj["original"]:
                superseded_by_ref = sorted_obj["original"]["superseded_by_ref"]
            for obj in possible:
                if created_by_ref != "" and obj["id"] == created_by_ref:
                    created_by_obj = {}
                    created_by_obj = obj
                    created_by_obj["edge"] = "created_by_ref"
                    temp_list.append(created_by_obj)
                elif obj["id"] in impacted_refs:
                    impacted_obj = {}
                    impacted_obj = obj
                    impacted_obj["edge"] = "impacted_refs"
                    temp_list.append(impacted_obj)
                elif obj["id"] == superseded_by_ref:
                    superseded_obj = {}
                    superseded_obj = obj
                    superseded_obj["edge"] = "superseded_by_ref"
                    temp_list.append(superseded_obj)
            for reln in relations:
                if sorted_obj["id"] == reln["original"]["source_ref"] and reln["original"]["target_ref"] != stix_incident_id:
                    if show_sro:
                        show_sro = {}
                        show_sro = reln
                        show_sro["edge"] = reln["relationship_type"]
                        show_sro["children"] = []
                        children2 = show_sro["children"]
                        for obj in possible:
                            if obj["id"] == reln["original"]["target_ref"]:
                                sub_obj = {}
                                sub_obj = obj
                                sub_obj["edge"] = reln["relationship_type"]
                                children2.append(sub_obj)
                        temp_list.append(show_sro)
                    else:
                        for obj in possible:
                            if obj["id"] == reln["original"]["target_ref"]:
                                sub_obj = {}
                                sub_obj = obj
                                sub_obj["edge"] = reln["relationship_type"]
                                temp_list.append(sub_obj)
                elif sorted_obj["id"] == reln["original"]["target_ref"] and reln["original"]["source_ref"] != stix_incident_id:
                    if show_sro:
                        show_sro = {}
                        show_sro = reln
                        show_sro["edge"] = reln["relationship_type"]
                        show_sro["children"] = []
                        children2 = show_sro["children"]
                        for obj in possible:
                            if obj["id"] == reln["original"]["source_ref"]:
                                sub_obj = {}
                                sub_obj = obj
                                sub_obj["edge"] = reln["relationship_type"]
                                children2.append(sub_obj)
                        temp_list.append(show_sro)
                    else:
                        for obj in possible:
                            if obj["id"] == reln["original"]["source_ref"]:
                                sub_obj = {}
                                sub_obj = obj
                                sub_obj["edge"] = reln["relationship_type"]
                                temp_list.append(sub_obj)

            if temp_list != []:
                level1["children"] = temp_list
            children.append(level1)

    else:
        return impact_index

    return impact_index


def main(inputfile, outputfile):
    context_type = None
    stix_object = None
    if os.path.exists(inputfile):
        with open(inputfile, "r") as script_input:
            input = json.load(script_input)

    # setup logger for execution
    hierarchy = get_impact_index()

    with open(outputfile, "w") as outfile:
        json.dump(hierarchy, outfile)


################################################################################
## body end                                                                   ##
################################################################################


################################################################################
## footer start                                                               ##
################################################################################
import argparse
import os


def getArgs():

  parser = argparse.ArgumentParser(description="Script params",
                                formatter_class=argparse.ArgumentDefaultsHelpFormatter)
  parser.add_argument("inputfile", nargs='?', default=f"{os.path.basename(__file__)}.input", help="input file (default: %(default)s)")
  parser.add_argument("outputfile", nargs='?', default=f"{os.path.basename(__file__)}.output", help="output file (default: %(default)s)")
  return parser.parse_args()

if __name__ == '__main__':
  args = getArgs()
  # setup logger for init
  # log = Logger
  # log.remove()
  # log.add(f'{os.path.basename(__file__)}.log', level="INFO")
  # log.info(args)
  main(args.inputfile, args.outputfile)


################################################################################
## footer end                                                                 ##
################################################################################