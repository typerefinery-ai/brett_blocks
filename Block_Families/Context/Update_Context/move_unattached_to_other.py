
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
# Title: Move "Unattached" to "Other" Context Memory
# Author: OS-Threat
# Organisation Repo: https://github.com/typerefinery-ai/brett_blocks
# Contact Email: denis@cloudaccelerator.co
# Date: 07/08/2023
#
# Description: This script is designed to take in a Stix Object ID
#       and return a Stix object
#
# One Mandatory Input:
# 1. Stix_list
# One Outpute
# 1. Context Return
#
# This code is licensed under the terms of the BSD.
##############################################################################

from stixorm.module.authorise import import_type_factory
import json
from Block_Families.General._library.convert_n_and_e import convert_relns, convert_sighting, convert_node

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
key_list = ["start", "sequence", "impact", "event", "task", "other"]


def add_node(node, context_type):
    exists = False
    stix_nodes_list = []
    if os.path.exists(TR_Context_Memory_Dir + refs[context_type]):
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


def del_node(node_id, context_type):
    exists = False
    stix_nodes_list = []
    if os.path.exists(TR_Context_Memory_Dir + refs[context_type]):
        with open(TR_Context_Memory_Dir + refs[context_type], "r") as mem_input:
            stix_nodes_list = json.load(mem_input)
            for i in range(len(stix_nodes_list)):
                #print(f"i->{i}, len->{len(stix_nodes_list)} node {stix_nodes_list[i]}")
                if stix_nodes_list[i]["id"] == node_id:
                    del stix_nodes_list[i]
                    print(f"delete element {i}, node id {node_id}")
                    break
    with open(TR_Context_Memory_Dir + refs[context_type], 'w') as f:
        f.write(json.dumps(stix_nodes_list))


def move_unattached_to_other(stix_list):
    # 2. Check basic directory exits
    if not os.path.exists(TR_Context_Memory_Dir):
        os.makedirs(TR_Context_Memory_Dir)
    if not os.path.exists(TR_Context_Memory_Dir + "/company_1"):
        os.makedirs(TR_Context_Memory_Dir + "/company_1")
    if not os.path.exists(TR_Context_Memory_Dir + "/incident_1"):
        os.makedirs(TR_Context_Memory_Dir + "/incident_1")

    # 4. for each object receieved, add it to the Other List, and remove it from the Unattached List
    report_id = []
    for stix_obj in stix_list:
        # if file exists, replce existing object if it exists, else add it, else create the list and add it
        if stix_obj["type"] == "relationship":
            nodes, edges, relation_edges, relation_replacement_edges = convert_relns(stix_obj)
            add_node(nodes[0], "other")
            del_node(stix_obj["id"], "unattached")
            report_id.append(stix_obj["id"])
        elif stix_obj["type"] == "sighting":
            nodes, edges = convert_sighting(stix_obj)
            add_node(nodes[0], "other")
            del_node(stix_obj["id"], "unattached")
            report_id.append(stix_obj["id"])
        else:
            nodes, edges = convert_node(stix_obj)
            add_node(nodes[0], "other")
            del_node(stix_obj["id"], "unattached")
            report_id.append(stix_obj["id"])

    return " transferred from 'Unattached' to 'Other' -> " + str(report_id)


def main(inputfile, outputfile):
    context_type = None
    stix_object = None
    if os.path.exists(inputfile):
        with open(inputfile, "r") as script_input:
            input = json.load(script_input)
    if "stix_list" in input:
        stix_list = input["stix_list"]

    # setup logger for execution
    result_string = move_unattached_to_other(stix_list)
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