
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
# Title: Get Report
# Author: OS-Threat
# Organisation Repo: https://github.com/typerefinery-ai/brett_blocks
# Contact Email: denis@cloudaccelerator.co
# Date: 07/08/2023
#
# Description: This script is designed to take in a Connection, and a Report ID,
#       nd return a list of Stix objects containing the report and all dependencies
# One Input:
# 1. Stix_Object
# One Output
# 1. Stix_ID_List
#
# This code is licensed under the terms of the BSD.
##############################################################################


from stixorm.module.typedb import TypeDBSource
from stixorm.module.authorise import import_type_factory
from posixpath import basename
import json
import copy
import os
import sys
import argparse
import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

import_type = import_type_factory.get_all_imports()


def get_embedded_links(stix_object):
    stix_type = stix_object.get("type")
    stix_list = []
    if stix_type == "report":
        if stix_object.get("created_by_ref", False):
            stix_list.append(stix_object.get("created_by_ref", False))
        if stix_object.get("object_refs", False):
            report_list = stix_object.get("object_refs", False)
            stix_list = stix_list + report_list

        return stix_list


def main(inputfile, outputfile):
    if os.path.exists(inputfile):
        with open(inputfile, "r") as script_input:
            input = json.load(script_input)
    stix_dict = input["stix_object"]
    # setup logger for execution
    stix_list = get_embedded_links(stix_dict)
    result = {}
    result["stix_id_list"] = stix_list
    with open(outputfile, "w") as outfile:
        json.dump(result, outfile)



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