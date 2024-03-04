
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
# Title: Get From Options
# Author: OS-Threat
# Organisation Repo: https://github.com/typerefinery-ai/brett_blocks
# Contact Email: denis@cloudaccelerator.co
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
# 1. Context
#
# This code is licensed under the terms of the BSD.
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
TR_Context_Memory_Dir = "./Context_Mem"
local = {
    "global": "/global_variables_dict.json",
    "me" : "/cache_me.json",
    "team" : "/cache_team.json",
    "users": "/company_1/users.json",
    "company" : "/company_1/company.json",
    "assets" : "/company_1/assets.json",
    "systems" : "/company_1/systems.json",
    "relations" : "/company_1/relations.json",
    "edges" : "/company_1/edges.json",
    "relation_edges" : "/company_1/relation_edges.json",
    "relation_replacement_edges" : "/company_1/relation_replacement_edges.json"
}
refs = {
    "incident" : "/incident_1/incident.json",
    "start" : "/incident_1/sequence_start_refs.json",
    "sequence" : "/incident_1/sequence_refs.json",
    "impact" : "/incident_1/impact_refs.json",
    "event" : "/incident_1/event_refs.json",
    "task" : "/incident_1/task_refs.json",
    "other" : "/incident_1/other_object_refs.json",
    "unattached" : "/incident_1/unattached_objs.json",
    "relations" : "/incident_1/incident_relations.json",
    "edges" : "/incident_1/incident_edges.json",
    "relation_edges" : "/incident_1/relation_edges.json",
    "relation_replacement_edges" : "/incident_1/relation_replacement_edges.json"
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

    if context_type:
        TR_Context_Filename = TR_Context_Memory_Dir + local[context_type]
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
                if "properties" in get_query or "embedded" in get_query:
                    if "properties" in get_query and "embedded" in get_query:
                        if check_properties(cont["original"], get_query["property"], source_value) and check_embedded(cont["original"], get_query["embedded"], source_id):
                            context_object = cont
                            return context_object
                    elif "properties" in get_query and "embedded" not in get_query:
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
            input = json.load(script_input)
    if "get_query" in input:
        get_query = input["get_query"]
    if "context_type" in input:
        context_type = input["context_type"]
    if "source_value" in input:
        source_value = input["source_value"]
    if "source_id" in input:
        source_id = input["source_id"]

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