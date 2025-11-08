"""
Analyze the differences in the test results to identify patterns.
"""
import json
from collections import defaultdict, Counter

def load_test_results():
    with open('generated/test_results.json', 'r') as f:
        return json.load(f)

def analyze_differences(results):
    """Extract and categorize all differences."""
    
    patterns = {
        'values_changed': defaultdict(list),
        'dictionary_item_added': defaultdict(list),
        'dictionary_item_removed': defaultdict(list),
        'iterable_item_added': defaultdict(list),
        'iterable_item_removed': defaultdict(list),
        'type_changes': defaultdict(list)
    }
    
    objects_by_type = defaultdict(lambda: {'identical': 0, 'different': 0})
    
    for comparison in results['comparison_report']['comparison_details']:
        obj_type = comparison['original_type']
        
        if comparison['is_identical']:
            objects_by_type[obj_type]['identical'] += 1
            continue
        
        objects_by_type[obj_type]['different'] += 1
        differences = comparison['differences']
        
        # Categorize each type of difference
        for diff_type, diff_data in differences.items():
            if diff_type == 'values_changed':
                for path, change in diff_data.items():
                    patterns['values_changed'][obj_type].append({
                        'path': path,
                        'old': change['old_value'],
                        'new': change['new_value'],
                        'id': comparison['original_id']
                    })
            elif diff_type == 'dictionary_item_added':
                # Parse the SetOrdered string representation
                import re
                matches = re.findall(r"'([^']+)'", diff_data)
                for item in matches:
                    patterns['dictionary_item_added'][obj_type].append({
                        'field': item,
                        'id': comparison['original_id']
                    })
            elif diff_type == 'dictionary_item_removed':
                # Parse the SetOrdered string representation
                import re
                matches = re.findall(r"'([^']+)'", diff_data)
                for item in matches:
                    patterns['dictionary_item_removed'][obj_type].append({
                        'field': item,
                        'id': comparison['original_id']
                    })
            elif diff_type == 'iterable_item_added':
                patterns['iterable_item_added'][obj_type].append({
                    'changes': diff_data,
                    'id': comparison['original_id']
                })
            elif diff_type == 'iterable_item_removed':
                patterns['iterable_item_removed'][obj_type].append({
                    'changes': diff_data,
                    'id': comparison['original_id']
                })
            elif diff_type == 'type_changes':
                patterns['type_changes'][obj_type].append({
                    'changes': diff_data,
                    'id': comparison['original_id']
                })
    
    return patterns, objects_by_type

def print_analysis(patterns, objects_by_type):
    """Print organized analysis of differences."""
    
    print("=" * 80)
    print("DIFFERENCE ANALYSIS")
    print("=" * 80)
    
    # Summary by object type
    print("\n1. OBJECT TYPE SUMMARY")
    print("-" * 80)
    for obj_type, counts in sorted(objects_by_type.items()):
        total = counts['identical'] + counts['different']
        pct = (counts['identical'] / total * 100) if total > 0 else 0
        print(f"{obj_type:30s} | Identical: {counts['identical']:3d} | Different: {counts['different']:3d} | Success: {pct:5.1f}%")
    
    # Fields Added
    print("\n2. FIELDS ADDED (dictionary_item_added)")
    print("-" * 80)
    field_added_counter = Counter()
    for obj_type, items in patterns['dictionary_item_added'].items():
        for item in items:
            field_added_counter[f"{obj_type}: {item['field']}"] += 1
    
    for field_path, count in field_added_counter.most_common(20):
        print(f"{count:3d}x | {field_path}")
    
    # Fields Removed
    print("\n3. FIELDS REMOVED (dictionary_item_removed)")
    print("-" * 80)
    field_removed_counter = Counter()
    for obj_type, items in patterns['dictionary_item_removed'].items():
        for item in items:
            field_removed_counter[f"{obj_type}: {item['field']}"] += 1
    
    for field_path, count in field_removed_counter.most_common(20):
        print(f"{count:3d}x | {field_path}")
    
    # Values Changed
    print("\n4. VALUES CHANGED (values_changed)")
    print("-" * 80)
    value_changed_counter = Counter()
    for obj_type, items in patterns['values_changed'].items():
        for item in items:
            value_changed_counter[f"{obj_type}: {item['path']}"] += 1
    
    for field_path, count in value_changed_counter.most_common(20):
        print(f"{count:3d}x | {field_path}")
    
    # Show specific examples for top issues
    print("\n5. DETAILED EXAMPLES")
    print("-" * 80)
    
    # Example: Fields added
    if patterns['dictionary_item_added']:
        print("\nExample: Field Added")
        obj_type = list(patterns['dictionary_item_added'].keys())[0]
        example = patterns['dictionary_item_added'][obj_type][0]
        print(f"  Type: {obj_type}")
        print(f"  Field: {example['field']}")
        print(f"  Object ID: {example['id']}")
    
    # Example: Values changed
    if patterns['values_changed']:
        print("\nExample: Value Changed")
        obj_type = list(patterns['values_changed'].keys())[0]
        example = patterns['values_changed'][obj_type][0]
        print(f"  Type: {obj_type}")
        print(f"  Path: {example['path']}")
        print(f"  Old: {example['old']}")
        print(f"  New: {example['new']}")
        print(f"  Object ID: {example['id']}")
    
    # Iterable changes
    if patterns['iterable_item_added'] or patterns['iterable_item_removed']:
        print("\n6. ITERABLE CHANGES (Lists/Arrays)")
        print("-" * 80)
        
        if patterns['iterable_item_added']:
            print(f"Items added to lists: {sum(len(v) for v in patterns['iterable_item_added'].values())} objects affected")
            for obj_type, items in list(patterns['iterable_item_added'].items())[:3]:
                print(f"\n  {obj_type}:")
                for item in items[:2]:
                    print(f"    ID: {item['id']}")
                    print(f"    Changes: {json.dumps(item['changes'], indent=6)[:200]}...")
        
        if patterns['iterable_item_removed']:
            print(f"\nItems removed from lists: {sum(len(v) for v in patterns['iterable_item_removed'].values())} objects affected")

def main():
    results = load_test_results()
    patterns, objects_by_type = analyze_differences(results)
    print_analysis(patterns, objects_by_type)
    
    # Save detailed analysis
    with open('generated/difference_analysis.json', 'w') as f:
        json.dump({
            'patterns': patterns,
            'objects_by_type': objects_by_type
        }, f, indent=2, default=str)
    
    print("\n" + "=" * 80)
    print("Detailed analysis saved to: generated/difference_analysis.json")
    print("=" * 80)

if __name__ == '__main__':
    main()
