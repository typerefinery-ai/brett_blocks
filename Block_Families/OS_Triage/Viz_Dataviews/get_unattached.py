
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
# Title: When any tab is selected, get all of the unattached
# Author: OS-Threat
# Organisation Repo: https://github.com/typerefinery-ai/brett_blocks
# Contact Email: brett@osthreat.com
# Date: 07/08/2023
#
# Description: This script is designed to take in a Stix Object ID
#       and return a Stix object
#
# No Input:
# 1.
# One Output
# 1. Unattached nodes and edges
#
# This code is licensed under the terms of the Apache 2.
##############################################################################

from stixorm.module.authorise import import_type_factory
import json
from typing import Dict, Union, List

import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

import_type = import_type_factory.get_all_imports()


# Common File Stuff
TR_Common_Files = "./generated/os-triage/common_files"
common = [
    {"module": "parse", "file": "parse.py", "url" : "https://raw.githubusercontent.com/typerefinery-ai/brett_blocks/refs/heads/main/Block_Families/General/_library/parse.py"}
]
# OS_Triage Memory Stuff
TR_Context_Memory_Dir = "./generated/os-triage/context_mem"
TR_User_Dir = "/usr"
context_map = "context_map.json"
user_data = {
    "global": "/global_variables_dict.json",
    "me": "/cache_me.json",
    "team": "/cache_team.json"
}
comp_data = {
    "users": "/users.json",
    "company" : "/company.json",
    "platforms" : "/platforms.json",
    "systems" : "/systems.json"
}
incident_data = {
    "incident" : "/incident.json",
    "start" : "/sequence_start_refs.json",
    "sequence" : "/sequence_refs.json",
    "impact" : "/impact_refs.json",
    "event" : "/event_refs.json",
    "task" : "/task_refs.json",
    "other" : "/other_object_refs.json",
    "unattached" : "/unattached_objs.json"
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

def create_edge(edge_label, source_id, target_id, edge_type)-> Dict[str, str]:
    edge = {}
    edge["source"] = source_id
    edge["target"] = target_id
    edge["name"] = edge_label.replace("_", "-")
    edge["type"] = edge_type
    return edge

def generate_nodes_and_edges(nodes):
    edges = []
    
    node_ids = [x['id'] for x in nodes]
    print(f"node ids->{node_ids}")
    for node in nodes:
        node_id = node["id"]
        references = node["references"]
        for edge_label, edge_list in references.items():
            for edge_id in edge_list:
                if edge_id in node_ids:
                    if node["type"] == "relationship" and (edge_label == "source_ref" or edge_label == "target_ref"):
                        edges.append(create_edge(node["original"]["relationship_type"], node_id, edge_id, "relationship"))
                    else:
                        edges.append(create_edge(edge_label, node_id, edge_id, "edge"))

    return nodes, edges


def get_unattached():
    show_sro = True
    unattached = {}
    # 1. Setup variables
    nodes = []
    edges = []

    # 1.B Find Current Incident directory
    local_map = {}
    with open(TR_Context_Memory_Dir + "/" + context_map, "r") as current_context:
        local_map = json.load(current_context)
        current_incident_dir = local_map["current_incident"]
        TR_Incident_Context_Dir = TR_Context_Memory_Dir + "/" + current_incident_dir
        # 2. open files and fill lists
        if os.path.exists(TR_Incident_Context_Dir + incident_data["unattached"]):
            with open(TR_Incident_Context_Dir + incident_data["unattached"], "r") as mem_input:
                nodes = json.load(mem_input)        # load unattached nodes list
                nodes, edges = generate_nodes_and_edges(nodes)

    unattached['nodes'] = nodes
    unattached['edges'] = edges
    return unattached


def main(inputfile, outputfile):
    context_type = None
    stix_object = None
    if os.path.exists(inputfile):
        with open(inputfile, "r") as script_input:
            input = json.load(script_input)

    # setup logger for execution
    unattached = get_unattached()

    with open(outputfile, "w") as outfile:
        json.dump(unattached, outfile)


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