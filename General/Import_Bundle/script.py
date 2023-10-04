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

from typedb.client import *
from stixorm.module.typedb import TypeDBSink
from stixorm.module.authorise import import_type_factory
from stixorm.module.typedb_lib.instructions import ResultStatus, Result
import json
import requests
import copy
import os
import sys
import argparse
from loguru import logger as Logger

import_type = import_type_factory.get_all_imports()

connection = {
    "uri": "localhost",
    "port": "1729",
    "database": "stix_test",
    "user": None,
    "password": None
}
url = "https://raw.githubusercontent.com/os-threat/Stix-ORM/main/test/data/threat_reports/poisonivy.json"
input = {
    "connection": connection,
    "url": url
}

def get_bundle(url):
    bundle = json.loads(requests.get(url, verify=True).text)
    print(f"\n bundle is {bundle}")
    return bundle

def main(input, outputfile, logger: Logger):
    connection = input["connection"]
    url = input["url"]
    # start the connection, reinitilise is true
    reinitilise = True
    typedb = TypeDBSink(connection=connection,
                        clear=reinitilise,
                        import_type=import_type)
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


# if this file is run directly, then start here
if __name__ == '__main__':

    main(input, "output.json", Logger)
