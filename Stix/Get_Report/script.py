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
from posixpath import basename
import json
import copy
import os
import sys
import argparse


def main(dbhost, dbport, dbdatabase, dbquery, outputfile, logger: Logger):
    # setup logger for execution
    colaGraph = ""
    with open(outputfile, "w") as outfile:
        json.dump(colaGraph, outfile)


# if this file is run directly, then start here
if __name__ == '__main__':
    pass
