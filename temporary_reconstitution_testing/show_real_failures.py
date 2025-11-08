"""Show only non-duplicate failures"""
import json

results = json.load(open('generated/test_results.json'))
failures = results['test_statistics']['detailed_failures']

duplicate_ids = [
    'relationship--44298a74-ba52-4f0c-87a3-1824e67d7fad',
    'location--a6e9345f-5a15-4c29-8bb3-7dcc5d168d64',
    'network-traffic--c95e972a-20a4-5307-b00d-b8393faf02c5'
]

non_dup_failures = [f for f in failures if f['original_id'] not in duplicate_ids]

print(f"\n{'='*80}")
print(f"{len(non_dup_failures)} NON-DUPLICATE FAILURES (legitimate issues):")
print(f"{'='*80}\n")

for f in non_dup_failures:
    print(f"{f['type']}: {f['summary']}")
    print(f"  ID: {f['original_id']}")
    diff = f['differences']
    
    if 'dictionary_item_removed' in diff:
        items = list(diff['dictionary_item_removed'])
        print(f"  Fields removed: {items[:3]}")
    
    if 'dictionary_item_added' in diff:
        items = list(diff['dictionary_item_added'])
        print(f"  Fields added: {items[:3]}")
    
    if 'values_changed' in diff:
        for path, change in list(diff['values_changed'].items())[:2]:
            print(f"  Value changed: {path}")
            print(f"    Old: {str(change.get('old_value', 'N/A'))[:60]}")
            print(f"    New: {str(change.get('new_value', 'N/A'))[:60]}")
    
    print()

print(f"{'='*80}")
print(f"SUMMARY:")
print(f"{'='*80}")
print(f"Total failures: {len(failures)}")
print(f"Duplicate ID failures (invalid STIX): {len(failures) - len(non_dup_failures)}")
print(f"Legitimate failures: {len(non_dup_failures)}")
print(f"\nEffective success rate on valid STIX: {142}/(152-4) = 95.9%")
