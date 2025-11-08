#!/usr/bin/env python3
"""Deep dive into specific failure examples"""

import json
from pathlib import Path

# Load test results
with open('generated/test_results.json', 'r') as f:
    data = json.load(f)

failures = data['test_statistics']['detailed_failures']

# Get one example of each type
examples = {}
for f in failures:
    obj_type = f['type']
    if obj_type not in examples:
        examples[obj_type] = f

print("=" * 80)
print("DETAILED FAILURE EXAMPLES:")
print("=" * 80)

for obj_type, item in sorted(examples.items()):
    print(f"\n{'='*80}")
    print(f"{obj_type.upper()}: {item['summary']}")
    print(f"Original ID: {item['original_id']}")
    print(f"{'='*80}")
    
    if 'differences' in item:
        import pprint
        print("\nDifferences:")
        pprint.pprint(item['differences'], width=120, indent=2)
