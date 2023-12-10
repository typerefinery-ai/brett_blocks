
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
# Title: Load Example Bundle Directory
# Author: OS-Threat
# Organisation Repo: https://github.com/typerefinery-ai/brett_blocks
# Contact Email: denis@cloudaccelerator.co
# Date: 07/08/2023
#
# Description: This script is designed to take in a Connection, and a Path string
#       that points to the subdirectory in the tests/data to read in, and then
#       load the bundle files in the directory (note files contain bundles not lists)
#
# Two Inputs:
# 1. Connection
# 2. URL
# One Output
# 1. Stix_Object
#
# This code is licensed under the terms of the BSD.
##############################################################################

from stixorm.module.typedb import TypeDBSink
from stixorm.module.authorise import import_type_factory
from stixorm.module.typedb_lib.instructions import ResultStatus, Result
import json
import requests
import copy
import os
import sys
import argparse
import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

import_type = import_type_factory.get_all_imports()



def get_bundle(url):
    bundle = json.loads(requests.get(url, verify=True).text)
    print(f"\n bundle is {bundle}")
    return bundle


def main(inputfile, outputfile):
    if os.path.exists(inputfile):
        with open(inputfile, "r") as script_input:
            input = json.load(script_input)

    connection = input["connection"]
    url = input["url"]
    # start the connection, reinitilise is true
    print("===========================================")
    print(f"{input}")
    print("===========================================")
    reinitilise = True
    typedb = TypeDBSink(connection=connection, clear=reinitilise, import_type=import_type)
    # get the bundle to load
    bundle = get_bundle(url)
    bundle_list = bundle["objects"]
    # add the list to TypeDB
    results_raw = typedb.add(bundle_list)
    result_list = [res.model_dump_json() for res in results_raw]
    print(f"\n result type is {type(result_list)} \n result is -> {result_list}")
    # export the result
    with open(outputfile, "w") as outfile:
        json.dump(result_list, outfile)


################################################################################
## body end                                                                   ##
################################################################################


################################################################################
## footer start                                                               ##
################################################################################
import argparse
import os

@Logger.catch
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