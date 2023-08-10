
from typedb.client import *
from loguru import logger as Logger
from stixorm.module.typedb import TypeDBSink
from stixorm.module.authorise import import_type_factory
from stixorm.module.typedb_lib.instructions import ResultStatus
import json
import requests
import copy
import os
import sys
import argparse

import logging
logging.basicConfig(level=logging.DEBUG, format='[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s')
logger = logging.getLogger(__name__)
#logger.addHandler(logging.StreamHandler())

from Import_Bundle.script import main as import_bundle

import_type = import_type_factory.get_all_imports()

connection = {
    "uri": "localhost",
    "port": "1729",
    "database": "stix_test",
    "user": None,
    "password": None
}
report_url = "https://raw.githubusercontent.com/os-threat/Stix-ORM/main/test/data/threat_reports/poisonivy.json"

def try_import_bundle():
    import_bundle(connection["uri"], connection["port"], connection["database"], report_url, "output.json", logger)


# if this file is run directly, then start here
if __name__ == '__main__':
    try_import_bundle()