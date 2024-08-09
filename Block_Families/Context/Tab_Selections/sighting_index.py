
################################################################################
## header start                                                               ##
################################################################################
# allow importing og service local packages
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
# Title: When Sighting tab selected, get data
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
# One Outpute
# 1. Sighting Hierarchy
#
# This code is licensed under the terms of the BSD.
##############################################################################

from stixorm.module.authorise import import_type_factory
import json
import copy

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
key_list = ["start", "sequence", "impact", "event", "task", "other"]


def get_sighting_index():
    sighting_index = {}
    # 1. Setup variables
    sightings = []
    SDO = []
    SCO = []
    relationship = []
    auth_factory = get_auth_factory_instance()
    auth = auth_factory.get_auth_for_import(import_type)
    auth_types = copy.deepcopy(auth["types"])
    # 2. open "others" list file, and split it into chunks
    if os.path.exists(TR_Context_Memory_Dir + refs["other"]):
        with open(TR_Context_Memory_Dir + refs["other"], "r") as mem_input:
            stix_others_list = json.load(mem_input)
            for stix_obj in stix_others_list:
                if stix_obj["type"] == "sighting":
                    sightings.append(stix_obj)
                elif stix_obj["type"] in auth_types["sdo"]:
                    SDO.append(stix_obj)
                elif stix_obj["type"] in auth_types["sco"]:
                    SCO.append(stix_obj)
                elif stix_obj["type"] == "relationship":
                    relationship.append(stix_obj)
                else:
                    return {"result": "error, type is unknown"}
    total_obs_components = SCO + relationship
    # 3. sort sightings by time
    if sightings != []:
        sorted_list = sorted(sightings, key=lambda t: datetime.strptime(t["original"]["created"], "%Y-%m-%dT%H:%M:%S.%fZ"))
        sighting_index["name"] = "Evidence List"
        sighting_index["icon"] = "sighting-generic"
        sighting_index["type"] = ""
        sighting_index["heading"] = "Evidence List"
        sighting_index["description"] = "list of sightings"
        sighting_index["edge"] = ""
        sighting_index["id"] = ""
        sighting_index["children"] = []
        children = sighting_index["children"]
        # 4. Process each sighting and place them into the children
        for sorted_obj in sorted_list:
            # 4A. First setup the sighting object
            level1 = {}
            level1 = sorted_obj
            level1["edge"] = "other_object_refs"
            level1["children"] = []
            children1 = level1["children"]
            sighting_of = ""
            observed = []
            where = []
            created_by_ref = ""
            if "sighting_of_ref" in sorted_obj["original"]:
                sighting_of = sorted_obj["original"]["sighting_of_ref"]
            if "observed_data_refs" in sorted_obj["original"]:
                observed = sorted_obj["original"]["observed_data_refs"]
            if "where_sighted_refs" in sorted_obj["original"]:
                where_sighted = sorted_obj["original"]["where_sighted_refs"]
            if "created_by_ref" in sorted_obj["original"]:
                created_by_ref = sorted_obj["original"]["created_by_ref"]
            for sdo_obj in SDO:
                if sighting_of != "" and sighting_of == sdo_obj["id"]:
                    sight = {}
                    sight = sdo_obj
                    sight["edge"] = "sighting_of_ref"
                    children1.append(sight)
                elif where_sighted != "" and sdo_obj["id"] in where_sighted:
                    where_obj = {}
                    where_obj = sdo_obj
                    where_obj["edge"] = "where_sighted_refs"
                    children1.append(where_obj)
                elif observed != [] and sdo_obj["id"] in observed:
                    observe = {}
                    observe = sdo_obj
                    observe["edge"] = "observed_data_refs"
                    observe["children"] = []
                    children2 = observe["children"]
                    for obs_comp in total_obs_components:
                        if obs_comp["id"] in sdo_obj["original"]["object_refs"]:
                            children2.append(obs_comp)
                    children1.append(observe)
                elif created_by_ref != "" and sdo_obj["id"] == created_by_ref:
                    created_by_obj = {}
                    created_by_obj = sdo_obj
                    created_by_obj["edge"] = "observed_data_refs"
                    children1.append(created_by_obj)
            children.append(level1)

    else:
        return sighting_index

    return sighting_index


def main(inputfile, outputfile):
    context_type = None
    stix_object = None
    if os.path.exists(inputfile):
        with open(inputfile, "r") as script_input:
            input = json.load(script_input)

    # setup logger for execution
    hierarchy = get_sighting_index()

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