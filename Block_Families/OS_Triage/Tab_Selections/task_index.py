
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
# Title: When Task tab selected, get data
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
# 1. Sighting Hierarchy
#
# This code is licensed under the terms of the Apache 2.
##############################################################################

from stixorm.module.authorise import import_type_factory
import json
import copy

import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

from datetime import datetime
from stixorm.module.typedb_lib.factories.auth_factory import get_auth_factory_instance
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


def get_task_index():
    show_sro = True
    task_index = {}
    # 1. Setup variables
    tasks = []
    possible = []
    relations = []
    stix_incident_id = ""
    auth_factory = get_auth_factory_instance()
    auth = auth_factory.get_auth_for_import(import_type)
    auth_types = copy.deepcopy(auth["types"])
    local_map = {}
    with open(TR_Context_Memory_Dir + "/" + context_map, "r") as current_context:
        local_map = json.load(current_context)
        current_incident_dir = local_map["current_incident"]
        TR_Incident_Context_Dir = TR_Context_Memory_Dir + "/" + current_incident_dir
        # 2. open "others" list file, and split it into chunks
        if os.path.exists(TR_Incident_Context_Dir + incident_data["incident"]):
            with open(TR_Incident_Context_Dir + incident_data["incident"], "r") as mem_input:
                stix_incident_obj = json.load(mem_input)
                stix_incident_id = stix_incident_obj[0]["id"]
        if os.path.exists(TR_Incident_Context_Dir + incident_data["task"]):
            with open(TR_Incident_Context_Dir + incident_data["task"], "r") as mem_input:
                stix_task_list = json.load(mem_input)
                for stix_obj in stix_task_list:
                    if stix_obj["type"] == "task":
                        tasks.append(stix_obj)
                    else:
                        return {"result": "error, type is not task"}
        for key in key_list:
            if os.path.exists(TR_Incident_Context_Dir + incident_data[key]):
                with open(TR_Incident_Context_Dir + incident_data[key], "r") as mem_input:
                    stix_obj_list = json.load(mem_input)
                    if key == "relations":
                        relations = stix_obj_list
                    else:
                        possible = possible + stix_obj_list
        # 3. sort sightings by time
        if tasks != []:
            sorted_list = sorted(tasks, key=lambda t: datetime.strptime(t["original"]["created"], "%Y-%m-%dT%H:%M:%S.%fZ"))
            task_index["name"] = "Task List"
            task_index["icon"] = "task-group"
            task_index["heading"] = "Task List"
            task_index["description"] = "List of all tasks"
            task_index["type"] = ""
            task_index["edge"] = ""
            task_index["id"] = ""
            task_index["children"] = []
            children = task_index["children"]
            # 4. Process each sighting and place them into the children
            for sorted_obj in sorted_list:
                # 4A. First setup the sighting object
                level1 = {}
                level1 = sorted_obj
                level1["edge"] = "task_refs"
                temp_list = []
                owner = ""
                changed_obj_ids = []
                created_by_ref = ""
                if "changed_objects" in sorted_obj["original"]:
                    changed_objects = sorted_obj["original"]["changed_objects"]
                    for change in changed_objects:
                        if "initial_ref" in change:
                            changed_obj_ids.append(change["initial_ref"])
                        elif "result_ref" in change:
                            changed_obj_ids.append(change["result_ref"])
                if "owner" in sorted_obj["original"]:
                    owner = sorted_obj["original"]["owner"]
                if "created_by_ref" in sorted_obj["original"]:
                    created_by_ref = sorted_obj["original"]["created_by_ref"]
                for obj in possible:
                    if changed_obj_ids != [] and obj["id"] in changed_obj_ids:
                        changed_obj = {}
                        changed_obj = obj
                        changed_obj["edge"] = "changed_object"
                        temp_list.append(changed_obj)
                    elif owner != "" and obj["id"] == owner:
                        owner = {}
                        owner["edge"] = "owner"
                        temp_list.append(owner)
                    elif created_by_ref != "" and obj["id"] == created_by_ref:
                        created_by_obj = {}
                        created_by_obj = obj
                        created_by_obj["edge"] = "created_by_ref"
                        temp_list.append(created_by_obj)
                for reln in relations:
                    if sorted_obj["id"] == reln["original"]["source_ref"] and reln["original"]["target_ref"] != stix_incident_id:
                        if show_sro:
                            show_sro = {}
                            show_sro = reln
                            show_sro["edge"] = reln["relationship_type"]
                            show_sro["children"] = []
                            children2 = show_sro["children"]
                            for obj in possible:
                                if obj["id"] == reln["original"]["target_ref"]:
                                    sub_obj = {}
                                    sub_obj = obj
                                    sub_obj["edge"] = reln["relationship_type"]
                                    children2.append(sub_obj)
                            temp_list.append(show_sro)
                        else:
                            for obj in possible:
                                if obj["id"] == reln["original"]["target_ref"]:
                                    sub_obj = {}
                                    sub_obj = obj
                                    sub_obj["edge"] = reln["relationship_type"]
                                    temp_list.append(sub_obj)
                    elif sorted_obj["id"] == reln["original"]["target_ref"] and reln["original"]["source_ref"] != stix_incident_id:
                        if show_sro:
                            show_sro = {}
                            show_sro = reln
                            show_sro["edge"] = reln["relationship_type"]
                            show_sro["children"] = []
                            children2 = show_sro["children"]
                            for obj in possible:
                                if obj["id"] == reln["original"]["source_ref"]:
                                    sub_obj = {}
                                    sub_obj = obj
                                    sub_obj["edge"] = reln["relationship_type"]
                                    children2.append(sub_obj)
                            temp_list.append(show_sro)
                        else:
                            for obj in possible:
                                if obj["id"] == reln["original"]["source_ref"]:
                                    sub_obj = {}
                                    sub_obj = obj
                                    sub_obj["edge"] = reln["relationship_type"]
                                    temp_list.append(sub_obj)

                if temp_list != []:
                    level1["children"] = temp_list
                children.append(level1)

        else:
            return task_index

    return task_index


def main(inputfile, outputfile):
    context_type = None
    stix_object = None
    if os.path.exists(inputfile):
        with open(inputfile, "r") as script_input:
            input = json.load(script_input)

    # setup logger for execution
    hierarchy = get_task_index()

    with open(outputfile, "w") as outfile:
        json.dump(hierarchy, outfile)


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