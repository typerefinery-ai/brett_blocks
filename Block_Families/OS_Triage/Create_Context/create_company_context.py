
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
# Title: Create Company OS_Triage
# Author: OS-Threat
# Organisation Repo: https://github.com/typerefinery-ai/brett_blocks
# Contact Email: brett@osthreat.com
# Date: 07/08/2023
#
# Description: This script is designed to take in a Stix Incident Object,
#       setup a context store for it, and save it
#
# One Mandatory Input:
# 1. Stix Identity Object
# One Output
# 1. Company Created Return
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

def create_context_map(c_map_file):
    local_map = {}
    local_map["current_incident"] = ""
    local_map["current_company"] = ""
    local_map["company_list"] = []
    local_map["incident_list"] = []
    local_map["update_company_list"] = []
    local_map["update_incident_list"] = []
    local_map["update_user"] = False
    local_map["update_team"] = False
    with open(TR_Context_Memory_Dir + "/" + c_map_file, 'w') as f:
        f.write(json.dumps(local_map))

def add_node(node, context_dir):
    exists = False
    stix_nodes_list = []
    if  os.path.exists(context_dir + comp_data["company"]):
        with open(context_dir + comp_data["company"], "r") as mem_input:
            stix_nodes_list = json.load(mem_input)
            for i in range(len(stix_nodes_list)):
                if stix_nodes_list[i]["id"] == node["id"]:
                    stix_nodes_list[i] = node
                    exists = True
            if not exists:
                stix_nodes_list.append(node)
    else:
        stix_nodes_list = [node]

    with open(context_dir + comp_data["company"], 'w') as f:
            f.write(json.dumps(stix_nodes_list))


def create_company_context(stix_object):
    if stix_object["type"] != "identity" or stix_object["identity_class"] != "organization":
        return "error, not an company object, cannot make company"
    # 1. First get hold of the stix-id
    stix_id = stix_object["id"]
    stix_type = stix_object["type"]
    TR_Company_Dir = TR_Context_Memory_Dir + "/" + stix_id

    # Make the directory to ensure the context memory is created properly
    if not os.path.exists(TR_Context_Memory_Dir + "/" + context_map):
        create_context_map(context_map)
    if not os.path.exists(TR_Context_Memory_Dir + "/usr"):
        os.makedirs(TR_Context_Memory_Dir + "/usr")
    if not os.path.exists(TR_Company_Dir):
        os.makedirs(TR_Company_Dir)

    # 3. Now we are sure the common files exist, we need to import them
    # Specify the path to the Nodes and Edges module
    module_path = TR_Common_Files + '/' + common[0]["file"]
    # Load the module spec using importlib.util.spec_from_file_location
    spec = importlib.util.spec_from_file_location('parse', module_path)
    # Create the module from the specification
    parse = importlib.util.module_from_spec(spec)
    # Load the module
    spec.loader.exec_module(parse)
    # 4. Get the Nodes and Edges, and save them to the lists
    wrapped = parse.wrap_stix_dict(stix_object)
    # 5. Get the Current Incident Directory in the map, update it and then save it
    local_map = {}
    with open(TR_Context_Memory_Dir + "/" + context_map, "r") as context_update:
        local_map = json.load(context_update)
        local_map["current_company"] = stix_id
        local_map["company_list"] = local_map.get("company_list", []) + [stix_id]
        local_map["update_company_list"] = local_map.get("update_company_list", []) + [stix_id]
    with open(TR_Context_Memory_Dir + "/" + context_map, 'w') as f:
        f.write(json.dumps(local_map))
    # 6. Add the node and edges
    add_node(wrapped, TR_Company_Dir)


    return " company context created -> " + str(stix_id) + "\nstix_id -> " + str(stix_object["id"])


def main(inputfile, outputfile):
    context_type = None
    stix_object = None
    if os.path.exists(inputfile):
        with open(inputfile, "r") as script_input:
            input = json.load(script_input)
            print(f"%%%% \ninput->{input}")
    stix_object = input["company"]

    # setup logger for execution
    result_string = create_company_context(stix_object)
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