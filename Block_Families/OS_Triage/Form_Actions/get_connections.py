
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
# Title: Get Connections
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



def check_object(unattached_obj, constraint_list):
    """Check if the unattached object passes the constraints."""
    # For each string constraint in the constraint list, run the clean string convert to list
    for constraint_layer in constraint_list:
        string_constraint = constraint_layer.get("target_type", "")
        # 1. clean the string and convert to a list
        constraints = clean_string_convert_to_list(string_constraint)
        # 2. for each constraint in constraints, check if the object passes
        for constraint in constraints:
            # 2.1 check if the object passes the constraint
            if constraint == "_any":
                    return True
            elif constraint == "_attack":
                if unattached_obj.get("x_mitre_version", False):
                    return True
            elif constraint == "_sdo":
                if unattached_obj["type"] in import_type["types"]["sdo"]:
                    return True
            elif constraint == "_sco":
                if unattached_obj["type"] in import_type["types"]["sco"]:
                    return True
            elif constraint == unattached_obj["type"]:
                return True

    return False

def get_objects_from_unattached(constraint_list):
    valid_connections = []
    with open(TR_Context_Memory_Dir + "/" + context_map, "r") as current_context:
        local_map = json.load(current_context)
        current_incident_dir = local_map["current_incident"]
        TR_Incident_Context_Dir = TR_Context_Memory_Dir + "/" + current_incident_dir
        # 2. open files and fill lists
        if os.path.exists(TR_Incident_Context_Dir + incident_data["unattached"]):
            with open(TR_Incident_Context_Dir + incident_data["unattached"], "r") as mem_input:
                unattached_nodes = json.load(mem_input)
                for unattached_obj in unattached_nodes:
                    object_passes = False
                    object_passes = check_object(unattached_obj, constraint_list)
                    if object_passes:
                        valid_connections.append(unattached_obj)

    return valid_connections

def get_connections(object_type: str, object_field: str):
    """Get the connections for a specific object type and field.
    Args:
        object_type (str): The type of the object to get connections for.
        object_field (str): The field of the object to get connections for.
    Returns:
        list: A list of valid connections for the object type and field."""
    # note they are stix objects, not dicts
    # 1. Get the SRO Types List open
    Connection_Types_File = TR_dialect_data + connection_types

    # 2. Check if the key directories exist, if not make them, and download common files
    if not os.path.exists(TR_dialect_data):
        os.makedirs(TR_dialect_data)
    # 3. Setup key variables needed
    valid_connections = []
    constraint_list = []
    if os.path.exists(Connection_Types_File):
        with open(Connection_Types_File, "r") as mem_input:
            constraint_list = json.load(mem_input)
    # 4. Filter the list based on the field "sourcetype" == object_type
    object_Constraint_list = [constraint for constraint in constraint_list if constraint.get("source_type") == object_type]
    # 5. Filter the object_Constraint_list based on the field "field" == object_field
    final_constraint_list = [constraint for constraint in object_Constraint_list if constraint.get("field") == object_field]
    # 6. For each constraint in the list, find which ones fit the source-target
    valid_connections = get_objects_from_unattached(final_constraint_list)

    return valid_connections


def main(inputfile, outputfile):
    object_type = None
    object_field = None
    connections_type_list = []
    if os.path.exists(inputfile):
        with open(inputfile, "r") as script_input:
            input = json.load(script_input)
            if "api" in input:
                object_type = input["api"]["object_type"]
                object_field = input["api"]["object_field"]
            else:
                object_type = input["object_type"]
                object_field = input["object_field"]
            #
            # setup logger for execution
            connections_type_list = get_connections(object_type, object_field)

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