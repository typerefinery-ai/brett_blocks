
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
# Title: Save Context
# Author: OS-Threat
# Organisation Repo: https://github.com/typerefinery-ai/brett_blocks
# Contact Email: denis@cloudaccelerator.co
# Date: 07/08/2023
#
# Description: This script is designed to take in a Stix Object ID
#       and return a Stix object
#
# One Mandatory Input:
# 1. Context
# No Outpute
#
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
    "me" : "/local_me.json",
    "team" : "/local_team.json",
    "users": "/base/local_users.json",
    "company" : "/base/local_company.json",
    "assets" : "/base/local_assets.json",
    "systems" : "/base/local_systems.json",
    "relations" : "/base/local_relations.json"
}
refs = {
    "start" : "sequence_start_refs",
    "sequence" : "sequence_refs",
    "impact" : "impact_refs",
    "event" : "event_refs",
    "task" : "task_refs",
    "other" : "other_object_refs"
}
key_list = ["start", "sequence", "impact", "event", "task", "other"]

def save_context(stix_object, context_type):
    # 1. Extract the components of the object

    if context_type:
        TR_Context_Filename = TR_Context_Memory_Dir + local[context_type]
    else:
        return "context_type unknown " + str(context_type)

    # does directory exits
    if not os.path.exists(TR_Context_Memory_Dir):
        os.makedirs(TR_Context_Memory_Dir)
    if not os.path.exists(TR_Context_Memory_Dir + "/base"):
        os.makedirs(TR_Context_Memory_Dir)

    # does file exist
    exists = False
    stix_list = []
    incident = {}
    if context_type != "incident":
        # if file exists, replce existing object if it exists, else add it, else create the list and add it
        if os.path.exists(TR_Context_Filename):
            with open(TR_Context_Filename, "r") as mem_input:
                stix_list = json.load(mem_input)
                # does the stix_object already appear in the list?
                for i in range(len(stix_list)):
                    if stix_list[i]["id"] == stix_object["id"]:
                        stix_list[i] = stix_object
                        exists = True
                if not exists:
                    stix_list.add(stix_object)
        else:
            stix_list.append(stix_object)

        with open(TR_Context_Filename, 'w') as f:
            f.write(json.dumps(stix_list))

        # Now add the ref into the incident object if it already exists, else ignore
        exists = False
        if os.path.exists(TR_Context_Memory_Dir + local["incident"]):
            with open(TR_Context_Memory_Dir + local["incident"], "r") as mem_input:
                incident = json.load(mem_input)
                # does the incident have the list?
                list_name = refs[context_type]
                if list_name in incident:
                    id_list = incident[list_name]
                    for i in range(id_list):
                        if id_list[i] == stix_object["id"]:
                            id_list[i] = stix_object["id"]
                            exists = True
                        if not exists:
                            id_list.add(stix_object["id"])
                else:
                    incident[list_name] = []
                    incident[list_name].append(stix_object["id"])

            with open(TR_Context_Memory_Dir + local["incident"], 'w') as f:
                f.write(json.dumps(incident))

    else:
        # if its an incident object, overwrite the eisting incident
        if os.path.exists(TR_Context_Memory_Dir + local["incident"]):
            # overwrite the incident
            with open(TR_Context_Memory_Dir + local["incident"], "w") as f:
                f.write(json.dumps(incident))

        # else write the incident and add any existing
        else:
            for key in key_list:
                # check if existing list holds id's
                if os.path.exists(TR_Context_Memory_Dir + local[key]):
                    with open(TR_Context_Memory_Dir + local[key], "r") as mem_input:
                        stix_list = json.load(mem_input)
                        list_name = refs[context_type]
                        if list_name in stix_object:
                            for obj in stix_list:
                                if obj["id"] not in stix_object[list_name]:
                                    stix_object[list_name].append(obj["id"])
            with open(TR_Context_Memory_Dir + local["incident"], "w") as f:
                f.write(json.dumps(stix_object))

    return " incident context saved -> " + str(context_type)


def main(inputfile, outputfile):
    context_type = None
    stix_object = None
    if os.path.exists(inputfile):
        with open(inputfile, "r") as script_input:
            input = json.load(script_input)
    stix_object = input["stix_object"]
    if "context_type" in input:
        context_type = input["context_type"]

    # setup logger for execution
    result_string = save_context(stix_object, context_type["context_type"])
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