##############################################################################
# Title: Get Report
# Author: OS-Threat
# Organisation Repo: https://github.com/typerefinery-ai/brett_blocks
# Contact Email: denis@cloudaccelerator.co
# Date: 07/08/2023
#
# Description: This script is designed to take in a Connection, and a Report ID,
#       nd return a list of Stix objects containing the report and all dependencies
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
report_url = "https://raw.githubusercontent.com/os-threat/Stix-ORM/main/test/data/threat_reports/poisonivy.json"

report_id = "report--f2b63e80-b523-4747-a069-35c002c690db"

def get_object_cluster(cluster_head_id, connection):
    cluster_type = cluster_head_id.split('--')[0]
    stix_list = []
    if cluster_type == "report":
        typedb_source = TypeDBSource(connection, import_type)
        report_obj = typedb_source.get(cluster_head_id)
        if report_obj.type == cluster_type:
            stix_list.append(report_obj)
            if hasattr(report_obj, "created_by_ref"):
                identity = typedb_source.get(report_obj.created_by_ref)
                stix_list.append(identity)
            if hasattr(report_obj, "object_refs"):
                report_list = report_obj.object_refs
                for report_component_id in report_list:
                    print(f"find obj {report_component_id}")
                    tmp_obj = typedb_source.get(report_component_id)
                    stix_list.append(tmp_obj)
                    print("found and added")

            for stix_obj in stix_list:
                print("\n+++++++++++++++++++++++++++++++++++++++++++++++++++++++")
                print(f"stix -> {stix_obj}")
                print("----------------------------------------------------------\n")
            return stix_list


def main(dbhost, dbport, dbdatabase, dbquery, outputfile, logger: Logger):
    instance_connection = {
        "uri": dbhost,
        "port": dbport,
        "database": dbdatabase,
        "user": None,
        "password": None
    }
    # setup logger for execution
    report_id = dbquery
    stix_list = get_object_cluster(report_id, instance_connection)
    with open(outputfile, "w") as outfile:
        json.dumps(stix_list, outfile)


# if this file is run directly, then start here
if __name__ == '__main__':
    main(connection["uri"], connection["port"], connection["database"], report_id, "output2.json", logger)
