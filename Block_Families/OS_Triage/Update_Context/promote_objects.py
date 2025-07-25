
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
# Title: Promote Objects
# Author: OS-Threat
# Organisation Repo: https://github.com/typerefinery-ai/brett_blocks
# Contact Email: denis@cloudaccelerator.co
# Date: 07/08/2023
#
# Description: This block takes a sub-graph of nodes from "Unattached" to OS_Triage Memory
#
# One Mandatory Input:
# 1. Stix_list
# One Outpute
# 1. OS_Triage Return
#
# This code is licensed under the terms of the BSD.
##############################################################################

from stixorm.module.authorise import import_type_factory
import json

import importlib.util
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


def add_node(node, context_dir, context_type):
    exists = False
    stix_nodes_list = []
    if os.path.exists(context_dir + incident_data[context_type]):
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


def del_node(node_id, context_dir, context_type):
    exists = False
    stix_nodes_list = []
    if os.path.exists(context_dir + incident_data[context_type]):
        with open(context_dir + incident_data[context_type], "r") as mem_input:
            stix_nodes_list = json.load(mem_input)
            for i in range(len(stix_nodes_list)):
                #print(f"i->{i}, len->{len(stix_nodes_list)} node {stix_nodes_list[i]}")
                if stix_nodes_list[i]["id"] == node_id:
                    del stix_nodes_list[i]
                    print(f"delete element {i}, node id {node_id}")
                    break
    with open(context_dir + incident_data[context_type], 'w') as f:
        f.write(json.dumps(stix_nodes_list))


def promote_objects(stix_list):
    # 1.B Find Current Incident directory
    local_map = {}
    wrapped = False
    exists = False
    with open(TR_Context_Memory_Dir + "/" + context_map, "r") as current_context:
        local_map = json.load(current_context)
        current_incident_dir = local_map["current_incident"]
        TR_Incident_Context_Dir = TR_Context_Memory_Dir + "/" + current_incident_dir
        # 1. Extract the components of the object
        TR_Context_Incident = TR_Incident_Context_Dir + incident_data["incident"]
        # 2. Check basic directory exits
        if not os.path.exists(TR_Context_Memory_Dir):
            os.makedirs(TR_Context_Memory_Dir)
        # if not os.path.exists(TR_Context_Memory_Dir + "/company_1"):
        #     os.makedirs(TR_Context_Memory_Dir + "/company_1")
        # if not os.path.exists(TR_Context_Memory_Dir + "/incident_1"):
        #     os.makedirs(TR_Context_Memory_Dir + "/incident_1")
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

        # 4. for each object receieved, add it to the Other List, and remove it from the Unattached List
        report_id = []
        for stix_obj in stix_list:
            if "original" in stix_obj:
                wrapped = True
            if stix_obj["type"] == "relationship":
                if wrapped:
                    add_node(stix_obj, TR_Incident_Context_Dir, "relations")
                else:
                    nodes, edges, relation_edges, relation_replacement_edges = n_and_e.convert_relns(stix_obj)
                    add_node(nodes[0],TR_Incident_Context_Dir, "relations")
                    del_node(stix_obj["id"],TR_Incident_Context_Dir, "unattached")
                    report_id.append(stix_obj["id"])
    
            elif stix_obj["type"] == "sighting":
                if wrapped:
                    add_node(stix_obj, "other")
                else:
                    nodes, edges = n_and_e.convert_sighting(stix_obj)
                    add_node(nodes[0], TR_Incident_Context_Dir, "other")
                    del_node(stix_obj["id"],TR_Incident_Context_Dir, "unattached")
                    report_id.append(stix_obj["id"])
            else:
                # its a node-type of object
                if stix_obj["type"] == "sequence":
                    if stix_obj["step_type"] == "start_step":
                        if wrapped:
                            add_node(stix_obj, "start")
                        else:
                            nodes, edges = n_and_e.convert_node(stix_obj)
                            add_node(nodes[0], TR_Incident_Context_Dir, "start")
                            del_node(stix_obj["id"],TR_Incident_Context_Dir, "unattached")
                            report_id.append(stix_obj["id"])
                    else:
                        if wrapped:
                            add_node(stix_obj, "sequence")
                        else:
                            nodes, edges = n_and_e.convert_node(stix_obj)
                            add_node(nodes[0], TR_Incident_Context_Dir, "sequence")
                            del_node(stix_obj["id"],TR_Incident_Context_Dir, "unattached")
                            report_id.append(stix_obj["id"])
                elif stix_obj["type"] == "task":
                    if wrapped:
                        add_node(stix_obj, "task")
                    else:
                        nodes, edges = n_and_e.convert_node(stix_obj)
                        add_node(nodes[0], TR_Incident_Context_Dir, "task")
                        del_node(stix_obj["id"],TR_Incident_Context_Dir, "unattached")
                        report_id.append(stix_obj["id"])
                elif stix_obj["type"] == "event":
                    if wrapped:
                        add_node(stix_obj, "event")
                    else:
                        nodes, edges = n_and_e.convert_node(stix_obj)
                        add_node(nodes[0], TR_Incident_Context_Dir, "event")
                        del_node(stix_obj["id"],TR_Incident_Context_Dir, "unattached")
                        report_id.append(stix_obj["id"])
                elif stix_obj["type"] == "impact":
                    if wrapped:
                        add_node(stix_obj, "impact")
                    else:
                        nodes, edges = n_and_e.convert_node(stix_obj)
                        add_node(nodes[0], TR_Incident_Context_Dir, "impact")
                        del_node(stix_obj["id"],TR_Incident_Context_Dir, "unattached")
                        report_id.append(stix_obj["id"])
                elif stix_obj["type"] != "incident":
                    if wrapped:
                        add_node(stix_obj, "other")
                    else:
                        nodes, edges = n_and_e.convert_node(stix_obj)
                        add_node(nodes[0], TR_Incident_Context_Dir, "other")
                        del_node(stix_obj["id"],TR_Incident_Context_Dir, "unattached")
                        report_id.append(stix_obj["id"])
                else:
                    return "Error: You cannot promote an incident"

    return " transferred from 'Unattached' to 'Other' -> " + str(report_id)


def main(inputfile, outputfile):
    context_type = None
    stix_obj = None
    if os.path.exists(inputfile):
        with open(inputfile, "r") as script_input:
            input = json.load(script_input)
    if "stix_list" in input:
        stix_list = input["stix_list"]

    if "api" in input:
        stix_list = input["api"]["stix_list"]

    # setup logger for execution
    result_string = promote_objects(stix_list)
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