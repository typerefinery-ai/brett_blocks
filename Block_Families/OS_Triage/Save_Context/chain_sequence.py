
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
# Title: Save Incident Context
# Author: OS-Threat
# Organisation Repo: https://github.com/typerefinery-ai/brett_blocks
# Contact Email: brett@osthreat.com
# Date: 07/08/2023
#
# Description: This script is designed to take in a Stix Object ID
#       and return a Stix object
#
# One Mandatory Input:
# 1. Stix-type Object
# 2. Context Type
# One Output
# 1. Context Memory Return Message
#
#
# This code is licensed under the terms of the Apache 2.
##############################################################################

from stixorm.module.definitions.stix21 import (
    ObservedData, IPv4Address, EmailAddress, DomainName, EmailMessage, URL, UserAccount, File,
    Identity, Incident, Indicator, Sighting, Indicator, Relationship, Location, Software, Process, Bundle
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
# from Block_Families.General._library.
# from Orchestration.Common.
from urllib.request import urlretrieve
import json
import sys
import importlib.util
import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
import os
import_type = import_type_factory.get_all_imports()


# 0-A-2  Extensions and Extension ID Definition's that are common
sight_ext = SightingEvidence(extension_type="property-extension")
sight_ext_id = "extension-definition--0d76d6d9-16ca-43fd-bd41-4f800ba8fc43"
event_ext = EventCoreExt(extension_type="new-sdo")
event_ext_id = "extension-definition--4ca6de00-5b0d-45ef-a1dc-ea7279ea910e"
event_ext_dict = {event_ext_id: event_ext}
seq_ext = SequenceExt(extension_type="new-sdo")
seq_ext_id = 'extension-definition--be0c7c79-1961-43db-afde-637066a87a64'
seq_ext_dict = {seq_ext_id: seq_ext}
imp_ext = ImpactCoreExt(extension_type="new-sdo")
imp_ext_id = 'extension-definition--7cc33dd6-f6a1-489b-98ea-522d351d71b9'
anec_ext = AnecdoteExt(extension_type="new-sco")
anec_ext_id = 'extension-definition--23676abf-481e-4fee-ac8c-e3d0947287a4'
anec_ext_dict = {anec_ext_id:anec_ext}
task_ext = TaskCoreExt(extension_type="new-sdo")
task_ext_id = 'extension-definition--2074a052-8be4-4932-849e-f5e7798e0030'
task_ext_dict = {task_ext_id: task_ext}
ident_ext_id = 'extension-definition--66e2492a-bbd3-4be6-88f5-cc91a017a498'
inc_ext_id = "extension-definition--ef765651-680c-498d-9894-99799f2fa126"
from datetime import datetime

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
    "behavior" : "/behavior_refs.json",
    "other" : "/other_object_refs.json",
    "unattached" : "/unattached_objs.json",
    "unattached_relations" : "/unattached_relation.json",
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
key_list = ["start", "sequence", "impact", "event", "task", "other"]

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

def add_node(node, context_dir, context_type):
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


def add_edge(edge, context_dir, context_type):
    exists = False
    stix_edge_list = []
    if os.path.exists(context_dir + incident_data[context_type]):
        with open(context_dir + incident_data[context_type], "r") as mem_input:
            stix_edge_list = json.load(mem_input)
            for i in range(len(stix_edge_list)):
                if stix_edge_list[i]["source"] == edge["source"] and stix_edge_list[i]["target"] == edge["target"]:
                    stix_edge_list[i] = edge
                    exists = True
            if not exists:
                stix_edge_list.append(edge)
    else:
        stix_edge_list = [edge]
    with open(context_dir + incident_data[context_type], 'w') as f:
        f.write(json.dumps(stix_edge_list))



def create_start_sequence(sequence_object, TR_Incident_Context_Dir):
    # Create a start sequence object
    start_sequence_object = {}
    start_sequence_object = Sequence(
        sequence_type=sequence_object["sequence_type"],
        step_type="start_step",
        next_step_refs=[sequence_object["id"]]
    )
    stix_dict = json.loads(start_sequence_object.serialize())
    time_list = ["created", "modified"]
    for tim in time_list:
        if tim in stix_dict:
            temp_string = convert_dt(stix_dict[tim])
            stix_dict[tim] = temp_string
    
    # Specify the path to the Nodes and Edges module
    module_path = TR_Common_Files + '/' + common[0]["file"]
    # Load the module spec using importlib.util.spec_from_file_location
    spec = importlib.util.spec_from_file_location('n_and_e', module_path)
    # Create the module from the specification
    n_and_e = importlib.util.module_from_spec(spec)
    # Load the module
    spec.loader.exec_module(n_and_e)
    if "original" in stix_dict:
        wrapped = True

    if wrapped:
        add_node(stix_dict, "start")
    else:
        nodes, edges = n_and_e.convert_node(stix_dict)
        add_node(nodes[0], TR_Incident_Context_Dir, "start")
        for edge in edges:
            add_edge(edge, TR_Incident_Context_Dir, "edges")

    # Make the return message
    return_message = " start sequence created and registered - \nstix_id -> " + str(stix_dict["id"])
    return return_message

def chain_sequence_objects(last_sequence_object, sequence_object, TR_Incident_Context_Dir):
    wrapped = False
    # Link from last sequence to new sequence in the next_step_refs field
    original_last_sequence_object = last_sequence_object.get("original", {})
    next_step_list = original_last_sequence_object.get("next_step_refs", [])
    next_step_list.append(sequence_object["id"])
    original_last_sequence_object["next_step_refs"] = next_step_list    
    
    
    # Specify the path to the Nodes and Edges module
    module_path = TR_Common_Files + '/' + common[0]["file"]
    # Load the module spec using importlib.util.spec_from_file_location
    spec = importlib.util.spec_from_file_location('n_and_e', module_path)
    # Create the module from the specification
    n_and_e = importlib.util.module_from_spec(spec)
    # Load the module
    spec.loader.exec_module(n_and_e)
    nodes, edges = n_and_e.convert_node(original_last_sequence_object)
    add_node(nodes[0], TR_Incident_Context_Dir, "sequence")
    for edge in edges:
        add_edge(edge, TR_Incident_Context_Dir, "edges")

    # Make the return message
    return_message = " sequence chained and registered - \nstix_id -> " + str(last_sequence_object["id"])
    return return_message



def chain_sequence(sequence_object):
    # 0 Check for "original"
    return_message = ""
    wrapped = False
    sequence_type = sequence_object.get("type", "")
    if "original" in sequence_object:
        wrapped = True
    # 1.B Find Current Incident directory
    local_map = {}
    with open(TR_Context_Memory_Dir + "/" + context_map, "r") as current_context:
        local_map = json.load(current_context)
        # 1. Setup the incident context directory
        current_incident_dir = local_map["current_incident"]
        TR_Incident_Context_Dir = TR_Context_Memory_Dir + "/" + current_incident_dir
        # 2. Get any start seqeunces and any existing sequences
        start_exists = False
        sequence_start_list = []
        sequences_list = []
        sequence_start_object = {}
        last_sequence_object = {}
        last_id = ""
        if os.path.exists(TR_Incident_Context_Dir + incident_data["start"]):
            with open(TR_Incident_Context_Dir + incident_data["start"], "r") as mem_input:
                sequence_start_list = json.load(mem_input)
        if os.path.exists(TR_Incident_Context_Dir + incident_data["sequence"]):
            with open(TR_Incident_Context_Dir + incident_data["sequence"], "r") as mem_input:
                sequence_list = json.load(mem_input)
        # 3. Isolate Existing Records of Starting Sequence Type
        for seq in sequence_start_list:
            if seq["original"]["sequence_type"] == sequence_type:
                sequence_start_object = seq
                original = seq.get("original", {})
                last_id_list = original.get("next_step_refs", [])
                last_id = last_id_list[0] if last_id_list else ""
                start_exists = True
        # 4. Isolate Existing Records of Sequence Type
        sequence_type_object_list = [x for x in sequence_list if x["original"]["sequence_type"] == sequence_type]
        for seq in sequence_type_object_list:
            if seq["original"]["id"] == last_id:
                last_sequence_object = seq
                original = seq.get("original", {})
                next_step_list = original.get("next_step_refs", [])
                if next_step_list != []:
                    last_id = next_step_list[0]
        # 5. Either create start, or link to end of chain
        if last_id == "":  # No Starting Sequence Exists - Create it
            return_message = create_start_sequence(sequence_object, TR_Incident_Context_Dir)        
        else:  # Link from last sequence to new sequence in the next_step_refs field
            return_message = chain_sequence_objects(last_sequence_object, sequence_object, TR_Incident_Context_Dir)
    return return_message


def main(inputfile, outputfile):
    context_type_string = ""
    stix_object = None
    if os.path.exists(inputfile):
        with open(inputfile, "r") as script_input:
            input_data = json.load(script_input)
            print(f"input data->{input_data}")
            if "sequence" in input_data:
                sequence_object = input_data["sequence_object"]
                result_string = chain_sequence(sequence_object)
            elif "api" in input_data:
                api_input_data = input_data["api"]
                stix_object = api_input_data["sequence_object"]
                if "sequence" in input_data:
                    sequence_object = input_data["sequence_object"]
                    result_string = chain_sequence(sequence_object)

            # setup logger for execution

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