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
from stixorm.module.orm.export_object import convert_ans_to_stix
from stixorm.module.typedb import get_embedded_match
from stixorm.module.typedb_lib.queries import delete_database, match_query

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


def __retrieve_stix_dict(stix_id: str):
    logger.debug(f'__retrieve_stix_object: {stix_id}')
    obj_var, type_ql = get_embedded_match(stix_id, import_type)
    query = 'match ' + type_ql
    logger.debug(f'query is {query}')

    stix_dict = match_query(uri=connection["uri"],
                       port=connection["port"],
                       database=connection["database"],
                       query=query,
                       data_query=convert_ans_to_stix,
                       import_type=import_type)

    logger.debug(f'stix_dict is -> {stix_dict}')

    # result = write_to_file("stixorm/module/orm/export_final.json", stix_obj)
    # if not is_successful(result):
    #     logging.exception("\n".join(traceback.format_exception(result.failure())))
    #     logger.error(str(result.failure()))

    return stix_dict


def get_object(object_id, connection):
    object_type = object_id.split('--')[0]

    typedb_source = TypeDBSource(connection, import_type)
    stix_dict = __retrieve_stix_dict(object_id)

    return stix_dict


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
    stix_dict = get_object(report_id, instance_connection)
    print(f"\n type of stix_dict is {type(stix_dict)}")
    print(stix_dict)
    with open(outputfile, "w") as outfile:
        json.dump(stix_dict, outfile)


# if this file is run directly, then start here
if __name__ == '__main__':
    main(connection["uri"], connection["port"], connection["database"], report_id, "output2.json", logger)
