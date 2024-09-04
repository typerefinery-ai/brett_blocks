
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
# Title: Make Email Message
# Author: OS-Threat
# Organisation Repo: https://github.com/typerefinery-ai/brett_blocks
# Contact Email: brett@osthreat.com
# Date: 07/08/2023
#
# Description: This script is designed to take in a Stix Object ID
#       and return a Stix object
#
# One Mandatory, One Optional Input:
# 1. Email Message Form
# 2. from email ref{}
# 3. [to email refs]
# 3.[cc email refs]
# 4. [bcc email refs]
# One Output
# 1. Email Message SCO (Dict)
#
# This code is licensed under the terms of the Apache 2.
##############################################################################

from stixorm.module.definitions.stix21 import (
    ObservedData, IPv4Address, EmailAddress, DomainName, EmailMessage, URL, UserAccount, File,
    Identity, Incident, Note, Sighting, Indicator, Relationship, Location, Software, Process, Bundle,
    EmailMessage
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

import json
import os

import logging
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

def make_email_msg(email_msg_form, from_ref=None, to_refs=None, cc_refs=None, bcc_refs=None):
    # 1. Extract the components of the object
    required = email_msg_form["base_required"]
    optional = email_msg_form["base_optional"]
    main = email_msg_form["object"]
    extensions = email_msg_form["extensions"]
    sub = email_msg_form["sub"]
    contents = {}
    empties_removed = {}
    # 2. Setup Object Params first
    for k,v in main.items():
        contents[k] = v
    for k,v in optional.items():
        contents[k] = v
    for k,v in extensions.items():
        contents["extensions"] = {k, v}
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

    if from_ref:
        empties_removed["from_ref"] = from_ref["id"]

    if to_refs:
        tmp_list = []
        for ref in to_refs:
            tmp_list.append(ref["id"])
        empties_removed["to_refs"] = tmp_list
    if cc_refs:
        tmp_list = []
        for ref in cc_refs:
            tmp_list.append(ref["id"])
        empties_removed["cc_refs"] = tmp_list
    if bcc_refs:
        tmp_list = []
        for ref in bcc_refs:
            tmp_list.append(ref["id"])
        empties_removed["bcc_refs"] = tmp_list


    stix_obj = EmailMessage(**empties_removed)

    stix_dict = json.loads(stix_obj.serialize())
    time_list = ["date"]
    for tim in time_list:
        if tim in stix_dict:
            temp_string = convert_dt(stix_dict[tim])
            stix_dict[tim] = temp_string

    return stix_dict


def main(inputfile, outputfile):
    belongs_to = None
    if os.path.exists(inputfile):
        with open(inputfile, "r") as script_input:
            input_data = json.load(script_input)

    if "email_msg_form" in input_data:
        email_msg_form = input_data["email_msg_form"]
        if "from_ref" in input_data:
            from_ref = input_data["from_ref"]
        else:
            from_ref=None
        if "to_refs" in input_data:
            to_refs = input_data["to_refs"]
        else:
            to_refs=None
        if "cc_refs" in input_data:
            cc_refs = input_data["cc_refs"]
        else:
            cc_refs=None
        if "bcc_refs" in input_data:
            bcc_refs = input_data["bcc_refs"]
        else:
            bcc_refs=None
    elif "api" in input_data:
        api_input = input_data["api"]
        email_msg_form = api_input["email_msg_form"]
        if "from_ref" in api_input:
            from_ref = api_input["from_ref"]
        else:
            from_ref = None
        if "to_refs" in api_input:
            to_refs = api_input["to_refs"]
        else:
            to_refs = None
        if "cc_refs" in api_input:
            cc_refs = api_input["cc_refs"]
        else:
            cc_refs = None
        if "bcc_refs" in api_input:
            bcc_refs = api_input["bcc_refs"]
        else:
            bcc_refs = None

    # setup logger for execution
    stix_dict = make_email_msg(email_msg_form, from_ref, to_refs, cc_refs, bcc_refs)
    results = {}
    results["email-message"] = []
    results["email-message"].append(stix_dict)
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
  main(args.inputfile, args.outputfile)


################################################################################
## footer end                                                                 ##
################################################################################