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
# This code is licensed under the terms of the BSD.
##############################################################################

from typedb.client import *
from loguru import logger as Logger
from stixorm.module.typedb import TypeDBSource
from stixorm.module.authorise import import_type_factory
from posixpath import basename
import json
import copy
import os
import sys
import argparse

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

def get_object(object_id, connection):
    object_type = object_id.split('--')[0]

    typedb_source = TypeDBSource(connection, import_type)
    stix_object = typedb_source.get(object_id)

    return stix_object


def main(dbhost, dbport, dbdatabase, dbquery, outputfile, logger: Logger):
    instance_connection = {
        "uri": dbhost,
        "port": "1729",
        "database": dbdatabase,
        "user": None,
        "password": None
    }
    # setup logger for execution
    report_id = dbquery
    stix_object = get_object(report_id, instance_connection)
    stix_dict = stix_object.serialize,
    print(f"\n type of stix_dict is {type(stix_dict)}")
    print(stix_object.serialize(pretty=True))
    with open(outputfile, "w") as outfile:
        json.dump(stix_dict, outfile)


# if this file is run directly, then start here
if __name__ == '__main__':
    main(connection["uri"], connection["port"], connection["database"], report_id, "output2.json", logger)
