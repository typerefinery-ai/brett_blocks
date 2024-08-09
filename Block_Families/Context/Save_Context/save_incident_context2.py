
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
# Title: Save Context
# Author: OS-Threat
# Organisation Repo: https://github.com/typerefinery-ai/brett_blocks
# Contact Email: denis@cloudaccelerator.co
# Date: 07/08/2023
#
# Description: This script is designed to take in a Stix Object ID
#       and return a Stix object
#
# One Mandatory Input:
# 1. Context
# One Output
# 1. Context Return
#
#
# This code is licensed under the terms of the BSD.
##############################################################################

from stixorm.module.authorise import import_type_factory
# from Block_Families.General._library.
from Orchestration.Common.convert_n_and_e import convert_relns, convert_sighting, convert_node
import json

import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

import_type = import_type_factory.get_all_imports()

TR_Context_Memory_Dir = "./Context_Mem"
TR_Common_Files = "./Common_Files"
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
field_names = {
    "start" : "sequence_start_refs",
    "sequence" : "sequence_refs",
    "impact" : "impact_refs",
    "event" : "event_refs",
    "task" : "task_refs",
    "other" : "other_object_refs"
}
key_list = ["start", "sequence", "impact", "event", "task", "other"]


def add_node(node, context_type):
    exists = False
    stix_nodes_list = []
    if  os.path.exists(TR_Context_Memory_Dir + refs[context_type]):
        with open(TR_Context_Memory_Dir + refs[context_type], "r") as mem_input:
            stix_nodes_list = json.load(mem_input)
            for i in range(len(stix_nodes_list)):
                if stix_nodes_list[i]["id"] == node["id"]:
                    stix_nodes_list[i] = node
                    exists = True
            if not exists:
                stix_nodes_list.append(node)
    else:
        stix_nodes_list = [node]
    with open(TR_Context_Memory_Dir + refs[context_type], 'w') as f:
        f.write(json.dumps(stix_nodes_list))


def add_edge(edge, context_type):
    exists = False
    stix_edge_list = []
    if os.path.exists(TR_Context_Memory_Dir + refs[context_type]):
        with open(TR_Context_Memory_Dir + refs[context_type], "r") as mem_input:
            stix_edge_list = json.load(mem_input)
            for i in range(len(stix_edge_list)):
                if stix_edge_list[i]["source"] == edge["source"] and stix_edge_list[i]["target"] == edge["target"]:
                    stix_edge_list[i] = edge
                    exists = True
            if not exists:
                stix_edge_list.append(edge)
    else:
        stix_edge_list = [edge]
    with open(TR_Context_Memory_Dir + refs[context_type], 'w') as f:
        f.write(json.dumps(stix_edge_list))


def save_context(stix_object, context_type):
    # 0 Check for "original"
    wrapped = False
    exists = False
    # if "original" in stix_object:
    #     wrapped = True
    # 1. Extract the components of the object
    TR_Context_Incident = TR_Context_Memory_Dir + refs["incident"]

    if context_type:
        TR_Context_Filename = TR_Context_Memory_Dir + refs[context_type]
    else:
        return "context_type unknown " + str(context_type)

    # does directory exits
    if not os.path.exists(TR_Common_Files):
        os.makedirs(TR_Common_Files)
    if not os.path.exists(TR_Context_Memory_Dir):
        os.makedirs(TR_Context_Memory_Dir)
    if not os.path.exists(TR_Context_Memory_Dir + "/company_1"):
        os.makedirs(TR_Context_Memory_Dir + "/company_1")
    if not os.path.exists(TR_Context_Memory_Dir + "/incident_1"):
        os.makedirs(TR_Context_Memory_Dir + "/incident_1")

    # does file exist
    stix_nodes_list = []
    incident = {}
    if stix_object["type"] == "relationship":
        if wrapped:
            add_node(stix_object["original"], context_type)
        else:
            nodes, edges, relation_edges, relation_replacement_edges = convert_relns(stix_object)
            add_node(nodes[0], "relations")
            for edge in edges:
                add_edge(edge, "edges")
            for edge in relation_edges:
                add_edge(edge, "relation_edges")
            for edge in relation_replacement_edges:
                add_edge(edge, "relation_replacement_edges")

    elif stix_object["type"] == "sighting":
        if wrapped:
            add_node(stix_object["original"], context_type)
        else:
            nodes, edges = convert_sighting(stix_object)
            add_node(nodes[0], "other")
            for edge in edges:
                add_edge(edge, "edges")
    else:
        # its a node-type of object
        if context_type != "incident":
            if wrapped:
                add_node(stix_object["original"], context_type)
            else:
                # if file exists, replce existing object if it exists, else add it, else create the list and add it
                nodes, edges = convert_node(stix_object)
                add_node(nodes[0], context_type)
                for edge in edges:
                    add_edge(edge, "edges")

        else:
            # first, update all of the id lists on the incident object
            for key in key_list:
                if os.path.exists(TR_Context_Memory_Dir + refs[key]):
                    with open(TR_Context_Memory_Dir + refs[key], "r") as list_input:
                        stix_list = json.load(list_input)
                        if key == "other":
                            # if we are filling the "other" list then add in the relations
                            if os.path.exists(TR_Context_Memory_Dir + refs["relations"]):
                                with open(TR_Context_Memory_Dir + refs[key], "r") as list2_input:
                                    stix_list2 = json.load(list2_input)
                                    stix_list = stix_list + stix_list2
                        stix_id_list = [x["id"] for x in stix_list]
                        # does the stix_object already appear in the list?
                        stix_object[field_names[key]] = stix_id_list
                else:
                    # list is empty
                    stix_object[field_names[key]] = []

            # create the nodes and edges
            if wrapped:
                add_node(stix_object["original"], context_type)
            else:
                nodes, edges = convert_node(stix_object)
                add_node(nodes[0], context_type)
                for edge in edges:
                    add_edge(edge, "edges")

    return " incident context saved -> " + str(context_type) + " stix_id -> " + str(stix_object["id"])


def main(inputfile, outputfile):
    context_type = None
    stix_object = None
    if os.path.exists(inputfile):
        with open(inputfile, "r") as script_input:
            input = json.load(script_input)
    stix_object = input["stix_object"]
    if "context_type" in input:
        context_type = input["context_type"]

    # setup logger for execution
    result_string = save_context(stix_object, context_type["context_type"])
    context_result = {}
    context_result["context_result"] = result_string
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