
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
# Title: Save Object from Attack Navigator into OS_Triage Context
# Author: OS-Threat
# Organisation Repo: https://github.com/typerefinery-ai/brett_blocks
# Contact Email: brett@osthreat.com
# Date: 07/08/2023
#
# Description: This script is designed to take in a `stix_id` from an Attack Navigator,
#       and save it into the OS_Triage Context
#
# Two Mandatory Inputs:
# 1. Stix ID
# 2. Context Type
# One Output
# 1. Context Saved Return
#
# This code is licensed under the terms of the Apache 2.
##############################################################################

from stixorm.module.authorise import import_type_factory
# from Block_Families.General._library.
# from Orchestration.Common.
from urllib.request import urlretrieve
import json
import sys
import importlib.util
import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

import_type = import_type_factory.get_all_imports()

# Attack Navigator Stuff
import requests
# stix2's MemoryStore is no longer used: the bundles are searched as plain dicts so the object can be
# handed to parse.wrap_stix_dict() unchanged (see get_data_from_branch).

class AttackSourceError(Exception):
    """The ATT&CK source could not be read.

    `reason` uses the vocabulary agreed in alpha-launch docs/decisions/0017 so the Flow route can map
    it to a status code without parsing prose.
    """

    def __init__(self, reason, detail):
        super().__init__(detail)
        self.reason = reason
        self.detail = detail


# The source is PINNED to a release tag rather than tracking master (R4.2b). Bumping this is a
# deliberate act: the demo must not change behaviour because MITRE published something. This is not
# hypothetical - alpha-launch docs/issues/0176 is the Navigator failing for exactly that reason.
ATTACK_DATA_REF = "v19.2"
ATTACK_DATA_BASE = "https://raw.githubusercontent.com/mitre-attack/attack-stix-data"
ATTACK_DOMAINS = ["enterprise-attack", "mobile-attack", "ics-attack"]

# Bundles are large - enterprise-attack alone is ~54 MB at v19.2 - so each is cached on disk after
# the first fetch (R4.2a). An uncached download per right-click is visible on stage.
TR_Attack_Cache_Dir = "./generated/os-triage/context_mem/attack_cache"


def attack_cache_path(domain):
    return f"{TR_Attack_Cache_Dir}/{domain}-{ATTACK_DATA_REF}.json"


def get_data_from_branch(domain):
    """Return one ATT&CK domain's STIX objects, from the on-disk cache when present.

    Domain is 'enterprise-attack', 'mobile-attack' or 'ics-attack'. Returns a list of plain dicts:
    the caller needs a dict for parse.wrap_stix_dict(), and scanning the list is far cheaper than
    building a stix2 MemoryStore over ~26,000 objects just to fetch one by id.
    """
    cache_file = attack_cache_path(domain)
    if os.path.exists(cache_file):
        print(f"ATT&CK cache hit: {domain} at {cache_file}")
        try:
            with open(cache_file, "r") as cached:
                return json.load(cached)
        except (ValueError, OSError) as cache_err:
            # A truncated cache must not masquerade as "object not found".
            print(f"ATT&CK cache unreadable for {domain} ({cache_err}), refetching")

    url = f"{ATTACK_DATA_BASE}/{ATTACK_DATA_REF}/{domain}/{domain}.json"
    print(f"ATT&CK cache miss: {domain}, fetching {url}")
    # A network failure used to surface as an unhandled exception, and a 404/429 used to surface as a
    # JSON decode error -- both indistinguishable from "object not found" by the time they reached the
    # caller (docs/decisions/0017).
    try:
        response = requests.get(url, timeout=120)
    except requests.RequestException as err:
        print(f"ATT&CK source unreachable: {domain} -> {err}")
        raise AttackSourceError("source_unreachable", f"{domain}: {err}")
    if response.status_code == 429:
        print(f"ATT&CK source rate limited: {domain}")
        raise AttackSourceError("rate_limited", f"{domain}: HTTP 429 from attack-stix-data")
    if response.status_code != 200:
        print(f"ATT&CK source returned HTTP {response.status_code}: {domain}")
        raise AttackSourceError("source_unreachable", f"{domain}: HTTP {response.status_code}")
    try:
        stix_json = response.json()
    except ValueError as err:
        raise AttackSourceError("source_unreachable", f"{domain}: response was not JSON ({err})")

    objects = stix_json.get("objects", [])
    print(f"ATT&CK domain loaded: {domain} ({len(objects)} objects at {ATTACK_DATA_REF})")

    # Write through a temp file and rename, so a killed process cannot leave a half-written bundle
    # that later reads as an empty domain.
    try:
        if not os.path.exists(TR_Attack_Cache_Dir):
            os.makedirs(TR_Attack_Cache_Dir)
        temp_file = cache_file + ".tmp"
        with open(temp_file, "w") as out:
            json.dump(objects, out)
        os.replace(temp_file, cache_file)
        print(f"ATT&CK domain cached: {domain} at {cache_file}")
    except OSError as cache_write_err:
        # Caching is an optimisation; failing to cache must not fail the request.
        print(f"ATT&CK cache write failed for {domain}: {cache_write_err}")

    return objects



