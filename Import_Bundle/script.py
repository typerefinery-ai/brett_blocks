##############################################################################
# Title: Load Example Bundle Directory
# Author: OS-Threat
# Organisation Repo: https://github.com/typerefinery-ai/brett_blocks
# Contact Email: denis@cloudaccelerator.co
# Date: 07/08/2023
#
# Description: This script is designed to take in a Connection, and a Path string
#       that points to the sub-directory in the tests/data to read in, and then
#       load the bundle files in the directory (note files contain bundles not lists)
#
# This code is licensed under the terms of the BSD.
##############################################################################

from typedb.client import *
from stixorm.module.typedb import TypeDBSink
from stixorm.module.authorise import import_type_factory
from stixorm.module.typedb_lib.instructions import ResultStatus
import json
import requests
import copy
import os
import sys
import argparse
from loguru import logger as Logger

import_type = import_type_factory.get_all_imports()

def get_bundle(url):
    bundle = json.loads(requests.get(url, verify=False).text)
    return bundle

def main(dbhost, dbport, dbdatabase, dbquery, outputfile, logger: Logger):
    instance_connection = {
        "uri": dbhost,
        "port": dbport,
        "database": dbdatabase,
        "user": None,
        "password": None
    }
    # start the connection, reinitilise is true
    reinitilise = True
    typedb = TypeDBSink(connection=instance_connection,
                        clear=reinitilise,
                        import_type=import_type)
    # get the bundle to load
    bundle = get_bundle(dbquery)
    bundle_list = bundle["objects"]
    # add the list to TypeDB
    result = typedb.add(bundle_list)
    # export the result
    with open(outputfile, "w") as outfile:
        json.dump(result, outfile)


# if this file is run directly, then start here
if __name__ == '__main__':
    connection = {
        "uri": "localhost",
        "port": "1729",
        "database": "stix_test",
        "user": None,
        "password": None
    }
    url = "https://raw.githubusercontent.com/os-threat/Stix-ORM/main/test/data/threat_reports/poisonivy.json"
    main(connection["uri"], connection["port"], connection["database"], url, "output.json", Logger)
