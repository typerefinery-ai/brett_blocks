
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
# Title: Save Incident Context
# Author: OS-Threat
# Organisation Repo: https://github.com/typerefinery-ai/brett_blocks
# Contact Email: brett@osthreat.com
# Date: 07/08/2023
#
# Description: This script is designed to take in a Stix Object ID
#       and return a Stix object
#
# One Mandatory Input:
# 1. Stix-type Object
# 2. Context Type
# One Output
# 1. Context Memory Return Message
#
#
# This code is licensed under the terms of the Apache 2.
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
    "behavior" : "/behavior_refs.json",
    "other" : "/other_object_refs.json",
    "unattached" : "/unattached_objs.json",
    "unattached_relations" : "/unattached_relation.json",
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

def process_node(stix_object, context_key, context_dir, n_and_e):
    if "original" in stix_object:
        add_node(stix_object, context_key)
    else:
        nodes, edges = n_and_e.convert_node(stix_object)
        add_node(nodes[0], context_dir, context_key)
        for edge in edges:
            add_edge(edge, context_dir, "edges")


def save_context(stix_object, context_type):
    # 0 Check for "original"
    wrapped = False
    exists = False
    if "original" in stix_object:
        wrapped = True
    # 1.B Find Current Incident directory
    local_map = {}
    with open(TR_Context_Memory_Dir + "/" + context_map, "r") as current_context:
        local_map = json.load(current_context)
        # 1. Setup the incident context directory
        current_incident_dir = local_map["current_incident"]
        TR_Incident_Context_Dir = TR_Context_Memory_Dir + "/" + current_incident_dir

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
                add_node(stix_object, TR_Incident_Context_Dir, "relations")
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
                add_node(stix_object, "other")
            else:
                nodes, edges = n_and_e.convert_sighting(stix_object)
                add_node(nodes[0], TR_Incident_Context_Dir, "other")
                for edge in edges:
                    add_edge(edge, TR_Incident_Context_Dir, "edges")
        else:
            # its a node-type of object
            if stix_object["type"] == "sequence":
                if stix_object["step_type"] == "start_step":
                    if wrapped:
                        add_node(stix_object, "start")
                    else:
                        nodes, edges = n_and_e.convert_node(stix_object)
                        add_node(nodes[0], TR_Incident_Context_Dir, "start")
                        for edge in edges:
                            add_edge(edge, TR_Incident_Context_Dir, "edges")
                else:
                    if wrapped:
                        add_node(stix_object, "sequence")
                    else:
                        nodes, edges = n_and_e.convert_node(stix_object)
                        add_node(nodes[0], TR_Incident_Context_Dir, "sequence")
                        for edge in edges:
                            add_edge(edge, TR_Incident_Context_Dir, "edges")
            elif stix_object["type"] == "task":
                if wrapped:
                    add_node(stix_object, "task")
                else:
                    nodes, edges = n_and_e.convert_node(stix_object)
                    add_node(nodes[0], TR_Incident_Context_Dir, "task")
                    for edge in edges:
                        add_edge(edge, TR_Incident_Context_Dir, "edges")
            elif stix_object["type"] == "event":
                if wrapped:
                    add_node(stix_object, "event")
                else:
                    nodes, edges = n_and_e.convert_node(stix_object)
                    add_node(nodes[0], TR_Incident_Context_Dir, "event")
                    for edge in edges:
                        add_edge(edge, TR_Incident_Context_Dir, "edges")
            elif stix_object["type"] == "impact":
                if wrapped:
                    add_node(stix_object, "impact")
                else:
                    nodes, edges = n_and_e.convert_node(stix_object)
                    add_node(nodes[0], TR_Incident_Context_Dir, "impact")
                    for edge in edges:
                        add_edge(edge, TR_Incident_Context_Dir, "edges")
            elif stix_object["type"] != "incident":
                if wrapped:
                    add_node(stix_object, "other")
                else:
                    nodes, edges = n_and_e.convert_node(stix_object)
                    add_node(nodes[0], TR_Incident_Context_Dir, "other")
                    for edge in edges:
                        add_edge(edge, TR_Incident_Context_Dir, "edges")
            else:
                # It is an Incident, so first, update all of the id lists on the incident object
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
                    add_node(stix_object, "incident")
                else:
                    nodes, edges = n_and_e.convert_node(stix_object)
                    add_node(nodes[0], "incident")
                    for edge in edges:
                        add_edge(edge, "edges")

    return " incident context saved - \nstix_id -> " + str(stix_object["id"])


def main(inputfile, outputfile):
    context_type_string = ""
    stix_object = None
    if os.path.exists(inputfile):
        with open(inputfile, "r") as script_input:
            input_data = json.load(script_input)
            print(f"input data->{input_data}")
            if "stix_object" in input_data:
                stix_object = input_data["stix_object"]
                if "context_type" in input_data:
                    context_type_string = input_data["context_type"]["context_type"]
                print(f"from ports \nstix_object->{stix_object}\ncontext type->{context_type_string}")
                result_string = save_context(stix_object, context_type_string)
            elif "api" in input_data:
                api_input_data = input_data["api"]
                stix_object = api_input_data["stix_object"]
                if "context_type" in api_input_data:
                    context_type_string = api_input_data["context_type"]["context_type"]
                print(f"api \nstix_object->{stix_object}\ncontext type->{context_type_string}")
                result_string = save_context(stix_object, context_type_string)

            # setup logger for execution

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