import sys
import os

# Add parent directory to path
sys.path.append('../')

# Import the functions from correct modules
from Utilities.local_make_sdo import invoke_make_incident_block
from Utilities.local_make_general import invoke_create_incident_context

# Set up paths
results_base = "./Results/"

# Initialize object reference lists for incident
sequence_start_refs = []
sequence_refs = []
task_refs = []
event_refs = []
impact_refs = []
other_object_refs = []

print("Creating incident object...")
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

print(f"✅ Incident created: {incident_obj['type']} - {incident_obj['id'][:40]}...")

# Create incident context directory
incident_obj_path = results_base + "step1/phishing_incident"
incident_context_path = results_base + "step1/incident_context.json"

print(f"Calling invoke_create_incident_context with:")
print(f"  incident_obj_path: {incident_obj_path}")
print(f"  incident_context_path: {incident_context_path}")
print("This is where it should show debug output from create_incident_context.py...")

result = invoke_create_incident_context(incident_obj_path, incident_context_path)

print(f"✅ Result: {result}")
