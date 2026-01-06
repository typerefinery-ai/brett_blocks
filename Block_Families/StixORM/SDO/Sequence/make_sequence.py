
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
# Title: Make Sequence
# Author: OS-Threat
# Organisation Repo: https://github.com/typerefinery-ai/brett_blocks
# Contact Email: denis@cloudaccelerator.co
# Date: 07/08/2023
#
# Description: This script is designed to take in a Stix Object ID
#       and return a Stix object
#
# One Mandatory, One Optional Input:
# 1. Sequence Form
# 2. step_type(enum)
# 3. sequence type (enum)
# 4. sequenced_object {}
# 5. on completion (sequence)
# 6. on success (sequence)
# 7. on failure (sequence)
# 8. next steps (sequence)
# One Output
# 1. Indicator SDO  (Dict)
#
# This code is licensed under the terms of the BSD.
##########b####################################################################

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
from posixpath import basename
import json
import os

import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

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

def make_sequence(sequence_form, step_type=None, sequence_type=None, sequenced_object=None, on_completion=None, on_success=None, on_failure=None, next_steps=None):
    # 1. Extract the components of the object
    required = sequence_form["base_required"]
    optional = sequence_form["base_optional"]
    main = sequence_form["object"]
    extensions = sequence_form["extensions"]
    sub = sequence_form["sub"]
    contents = {}
    empties_removed = {}
    # 2. Setup Object Params first
    for k,v in main.items():
        contents[k] = v
    for k,v in optional.items():
        contents[k] = v
    if seq_ext_id in extensions:
        contents["extensions"] = {seq_ext_id: seq_ext}
    else:
        contents["extensions"] = {seq_ext_id: seq_ext}
    for k,v in sub.items():
        pass

    for (k,v) in contents.items():
        if v == "":
            continue
        elif v == []:
            continue
        elif v == None:
            continue
        else:
            empties_removed[k] = v


    if step_type:
        empties_removed["step_type"] = step_type

    if sequence_type:
        empties_removed["sequence_type"] = sequence_type

    if sequenced_object:
        empties_removed["sequenced_object"] = sequenced_object["id"]

    if on_completion:
        empties_removed["on_completion"] = on_completion["id"]

    if on_success:
        empties_removed["on_success"] = on_success["id"]

    if on_failure:
        empties_removed["on_failure"] = on_failure["id"]

    if next_steps:
        empties_removed["next_steps"] = next_steps

    if "modified" in required and required["modified"] == "":
        # object needs to be created
        stix_obj = Sequence(**empties_removed)

    else:
        # object needs to be updated, but we can't
        #  update properly yet, so recreate instead
        stix_obj = Sequence(**empties_removed)

    stix_dict = json.loads(stix_obj.serialize())
    time_list = ["created", "modified"]
    for tim in time_list:
        if tim in stix_dict:
            temp_string = convert_dt(stix_dict[tim])
            stix_dict[tim] = temp_string

    return stix_dict


def main(inputfile, outputfile):
    step_type = None
    sequence_type = None
    sequenced_object = None
    sequence_type = None
    on_completion = None
    on_success = None
    on_failure = None
    next_steps = None
    if os.path.exists(inputfile):
        with open(inputfile, "r") as script_input:
            input_data = json.load(script_input)
            if "sequence_form" in input_data:
                sequence_form = input_data["sequence_form"]
                if "step_type" in input_data:
                    step_type = input_data["step_type"]
                if "sequence_type" in input_data:
                    sequence_type = input_data["sequence_type"]
                if "sequenced_object" in input_data:
                    sequenced_object = input_data["sequenced_object"]
                if "on_completion" in input_data:
                    on_completion = input_data["on_completion"]
                if "on_success" in input_data:
                    on_success = input_data["on_success"]
                if "on_failure" in input_data:
                    on_failure = input_data["on_failure"]
                if "next_steps" in input_data:
                    next_steps = input_data["next_steps"]
            elif "api" in input_data:
                api_input = input_data["api"]
                sequence_form = api_input["sequence_form"]
                if "step_type" in api_input:
                    step_type = api_input["step_type"]
                if "sequence_type" in api_input:
                    sequence_type = api_input["sequence_type"]
                if "sequenced_object" in api_input:
                    sequenced_object = api_input["sequenced_object"]
                if "on_completion" in api_input:
                    on_completion = api_input["on_completion"]
                if "on_success" in api_input:
                    on_success = api_input["on_success"]
                if "on_failure" in api_input:
                    on_failure = api_input["on_failure"]
                if "next_steps" in api_input:
                    next_steps = api_input["next_steps"]

    # setup logger for execution
    stix_dict = make_sequence(sequence_form, step_type=step_type, sequence_type=sequence_type, sequenced_object=sequenced_object, on_completion=on_completion, on_success=on_success, on_failure=on_failure, next_steps=next_steps)
    results = {}
    results["sequence"] = []
    results["sequence"].append(stix_dict)
    with open(outputfile, "w") as outfile:
        json.dump(stix_dict, outfile)


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
  #main(args.inputfile, args.outputfile)

  main(args.inputfile, args.outputfile)


################################################################################
## footer end                                                                 ##
################################################################################