
################################################################################
## header start                                                               ##
################################################################################
# allow importing og service local packages
import os
import sys
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
# Title: Get From Incident
# Author: OS-Threat
# Organisation Repo: https://github.com/typerefinery-ai/brett_blocks
# Contact Email: brett@osthreat.com
# Date: 07/08/2023
#
# Description: This script is designed to take in a Stix Object ID
#       and return a Stix object
#
# One Mandatory Input:
# 1. Get Query Form
# 2. Context_Path
# 3. Source Value
# 4. Source Object
# One Output
# 1. OS_Triage
#
# This code is licensed under the terms of the Apache 2.
##############################################################################

from stixorm.module.definitions.os_threat import (
    StateChangeObject, EventCoreExt, Event, ImpactCoreExt,
    Availability, Confidentiality, External, Integrity, Monetary, Physical,
    Traceability, Impact, IncidentScoreObject, IncidentCoreExt, TaskCoreExt,
    Task, SightingEvidence, Sequence, SequenceExt, ContactNumber, EmailContact,
    SocialMediaContact, IdentityContact, AnecdoteExt, Anecdote,
    SightingAnecdote, SightingAlert, SightingContext, SightingExclusion,
    SightingEnrichment, SightingHunt, SightingFramework, SightingExternal
)
from stixorm.module.authorise import import_type_factory
from posixpath import basename
import json
import os

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


def check_properties(cont, prop, source_value):
    source_val = ""
    object_val = ""
    object_path_list = prop["path"]
    comparator = prop["comparator"]
    if "source_path" in prop:
        source_path_list = prop["source_path"]
        length = len(source_path_list)
        interim_object = source_value
        for i, source_path in enumerate(source_path_list):
            if i == (length - 1):
                source_val = interim_object[source_path]
            elif source_path in interim_object:
                interim_object = interim_object[source_path]
            else:
                return False
    else:
        source_val = prop["source_value"]
    # we have a source source_val now
    length = len(object_path_list)
    interim_object = cont
    for i, object_path in enumerate(object_path_list):
        if i == (length - 1):
            object_val = interim_object[object_path]
        elif object_path in interim_object:
            interim_object = interim_object[object_path]
        else:
            return False
    # we have now found the object_val, we need to compare
    if comparator == "EQ":
        if source_val == object_val:
            return True
        else:
            return False
    else:
        return False



def check_embedded(cont, embedded, source_id):
    source_val = ""
    object_val = ""
    source_path_list = embedded["source_path"]
    object_path_list = embedded["path"]
    comparator = embedded["comparator"]
    length = len(source_path_list)
    interim_object = source_id
    for i, source_path in enumerate(source_path_list):
        if i == (length - 1):
            source_val = interim_object[source_path]
        elif source_path in interim_object:
            interim_object = interim_object[source_path]
        else:
            return False
    # we have a source source_val now
    length = len(object_path_list)
    interim_object = cont
    for i, object_path in enumerate(object_path_list):
        if i == (length - 1):
            object_val = interim_object[object_path]
        elif object_path in interim_object:
            interim_object = interim_object[object_path]
        else:
            return False
    # we have now found the object_val, we need to compare
    if comparator == "EQ":
        if source_val == object_val:
            return True
        else:
            return False
    else:
        return False


def get_context_object(get_query, context_type, source_value=None, source_id=None):
    # 1. Extract the components of the object
    # 1.B Find Current Incident directory
    local_map = {}
    with open(TR_Context_Memory_Dir + "/" + context_map, "r") as current_context:
        local_map = json.load(current_context)
        current_incident_dir = local_map["current_incident"]
        TR_Incident_Context_Dir = TR_Context_Memory_Dir + "/" + current_incident_dir

        if context_type:
            TR_Context_Filename = TR_Incident_Context_Dir + incident_data[context_type]
        else:
            return "context_type unknown " + str(context_type)

        context_data_list = []
        context_object = {}
        if os.path.exists(TR_Context_Filename):
            with open(TR_Context_Filename, "r") as context_file:
                context_data_list = json.load(context_file)

        if context_data_list:
            for cont in context_data_list:
                if cont["type"] == get_query["type"]:
                    if "property" in get_query or "embedded" in get_query:
                        if "property" in get_query and "embedded" in get_query:
                            if check_properties(cont["original"], get_query["property"], source_value) and check_embedded(cont["original"], get_query["embedded"], source_id):
                                context_object = cont
                                return context_object
                        elif "property" in get_query and "embedded" not in get_query:
                            if check_properties(cont["original"], get_query["property"], source_value):
                                context_object = cont
                        else:
                            if check_embedded(cont["original"], get_query["embedded"], source_id):
                                context_object = cont
                    else:
                        context_object = cont
                        return context_object

    return context_object


def main(inputfile, outputfile):
    source_value = None
    source_id = None
    if os.path.exists(inputfile):
        with open(inputfile, "r") as script_input:
            input_data = json.load(script_input)
            if "get_query" in input_data:
                get_query = input_data["get_query"]
                if "context_type" in input_data:
                    context_type = input_data["context_type"]
                if "source_value" in input_data:
                    source_value = input_data["source_value"]
                if "source_id" in input_data:
                    source_id = input_data["source_id"]
            elif "api" in input_data:
                api_input = input_data["api"]
                if "get_query" in api_input:
                    get_query = api_input["get_query"]
                    if "context_type" in api_input:
                        context_type = api_input["context_type"]
                    if "source_value" in api_input:
                        source_value = api_input["source_value"]
                    if "source_id" in api_input:
                        source_id = api_input["source_id"]

    # setup logger for execution
    context_data = get_context_object(get_query, context_type["context_type"], source_value, source_id)
    with open(outputfile, "w") as outfile:
        json.dump(context_data, outfile)


# 1. Get Query Form
# 2. Context_Path
# 3. Source Value
# 4. Source Object

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