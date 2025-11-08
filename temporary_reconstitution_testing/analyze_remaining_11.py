"""
Detailed analysis of the remaining 11 failures
"""
import json
from pathlib import Path
from deepdiff import DeepDiff

def analyze_failures():
    """Analyze each of the 11 remaining failures in detail"""
    
    # Load test results
    results_file = Path("generated/test_results.json")
    with open(results_file) as f:
        results = json.load(f)
    
    failures = results['test_statistics']['detailed_failures']
    
    print("=" * 80)
    print(f"ANALYZING {len(failures)} REMAINING FAILURES")
    print("=" * 80)
    
    # Group failures by type
    by_type = {}
    for failure in failures:
        obj_type = failure['type']
        if obj_type not in by_type:
            by_type[obj_type] = []
        by_type[obj_type].append(failure)
    
    for obj_type, type_failures in sorted(by_type.items()):
        print(f"\n{'=' * 80}")
        print(f"{obj_type.upper()} FAILURES: {len(type_failures)} instance(s)")
        print("=" * 80)
        
        for idx, failure in enumerate(type_failures, 1):
            print(f"\n--- Instance {idx} ---")
            print(f"Object ID: {failure['original_id']}")
            print(f"Summary: {failure['summary']}")
            
            diff = failure['differences']
            
            # Show values changed
            if 'values_changed' in diff:
                print(f"\n  VALUES CHANGED ({len(diff['values_changed'])}):")
                for path, change in list(diff['values_changed'].items())[:5]:
                    old = str(change.get('old_value', 'N/A'))[:80]
                    new = str(change.get('new_value', 'N/A'))[:80]
                    print(f"    {path}")
                    print(f"      Old: {old}")
                    print(f"      New: {new}")
            
            # Show fields added
            if 'dictionary_item_added' in diff:
                print(f"\n  FIELDS ADDED ({len(diff['dictionary_item_added'])}):")
                for path in list(diff['dictionary_item_added'])[:5]:
                    print(f"    {path}")
            
            # Show fields removed
            if 'dictionary_item_removed' in diff:
                print(f"\n  FIELDS REMOVED ({len(diff['dictionary_item_removed'])}):")
                for path in list(diff['dictionary_item_removed'])[:5]:
                    print(f"    {path}")
            
            # Show list items removed
            if 'iterable_item_removed' in diff:
                print(f"\n  LIST ITEMS REMOVED ({len(diff['iterable_item_removed'])}):")
                for path, value in list(diff['iterable_item_removed'].items())[:5]:
                    print(f"    {path}: {str(value)[:80]}")
            
            # Show list items added
            if 'iterable_item_added' in diff:
                print(f"\n  LIST ITEMS ADDED ({len(diff['iterable_item_added'])}):")
                for path, value in list(diff['iterable_item_added'].items())[:5]:
                    print(f"    {path}: {str(value)[:80]}")
            
            # For deeper investigation, show the actual objects
            print(f"\n  Loading actual objects for comparison...")
            orig_id_short = failure['original_id'].split('--')[1][:8]
            
            # Find original
            orig_files = list(Path("generated/input_objects").glob(f"{obj_type}_{orig_id_short}*.json"))
            if orig_files:
                with open(orig_files[0]) as f:
                    original = json.load(f)
                
                # Find reconstituted
                recon_files = list(Path("generated/output_objects").glob(f"{obj_type}_*_reconstituted.json"))
                reconstituted = None
                for recon_file in recon_files:
                    with open(recon_file) as f:
                        recon_obj = json.load(f)
                        # Match by comparing some unique field
                        if obj_type == 'relationship':
                            if (original.get('source_ref', '').split('--')[0] == recon_obj.get('source_ref', '').split('--')[0] and
                                original.get('target_ref', '').split('--')[0] == recon_obj.get('target_ref', '').split('--')[0] and
                                original.get('relationship_type') == recon_obj.get('relationship_type')):
                                reconstituted = recon_obj
                                break
                        elif 'name' in original and 'name' in recon_obj:
                            if original['name'] == recon_obj['name']:
                                reconstituted = recon_obj
                                break
                
                if reconstituted:
                    print(f"  ✓ Found matching reconstituted object")
                    
                    # Show specific problematic fields
                    if obj_type == 'relationship' and 'values_changed' in diff:
                        print(f"\n  RELATIONSHIP DETAILS:")
                        print(f"    Type: {original.get('relationship_type')}")
                        print(f"    Source: {original.get('source_ref', 'N/A')}")
                        print(f"    Target: {original.get('target_ref', 'N/A')}")
                        print(f"    Recon Source: {reconstituted.get('source_ref', 'N/A')}")
                        print(f"    Recon Target: {reconstituted.get('target_ref', 'N/A')}")
                    
                    if obj_type == 'file':
                        print(f"\n  FILE DETAILS:")
                        print(f"    Name: {original.get('name', 'N/A')}")
                        print(f"    Contains refs (orig): {original.get('contains_refs', [])}")
                        print(f"    Contains refs (recon): {reconstituted.get('contains_refs', [])}")
                        print(f"    Content ref (orig): {original.get('content_ref', 'N/A')}")
                        print(f"    Content ref (recon): {reconstituted.get('content_ref', 'N/A')}")
                    
                    if obj_type == 'location':
                        print(f"\n  LOCATION DETAILS:")
                        for key in ['region', 'country', 'city', 'street_address', 'postal_code',
                                   'latitude', 'longitude', 'precision', 'administrative_area']:
                            orig_val = original.get(key)
                            recon_val = reconstituted.get(key)
                            if orig_val != recon_val:
                                print(f"    {key}: {orig_val} → {recon_val}")
                    
                    if obj_type == 'network-traffic':
                        print(f"\n  NETWORK-TRAFFIC DETAILS:")
                        print(f"    Protocols (orig): {original.get('protocols', [])}")
                        print(f"    Protocols (recon): {reconstituted.get('protocols', [])}")
                        print(f"    Src ref (orig): {original.get('src_ref', 'N/A')}")
                        print(f"    Src ref (recon): {reconstituted.get('src_ref', 'N/A')}")
                    
                    if obj_type == 'observed-data':
                        print(f"\n  OBSERVED-DATA DETAILS:")
                        print(f"    Object refs (orig): {len(original.get('object_refs', []))} items")
                        print(f"    Object refs (recon): {len(reconstituted.get('object_refs', []))} items")
                else:
                    print(f"  ✗ Could not find matching reconstituted object")

if __name__ == "__main__":
    analyze_failures()
