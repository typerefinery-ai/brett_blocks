"""
Test script to verify find_embedded_references function works correctly
with incident extension objects.
"""
import json
import sys
from pathlib import Path

# Add the parse module directory to path
parse_module_path = Path(__file__).parent / "Orchestration" / "generated" / "os-triage" / "common_files"
sys.path.insert(0, str(parse_module_path))

from parse import find_embedded_references

# Test incident object with extension containing multiple reference arrays
test_incident = {
	"type": "incident",
	"spec_version": "2.1",
	"id": "incident--e797e22f-89bd-4aa8-a541-621a2bcf14b6",
	"created": "2025-12-10T01:15:29.566Z",
	"modified": "2025-12-10T01:15:29.566Z",
	"name": "potential phishing",
	"extensions": {
		"extension-definition--ef765651-680c-498d-9894-99799f2fa126": {
			"extension_type": "property-extension",
			"investigation_status": "new",
			"incident_types": [
				"dissemination-phishing-emails"
			],
			"other_object_refs": [
				"email-addr--eb38d07e-6ba8-56c1-b107-d4db4aacf212",
				"email-addr--4722424c-7012-56b0-84d5-01d076fc547b",
				"user-account--597ad4d4-35ba-585d-8f6d-134a75032f9b",
				"identity--6beaedd7-7259-41ac-8937-0f57cd393a39",
				"identity--b18b013b-88a8-4c90-b48a-30953ecd78bd",
				"url--3279c7de-8f91-5c1a-99d9-d6546c6c41f7",
				"email-message--6090e3d4-1fa8-5b36-9d2d-4a66d824995d",
				"relationship--61ddd63c-0603-4a54-a77e-518d28813986",
				"observed-data--9e79a0e4-426f-4771-9880-e01edc02ed91",
				"indicator--51b7f178-7a2d-437f-86a2-d926a77da3a4",
				"sighting--862ae1df-9d24-4247-91e4-8923c8b61132",
				"identity--57268468-cd4a-480c-a884-dbeb14094e48",
				"identity--e4f222c1-6aaf-41f2-a854-b3ac35765cea",
				"identity--267ca3c7-6796-4e4f-a51f-7dfd3cc7e79b",
				"anecdote--e1298bc0-818e-5cdb-9154-eac37c8e260f",
				"observed-data--e97ab908-23fb-4aa1-854c-d8dc6a80014c",
				"sighting--5d6d51cb-1dfb-4f09-8266-38da69a561f5"
			],
			"event_refs": [
				"event--f8e9b853-143d-4b62-acd6-f0d9e6e20aa4"
			],
			"sequence_refs": [
				"sequence--9b3181c3-77b0-4ca8-9ced-07c4c3cb9787",
				"sequence--e1b8601d-9633-46e5-9643-d8a0d3a6a5dd",
				"sequence--061372cf-627c-42bd-980e-3f9811cfd2f9"
			],
			"task_refs": [
				"task--1a427cfe-d21c-4c86-a170-1270f443d1ef",
				"task--1fa2b059-4d89-46a4-933a-48c89b946bb6"
			],
			"impact_refs": [
				"impact--45c4a640-64dd-484c-bbb3-84612a0a5b78"
			],
			"sequence_start_refs": [
				"sequence--bd78a4d1-e7f4-48cc-835e-876e4677b7c0",
				"sequence--f5033b9d-6ce3-4fb1-b3ce-1fbbf52c1c4e"
			]
		}
	}
}

# Expected counts
expected_properties = {
    "other_object_refs": 17,
    "event_refs": 1,
    "sequence_refs": 3,
    "task_refs": 2,
    "impact_refs": 1,
    "sequence_start_refs": 2
}
expected_total = sum(expected_properties.values())  # 26 total

print("Testing find_embedded_references function...")
print("=" * 80)

# Call the function
try:
    result = find_embedded_references(test_incident)
    
    print(f"\nReturned type: {type(result)}")
    print(f"References dict: {result.references}")
    print(f"\nNumber of properties found: {len(result.references)}")
    
    # Count total references
    total_refs = sum(len(refs) for refs in result.references.values())
    print(f"Total STIX IDs found: {total_refs}")
    print(f"Expected total: {expected_total}")
    
    print("\nBreakdown by property:")
    for prop_name, expected_count in expected_properties.items():
        actual_count = len(result.references.get(prop_name, []))
        status = "✓" if actual_count == expected_count else "✗"
        print(f"  {status} {prop_name}: {actual_count}/{expected_count}")
        
        # Show the actual IDs if counts don't match
        if actual_count != expected_count:
            print(f"    Found: {result.references.get(prop_name, [])}")
    
    # Check for unexpected properties
    unexpected = set(result.references.keys()) - set(expected_properties.keys())
    if unexpected:
        print(f"\n⚠ Unexpected properties found: {unexpected}")
        for prop in unexpected:
            print(f"  {prop}: {result.references[prop]}")
    
    # Final verdict
    print("\n" + "=" * 80)
    if total_refs == expected_total and len(result.references) == len(expected_properties):
        print("✓ SUCCESS: Function correctly identified all embedded references!")
    else:
        print("✗ FAILURE: Function did not correctly identify all embedded references")
        print(f"  Found {total_refs}/{expected_total} total references")
        print(f"  Found {len(result.references)}/{len(expected_properties)} properties")
    
except Exception as e:
    print(f"\n✗ ERROR: Function raised an exception:")
    print(f"  {type(e).__name__}: {e}")
    import traceback
    traceback.print_exc()
