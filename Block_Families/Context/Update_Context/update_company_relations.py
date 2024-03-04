
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
# Title: Update Company Relations
# Author: OS-Threat
# Organisation Repo: https://github.com/typerefinery-ai/brett_blocks
# Contact Email: denis@cloudaccelerator.co
# Date: 07/08/2023
#
# Description: This script is designed to take in a Stix Object ID
#       and return a Stix object
#
# One Mandatory Input:
# 1. Trigger
# Report Outpute
# 1. Report (string)
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
from stixorm.module.definitions.stix21 import (
    Relationship
)
from Block_Families.General._library.convert_n_and_e import convert_relns, convert_sighting, convert_node, \
    refine_edges, generate_legend
from stixorm.module.authorise import import_type_factory
from posixpath import basename
import json
import os

import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

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
identity_types = ["me", "team", "users", "assets", "systems"]
edge_types = ["edges", "relation_edges", "relation_replacement_edges"]

from datetime import datetime

def convert_dt(dt_stamp_string):
    if dt_stamp_string.find(".") >0:
        dt = datetime.strptime(dt_stamp_string, "%Y-%m-%dT%H:%M:%S.%fZ")
        microsecs = dt.microsecond
        milisecs = (round(microsecs / 1000))
        dt_list = dt_stamp_string.split('.')
        actual = dt_list[0] + "." + str(milisecs) + "Z"
    else:
        if dt_stamp_string.find("T") > 0:
            dt_list = dt_stamp_string.split('T')
            t_list = dt_list[1].split(':')
            if len(t_list) == 3:
                secs = t_list[2]
                sec_list = secs.split('Z')
                actual = dt_list[0] + "T" + t_list[0] + ":" + t_list[1] + ":" + sec_list[0] + ".000Z"
            else:
                mins = t_list[1]
                mins_list = mins.split('Z')
                actual = dt_list[0] + "T" + t_list[0] + ":" + mins_list[0] + ":00.000Z"
        else:
            actual = dt_stamp_string + "T00:00:00.000Z"
    return actual

def conv(stix_object):
    # Convert Stix Object to valid Python dict
    if type(stix_object) is dict:
        return stix_object
    string_dict = stix_object.serialize()
    jdict = json.loads(string_dict)
    time_list = ["created", "modified"]
    for tim in time_list:
        if tim in jdict:
            temp_string = convert_dt(jdict[tim])
            jdict[tim] = temp_string
    return jdict

def add_node(node, context_type):
    exists = False
    stix_nodes_list = []
    if os.path.exists(TR_Context_Memory_Dir + local[context_type]):
        with open(TR_Context_Memory_Dir + local[context_type], "r") as mem_input:
            stix_nodes_list = json.load(mem_input)
            for i in range(len(stix_nodes_list)):
                if stix_nodes_list[i]["id"] == node["id"]:
                    stix_nodes_list[i] = node
                    exists = True
            if not exists:
                stix_nodes_list.append(node)
    else:
        stix_nodes_list = [node]
    with open(TR_Context_Memory_Dir + local[context_type], 'w') as f:
        f.write(json.dumps(stix_nodes_list))


def add_edge(edge, context_type):
    exists = False
    stix_edge_list = []
    if os.path.exists(TR_Context_Memory_Dir + local[context_type]):
        with open(TR_Context_Memory_Dir + local[context_type], "r") as mem_input:
            stix_edge_list = json.load(mem_input)
            for i in range(len(stix_edge_list)):
                if stix_edge_list[i]["source"] == edge["source"] and stix_edge_list[i]["target"] == edge["target"]:
                    stix_edge_list[i] = edge
                    exists = True
            if not exists:
                stix_edge_list.append(edge)
    else:
        stix_edge_list = [edge]
    with open(TR_Context_Memory_Dir + local[context_type], 'w') as f:
        f.write(json.dumps(stix_edge_list))



def add_relation_to_context_memory(nodes, edges, relation_edges, relation_replacement_edges ):
    add_node(nodes[0], "relations")
    for edge in edges:
        add_edge(edge, "edges")
    for edge in relation_edges:
        add_edge(edge, "relation_edges")
    for edge in relation_replacement_edges:
        add_edge(edge, "relation_replacement_edges")


