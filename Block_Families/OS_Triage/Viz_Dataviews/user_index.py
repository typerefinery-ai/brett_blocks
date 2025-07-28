
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
# Title: When User tab is selected, get data
# Author: OS-Threat
# Organisation Repo: https://github.com/typerefinery-ai/brett_blocks
# Contact Email: brett@osthreat.com
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
# This code is licensed under the terms of the Apache 2.
##############################################################################

from stixorm.module.authorise import import_type_factory
import json
import copy

import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

from stixorm.module.typedb_lib.factories.auth_factory import get_auth_factory_instance
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
key_list = ["me", "team"]


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
    if os.path.exists(TR_Context_Memory_Dir + TR_User_Dir + "/" + user_data["me"]):
        with open(TR_Context_Memory_Dir + TR_User_Dir + "/" + user_data["me"], "r") as mem_input:
            stix_me_list = json.load(mem_input)
    if os.path.exists(TR_Context_Memory_Dir + TR_User_Dir + "/" + user_data["team"]):
        with open(TR_Context_Memory_Dir + TR_User_Dir + "/" + user_data["team"], "r") as mem_input:
            stix_team_list = json.load(mem_input)
    # 3. sort sightings by time
    me_index["name"] = "Type Refinery User"
    me_index["icon"] = "identity-class"
    me_index["type"] = ""
    me_index["heading"] = "Type Refinery User"
    me_index["description"] = "User identity, email addresses, contact numbers and user accounts"
    me_index["edge"] = ""
    me_index["id"] = ""
    me_index["original"] = ""
    me_index["children"] = []
    children0 = me_index["children"]
    # 4. Process each sighting and place them into the children
    if stix_me_list != []:
        for obj in stix_me_list:
            if obj["type"] == "identity":
                sub_ids = []
                identity_obj = {}
                identity_obj = obj
                identity_obj["edge"] = "owner"
                exts = obj['original']['extensions']
                if "extension-definition--66e2492a-bbd3-4be6-88f5-cc91a017a498" in exts:
                    if "email_addresses" in exts["extension-definition--66e2492a-bbd3-4be6-88f5-cc91a017a498"]:
                        email_addr_list = exts["extension-definition--66e2492a-bbd3-4be6-88f5-cc91a017a498"]["email_addresses"]
                        for email_addr in email_addr_list:
                            sub_ids.append(email_addr["email_address_ref"])
                    if "social_media_accounts" in exts["extension-definition--66e2492a-bbd3-4be6-88f5-cc91a017a498"]:
                        accounts_list = exts["extension-definition--66e2492a-bbd3-4be6-88f5-cc91a017a498"]["social_media_accounts"]
                        for usr_acct in accounts_list:
                            sub_ids.append(usr_acct["user_account_ref"])
                if sub_ids != []:
                    identity_obj["children"] = []
                    children1 = identity_obj["children"]
                    for sub_obj in stix_me_list:
                        if sub_obj["id"] in sub_ids:
                            sub = {}
                            sub = sub_obj
                            sub["edge"] = "owner-of"
                            children1.append(sub)
                children0.append(identity_obj)
        if stix_team_list != []:
            for obj in stix_team_list:
                if obj["type"] == "identity":
                    sub_ids = []
                    identity_obj = {}
                    identity_obj = obj
                    identity_obj["edge"] = "team-member"
                    exts = obj['original']['extensions']
                    if "extension-definition--66e2492a-bbd3-4be6-88f5-cc91a017a498" in exts:
                        if "email_addresses" in exts["extension-definition--66e2492a-bbd3-4be6-88f5-cc91a017a498"]:
                            email_addr_list = exts["extension-definition--66e2492a-bbd3-4be6-88f5-cc91a017a498"]["email_addresses"]
                            for email_addr in email_addr_list:
                                sub_ids.append(email_addr["email_address_ref"])
                        if "social_media_accounts" in exts["extension-definition--66e2492a-bbd3-4be6-88f5-cc91a017a498"]:
                            accounts_list = exts["extension-definition--66e2492a-bbd3-4be6-88f5-cc91a017a498"]["social_media_accounts"]
                            for usr_acct in accounts_list:
                                sub_ids.append(usr_acct["user_account_ref"])
                    if sub_ids != []:
                        identity_obj["children"] = []
                        children2 = identity_obj["children"]
                        for sub_obj in stix_team_list:
                            if sub_obj["id"] in sub_ids:
                                sub = {}
                                sub = sub_obj
                                sub["edge"] = "owner-of"
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