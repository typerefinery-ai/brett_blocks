
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
# One Output
# 1. Context Return
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
    "me" : "/cache_me.json",
    "team" : "/cache_team.json",
    "users": "/company_1/cache_users.json",
    "company" : "/company_1/cache_company.json",
    "assets" : "/company_1/cache_assets.json",
    "systems" : "/company_1/cache_systems.json",
    "relations" : "/company_1/cache_relations.json"
}
refs = {
    "incident" : "/incident_1/incident.json",
    "start" : "/incident_1/sequence_start_refs.json",
    "sequence" : "/incident_1/sequence_refs.json",
    "impact" : "/incident_1/impact_refs.json",
    "event" : "/incident_1/event_refs.json",
    "task" : "/incident_1/task_refs.json",
    "other" : "/incident_1/other_object_refs.json",
    "unattached" : "/incident_1/unattached_objs.json"
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

def save_context(stix_object, context_type):
    # 1. Extract the components of the object
    TR_Context_Incident = TR_Context_Memory_Dir + refs["incident"]

    if context_type:
        TR_Context_Filename = TR_Context_Memory_Dir + refs[context_type]
    else:
        return "context_type unknown " + str(context_type)

    # does directory exits
    if not os.path.exists(TR_Context_Memory_Dir):
        os.makedirs(TR_Context_Memory_Dir)
    if not os.path.exists(TR_Context_Memory_Dir + "/company_1"):
        os.makedirs(TR_Context_Memory_Dir + "/company_1")
    if not os.path.exists(TR_Context_Memory_Dir + "/incident_1"):
        os.makedirs(TR_Context_Memory_Dir + "/incident_1")

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
                    stix_list.append(stix_object)
        else:
            stix_list.append(stix_object)

        with open(TR_Context_Filename, 'w') as f:
            f.write(json.dumps(stix_list))

        # Now add the ref into the incident object if it already exists, else ignore
        exists = False
        if os.path.exists(TR_Context_Incident):
            with open(TR_Context_Incident, "r") as mem_input:
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

            with open(TR_Context_Incident, 'w') as f:
                f.write(json.dumps(incident))

    else:
        # first, get all of the lists of objects first, turn them into id's and add them to the incident object
        for key in key_list:
            if os.path.exists(TR_Context_Memory_Dir + refs[key]):
                with open(TR_Context_Memory_Dir + refs[key], "r") as list_input:
                    stix_list = json.load(list_input)
                    stix_id_list = [x["id"] for x in stix_list]
                    # does the stix_object already appear in the list?
                    stix_object[field_names[key]] = stix_id_list
            else:
                # list is empty
                stix_object[field_names[key]] = []

        # overwrite the incident
        with open(TR_Context_Memory_Dir + refs["incident"], "w") as f:
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