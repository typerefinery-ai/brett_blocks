
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

TR_Settings_Dir = "./generated/os-triage/context_mem/settings"
TR_Settings_URL = "https://raw.githubusercontent.com/typerefinery-ai/brett_blocks/refs/heads/main/Block_Families/OS_Triage/User_Options/options.json"

def download_settings():
    if not os.path.exists(TR_Settings_Dir):
        os.makedirs(TR_Settings_Dir)
    result = urlretrieve(TR_Settings_URL, TR_Settings_Dir + "/options.json")
    print(f'settings file result ->', result)




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



def register_id(id, field, TR_Incident_Context_Dir):
    incident_list = []
    with open(TR_Incident_Context_Dir + incident_data["incident"], "r") as incident_object:
        incident_list = json.load(incident_object)
        wrapped_incident = incident_list[0]
        incident = wrapped_incident["original"]
        incident_references = wrapped_incident["references"]
        incident_ext = incident["extensions"]["extension-definition--ef765651-680c-498d-9894-99799f2fa126"]
        # register first in the object
        # check whether field exists first
        if field_names[field] in incident_ext:
            id_list = incident_ext[field_names[field]]
            if id not in id_list:
                id_list.append(id)
        else:
            id_list = []
            id_list.append(id)
            incident_ext[field_names[field]] = id_list
        # register second in the references
        # check whether field exists first
        if field_names[field] in incident_references:
            id_list = incident_references[field_names[field]]
            if id not in id_list:
                id_list.append(id)
        else:
            id_list = []
            id_list.append(id)
            incident_references[field_names[field]] = id_list


    with open(TR_Incident_Context_Dir + incident_data["incident"], 'w') as f:
        f.write(json.dumps(incident_list))


def save_incident_context(stix_object):
    if "original" in stix_object:
        stix_object = stix_object["original"]
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
        # if not os.path.exists(TR_Common_Files):
        #     os.makedirs(TR_Common_Files)
        #     download_common(common)
        if not os.path.exists(TR_Context_Memory_Dir):
            os.makedirs(TR_Context_Memory_Dir)
        if not os.path.exists(TR_Context_Memory_Dir + "/usr"):
            os.makedirs(TR_Context_Memory_Dir + "/usr")
        if not os.path.exists(TR_Settings_Dir):
            download_settings()
        # if not os.path.exists(TR_Context_Memory_Dir + "/incident_1"):
        #     os.makedirs(TR_Context_Memory_Dir + "/incident_1")

        # 3. Now we are sure the common files exist, we need to import them
        # Specify the path to the Nodes and Edges module
        module_path = TR_Common_Files + '/' + common[0]["file"]
        # Load the module spec using importlib.util.spec_from_file_location
        spec = importlib.util.spec_from_file_location('parse', module_path)
        # Create the module from the specification
        parse = importlib.util.module_from_spec(spec)
        # Load the module
        spec.loader.exec_module(parse)
        # 4. Depending on Object Type, Get the Nodes and Edges, and save them to the lists
        stix_nodes_list = []
        incident = {}
        # its a node-type of object
        wrapped = parse.wrap_stix_dict(stix_object)
        if stix_object["type"] == "sequence":
            add_node(wrapped, TR_Incident_Context_Dir, "sequence")
            register_id(stix_object["id"], "sequence", TR_Incident_Context_Dir)
        elif stix_object["type"] == "task":
            add_node(wrapped, TR_Incident_Context_Dir, "task")
            register_id(stix_object["id"], "task", TR_Incident_Context_Dir)
        elif stix_object["type"] == "event":
            add_node(wrapped, TR_Incident_Context_Dir, "event")
            register_id(stix_object["id"], "event", TR_Incident_Context_Dir)
        elif stix_object["type"] == "impact":
            add_node(wrapped, TR_Incident_Context_Dir, "impact")
            register_id(stix_object["id"], "impact", TR_Incident_Context_Dir)
        elif stix_object["type"] != "incident":
            add_node(wrapped, TR_Incident_Context_Dir, "other")
            register_id(stix_object["id"], "other", TR_Incident_Context_Dir)
        else:
            # It is an Incident, so first, update all of the id lists on the incident object
            for key in key_list:
                if os.path.exists(TR_Incident_Context_Dir + incident_data[key]):
                    with open(TR_Incident_Context_Dir + incident_data[key], "r") as list_input:
                        stix_list = json.load(list_input)
                        stix_id_list = [x["id"] for x in stix_list]
                        # does the stix_object already appear in the list?
                        wrapped["original"][field_names[key]] = stix_id_list
                else:
                    # list is empty
                    wrapped["original"][field_names[key]] = []

            add_node(wrapped, TR_Incident_Context_Dir, "incident")
        # 5. 
        # 5. Add the id to the Update Incident List, if it is not already in there
        if current_incident_dir not in local_map.get("update_incident_list", []):
            local_map["update_incident_list"] = local_map.get("update_incident_list", []) + [current_incident_dir]
    with open(TR_Context_Memory_Dir + "/" + context_map, 'w') as f:
        f.write(json.dumps(local_map))

    return " incident context saved - \nstix_id -> " + str(stix_object["id"])


def main(inputfile, outputfile):
    stix_object = None
    if os.path.exists(inputfile):
        with open(inputfile, "r") as script_input:
            input_data = json.load(script_input)
            print(f"input data->{input_data}")
            if "stix_object" in input_data:
                stix_object = input_data["stix_object"]
                result_string = save_incident_context(stix_object)
            elif "api" in input_data:
                api_input_data = input_data["api"]
                stix_object = api_input_data["stix_object"]
                print(f"api \nstix_object->{stix_object}\n")
                result_string = save_incident_context(stix_object)

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