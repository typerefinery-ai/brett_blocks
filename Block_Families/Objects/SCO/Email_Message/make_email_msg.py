
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
# Title: Make URL
# Author: OS-Threat
# Organisation Repo: https://github.com/typerefinery-ai/brett_blocks
# Contact Email: denis@cloudaccelerator.co
# Date: 07/08/2023
#
# Description: This script is designed to take in a Stix Object ID
#       and return a Stix object
#
# One Mandatory, One Optional Input:
# 1. URL_Form
# 2. hyperlink string
# One Output
# 1. URL SCO (Dict)
#
# This code is licensed under the terms of the BSD.
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


    stix_dict = EmailMessage(**empties_removed)

    return stix_dict.serialize()


def main(inputfile, outputfile):
    belongs_to = None
    if os.path.exists(inputfile):
        with open(inputfile, "r") as script_input:
            input = json.load(script_input)

    email_msg_form = input["email_msg_form"]
    if "from_ref" in input:
        from_ref = input["from_ref"]
    else:
        from_ref=None
    if "to_refs" in input:
        to_refs = input["to_refs"]
    else:
        to_refs=None
    if "cc_refs" in input:
        cc_refs = input["cc_refs"]
    else:
        cc_refs=None
    if "bcc_refs" in input:
        bcc_refs = input["bcc_refs"]
    else:
        bcc_refs=None

    # setup logger for execution
    stix_dict = make_email_msg(email_msg_form, from_ref, to_refs, cc_refs, bcc_refs)
    results = {}
    results["email-message"] = []
    results["email-message"].append(json.loads(stix_dict))
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