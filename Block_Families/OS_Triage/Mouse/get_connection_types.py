
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
# Title: Get Connection Types
# Author: OS-Threat
# Organisation Repo: https://github.com/typerefinery-ai/brett_blocks
# Contact Email: brett@osthreat.com
# Date: 07/08/2023
#
# Description: This script is designed to take in a source and target object and
#              return a list of relationship types, and provide the source_ref, target_ref
#
# One Mandatory Input:
# 1. Object Type
# 2. Object Field
# One Output
# 1. ID's of Suitable Objects
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
connection_types = "/connections.json"
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


def clean_string_convert_to_list(string):
	"""Convert a string to a list of strings."""	
	result_list = []	
	if isinstance(string, str):
		# Check if a comma exists and split
		if ',' in string:
			result_list = string.split(',')
		else:
			result_list = [string]  # Keep the string as is if no comma
		# strip out any space in the strings in the list
		result_list = [item.strip() for item in result_list]
		return result_list
	elif isinstance(string, list):
		# For each item in the list, split on any commas
		for item in string:
			if isinstance(item, str):
				if ',' in item:
					result_list += item.split(',')
				else:
					result_list.append(item)
		# strip out any space in the strings in the list
		result_list = [item.strip() for item in result_list]
		return result_list
	else:
		return result_list



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

def get_connection_type(source, target):
    # note they are stix objects, not dicts
    # 1. Get the SRO Types List open
    SRO_Types_File = TR_dialect_data + connection_types

    # 2. Check if the key directories exist, if not make them, and download common files
    if not os.path.exists(TR_dialect_data):
        os.makedirs(TR_dialect_data)
    # 3. Setup key variables needed
    source_type = source.type
    target_type = target.type
    source_id = source.id
    target_id = target.id
    valid_connection_types = []
    connect_type_object = {}
    connection_list = []
    if os.path.exists(SRO_Types_File):
        with open(SRO_Types_File, "r") as mem_input:
            connection_list = json.load(mem_input)
    # 6. For each constraint in the list, find which ones fit the source-target
    for connect_layer in connection_list:
        source_passes = False
        target_passes = False
        connect_source = connect_layer["source_type"]
        connect_target_list = clean_string_convert_to_list(connect_layer["target_type"])
        # 6.A Evaluate whether the source object is in the source
        # 1. Consider the constraint source first
        if connect_source[:1] == "_":
            if connect_source == "_same":
                if source_type == target_type:
                    source_passes = True
                    target_passes = True
            else:
                # constraint type is general category
                source_passes = process_category(source, connect_source)
        else:
            # constraint type a direct type
            if connect_source == source_type:
                source_passes = True
        for connect_target in connect_target_list:
            # 2. Consider the constraint target second
            if connect_target[:1] == "_":
                if connect_target == "_same":
                    if target_type == source_type:
                        source_passes = True
                        target_passes = True
                        break
                else:
                    # constraint type is a general category vs object
                    target_passes = process_category(target, connect_target)
            else:
                # constraint type a direct type to  object comparison
                if connect_target == target_type:
                    target_passes = True
                    break

        # 3. Finally .If source and target both pass, then append the relationship type
        if source_passes and target_passes:
            valid_connection_types.append(connect_layer["field"])

        # 4. Setup the object for the form fields
        connect_form_values = {}
        connect_form_values["source_ref"] = source_id
        connect_form_values["target_ref"] = target_id
        # 5. Setup and send the final object
        connect_type_object["connection_field_list"] = valid_connection_types
        connect_type_object["connect_objects"] = connect_form_values
    return connect_type_object


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
            connections_type_list = get_connection_type(source_obj, target_obj)

    with open(outputfile, "w") as outfile:
        json.dump(connections_type_list, outfile)


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