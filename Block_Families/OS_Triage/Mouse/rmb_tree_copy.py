
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
# Title: RMB Tree Copy OS_Triage
# Author: OS-Threat
# Organisation Repo: https://github.com/typerefinery-ai/brett_blocks
# Contact Email: brett@osthreat.com
# Date: 07/08/2023
#
# Description: This script is designed to take in a Stix Object from the tree
#       and save it in the unattached list
#
# One Mandatory Input:
# 1. Stix Tree Object
# One Output
# 1. Context Return
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


def download_common(module_list):
    for module in module_list:
        # Step 1: download the module
        result = urlretrieve(module["url"], TR_Common_Files + "/" + module["file"])
        print(f'common file result ->', result)
        # Step 2: install the module



def add_node(node, context_dir, context_type="unattached"):
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


def copy_tree_object_to_unattached(tree_object):
    # 0 Check for "original"
    unwrapped = {}
    if "original" in tree_object:
        unwrapped = tree_object["original"]
    # if "original" in stix_object:
    #     wrapped = True
    # 1.B Find Current Incident directory
    local_map = {}
    with open(TR_Context_Memory_Dir + "/" + context_map, "r") as current_context:
        local_map = json.load(current_context)
        # 1. Setup the directory
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

        
        # Specify the path to the Nodes and Edges module
        module_path = TR_Common_Files + '/' + common[0]["file"]
        # Load the module spec using importlib.util.spec_from_file_location
        spec = importlib.util.spec_from_file_location('parse', module_path)
        # Create the module from the specification
        parse = importlib.util.module_from_spec(spec)
        # Load the module
        spec.loader.exec_module(parse)
        # 4. Depending on Object Tupe, Get the Nodes and Edges, and save them to the lists
        stix_nodes_list = []
        incident = {}
        wrapped = parse.wrap_stix_dict(unwrapped)
        add_node(wrapped, TR_Incident_Context_Dir, "unattached")


    return "object saved to unattached context - \nstix_id -> " + str(wrapped["id"])


def main(inputfile, outputfile):
    context_type = None
    context_type_string = ""
    stix_object = None
    if os.path.exists(inputfile):
        with open(inputfile, "r") as script_input:
            input_data = json.load(script_input)
            print(f"input data->{input_data}")
            if "tree_object" in input_data:
                tree_object = input_data["tree_object"]
                result_string = copy_tree_object_to_unattached(tree_object)
            elif "api" in input_data:
                api_input_data = input_data["api"]
                tree_object = api_input_data["tree_object"]
                result_string = copy_tree_object_to_unattached(tree_object)

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