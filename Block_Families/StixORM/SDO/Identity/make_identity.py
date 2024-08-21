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
# Title: Make Identity
# Author: OS-Threat
# Organisation Repo: https://github.com/typerefinery-ai/brett_blocks
# Contact Email: denis@cloudaccelerator.co
# Date: 07/08/2023
#
# Description: This script is designed to take in a Stix Object ID
#       and return a Stix object
#
# One Mandatory, One Optional Input:
# 1. Identity_Form
# 2. User Account (optional)
# 3. Email Addr (optional
# One Output
# 1. Identity SDO Extension (Dict)
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
from posixpath import basename
import json
import os

import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

import_type = import_type_factory.get_all_imports()
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


def make_identity(identity_form, email_addr=None, user_account=None):
    print(f"Step 1 >>")
    # 1. Extract the components of the object
    required = identity_form["base_required"]
    optional = identity_form["base_optional"]
    main = identity_form["object"]
    extensions = identity_form["extensions"]
    sub = identity_form["sub"]
    contents = {}
    empties_removed = {}
    # 2. Setup Object Params first
    print(f"Step 2 >>")
    for k, v in main.items():
        contents[k] = v
    for k, v in optional.items():
        contents[k] = v
    for k,v in sub.items():
        if k == "contact_numbers":
            if "extension-definition--66e2492a-bbd3-4be6-88f5-cc91a017a498" in extensions:
                identity_contact = extensions["extension-definition--66e2492a-bbd3-4be6-88f5-cc91a017a498"]
                stix_list = []
                for val in v:
                    stix_list.append(ContactNumber(**val))
                identity_contact["contact_numbers"] = stix_list
        if k == "email_addresses":
            if "extension-definition--66e2492a-bbd3-4be6-88f5-cc91a017a498" in extensions:
                identity_contact = extensions["extension-definition--66e2492a-bbd3-4be6-88f5-cc91a017a498"]
                stix_list = []
                print(f"#>> v {v}")
                print(f"#>> email_addrs {email_addr}")
                for i, val in enumerate(v):
                    print(f"#>> v {v}")
                    if email_addr:
                        val["email_address_ref"] = email_addr["id"]
                    stix_list.append(EmailContact(**val))
                identity_contact["email_addresses"] = stix_list
        if k == "social_media_accounts":
            if "extension-definition--66e2492a-bbd3-4be6-88f5-cc91a017a498" in extensions:
                identity_contact = extensions["extension-definition--66e2492a-bbd3-4be6-88f5-cc91a017a498"]
                stix_list = []
                for i, val in enumerate(v):
                    if user_account:
                        val["user_account_ref"] = user_account["id"]
                    stix_list.append(SocialMediaContact(**val))
                identity_contact["social_media_accounts"] = stix_list

    if extensions != {}:
        if "extension-definition--66e2492a-bbd3-4be6-88f5-cc91a017a498" in extensions:
            identity_contact = extensions["extension-definition--66e2492a-bbd3-4be6-88f5-cc91a017a498"]
            identity_ext = IdentityContact(**identity_contact)
            contents["extensions"] = {"extension-definition--66e2492a-bbd3-4be6-88f5-cc91a017a498":identity_ext}

    for (k,v) in contents.items():
        if v == "":
            continue
        elif v == []:
            continue
        elif v == None:
            continue
        else:
            empties_removed[k] = v

    if "modified" in required and required["modified"] == "":
        # object needs to be created
        stix_obj = Identity(**empties_removed)

    else:
        # object needs to be updated, but we can't
        #  update properly yet, so recreate instead
        stix_obj = Identity(**empties_removed)

    stix_dict = json.loads(stix_obj.serialize())
    print(f"Step 3 >>")
    time_list = ["created", "modified"]
    for tim in time_list:
        if tim in stix_dict:
            temp_string = convert_dt(stix_dict[tim])
            stix_dict[tim] = temp_string

    return stix_dict


def main(inputfile, outputfile):
    email_addr = None
    user_account = None
    if os.path.exists(inputfile):
        with open(inputfile, "r") as script_input:
            input = json.load(script_input)
    identity_form = input["identity_form"]
    if "email-addr" in input:
        email_addr = input["email-addr"]
    if "user-account" in input:
        user_account = input["user-account"]

    print(f"type identity->{type(identity_form)}, type email->{type(email_addr)}, type user acct->{type(user_account)}")
    # setup logger for execution
    stix_dict = make_identity(identity_form, email_addr, user_account)
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