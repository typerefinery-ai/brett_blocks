
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

def make_sighting(sighting_form, observed_data_refs, where_sighted_refs, sighting_of_ref):
    # 1. Extract the components of the object
    required = sighting_form["base_required"]
    optional = sighting_form["base_optional"]
    main = sighting_form["object"]
    extensions = sighting_form["extensions"]
    sub = sighting_form["sub"]
    contents = {}
    empties_removed = {}
    # 2. Setup Object Params first
    for k,v in main.items():
        contents[k] = v
    for k,v in optional.items():
        contents[k] = v
    for k,v in extensions.items():
        if k == sight_ext_id:
            contents["extensions"] = {sight_ext_id: sight_ext}
        elif k == "sighting-alert":
            contents["extensions"] = {"sighting-alert": SightingAlert(**v)}
        elif k == "sighting-anecdote":
            contents["extensions"] = {"sighting-anecdote": SightingAnecdote(**v)}
        elif k == "sighting-context":
            contents["extensions"] = {"sighting-context": SightingContext(**v)}
        elif k == "sighting-enrichment":
            contents["extensions"] = {"sighting-enrichment": SightingEnrichment(**v)}
        elif k == "sighting-exclusion":
            contents["extensions"] = {"sighting-exclusion": SightingExclusion(**v)}
        elif k == "sighting-external":
            contents["extensions"] = {"sighting-external": SightingExternal(**v)}
        elif k == "sighting-framework":
            contents["extensions"] = {"sighting-framework": SightingFramework(**v)}
        elif k == "sighting-hunt":
            contents["extensions"] = {"sighting-hunt": SightingHunt(**v)}

    for k,v in sub.items():
        pass

    if where_sighted_refs:
        wherelist = []
        for where in where_sighted_refs:
            wherelist.append(where)
        contents["where_sighted_refs"] = wherelist
    if observed_data_refs:
        obs_list = []
        for where in observed_data_refs:
            obs_list.append(where)
        contents["observed_data_refs"] = obs_list
    if sighting_of_ref:
        contents["sighting_of_ref"] = sighting_of_ref

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
        stix_dict = Sighting(**empties_removed)

    else:
        # object needs to be updated, but we can't
        #  update properly yet, so recreate instead
        stix_dict = Sighting(**empties_removed)

    return stix_dict.serialize()


def main(inputfile, outputfile):
    if os.path.exists(inputfile):
        with open(inputfile, "r") as script_input:
            input_data = json.load(script_input)

    sro_form = input_data["sighting_form"]
    observed_data_refs = None
    where_sighted_refs = None
    sighting_of_ref = None
    if "observed_data_refs" in input_data:
        observed_data_refs = input_data["observed_data_refs"]
    if "where_sighted_refs" in input_data:
        where_sighted_refs = input_data["where_sighted_refs"]
    if "sighting_of_ref" in input_data:
        sighting_of_ref = input_data["sighting_of_ref"]

    # setup logger for execution
    stix_dict = make_sighting(sro_form, observed_data_refs, where_sighted_refs, sighting_of_ref)
    results = {}
    results["sighting"] = []
    results["sighting"].append(json.loads(stix_dict))
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