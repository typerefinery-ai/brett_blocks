import sys
import os

# Change to Orchestration directory if not already there
script_dir = os.path.dirname(os.path.abspath(__file__))
if os.path.basename(script_dir) == 'Orchestration':
    os.chdir(script_dir)
else:
    os.chdir(os.path.join(script_dir, 'Orchestration'))

sys.path.append('../')

from stixorm.module.authorise import import_type_factory
from stixorm.module.definitions.stix21 import (
    Identity, EmailAddress, UserAccount, Relationship, Bundle, 
    Incident, Indicator, ObservedData, URL, File
)
from stixorm.module.typedb_lib.instructions import ResultStatus, Result
from stixorm.module.parsing import parse_objects

import_type = import_type_factory.get_all_imports()

import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

print("✅ STIX 2.1 libraries loaded")
print("✅ Incident objects loaded: Incident, Indicator, ObservedData, Sighting, Event")
print("✅ Act 1, Scene 1 complete")


cwd = os.getcwd()

print(f"✅ Working directory: {cwd}")
print("✅ Act 1, Scene 2 complete")

import json

# Incident management utilities
from Utilities.local_make_general import (
    invoke_create_incident_context, 
    invoke_save_incident_context_block,
    invoke_get_from_company_block,
    invoke_get_from_user_block,
    invoke_chain_sequence_block
)

# SDO creation utilities
from Utilities.local_make_sdo import (
    invoke_make_incident_block,
    invoke_make_indicator_block,
    invoke_make_observed_data_block,
    invoke_make_event_block,
    invoke_make_sequence_block,
    invoke_make_task_block
)

# SCO creation utilities
from Utilities.local_make_sco import (
    invoke_make_email_addr_block,
    invoke_make_url_block,
    invoke_make_e_msg_block
)

# SRO creation utilities
from Utilities.local_make_sro import invoke_sro_block, invoke_sighting_block

from Utilities.util import emulate_ports, unwind_ports, conv

# Paths
path_base = "../Block_Families/StixORM/"
results_base = "../Orchestration/Results/step3/context/"
context_base = "../Orchestration/generated/os-triage/context_mem/"

# Phishing scenario

sequence_name = "chain_test.json"

sequence_obj = {
            "type": "sequence",
            "spec_version": "2.1",
            "id": "sequence--9fdc38e0-9e57-4c0b-9650-18aeaff39bf8a",
            "created": "2025-11-21T06:32:08.411Z",
            "modified": "2025-11-21T06:32:08.411Z",
            "sequenced_object": "event--d38f9502-a2d2-4d46-bc29-d7d7bdf61f8a",
            "sequence_type": "event",
            "step_type": "single_step",
            "extensions": {
                "extension-definition--be0c7c79-1961-43db-afde-637066a87a64": {
                    "extension_type": "new-sdo"
                }
            }
        }

# save the sequence to a file
with open(results_base + sequence_name, 'w') as f:
    f.write(json.dumps(sequence_obj))

test_return = invoke_chain_sequence_block(results_base + sequence_name, results_base + "step3/chain_test_result.json")
print(f"Chain sequence block returned: {test_return}")