# Common File Stuff
TR_Common_Files = "./generated/os-triage/common_files"
common = [
    {"module": "parse", "file": "parse.py", "url" : "https://raw.githubusercontent.com/typerefinery-ai/brett_blocks/refs/heads/main/Block_Families/General/_library/parse.py"}
]
# OS_Triage Memory Stuff
TR_Context_Memory_Dir = "./generated/os-triage/context_mem"
TR_User_Dir = "/usr"
context_map = "context_map.json"
user_data = {
    "global": "/global_variables_dict.json",
    "me": "/cache_me.json",
    "team": "/cache_team.json"
}
comp_data = {
    "users": "/users.json",
    "company" : "/company.json",
    "platforms" : "/platforms.json",
    "systems" : "/systems.json"
}
incident_data = {
    "incident" : "/incident.json",
    "start" : "/sequence_start_refs.json",
    "sequence" : "/sequence_refs.json",
    "impact" : "/impact_refs.json",
    "event" : "/event_refs.json",
    "task" : "/task_refs.json",
    "other" : "/other_object_refs.json",
    "unattached" : "/unattached_objs.json"
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

# NOTE: the settings download that used to live here has been REMOVED (alpha-launch docs/issues/0068).
#
# It fetched User_Options/options.json from `refs/heads/main` and guarded on the *directory* rather
# than the file, so on a clean machine -- where the directory does not yet exist -- it installed the
# stale `main` copy, which defines only `composer_options`. The sections the options algorithms read
# (`common`, `colours`) live on `os_triage`, and installing the wrong file is what made both #82
# options APIs answer {"error":"true"} with KeyError: 'current_theme' (docs/issues/0041).
#
# This block never read a settings value -- TR_Settings_Dir existed only to guard its own download --
# so the download is deleted rather than repaired. Settings belong to the options algorithms that
# own them. ! The same pattern still exists in ~20 sibling blocks here; fixing those is a separate
# change (0068 Option 3), not something to do file-by-file.


def download_common(module_list):
    for module in module_list:
        # Step 1: download the module
        result = urlretrieve(module["url"], TR_Common_Files + "/" + module["file"])
        print(f'common file result ->', result)
        # Step 2: install the module

def add_node(node, context_dir, context_type):
    # This block's copy took TWO parameters and hardcoded comp_data["company"], while its only caller
    # passed THREE and meant "unattached" - so every call raised TypeError, and had it not, it would
    # have written the company file instead of the scratch pad. The 3-parameter form below is the one
    # all 13 sibling blocks use (see Save_Context/save_unattached_context.py).
    exists = False
    stix_nodes_list = []
    if  os.path.exists(context_dir + incident_data[context_type]):
        with open(context_dir + incident_data[context_type], "r") as mem_input:
            stix_nodes_list = json.load(mem_input)
            for i in range(len(stix_nodes_list)):
                if stix_nodes_list[i]["id"] == node["id"]:
                    stix_nodes_list[i] = node
                    exists = True
            if not exists:
                stix_nodes_list.append(node)
    else:
        stix_nodes_list = [node]

    with open(context_dir + incident_data[context_type], 'w') as f:
        f.write(json.dumps(stix_nodes_list))


def retrieve_attack_object_and_save_in_unattached(stix_id):
    # Returns a STRUCTURED result, not a message string (docs/decisions/0017):
    #   success -> {"ok": True,  "stix_id": "<id>", "domain": "<attack domain>"}
    #   failure -> {"ok": False, "reason": "<not_found|source_unreachable|rate_limited|
    #                                       no_current_incident|bad_request>", "detail": "..."}
    # The Flow route maps `reason` to 404 / 502 / 429 / 409 and passes the body through. The previous
    # contract returned prose with HTTP 200 for both outcomes, so a caller could not tell a failure
    # from a success without reading English.
    if not stix_id:
        return {"ok": False, "reason": "bad_request", "detail": "no stix_id supplied"}

    # 1. Retrieve the object from the Attack Navigator
    # A. Setup memory stores for each of the ATT&CK domains
    attack_dict = {}
    found_in = None
    try:
        # Each domain is searched in turn and the search STOPS at the first hit. The previous version
        # fetched mobile AND ics before testing either, so a mobile technique still paid for the ics
        # bundle. Note wrap_stix_dict() takes a DICT: passing stix2's serialize() output (a JSON
        # STRING, as this block used to) raises AttributeError on .get() before anything is saved.
        for domain in ATTACK_DOMAINS:
            objects = get_data_from_branch(domain)
            for candidate in objects:
                if candidate.get("id") == stix_id:
                    attack_dict = candidate
                    found_in = domain
                    break
            if found_in:
                print(f"ATT&CK object {stix_id} found in {found_in}")
                break
        if not found_in:
            print(f"ATT&CK Object not found: {stix_id}")
            return {"ok": False, "reason": "not_found", "detail": str(stix_id)}
    except AttackSourceError as err:
        # ! Distinguish "we could not ask" from "it is not there". Reporting an unreachable source as
        # not_found would send an analyst looking for a typo in a correct id.
        return {"ok": False, "reason": err.reason, "detail": err.detail}


    # 1.B Find Current Incident directory
    #
    # ! There may be no current incident -- the map file can be absent, or carry no `current_incident`.
    # That used to raise (an unhandled IOError or KeyError) and surface as a 500 with a stack trace;
    # 0017 makes it a reportable outcome, because "nowhere to put it" is a normal state the analyst
    # can fix, not a crash.
    local_map = {}
    context_map_path = TR_Context_Memory_Dir + "/" + context_map
    if not os.path.exists(context_map_path):
        print(f"no context map at {context_map_path}")
        return {"ok": False, "reason": "no_current_incident", "detail": f"no context map at {context_map_path}"}
    with open(context_map_path, "r") as current_context:
        local_map = json.load(current_context)
        # 1. Setup the directory
        current_incident_dir = local_map.get("current_incident")
        if not current_incident_dir:
            print("context map has no current_incident")
            return {"ok": False, "reason": "no_current_incident", "detail": "context map has no current_incident"}
        TR_Incident_Context_Dir = TR_Context_Memory_Dir + "/" + current_incident_dir
        # 2. Check if the key directories exist, if not make them, and download common files
        # if not os.path.exists(TR_Common_Files):
        #     os.makedirs(TR_Common_Files)
        #     download_common(common)
        if not os.path.exists(TR_Context_Memory_Dir):
            os.makedirs(TR_Context_Memory_Dir)
        if not os.path.exists(TR_Context_Memory_Dir + "/usr"):
            os.makedirs(TR_Context_Memory_Dir + "/usr")
        # if not os.path.exists(TR_Context_Memory_Dir + "/incident_1"):
        #     os.makedirs(TR_Context_Memory_Dir + "/incident_1")

        # 3. Now we are sure the common files exist, we need to import them
        # Specify the path to the Nodes and Edges module
        module_path = TR_Common_Files + '/' + common[0]["file"]
        # Load the module spec using importlib.util.spec_from_file_location
        spec = importlib.util.spec_from_file_location('parse', module_path)
        # Create the module from the specification
        parse = importlib.util.module_from_spec(spec)
        # Load the module
        spec.loader.exec_module(parse)
        # 4. Wrap the object
        wrapped = parse.wrap_stix_dict(attack_dict)
        # 5. Add the object to the unattached context
        add_node(wrapped, TR_Incident_Context_Dir, "unattached")

    print(f"object saved to unattached context: {wrapped['id']} (from {found_in})")
    return {"ok": True, "stix_id": str(wrapped["id"]), "domain": found_in}



def main(inputfile, outputfile):
    stix_id = None
    if os.path.exists(inputfile):
        with open(inputfile, "r") as script_input:
            input = json.load(script_input)
            print(f"%%%% \ninput->{input}")
            stix_id = input["stix_id"]

    # setup logger for execution
    # `context_result` is now the structured object from docs/decisions/0017 rather than a message
    # string. The Flow route reads `context_result.ok` and maps `context_result.reason` to a status
    # (not_found -> 404, source_unreachable -> 502, rate_limited -> 429, no_current_incident -> 409).
    result = retrieve_attack_object_and_save_in_unattached(stix_id)
    print(f"%%%% \nresult->{result}")
    context_result = {}
    context_result["context_result"] = result
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