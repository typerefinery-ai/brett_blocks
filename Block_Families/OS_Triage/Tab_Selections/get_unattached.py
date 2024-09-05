
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

import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

import_type = import_type_factory.get_all_imports()

# Common File Stuff
TR_Common_Files = "./generated/os-triage/common_files"
common = [
    {"module": "convert_n_and_e", "file": "convert_n_and_e.py", "url" : "https://raw.githubusercontent.com/typerefinery-ai/brett_blocks/main/Block_Families/General/_library/convert_n_and_e.py"}
]

# OS_Triage Memory Stuff
TR_Context_Memory_Dir = "./generated/os-triage/context_mem"
TR_User_Dir = "/usr"
context_map = "context_map.json"
user_data = {
    "global": "/global_variables_dict.json",
    "me": "/cache_me.json",
    "team": "/cache_team.json",
    "relations" : "/relations.json",
    "edges" : "/edges.json",
    "relation_edges" : "/relation_edges.json",
    "relation_replacement_edges" : "/relation_replacement_edges.json"
}
comp_data = {
    "users": "/users.json",
    "company" : "/company.json",
    "assets" : "/assets.json",
    "systems" : "/systems.json",
    "relations" : "/relations.json",
    "edges" : "/edges.json",
    "relation_edges" : "/relation_edges.json",
    "relation_replacement_edges" : "/relation_replacement_edges.json"
}
incident_data = {
    "incident" : "/incident.json",
    "start" : "/sequence_start_refs.json",
    "sequence" : "/sequence_refs.json",
    "impact" : "/impact_refs.json",
    "event" : "/event_refs.json",
    "task" : "/task_refs.json",
    "other" : "/other_object_refs.json",
    "unattached" : "/unattached_objs.json",
    "relations" : "/incident_relations.json",
    "edges" : "/incident_edges.json",
    "relation_edges" : "/relation_edges.json",
    "relation_replacement_edges" : "/relation_replacement_edges.json"
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


def get_unattached():
    show_sro = True
    task_index = {}
    # 1. Setup variables
    nodes = []
    edges = []
    inc_edges = []
    inc_nodes = []
    relations = []
    relation_edges = []
    relation_replacement_edges = []
    unattached = {}
    # 1.B Find Current Incident directory
    local_map = {}
    with open(TR_Context_Memory_Dir + "/" + context_map, "r") as current_context:
        local_map = json.load(current_context)
        current_incident_dir = local_map["current_incident"]
        TR_Incident_Context_Dir = TR_Context_Memory_Dir + "/" + current_incident_dir
        # 2. open files and fill lists
        if os.path.exists(TR_Incident_Context_Dir + incident_data["unattached"]):
            with open(TR_Incident_Context_Dir + incident_data["unattached"], "r") as mem_input:
                inc_nodes = json.load(mem_input)
        if os.path.exists(TR_Incident_Context_Dir + incident_data["edges"]):
            with open(TR_Incident_Context_Dir + incident_data["edges"], "r") as mem_input:
                inc_edges = json.load(mem_input)
        if os.path.exists(TR_Incident_Context_Dir + incident_data["relations"]):
            with open(TR_Incident_Context_Dir + incident_data["relations"], "r") as mem_input:
                relations = json.load(mem_input)
        if os.path.exists(TR_Incident_Context_Dir + incident_data["relation_edges"]):
            with open(TR_Incident_Context_Dir + incident_data["relation_edges"], "r") as mem_input:
                relation_edges = json.load(mem_input)
        if os.path.exists(TR_Incident_Context_Dir + incident_data["relation_replacement_edges"]):
            with open(TR_Incident_Context_Dir + incident_data["relation_replacement_edges"], "r") as mem_input:
                relation_replacement_edges = json.load(mem_input)
        # 3. sort sightings by time
        nodes = inc_nodes
        node_ids = [x['id'] for x in nodes]
        print(f"node ids->{node_ids}")
        for rel in relations:
            if rel["original"]["source_ref"] in node_ids and rel["original"]["target_ref"] in node_ids:
                if show_sro:
                    nodes.append(rel)
                    for edge in relation_edges:
                        if edge["source"] == rel["id"]:
                            print(f"relation_edges->{edge}")
                            edges.append(edge)
                else:
                    for edge in relation_replacement_edges:
                        if edge["source"] == rel["original"]["source_ref"] and edge["target"] == rel["original"]["target_ref"]:
                            print(f"relation_replacement_edges->{edge}")
                            edges.append(edge)

        for edge in inc_edges:
            if edge["source"] in node_ids and edge["target"] in node_ids:
                print(f"edges->{edge}")
                edges.append(edge)
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