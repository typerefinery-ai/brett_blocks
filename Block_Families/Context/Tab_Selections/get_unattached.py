
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
# Contact Email: denis@cloudaccelerator.co
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
# This code is licensed under the terms of the BSD.
##############################################################################

from stixorm.module.authorise import import_type_factory
import json

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
key_list = ["start", "impact", "event", "other", "relations"]


def get_unattached():
    show_sro = True
    task_index = {}
    # 1. Setup variables
    nodes = []
    edges = []
    relations = []
    relation_edges = []
    relation_replacement_edges = []
    unattached = {}
    # 2. open files and fill lists
    if os.path.exists(TR_Context_Memory_Dir + refs["unattached"]):
        with open(TR_Context_Memory_Dir + refs["unattached"], "r") as mem_input:
            nodes = json.load(mem_input)
    if os.path.exists(TR_Context_Memory_Dir + refs["edges"]):
        with open(TR_Context_Memory_Dir + refs["edges"], "r") as mem_input:
            edges = json.load(mem_input)
    if os.path.exists(TR_Context_Memory_Dir + refs["relations"]):
        with open(TR_Context_Memory_Dir + refs["relations"], "r") as mem_input:
            relations = json.load(mem_input)
    if os.path.exists(TR_Context_Memory_Dir + refs["relation_edges"]):
        with open(TR_Context_Memory_Dir + refs["relation_edges"], "r") as mem_input:
            relation_edges = json.load(mem_input)
    if os.path.exists(TR_Context_Memory_Dir + refs["relation_replacement_edges"]):
        with open(TR_Context_Memory_Dir + refs["relation_replacement_edges"], "r") as mem_input:
            relation_replacement_edges = json.load(mem_input)
    # 3. sort sightings by time
    node_ids = [x['id'] for x in nodes]
    for rel in relations:
        if rel["source_ref"] in node_ids and rel["target_ref"] in node_ids:
            if show_sro:
                nodes.append(rel)
                for edge in relation_edges:
                    if edge["source"] == rel["id"]:
                        edges.append(edge)
            else:
                for edge in relation_replacement_edges:
                    if edge["source"] == rel["source_ref"] and edge["target"] == rel["target_ref"]:
                        edges.append(edge)

    for edge in edges:
        if edge["source"] in node_ids and edge["target"] in node_ids:
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