def update_company_relations(reln_type=None):
    # 1. Extract the components of the object
    Paths = {}
    Object_lists = {}
    Object_ID_Lists = {}
    company = {}
    relation_list = []
    Paths["me"] = TR_Context_Memory_Dir + local["me"]
    Paths["team"] = TR_Context_Memory_Dir + local["team"]
    Paths["users"] = TR_Context_Memory_Dir + local["users"]
    Paths["company"] = TR_Context_Memory_Dir + local["company"]
    Paths["assets"] = TR_Context_Memory_Dir + local["assets"]
    Paths["systems"] = TR_Context_Memory_Dir + local["systems"]
    Paths["relations"] = TR_Context_Memory_Dir + local["relations"]
    Paths["edges"] = TR_Context_Memory_Dir + local["edges"]
    Paths["relation_edges"] = TR_Context_Memory_Dir + local["relation_edges"]
    Paths["relation_replacement_edges"] = TR_Context_Memory_Dir + local["relation_replacement_edges"]

    # 2. Open All the Files that may contain identities first, then the company and then the relations
    for context in identity_types:
        if os.path.exists(Paths[context]):
            with open(Paths[context], "r") as mem_input:
                Object_lists[context] = json.load(mem_input)
        else:
            Object_lists[context] = []
    if os.path.exists(Paths["company"]):
        with open(Paths["company"], "r") as mem_input:
            Object_lists["company"] = json.load(mem_input)
            company = Object_lists["company"][0]
    else:
        Object_lists["company"] = []
        company = {}
    if os.path.exists(Paths["relations"]):
        with open(Paths["relations"], "r") as mem_input:
            Object_lists["relations"] = json.load(mem_input)
    else:
        Object_lists["relations"] = []

    for edg in edge_types:
        if os.path.exists(Paths[edg]):
            with open(Paths[edg], "r") as mem_input:
                Object_lists[edg] = json.load(mem_input)
        else:
            Object_lists[edg] = []

    # 3. Setup Existing List of Existing ID's in Relations
    source_id_list = [x["source_ref"] for x in Object_lists["relations"]]
    target_id_list = [x["target_ref"] for x in Object_lists["relations"]]
    total_id_list = source_id_list + target_id_list
    # 4. Setup reduce lists of objects, that aren't in SRO's
    for context in identity_types:
            Object_lists[context] = [x for x in Object_lists[context] if x["type"] == "identity" and x["id"] not in total_id_list]

    # 5. if Me exists, or Team setup, then setup relationship_type
    reln_ids = []
    if company:
        if Object_lists["me"] and reln_type:
            me_ident = Object_lists["me"][0]
            temp_rel = Relationship(relationship_type=reln_type, source_ref=company["id"], target_ref=me_ident["id"])
            nodes, edges, relation_edges, relation_replacement_edges = convert_relns(conv(temp_rel))
            add_relation_to_context_memory(nodes, edges, relation_edges, relation_replacement_edges)
            reln_ids.append(nodes[0]["id"])
        if Object_lists["team"] !=  []: # and reln_type:
            for team_ident in Object_lists["team"]:
                temp_rel = Relationship(relationship_type=reln_type, source_ref=company["id"], target_ref=team_ident["id"])
                nodes, edges, relation_edges, relation_replacement_edges = convert_relns(conv(temp_rel))
                add_relation_to_context_memory(nodes, edges, relation_edges, relation_replacement_edges)
                reln_ids.append(nodes[0]["id"])
        if Object_lists["users"] != []:
            for team_ident in Object_lists["users"]:
                temp_rel = Relationship(relationship_type='employed-by', source_ref=company["id"], target_ref=team_ident["id"])
                nodes, edges, relation_edges, relation_replacement_edges = convert_relns(conv(temp_rel))
                add_relation_to_context_memory(nodes, edges, relation_edges, relation_replacement_edges)
                reln_ids.append(nodes[0]["id"])
        if Object_lists["assets"] != []:
            for team_ident in Object_lists["assets"]:
                temp_rel = Relationship(relationship_type='asset-of', source_ref=company["id"], target_ref=team_ident["id"])
                nodes, edges, relation_edges, relation_replacement_edges = convert_relns(conv(temp_rel))
                add_relation_to_context_memory(nodes, edges, relation_edges, relation_replacement_edges)
                reln_ids.append(nodes[0]["id"])
        if Object_lists["systems"] != []:
            for team_ident in Object_lists["systems"]:
                temp_rel = Relationship(relationship_type='system-of', source_ref=company["id"], target_ref=team_ident["id"])
                nodes, edges, relation_edges, relation_replacement_edges = convert_relns(conv(temp_rel))
                add_relation_to_context_memory(nodes, edges, relation_edges, relation_replacement_edges)
                reln_ids.append(nodes[0]["id"])

    # does file exist
    return_string = ""
    for reln_id in reln_ids:
        return_string += "\n" + reln_id
    return " relations saved -> " + str(return_string)


def main(inputfile, outputfile):
    if os.path.exists(inputfile):
        with open(inputfile, "r") as script_input:
            input = json.load(script_input)
    reln_type = input["reln_type"]

    # setup logger for execution
    result_string = update_company_relations(reln_type)
    context_result = {}
    context_result["update_company_relations_result"] = result_string

    with open(outputfile, "w") as outfile:
        json.dump(context_result, outfile)


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