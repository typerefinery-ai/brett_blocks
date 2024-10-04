
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
# Title: Relationship Type
# Author: OS-Threat
# Organisation Repo: https://github.com/typerefinery-ai/brett_blocks
# Contact Email: brett@osthreat.com
# Date: 07/08/2023
#
# Description: This script is designed to take in a source and target object and
#              return a list of relationship types, and provide the source_ref, target_ref
#
# One Mandatory Input:
# 1. Enum_Name
# One Output
# 1. Enum
#
#
# This code is licensed under the terms of the Apache 2.
##############################################################################

from stixorm.module.authorise import import_type_factory
from stixorm.module.parsing.parse_objects import parse
from stixorm.module.typedb_lib.factories.auth_factory import get_auth_factory_instance
# from Block_Families.General._library.
# from Orchestration.Common.
from urllib.request import urlretrieve
import json
import sys
import importlib.util
import logging
import copy
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

import_type = import_type_factory.get_all_imports()

# Common File Stuff
TR_Common_Files = "./generated/os-triage/common_files"
common = [
    {"module": "convert_n_and_e", "file": "convert_n_and_e.py", "url" : "https://raw.githubusercontent.com/typerefinery-ai/brett_blocks/main/Block_Families/General/_library/convert_n_and_e.py"}
]

# StixORM Dialect Data Stuff
TR_dialect_data = "./generated/os-triage/dialect_data/summary"
sro_types = "/constraints.json"
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

def  process_category(stix_object, constraint):
    # 1. StixORM stuff
    auth_factory = get_auth_factory_instance()
    auth = auth_factory.get_auth_for_import(import_type)
    auth_types = copy.deepcopy(auth["types"])
    stix_dict = stix_object.__dict__
    # 2. Step through the constraints
    if constraint == "_any":
        return True
    elif constraint == "_attack":
        return False if not stix_dict.get("x_mitre_version", False) else True
    elif constraint == "_sdo":
        if stix_object.type in auth_types["sdo"]:
            logger.debug(f' going into sdo ---? {stix_object}')
            return True
    elif constraint == "_sco":
        if stix_object.type in auth_types["sco"]:
            logger.debug(f' going into sco ---? {stix_object}')
            return True
    else:
        pass

    return False

def get_relationship_type(source, target):
    # note they are stix objects, not dicts
    # 1. Get the SRO Types List open
    SRO_Types_File = TR_dialect_data + sro_types

    # 2. Check if the key directories exist, if not make them, and download common files
    if not os.path.exists(TR_dialect_data):
        os.makedirs(TR_dialect_data)
    # 3. Setup key variables needed
    source_type = source.type
    target_type = target.type
    source_id = source.id
    target_id = target.id
    valid_relationship_types = []
    reln_type_object = {}
    constraint_list = []
    if os.path.exists(SRO_Types_File):
        with open(SRO_Types_File, "r") as mem_input:
            constraint_list = json.load(mem_input)
    # 6. For each constraint in the list, find which ones fit the source-target
    for constraint_layer in constraint_list:
        source_passes = False
        target_passes = False
        constraint_source_list = constraint_layer["source"]
        constraint_target_list = constraint_layer["target"]
        # 6.A Evaluate whether the source object is in the source list
        for constraint_source in constraint_source_list:
            # 1. Consider the constraint source first
            if constraint_source[:1] == "_":
                if constraint_source == "_same":
                    if source_type == target_type:
                        source_passes = True
                        target_passes = True
                        break
                else:
                    # constraint type is general category
                    source_passes = process_category(source, constraint_source)
            else:
                # constraint type a direct type
                if constraint_source == source_type:
                    source_passes = True
                    break
        for constraint_target in constraint_target_list:
            # 2. Consider the constraint target second
            if constraint_target[:1] == "_":
                if constraint_target == "_same":
                    if source_type == source_type:
                        source_passes = True
                        target_passes = True
                        break
                else:
                    # constraint type is a general category vs object
                    target_passes = process_category(target, constraint_target)
            else:
                # constraint type a direct type to  object comparison
                if constraint_target == target_type:
                    target_passes = True
                    break

        # 3. Finally .If source and target both pass, then append the relationship type
        if source_passes and target_passes:
            valid_relationship_types.append(constraint_layer["relationship_types"])

        # 4. Setup the object for the form fields
        reln_form_values = {}
        reln_form_values["source_ref"] = source_id
        reln_form_values["target_ref"] = target_id
        # 5. Setup and send the final object
        reln_type_object["relationship_type_list"] = valid_relationship_types
        reln_type_object["reln_form_values"] = reln_form_values
    return reln_type_object


def main(inputfile, outputfile):
    source = None
    target = None
    reln_type_list = []
    if os.path.exists(inputfile):
        with open(inputfile, "r") as script_input:
            input = json.load(script_input)
            if "api" in input:
                source_dict = input["api"]["source"]
                target_dict = input["api"]["target"]
            else:
                source_dict = input["source"]
                target_dict = input["target"]
            if "original" in source_dict:
                source_obj = parse(source_dict["original"], import_type=import_type)
            else:
                source_obj = parse(source_dict, import_type=import_type)
            if "original" in target_dict:
                target_obj = parse(target_dict["original"], import_type=import_type)
            else:
                target_obj = parse(target_dict, import_type=import_type)
            #
            # setup logger for execution
            reln_type_list = get_relationship_type(source_obj, target_obj)

    with open(outputfile, "w") as outfile:
        json.dump(reln_type_list, outfile)


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