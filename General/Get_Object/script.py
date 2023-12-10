
################################################################################
## header start                                                               ##
################################################################################
# allow importing og service local packages
import os
import sys
import os.path

where_am_i = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.environ["APP_SERVICE_PACKAGES_PATH"])
sys.path.append(where_am_i)
# end of local package imports
################################################################################
## header end                                                                 ##
################################################################################


################################################################################
## body start                                                                 ##
################################################################################

##############################################################################
# Title: Get Object
# Author: OS-Threat
# Organisation Repo: https://github.com/typerefinery-ai/brett_blocks
# Contact Email: denis@cloudaccelerator.co
# Date: 07/08/2023
#
# Description: This script is designed to take in a Stix Object ID
#       and return a Stix object
#
# Two Inputs:
# 1. Connection
# 2. Stix_ID
# One Output
# 1. Stix_Object
#
# This code is licensed under the terms of the BSD.
##############################################################################

from stixorm.module.typedb import TypeDBSource
from stixorm.module.authorise import import_type_factory
from posixpath import basename
import json
import os

import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

import_type = import_type_factory.get_all_imports()


def get_object(stix_id, connection):
    object_type = stix_id.split('--')[0]

    typedb_source = TypeDBSource(connection, import_type)
    stix_dict = typedb_source.get(stix_id)
    print(f"type is -> {type(stix_dict)}")

    return stix_dict.serialize()


def main(inputfile, outputfile):
    if os.path.exists(inputfile):
        with open(inputfile, "r") as script_input:
            input = json.load(script_input)
    connection = input["connection"]
    stix_id = input["stix_id"]

    # setup logger for execution
    stix_dict = get_object(stix_id, connection)
    print(f"\n type of stix_dict is {type(stix_dict)}")
    print(stix_dict)
    results = {}
    results["stix_object"] = stix_dict
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