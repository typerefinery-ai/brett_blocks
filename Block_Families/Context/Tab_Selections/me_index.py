
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
# Title: When Me tab selected, get data
# Author: OS-Threat
# Organisation Repo: https://github.com/typerefinery-ai/brett_blocks
# Contact Email: denis@cloudaccelerator.co
# Date: 07/08/2023
#
# Description: This script is designed to take in a Stix Object ID
#       and return a Stix object
#
# No Input:
# 1.
# One Output
# 1. Me and Team Hierarchy's
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
import copy
from Block_Families.General._library.convert_n_and_e import convert_relns, convert_sighting, convert_node, \
    refine_edges, generate_legend

import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

from datetime import datetime
from stixorm.module.typedb_lib.factories.auth_factory import get_auth_factory_instance
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
comp_list = ["me", "team"]


def get_me_index():
    show_sro = True
    me_index = {}
    stix_me_list = []
    stix_team_list = []
    # 1. Setup variables
    comp_obj = {}
    possible = []
    relations = []
    stix_incident_id = ""
    auth_factory = get_auth_factory_instance()
    auth = auth_factory.get_auth_for_import(import_type)
    auth_types = copy.deepcopy(auth["types"])
    # 2. open the company file, and then the assets, systems and users
    if os.path.exists(TR_Context_Memory_Dir + local["me"]):
        with open(TR_Context_Memory_Dir + local["me"], "r") as mem_input:
            stix_me_list = json.load(mem_input)
    if os.path.exists(TR_Context_Memory_Dir + local["team"]):
        with open(TR_Context_Memory_Dir + local["team"], "r") as mem_input:
            stix_team_list = json.load(mem_input)
    # 3. sort sightings by time
    if stix_me_list != []:
        me_index["name"] = "Type Refinery User"
        me_index["icon"] = "identity-person"
        me_index["type"] = ""
        me_index["edge"] = ""
        me_index["id"] = ""
        me_index["original"] = ""
        me_index["children"] = []
        children0 = me_index["children"]
        # 4. Process each sighting and place them into the children
        for obj in stix_me_list:
            if obj["type"] == "identity":
                sub_ids = []
                identity_obj = {}
                identity_obj["name"] = obj["name"]
                identity_obj["icon"] = obj["icon"]
                identity_obj["edge"] = "owner"
                identity_obj["type"] = obj["type"]
                identity_obj["id"] = obj["id"]
                identity_obj["original"] = obj["original"]
                if "extension-definition--66e2492a-bbd3-4be6-88f5-cc91a017a498" in obj:
                    if "email_addresses" in obj["extension-definition--66e2492a-bbd3-4be6-88f5-cc91a017a498"]:
                        email_addr_list = obj["extension-definition--66e2492a-bbd3-4be6-88f5-cc91a017a498"]["email_addresses"]
                        for email_addr in email_addr_list:
                            sub_ids.append(email_addr["email_address_ref"])
                    if "social_media_accounts" in obj["extension-definition--66e2492a-bbd3-4be6-88f5-cc91a017a498"]:
                        accounts_list = obj["extension-definition--66e2492a-bbd3-4be6-88f5-cc91a017a498"]["social_media_accounts"]
                        for usr_acct in accounts_list:
                            sub_ids.append(usr_acct["user_account_ref"])
                if sub_ids != []:
                    identity_obj["children"] = []
                    children1 = identity_obj["children"]
                    for sub_obj in comp_obj["users"]:
                        if sub_obj["id"] in sub_ids:
                            sub = {}
                            sub["name"] = obj["name"]
                            sub["icon"] = obj["icon"]
                            sub["edge"] = "owner-of"
                            sub["type"] = obj["type"]
                            sub["id"] = obj["id"]
                            sub["original"] = obj["original"]
                            children1.append(sub)
                children0.append(identity_obj)
        if stix_team_list != []:
            for obj in stix_team_list:
                if obj["type"] == "identity":
                    sub_ids = []
                    identity_obj = {}
                    identity_obj["name"] = obj["name"]
                    identity_obj["icon"] = obj["icon"]
                    identity_obj["edge"] = "team-member"
                    identity_obj["type"] = obj["type"]
                    identity_obj["id"] = obj["id"]
                    identity_obj["original"] = obj["original"]
                    if "extension-definition--66e2492a-bbd3-4be6-88f5-cc91a017a498" in obj:
                        if "email_addresses" in obj["extension-definition--66e2492a-bbd3-4be6-88f5-cc91a017a498"]:
                            email_addr_list = obj["extension-definition--66e2492a-bbd3-4be6-88f5-cc91a017a498"]["email_addresses"]
                            for email_addr in email_addr_list:
                                sub_ids.append(email_addr["email_address_ref"])
                        if "social_media_accounts" in obj["extension-definition--66e2492a-bbd3-4be6-88f5-cc91a017a498"]:
                            accounts_list = obj["extension-definition--66e2492a-bbd3-4be6-88f5-cc91a017a498"]["social_media_accounts"]
                            for usr_acct in accounts_list:
                                sub_ids.append(usr_acct["user_account_ref"])
                    if sub_ids != []:
                        identity_obj["children"] = []
                        children2 = identity_obj["children"]
                        for sub_obj in comp_obj["users"]:
                            if sub_obj["id"] in sub_ids:
                                sub = {}
                                sub["name"] = obj["name"]
                                sub["icon"] = obj["icon"]
                                sub["edge"] = "-of"
                                sub["type"] = obj["type"]
                                sub["id"] = obj["id"]
                                sub["original"] = obj["original"]
                                children2.append(sub)
                    children0.append(identity_obj)
    else:
        return me_index

    return me_index


def main(inputfile, outputfile):
    context_type = None
    stix_object = None
    if os.path.exists(inputfile):
        with open(inputfile, "r") as script_input:
            input = json.load(script_input)

    # setup logger for execution
    hierarchy = get_me_index()

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