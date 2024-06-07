
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
# Title: Make Impact
# Author: OS-Threat
# Organisation Repo: https://github.com/typerefinery-ai/brett_blocks
# Contact Email: denis@cloudaccelerator.co
# Date: 07/08/2023
#
# Description: This script is designed to take in a Stix Object ID
#       and return a Stix object
#
# One Mandatory, One Optional Input:
# 1. Impact_Form
# 2. changed_objects  (optional
# One Output
# 1. Impact SDO  (Dict)
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

def make_impact(impact_form, impacted_entity_counts=None, impacted_refs=None, superseded_by_ref=None):
    # 1. Extract the components of the object
    required = impact_form["base_required"]
    optional = impact_form["base_optional"]
    main = impact_form["object"]
    extensions = impact_form["extensions"]
    sub = impact_form["sub"]
    contents = {}
    empties_removed = {}
    # 2. Setup Object Params first
    for k,v in main.items():
        contents[k] = v
    for k,v in optional.items():
        contents[k] = v
    for k,v in extensions.items():
        if k == "availability":
            contents["extensions"] = {"availability": Availability(**v)}
        elif k == "confidentiality":
            contents["extensions"] = {"confidentiality": Confidentiality(**v)}
        elif k == "external":
            contents["extensions"] = {"external": External(**v)}
        elif k == "integrity":
            contents["extensions"] = {"integrity": Integrity(**v)}
        elif k == "monetary":
            contents["extensions"] = {"monetary": Monetary(**v)}
        elif k == "physical":
            contents["extensions"] = {"physical": Physical(**v)}
        elif k == "traceability":
            contents["extensions"] = {"traceability": Traceability(**v)}
    if imp_ext_id in extensions:
        contents["extensions"][imp_ext_id] = imp_ext
    else:
        contents["extensions"][imp_ext_id] = imp_ext
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

    if impacted_entity_counts:
        empties_removed["impacted_entity_counts"] = impacted_entity_counts
    if impacted_refs:
        empties_removed["impacted_refs"] = impacted_refs
    if superseded_by_ref:
        empties_removed["superseded_by_ref"] = superseded_by_ref

    if "modified" in required and required["modified"] == "":
        # object needs to be created
        stix_obj = Impact(**empties_removed)

    else:
        # object needs to be updated, but we can't
        #  update properly yet, so recreate instead
        stix_obj = Impact(**empties_removed)

    stix_dict = json.loads(stix_obj.serialize())
    time_list = ["created", "modified", "end_time", "start_time"]
    for tim in time_list:
        if tim in stix_dict:
            temp_string = convert_dt(stix_dict[tim])
            stix_dict[tim] = temp_string

    if "extensions" in stix_dict:
        extensions = stix_dict["extensions"]
        if "monetary" in extensions:
            monetary = extensions["monetary"]
            if "conversion_time" in monetary:
                temp_string = convert_dt(monetary["conversion_time"])
                monetary["conversion_time"] = temp_string

    return stix_dict


def main(inputfile, outputfile):
    impacted_entity_counts = None
    impacted_refs = None
    superseded_by_ref = None
    if os.path.exists(inputfile):
        with open(inputfile, "r") as script_input:
            input = json.load(script_input)
    event_form = input["impact_form"]
    if "impacted_entity_counts" in input:
        impacted_entity_counts = input["impacted_entity_counts"]
    if "impacted_refs" in input:
        impacted_refs = input["impacted_refs"]
    if "superseded_by_ref" in input:
        superseded_by_ref = input["superseded_by_ref"]


    # setup logger for execution
    stix_dict = make_impact(event_form, impacted_entity_counts, impacted_refs, superseded_by_ref)
    results = {}
    results["impact"] = []
    results["impact"].append(stix_dict)
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

  main("./sequence_alert.json", "test_output.json")


################################################################################
## footer end                                                                 ##
################################################################################