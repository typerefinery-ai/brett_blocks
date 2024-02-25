
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
# Title: Update Company Relations
# Author: OS-Threat
# Organisation Repo: https://github.com/typerefinery-ai/brett_blocks
# Contact Email: denis@cloudaccelerator.co
# Date: 07/08/2023
#
# Description: This script is designed to take in a Stix Object ID
#       and return a Stix object
#
# One Mandatory Input:
# 1. Trigger
# Report Outpute
# 1. Report (string)
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
from stixorm.module.definitions.stix21 import (
    Relationship
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
identity_types = ["me", "team", "users", "assets", "systems"]

from datetime import datetime

def convert_dt(dt_stamp_string):
    if dt_stamp_string.find(".") >0:
        dt = datetime.strptime(dt_stamp_string, "%Y-%m-%dT%H:%M:%S.%fZ")
        microsecs = dt.microsecond
        milisecs = (round(microsecs / 1000))
        dt_list = dt_stamp_string.split('.')
        actual = dt_list[0] + "." + str(milisecs) + "Z"
    else:
        if dt_stamp_string.find("T") > 0:
            dt_list = dt_stamp_string.split('T')
            t_list = dt_list[1].split(':')
            if len(t_list) == 3:
                secs = t_list[2]
                sec_list = secs.split('Z')
                actual = dt_list[0] + "T" + t_list[0] + ":" + t_list[1] + ":" + sec_list[0] + ".000Z"
            else:
                mins = t_list[1]
                mins_list = mins.split('Z')
                actual = dt_list[0] + "T" + t_list[0] + ":" + mins_list[0] + ":00.000Z"
        else:
            actual = dt_stamp_string + "T00:00:00.000Z"
    return actual

def conv(stix_object):
    # Convert Stix Object to valid Python dict
    if type(stix_object) is dict:
        return stix_object
    string_dict = stix_object.serialize()
    jdict = json.loads(string_dict)
    time_list = ["created", "modified"]
    for tim in time_list:
        if tim in jdict:
            temp_string = convert_dt(jdict[tim])
            jdict[tim] = temp_string
    return jdict

def update_company_relations(reln_type=None):
    # 1. Extract the components of the object
    Paths = {}
    Object_lists = {}
    Object_ID_Lists = {}
    company = {}
    relation_list = []
    Paths["me"] = TR_Context_Memory_Dir + local["me"]
    Paths["team"] = TR_Context_Memory_Dir + local["team"]
    Paths["users"] = TR_Context_Memory_Dir + local["users"]
    Paths["company"] = TR_Context_Memory_Dir + local["company"]
    Paths["assets"] = TR_Context_Memory_Dir + local["assets"]
    Paths["systems"] = TR_Context_Memory_Dir + local["systems"]
    Paths["relations"] = TR_Context_Memory_Dir + local["relations"]

    # 2. Open All the Files that may contain identities first, then the company and then the relations
    for context in identity_types:
        if os.path.exists(Paths[context]):
            with open(Paths[context], "r") as mem_input:
                Object_lists[context] = json.load(mem_input)
        else:
            Object_lists[context] = []
    if os.path.exists(Paths["company"]):
        with open(Paths["company"], "r") as mem_input:
            Object_lists["company"] = json.load(mem_input)
            company = Object_lists["company"][0]
    else:
        Object_lists["company"] = []
        company = {}
    if os.path.exists(Paths["relations"]):
        with open(Paths["relations"], "r") as mem_input:
            Object_lists["relations"] = json.load(mem_input)
    else:
        Object_lists["relations"] = []

    # 3. Setup Existing List of Existing ID's in Relations
    source_id_list = [x["source_ref"] for x in Object_lists["relations"]]
    target_id_list = [x["target_ref"] for x in Object_lists["relations"]]
    # 4. Setup reduce lists of objects, that aren't in SRO's
    for context in identity_types:
            Object_lists[context] = [x for x in Object_lists[context] if x["type"] == "identity" and x["id"] not in target_id_list]

    # 5. if Me exists, or Team setup, then setup relationship_type
    New_Relations = []
    if company:
        if Object_lists["me"] and reln_type:
            me_ident = Object_lists["me"][0]
            temp_rel = Relationship(relationship_type=reln_type, source_ref=company["id"], target_ref=me_ident["id"])
            New_Relations.append(conv(temp_rel))
        if Object_lists["team"] !=  []: # and reln_type:
            for team_ident in Object_lists["team"]:
                temp_rel = Relationship(relationship_type=reln_type, source_ref=company["id"], target_ref=team_ident["id"])
                New_Relations.append(conv(temp_rel))
        if Object_lists["users"] != []:
            for team_ident in Object_lists["users"]:
                temp_rel = Relationship(relationship_type='employed-by', source_ref=company["id"], target_ref=team_ident["id"])
                New_Relations.append(conv(temp_rel))
        if Object_lists["assets"] != []:
            for team_ident in Object_lists["assets"]:
                temp_rel = Relationship(relationship_type='asset-of', source_ref=company["id"], target_ref=team_ident["id"])
                New_Relations.append(conv(temp_rel))
        if Object_lists["systems"] != []:
            for team_ident in Object_lists["systems"]:
                temp_rel = Relationship(relationship_type='system-of', source_ref=company["id"], target_ref=team_ident["id"])
                New_Relations.append(conv(temp_rel))

    # does file exist
    return_string = ""
    relation_list = Object_lists["relations"] + New_Relations
    with open(Paths["relations"], 'w') as f:
        f.write(json.dumps(relation_list))

    for reln in relation_list:
        return_string += "\n" + reln["relationship_type"] + ", " + reln["source_ref"] + ", " + reln["target_ref"]
    return " relations saved -> " + str(return_string)


def main(inputfile, outputfile):
    if os.path.exists(inputfile):
        with open(inputfile, "r") as script_input:
            input = json.load(script_input)
    reln_type = input["reln_type"]

    # setup logger for execution
    result_string = update_company_relations(reln_type)
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