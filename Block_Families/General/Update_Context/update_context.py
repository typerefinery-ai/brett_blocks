
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
# Title: Update Context
# Author: OS-Threat
# Organisation Repo: https://github.com/typerefinery-ai/brett_blocks
# Contact Email: denis@cloudaccelerator.co
# Date: 07/08/2023
#
# Description: This script is designed to take in a Stix Object ID
#       and return a Stix object
#
# Two Mandatory, Two Optional Input:
# 1. OS_Threat_Context
# 2. Connection
# 3. Original_Stix_list
# 4. Updated_Stix_List
# One Output
# 1. Update Results (JSON)
#
# This code is licensed under the terms of the BSD.
##############################################################################

from stixorm.module.definitions.stix21 import (
    ObservedData, IPv4Address, EmailAddress, DomainName, EmailMessage, URL, UserAccount, File,
    Identity, Incident, Note, Sighting, Indicator, Relationship, Location, Software, Process, Bundle
)
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

from stixorm.module.typedb import TypeDBSource, TypeDBSink
from stixorm.module.authorise import import_type_factory
from posixpath import basename
from Block_Families.General._library.update import find_list_diff, find_obj_diff, handle_object_diff
import json
import os

import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

import_type = import_type_factory.get_all_imports()

def load_context(OS_Threat_Context_Memory_Path):
    # 1. Load the Context
    with open(OS_Threat_Context_Memory_Path, "r") as context_file:
        OS_Threat_Context = json.load(context_file)
    #
    # 2. Setup the  TR User Context
    #
    local = OS_Threat_Context["local"]
    me = local["me"]
    team = local["team"]
    company = local["company"]
    systems = local["systems"]
    assets = local["assets"]
    #
    # 3. Setup the Incident Context
    #
    incident = OS_Threat_Context["incident"]
    sequence_start_objs = incident["sequence_start_objs"]
    sequence_objs = incident["sequence_objs"]
    task_objs = incident["task_objs"]
    event_objs = incident["event_objs"]
    impact_objs = incident["impact_objs"]
    other_object_objs = incident["other_object_objs"]
    incident_obj = incident["incident_obj"]

    #
    # 4. Load the TypeDB Context
    #
    typedb = OS_Threat_Context["typedb"]
    t_sequence_start_objs = typedb["sequence_start_objs"]
    t_sequence_objs = typedb["sequence_objs"]
    t_task_objs = typedb["task_objs"]
    t_event_objs = typedb["event_objs"]
    t_impact_objs = typedb["impact_objs"]
    t_other_object_objs = typedb["other_object_objs"]
    t_incident_obj = typedb["incident_obj"]
    #
    # 5. Add the lists together and put them into typedb
    #
    typedb_add_list = t_sequence_start_objs + t_sequence_objs + t_task_objs + t_event_objs + t_other_object_objs + t_impact_objs
    typedb_add_list = typedb_add_list + me + team + company + systems + assets
    second_list = sequence_start_objs + sequence_objs + task_objs + event_objs + impact_objs + other_object_objs
    second_list = second_list + me + team + company + systems + assets
    # typedb_add_list.append(t_incident_obj)
    # typedb_sink = TypeDBSink(connection, True, import_type)
    # results_raw = typedb_sink.add(typedb_add_list)
    # result_list = [res.model_dump_json() for res in results_raw]
    # for res in result_list:
    #     print(f"\n result is -> {res}")
    return typedb_add_list, t_incident_obj, second_list, incident_obj


def update_context(OS_Threat_Context, connection, original_stix,  current_stix):
    OS_Threat_Context_Memory_Path = "./Orchestration/Context_Mem/OS_Threat_Context.json"
    # 1. First add the Step 1 objects to typedb
    #
    t_original_list, t_original_incident_obj, current_list, current_incident_obj = load_context(OS_Threat_Context_Memory_Path)
    #
    # 2. Find out the set operations between the lists of object already in TypeDB, and the list of objects now
    delete_object_ids, add_objects_list, may_have_changed_list = find_list_diff(t_original_list, current_list)
    # 3. Setup TypeDB Sink and Source
    reinitilise = False
    typedb_sink = TypeDBSink(connection=connection, clear=reinitilise, import_type=import_type)
    typedb_source = TypeDBSource(connection=connection,)
    # 4. Add the new object list to Typedb
    results_raw = typedb_sink.add(add_objects_list)
    result_list = [res.model_dump_json() for res in results_raw]
    print(f"\n result type is {type(result_list)} \n result is -> {result_list}")
    # 5. Run the Delete object option
    delete_raw = typedb_sink.delete(delete_object_ids)
    print(f"\n delete_raw type is {type(delete_raw)} \n delete_raw is -> {delete_raw}")
    # 6. Calculate whether update is needed per object, if so push it
    change_list = []
    for current_obj in may_have_changed_list:
        orig_object = [x for x in t_original_list if x["id"] == current_obj["id"]]
        obj_diff = find_obj_diff(orig_object[0], current_obj)
        if obj_diff != {}:
            diff_report = handle_object_diff(obj_diff, orig_object[0], current_obj, connection)
            change_list.append(diff_report)
    report = {}
    report["add_result"] = result_list
    report["delete_raw"] = delete_raw
    report["changed_list"] = change_list
    report["original_list"] = t_original_list
    report["original_incident"] = t_original_incident_obj
    report["current_list"] = current_list
    report["current_incident"] = current_incident_obj

    return report


def main(inputfile, outputfile):
    OS_Threat_Context = ""
    connection = {}
    original_stix = {}
    current_stix = {}
    if os.path.exists(inputfile):
        with open(inputfile, "r") as script_input:
            input_data = json.load(script_input)

    if "OS_Threat_Context" in input_data:
        OS_Threat_Context = input_data["OS_Threat_Context"]
    if "connection" in input_data:
        connection = input_data["connection"]
    if "original_stix" in input_data:
        original_stix = input_data["original_stix"]
    if "current_stix" in input_data:
        current_stix = input_data["current_stix"]

    # setup logger for execution
    report = {}
    report = update_context(OS_Threat_Context, connection, original_stix,  current_stix)
    results = {}
    results["context_update_record"] = []
    results["context_update_record"].append(json.loads(report))
    with open(outputfile, "w") as outfile:
        json.dump(results, outfile)


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