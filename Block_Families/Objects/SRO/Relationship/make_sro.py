
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
# Title: Make SRO
# Author: OS-Threat
# Organisation Repo: https://github.com/typerefinery-ai/brett_blocks
# Contact Email: denis@cloudaccelerator.co
# Date: 07/08/2023
#
# Description: This script is designed to take in form, 2 Stix Objects
#       and a relationship type
#
# One Mandatory, 3 Optional Input Ports:
# 1. SRO Form
# 2. Source Stix Object
# 3. Target Stix Object
# 4. Relationship_Type
# One Output
# 1. Valid SRO (Dict)
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
    dt = datetime.strptime(dt_stamp_string, "%Y-%m-%dT%H:%M:%S.%fZ")
    microsecs = dt.microsecond
    milisecs = (round(microsecs / 1000))
    dt_list = dt_stamp_string.split('.')
    actual = dt_list[0] + "." + str(milisecs) + "Z"
    return actual



def make_sro(sro_form, source, target, relationship_type):
    # 1. Extract the components of the object
    required = sro_form["base_required"]
    optional = sro_form["base_optional"]
    main = sro_form["object"]
    extensions = sro_form["extensions"]
    sub = sro_form["sub"]
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

    if source:
        contents["source_ref"] = source["id"]
    if target:
        contents["target_ref"] = target["id"]
    if relationship_type:
        contents["relationship_type"] = relationship_type

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
        stix_obj = Relationship(**empties_removed)

    else:
        # object needs to be updated, but we can't
        #  update properly yet, so recreate instead
        stix_obj = Relationship(**empties_removed)

    stix_dict = json.loads(stix_obj.serialize())
    time_list = ["created", "modified", "start_time", "stop_time"]
    for tim in time_list:
        if tim in stix_dict:
            temp_string = convert_dt(stix_dict[tim])
            stix_dict[tim] = temp_string

    return stix_dict


def main(inputfile, outputfile):
    if os.path.exists(inputfile):
        with open(inputfile, "r") as script_input:
            input_data = json.load(script_input)

    sro_form = input_data["relationship_form"]
    source = None
    target = None
    relationship_type = None
    if "source" in input_data:
        source = input_data["source"]
    if "target" in input_data:
        target = input_data["target"]
    if "relationship_type" in input_data:
        relationship_type = input_data["relationship_type"]

    # setup logger for execution
    stix_dict = make_sro(sro_form, source, target, relationship_type)
    results = {}
    results["relationship"] = []
    results["relationship"].append(stix_dict)
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