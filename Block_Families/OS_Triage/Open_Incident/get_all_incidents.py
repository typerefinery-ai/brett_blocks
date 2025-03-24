
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
# Title: Get All Incidents
# Author: OS-Threat
# Organisation Repo: https://github.com/typerefinery-ai/brett_blocks
# Contact Email: brett@osthreat.com
# Date: 07/08/2023
#
# Description: This script is designed to take in a Stix Object
#       and save it in the unattached list for the currently selected incident
#
# No Input, Just Trigger:
#
# One Output
# 1. List of Incidents
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



def get_all_incidents():
    # 0 Check for "original"
    incident_list = []
    # 1.B Find Current Incident directory
    if not os.path.exists(TR_Common_Files):
        os.makedirs(TR_Common_Files)
        download_common(common)
    if not os.path.exists(TR_Context_Memory_Dir):
        os.makedirs(TR_Context_Memory_Dir)
    if not os.path.exists(TR_Context_Memory_Dir + "/usr"):
        os.makedirs(TR_Context_Memory_Dir + "/usr")
    if os.path.exists(TR_Context_Memory_Dir + "/" + context_map):
        with open(TR_Context_Memory_Dir + "/" + context_map, "r") as current_context:
            local_map = json.load(current_context)
            # 1. If the map exists, then get incident details
            current_incident_dir = local_map["current_incident"]
            list_of_incidents = local_map["incident_list"]
            # 2. For each Incident in the list, load the incident object
            for incident_id in list_of_incidents:
                incident_obj = {}
                changed = False
                TR_Incident_Dir = TR_Context_Memory_Dir + "/" + incident_id
                with open(TR_Incident_Dir + "/" + incident_data["incident"] ) as current_obj:
                    incident_list = json.load(current_obj)
                    incident_obj = incident_list[0]
                    for key in key_list:
                        print(f"key is --> {key}")
                        print(f"incident obj -> {incident_obj}")
                        print(f"type of incident obj -?{type(incident_obj)}")
                        if os.path.exists(TR_Incident_Dir + "/" + incident_data[key] ):
                            with open(TR_Incident_Dir + "/" + incident_data[key]) as prop_list:
                                list_of_objs  = json.load(prop_list)
                                field_name = field_names[key]
                                if field_name in incident_obj["original"]:
                                    current_refs_list = incident_obj["original"][field_name]
                                else:
                                    incident_obj["original"][field_name] = []
                                    current_refs_list = incident_obj["original"][field_name]
                                    changed = True
                                for stix_obj in list_of_objs:
                                   if stix_obj["id"] not in current_refs_list:
                                        current_refs_list.append(stix_obj["id"])
                                        changed = True
                # if changed, may as well update it to latest
                if changed:
                    with open(TR_Incident_Dir + "/" + incident_data["incident"], 'w') as f:
                        f.write(json.dumps([incident_obj]))
                # Then, add it to the list
                incident_list.append(incident_obj)

    return incident_list


def main(inputfile, outputfile):
    # No input data, just a trigger
    stix_list = get_all_incidents()

    with open(outputfile, "w") as outfile:
        json.dump(stix_list, outfile)


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