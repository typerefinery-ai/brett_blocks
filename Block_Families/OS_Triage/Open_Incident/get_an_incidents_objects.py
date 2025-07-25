
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



def get_an_incidents_objects(incident_id):
    # 0 Check for "original"
    incident_list = []
    changed = False
    if incident_id is None: # open the default incident
        if os.path.exists(TR_Context_Memory_Dir + "/" + context_map):
            with open(TR_Context_Memory_Dir + "/" + context_map, "r") as current_context:
                local_map = json.load(current_context)
                # 1. Since the map exists and the incident, then set the current incident details
                incident_id = local_map["current_incident"]
                TR_Incident_Dir = TR_Context_Memory_Dir + "/" + incident_id
                # 2. Open the Incident File, and extract the Ext (for checking/updating)
                with open(TR_Incident_Dir + "/" + incident_data["incident"]) as current_obj:
                    incident_list = json.load(current_obj)

    else:# 1.B Find input Incident directory
        TR_Incident_Dir = TR_Context_Memory_Dir + "/" + incident_id
        # 1 First, Set the Current Incident directory to the new value
        if os.path.exists(TR_Context_Memory_Dir + "/" + context_map):
            with open(TR_Context_Memory_Dir + "/" + context_map, "r") as current_context:
                local_map = json.load(current_context)
                if os.path.exists(TR_Incident_Dir + "/" + incident_data["incident"]):
                    # 1. Since the map exists and the incident, then set the current incident details
                    local_map["current_incident"] = incident_id
                else:
                    return []
            with open(TR_Context_Memory_Dir + "/" + context_map, "w") as f:
                f.write(json.dumps(local_map))

        # 2. Open the Incident File, and extract the Ext (for checking/updating)
        with open(TR_Incident_Dir + "/" + incident_data["incident"] ) as current_obj:
            incident_list = json.load(current_obj)


    wrapped_incident = incident_list[0]
    incident = wrapped_incident["original"]
    incident_ext = incident["extensions"]["extension-definition--ef765651-680c-498d-9894-99799f2fa126"]
    # 3. For each of the lists of id's in the Icnident, collect objects and check whether they are registered
    for key in key_list:
        if os.path.exists(TR_Incident_Dir + "/" + incident_data[key] ):
            with open(TR_Incident_Dir + "/" + incident_data[key]) as prop_list:
                current_refs_list = []
                list_of_objs = json.load(prop_list)
                field_name = field_names[key]
                # Either get the list, or make the list
                if field_name in incident_ext:
                    current_refs_list = incident_ext[field_name]
                else:
                    incident_ext[field_name] = []
                    current_refs_list = incident_ext[field_name]
                    changed = True
                # 4. Add each object to the list, and register the id on the incident, if it is not already
                for stix_obj in list_of_objs:
                    incident_list.append(stix_obj)
                    if stix_obj["id"] not in current_refs_list:
                        current_refs_list.append(stix_obj["id"])
                        changed = True
    # 5. If the Incident has been changed, may as well update context mem
    if changed:
        with open(TR_Incident_Dir + "/" + incident_data["incident"], 'w') as f:
            f.write(json.dumps([wrapped_incident]))
    # 6. Finally, add the incident to the list
    incident_list.append(wrapped_incident)

    return incident_list


def main(inputfile, outputfile):
    incident_id = None
    if os.path.exists(inputfile):
        with open(inputfile, "r") as script_input:
            input_data = json.load(script_input)
            print(f"input data->{input_data}")
            if "incident_id" in input_data:
                incident_id = input_data["incident_id"]
            if "api" in input_data:
                incident_data = input_data["api"]
                incident_id = incident_data["incident_id"]
            # No input data, just a trigger
            stix_list = get_an_incidents_objects(incident_id)

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