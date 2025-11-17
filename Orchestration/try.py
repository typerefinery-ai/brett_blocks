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
results_base = "../Orchestration/Results/"
context_base = "../Orchestration/generated/os-triage/context_mem/"

# Phishing scenario
phishing_scenario = {
    "incident_name": "Phishing Email Investigation",
    "attacker_email": "attacker@evil.com",
    "target_email": "ceo@victim-company.com",
    "malicious_url": "https://evil.com/phish",
    "subject": "Urgent: Verify your account"
}

print("✅ Incident utilities loaded")
print(f"✅ Phishing scenario configured:")
print(f"   - Attacker: {phishing_scenario['attacker_email']}")
print(f"   - Target: {phishing_scenario['target_email']}")
print(f"   - Malicious URL: {phishing_scenario['malicious_url']}")
print("✅ Act 1 complete - Ready to create incident!")


# Initialize object reference lists for incident
sequence_start_refs = []
sequence_refs = []
task_refs = []
event_refs = []
impact_refs = []
other_object_refs = []

# Create incident object
incident_obj = invoke_make_incident_block(
    "SDO/Incident/phishing_incident.json",
    "step1/phishing_incident",
    sequence_start_refs,
    sequence_refs,
    task_refs,
    event_refs,
    impact_refs,
    other_object_refs
)

# Create incident context directory
incident_obj_path = results_base + "step1/phishing_incident"
incident_context_path = results_base + "step1/incident_context.json"
result = invoke_create_incident_context(incident_obj_path, incident_context_path)

print(f"✅ Incident created: {incident_obj['type']} - {incident_obj['id'][:40]}...")
print(f"✅ Incident context: /incident--{incident_obj['id'][10:46]}/")
print(f"✅ Result: {result}")
print("")
print("� Incident container ready - now let's add evidence!")
print("✅ Act 1 complete - Moving to Act 2")