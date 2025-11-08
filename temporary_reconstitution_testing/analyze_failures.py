#!/usr/bin/env python3
"""Analyze the 18 remaining failures from the test results"""

import json
from pathlib import Path
from collections import defaultdict

# Load test results
with open('generated/test_results.json', 'r') as f:
    data = json.load(f)

failures = data['test_statistics']['detailed_failures']

print(f"Total failures: {len(failures)}\n")
print("=" * 80)
print("FAILURE SUMMARY:")
print("=" * 80)

# Group by type
by_type = defaultdict(list)
for f in failures:
    by_type[f['type']].append(f)

for obj_type, items in sorted(by_type.items()):
    print(f"\n{obj_type} ({len(items)} failures):")
    for item in items:
        print(f"  - {item['summary']}")
        # Show first diff detail
        if 'differences' in item and item['differences']:
            diff_keys = list(item['differences'].keys())
            print(f"    Diff types: {', '.join(diff_keys)}")
