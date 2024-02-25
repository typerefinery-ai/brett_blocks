
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
# Title: Move "Unattached" to "Other" Context Memory
# Author: OS-Threat
# Organisation Repo: https://github.com/typerefinery-ai/brett_blocks
# Contact Email: denis@cloudaccelerator.co
# Date: 07/08/2023
#
# Description: This script is designed to take in a Stix Object ID
#       and return a Stix object
#
# One Mandatory Input:
# 1. Stix_list
# One Outpute
# 1. Context Return
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
key_list = ["start", "sequence", "impact", "event", "task", "other"]


def move_unattached_to_other(stix_list):
    # 1. Setup the paths and lists for the Unattached and Other
    TR_Unattached_Filename = TR_Context_Memory_Dir + refs["unattached"]
    Unattached_List = []
    TR_Other_Filename = TR_Context_Memory_Dir + refs["other"]
    Other_List = []

    # 2. Check basic directory exits
    if not os.path.exists(TR_Context_Memory_Dir):
        os.makedirs(TR_Context_Memory_Dir)
    if not os.path.exists(TR_Context_Memory_Dir + "/company_1"):
        os.makedirs(TR_Context_Memory_Dir + "/company_1")
    if not os.path.exists(TR_Context_Memory_Dir + "/incident_1"):
        os.makedirs(TR_Context_Memory_Dir + "/incident_1")

    # 3. open "unattached" and "other" context files if file exist
    if os.path.exists(TR_Unattached_Filename):
        with open(TR_Unattached_Filename, "r") as unattached_read:
            Unattached_List = json.load(unattached_read)
    if os.path.exists(TR_Other_Filename):
        with open(TR_Other_Filename, "r") as other_read:
            Other_List = json.load(other_read)

    # 4. for each object receieved, add it to the Other List, and remove it from the Unattached List
    report_id = []
    for stix_obj in stix_list:
        report_id.append(stix_obj["id"])
        # add the object to the Other List
        Other_List.append(stix_obj)
        # remove the object from the Unattached List based on the id
        for unattached in Unattached_List:
            if unattached["id"] == stix_obj["id"]:
                Unattached_List.remove(unattached)

    # 5. Now rewrite the  Other List and Unattached Lists to update the memory transfer
    with open(TR_Unattached_Filename, "w") as unattached_write:
        unattached_write.write(json.dumps(Unattached_List))
    with open(TR_Other_Filename, "w") as other_write:
        other_write.write(json.dumps(Other_List))

    return " transferred from 'Unattached' to 'Other' -> " + str(report_id)


def main(inputfile, outputfile):
    context_type = None
    stix_object = None
    if os.path.exists(inputfile):
        with open(inputfile, "r") as script_input:
            input = json.load(script_input)
    if "stix_list" in input:
        stix_list = input["stix_list"]

    # setup logger for execution
    result_string = move_unattached_to_other(stix_list)
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