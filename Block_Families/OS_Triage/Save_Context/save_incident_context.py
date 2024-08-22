
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
# Title: Save OS_Triage
# Author: OS-Threat
# Organisation Repo: https://github.com/typerefinery-ai/brett_blocks
# Contact Email: denis@cloudaccelerator.co
# Date: 07/08/2023
#
# Description: This script is designed to take in a Stix Object ID
#       and return a Stix object
#
# One Mandatory Input:
# 1. OS_Triage
# One Output
# 1. OS_Triage Return
#
#
# This code is licensed under the terms of the BSD.
##############################################################################

from stixorm.module.authorise import import_type_factory
# from Block_Families.General._library.
# from Orchestration.Common.
from urllib.request import urlretrieve
import json
import sys
import importlib.util
import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
import os
import_type = import_type_factory.get_all_imports()

# Common File Stuff
TR_Common_Files = "./generated/OS-Triage/Common_Files"
common = [
    {"module": "convert_n_and_e", "file": "convert_n_and_e.py", "url" : "https://raw.githubusercontent.com/typerefinery-ai/brett_blocks/main/Block_Families/General/_library/convert_n_and_e.py"}
]

# OS_Triage Memory Stuff
TR_Context_Memory_Dir = "./generated/OS-Triage/Context_Mem"
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

def download_common(module_list):
    for module in module_list:
        # Step 1: download the module
        result = urlretrieve(module["url"], TR_Common_Files + "/" + module["file"])
        print(f'common file result ->', result)
        # Step 2: install the module



def add_node(node, context_dir, context_type):
    exists = False
    stix_nodes_list = []
    if  os.path.exists(context_dir + incident_data[context_type]):
        with open(context_dir + incident_data[context_type], "r") as mem_input:
            stix_nodes_list = json.load(mem_input)
            for i in range(len(stix_nodes_list)):
                if stix_nodes_list[i]["id"] == node["id"]:
                    stix_nodes_list[i] = node
                    exists = True
            if not exists:
                stix_nodes_list.append(node)
    else:
        stix_nodes_list = [node]
    with open(context_dir + incident_data[context_type], 'w') as f:
        f.write(json.dumps(stix_nodes_list))


def add_edge(edge, context_dir, context_type):
    exists = False
    stix_edge_list = []
    if os.path.exists(context_dir + incident_data[context_type]):
        with open(context_dir + incident_data[context_type], "r") as mem_input:
            stix_edge_list = json.load(mem_input)
            for i in range(len(stix_edge_list)):
                if stix_edge_list[i]["source"] == edge["source"] and stix_edge_list[i]["target"] == edge["target"]:
                    stix_edge_list[i] = edge
                    exists = True
            if not exists:
                stix_edge_list.append(edge)
    else:
        stix_edge_list = [edge]
    with open(context_dir + incident_data[context_type], 'w') as f:
        f.write(json.dumps(stix_edge_list))


def save_context(stix_object, context_type):
    # 0 Check for "original"
    wrapped = False
    exists = False
    # if "original" in stix_object:
    #     wrapped = True
    # 1.B Find Current Incident directory
    local_map = {}
    with open(TR_Context_Memory_Dir + "/" + context_map, "r") as current_context:
        local_map = json.load(current_context)
        current_incident_dir = local_map["current_incident"]
        TR_Incident_Context_Dir = TR_Context_Memory_Dir + "/" + current_incident_dir
        # 1. Extract the components of the object
        TR_Context_Incident = TR_Incident_Context_Dir + incident_data["incident"]

        if context_type:
            TR_Context_Filename = TR_Context_Incident + incident_data[context_type]
        else:
            return "context_type unknown " + str(context_type)

        # 2. Check if the key directories exist, if not make them, and download common files
        if not os.path.exists(TR_Common_Files):
            os.makedirs(TR_Common_Files)
            download_common(common)
        if not os.path.exists(TR_Context_Memory_Dir):
            os.makedirs(TR_Context_Memory_Dir)
        if not os.path.exists(TR_Context_Memory_Dir + "/usr"):
            os.makedirs(TR_Context_Memory_Dir + "/usr")
        # if not os.path.exists(TR_Context_Memory_Dir + "/incident_1"):
        #     os.makedirs(TR_Context_Memory_Dir + "/incident_1")

        # 3. Now we are sure the common files exist, we need to import them
        # Specify the path to the Nodes and Edges module
        module_path = TR_Common_Files + '/' + common[0]["file"]
        # Load the module spec using importlib.util.spec_from_file_location
        spec = importlib.util.spec_from_file_location('n_and_e', module_path)
        # Create the module from the specification
        n_and_e = importlib.util.module_from_spec(spec)
        # Load the module
        spec.loader.exec_module(n_and_e)
        # 4. Depending on Object Tupe, Get the Nodes and Edges, and save them to the lists
        stix_nodes_list = []
        incident = {}
        if stix_object["type"] == "relationship":
            if wrapped:
                add_node(stix_object["original"], TR_Incident_Context_Dir, context_type)
            else:
                nodes, edges, relation_edges, relation_replacement_edges = n_and_e.convert_relns(stix_object)
                add_node(nodes[0],TR_Incident_Context_Dir, "relations")
                for edge in edges:
                    add_edge(edge, TR_Incident_Context_Dir, "edges")
                for edge in relation_edges:
                    add_edge(edge, TR_Incident_Context_Dir, "relation_edges")
                for edge in relation_replacement_edges:
                    add_edge(edge, TR_Incident_Context_Dir, "relation_replacement_edges")

        elif stix_object["type"] == "sighting":
            if wrapped:
                add_node(stix_object["original"], context_type)
            else:
                nodes, edges = n_and_e.convert_sighting(stix_object)
                add_node(nodes[0], TR_Incident_Context_Dir, "other")
                for edge in edges:
                    add_edge(edge, TR_Incident_Context_Dir, "edges")
        else:
            # its a node-type of object
            if context_type != "incident":
                if wrapped:
                    add_node(stix_object["original"], TR_Incident_Context_Dir, context_type)
                else:
                    # if file exists, replce existing object if it exists, else add it, else create the list and add it
                    nodes, edges = n_and_e.convert_node(stix_object)
                    add_node(nodes[0], TR_Incident_Context_Dir, context_type)
                    for edge in edges:
                        add_edge(edge, TR_Incident_Context_Dir, "edges")

            else:
                # first, update all of the id lists on the incident object
                for key in key_list:
                    if os.path.exists(TR_Incident_Context_Dir + incident_data[key]):
                        with open(TR_Incident_Context_Dir + incident_data[key], "r") as list_input:
                            stix_list = json.load(list_input)
                            if key == "other":
                                # if we are filling the "other" list then add in the relations
                                if os.path.exists(TR_Incident_Context_Dir + incident_data["relations"]):
                                    with open(TR_Incident_Context_Dir + incident_data[key], "r") as list2_input:
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
                    nodes, edges = n_and_e.convert_node(stix_object)
                    add_node(nodes[0], context_type)
                    for edge in edges:
                        add_edge(edge, "edges")

    return " incident context saved -> " + str(context_type) + "\nstix_id -> " + str(stix_object["id"])


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