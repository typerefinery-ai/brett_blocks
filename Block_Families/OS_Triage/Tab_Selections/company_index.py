
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
# Title: When Company tab selected, get data
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
# 1. Company Hierarchy
#
# This code is licensed under the terms of the BSD.
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
TR_Common_Files = "./Common_Files"
common = [
    {"module": "convert_n_and_e", "file": "convert_n_and_e.py", "url" : "https://raw.githubusercontent.com/typerefinery-ai/brett_blocks/main/Block_Families/General/_library/convert_n_and_e.py"}
]

# OS_Triage Memory Stuff
TR_Context_Memory_Dir = "./Context_Mem"
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

comp_list = ["assets", "systems", "users"]



def get_company_index():
    show_sro = True
    company_index = {}
    stix_company_obj = {}
    # 1. Setup variables
    comp_obj = {}
    possible = []
    relations = []
    stix_incident_id = ""
    auth_factory = get_auth_factory_instance()
    auth = auth_factory.get_auth_for_import(import_type)
    auth_types = copy.deepcopy(auth["types"])
    local_map = {}
    with open(TR_Context_Memory_Dir + "/" + context_map, "r") as current_context:
        local_map = json.load(current_context)
        current_company_dir = local_map["current_company"]
        TR_Company_Context_Dir = TR_Context_Memory_Dir + "/" + current_company_dir
        # 2. open the company file, and then the assets, systems and users
        if os.path.exists(TR_Company_Context_Dir + comp_data["company"]):
            with open(TR_Company_Context_Dir + comp_data["company"], "r") as mem_input:
                stix_company_list = json.load(mem_input)
                stix_company_obj = stix_company_list[0]
                for key in comp_list:
                    if os.path.exists(TR_Company_Context_Dir + comp_data[key]):
                        with open(TR_Company_Context_Dir + comp_data[key], "r") as mem_input:
                            comp_obj[key] = json.load(mem_input)
        # 3. setup the root record
        if stix_company_obj != {}:
            company_index = stix_company_obj
            company_index["icon"] = "identity-organization"
            company_index["edge"] = ""
            company_index["children"] = []
            children0 = company_index["children"]
            # 4. Add the assets
            if comp_obj["assets"] != []:
                # 4A. First setup the sighting object
                level2 = {}
                level2["name"] = "Company Assets"
                level2["icon"] = "identity-asset"
                level2["type"] = "company"
                level2["heading"] = "Company Assets"
                level2["description"] = "Assets owned by the company"
                level2["id"] = ""
                level2["edge"] = "assets"
                level2["original"] = ""
                level2["children"] = []
                children2 = level2["children"]
                for obj in comp_obj["assets"]:
                    identity_obj = {}
                    identity_obj = obj
                    identity_obj["edge"] = "asset-of"
                    children2.append(identity_obj)
                children0.append(level2)
            if comp_obj["systems"] != []:
                # 4A. Add the systems objects
                level3 = {}
                level3["name"] = "Company Systems"
                level3["icon"] = "identity-system"
                level3["type"] = "company"
                level3["heading"] = "Company Systems"
                level3["description"] = "Systems owned by the company"
                level3["id"] = ""
                level3["edge"] = "systems"
                level3["original"] = ""
                level3["children"] = []
                children3 = level3["children"]
                for obj in comp_obj["systems"]:
                    identity_obj = {}
                    identity_obj = obj
                    identity_obj["edge"] = "system-of"
                    children3.append(identity_obj)
                children0.append(level3)
            if comp_obj["users"] != []:
                # 4B. Add the users objects
                level1 = {}
                level1["name"] = "Company Users"
                level1["icon"] = "identity-individual"
                level1["type"] = "company users"
                level1["heading"] = "Company Users"
                level1["description"] = "Users of company assets and systems"
                level1["id"] = ""
                level1["edge"] = "users-of"
                level1["original"] = ""
                level1["children"] = []
                children1 = level1["children"]
                for obj in comp_obj["users"]:
                    if obj["type"] == "identity":
                        sub_ids = []
                        user_obj = {}
                        user_obj = obj
                        user_obj["edge"] = "user-of"
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
                            user_obj["children"] = []
                            children2 = user_obj["children"]
                            for sub_obj in comp_obj["users"]:
                                if sub_obj["id"] in sub_ids:
                                    sub = {}
                                    sub = sub_obj
                                    sub["edge"] = "owner-of"
                                    children2.append(sub)
                        children1.append(user_obj)
                children0.append(level1)
        else:
            return company_index

    return company_index


def main(inputfile, outputfile):
    context_type = None
    stix_object = None
    if os.path.exists(inputfile):
        with open(inputfile, "r") as script_input:
            input = json.load(script_input)

    # setup logger for execution
    hierarchy = get_company_index()

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