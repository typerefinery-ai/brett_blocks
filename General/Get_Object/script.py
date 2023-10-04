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

from typedb.client import *
from loguru import logger as Logger
from stixorm.module.typedb import TypeDBSource
from stixorm.module.authorise import import_type_factory
from posixpath import basename
import json

import logging
logging.basicConfig(level=logging.DEBUG, format='[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s')
logger = logging.getLogger(__name__)

import_type = import_type_factory.get_all_imports()

connection = {
    "uri": "localhost",
    "port": "1729",
    "database": "stix_test",
    "user": None,
    "password": None
}
report_id = "report--f2b63e80-b523-4747-a069-35c002c690db"
input = {
    "connection": connection,
    "stix_id": report_id
}

def get_object(stix_id, connection):
    object_type = stix_id.split('--')[0]

    typedb_source = TypeDBSource(connection, import_type)
    stix_dict = typedb_source.get(stix_id)
    print(f"type is -> {type(stix_dict)}")

    return stix_dict.serialize()


def main(input, outputfile, logger: Logger):
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


# if this file is run directly, then start here
if __name__ == '__main__':
    main(input, "output2.json", logger)
