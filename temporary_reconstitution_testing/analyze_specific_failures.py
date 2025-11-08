#!/usr/bin/env python3
"""Detailed analysis of specific failures to understand root causes"""

import json
from pathlib import Path

# Load test results
with open('generated/test_results.json', 'r') as f:
    data = json.load(f)

failures = data['test_statistics']['detailed_failures']

# Focus on specific failure types
print("=" * 80)
print("SEQUENCE FAILURES (on_completion reference):")
print("=" * 80)

sequence_failures = [f for f in failures if f['type'] == 'sequence']
for fail in sequence_failures[:2]:  # Show first 2
    print(f"\nObject ID: {fail['original_id']}")
    if 'differences' in fail and 'values_changed' in fail['differences']:
        for path, change in fail['differences']['values_changed'].items():
            print(f"  Path: {path}")
            print(f"  Old: {change['old_value']}")
            print(f"  New: {change['new_value']}")

print("\n" + "=" * 80)
print("IDENTITY FAILURES (extension embedded refs):")
print("=" * 80)

identity_failures = [f for f in failures if f['type'] == 'identity']
for fail in identity_failures[:1]:  # Show first 1
    print(f"\nObject ID: {fail['original_id']}")
    if 'differences' in fail and 'values_changed' in fail['differences']:
        for path, change in fail['differences']['values_changed'].items():
            print(f"  Path: {path}")
            print(f"  Old: {change['old_value']}")
            print(f"  New: {change['new_value']}")

# Now let's look at the actual original objects
print("\n" + "=" * 80)
print("EXAMINING ORIGINAL SEQUENCE OBJECT:")
print("=" * 80)

# Find the sequence object file
seq_id = "sequence--5ced78bf-aab8-4650-9c9e-a6914d68b46e"
input_dir = Path('generated/input_objects')
for f in input_dir.glob('sequence*.json'):
    with open(f, 'r') as file:
        obj = json.load(file)
        if obj.get('id') == seq_id:
            print(f"\nFound in: {f.name}")
            print(f"on_completion field: {obj.get('on_completion', 'NOT FOUND')}")
            if 'on_completion' in obj:
                print(f"  Type: {type(obj['on_completion'])}")
            break

print("\n" + "=" * 80)
print("EXAMINING ORIGINAL IDENTITY OBJECT WITH EXTENSIONS:")
print("=" * 80)

ident_id = "identity--ce31dd38-f69b-45ba-9bcd-2a208bbf8017"
for f in input_dir.glob('identity*.json'):
    with open(f, 'r') as file:
        obj = json.load(file)
        if obj.get('id') == ident_id:
            print(f"\nFound in: {f.name}")
            if 'extensions' in obj:
                print("Extensions found:")
                for ext_id, ext_data in obj['extensions'].items():
                    print(f"  Extension: {ext_id}")
                    if isinstance(ext_data, dict):
                        for key, value in ext_data.items():
                            if '_ref' in key or isinstance(value, list):
                                print(f"    {key}: {value}")
            break
