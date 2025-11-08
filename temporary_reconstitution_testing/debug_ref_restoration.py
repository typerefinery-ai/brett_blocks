"""
Debug script to trace reference restoration with added logging
"""
import json
from pathlib import Path

def test_restoration_with_logging():
    print("=" * 80)
    print("TESTING REFERENCE RESTORATION WITH LOGGING")
    print("=" * 80)
    
    # Load a sequence object that should reference another sequence
    seq_file = Path("generated/data_forms/sequence_e63de439_data_form.json")
    if not seq_file.exists():
        print(f"ERROR: {seq_file} not found")
        return
    
    with open(seq_file) as f:
        data_form = json.load(f)
    
    print(f"\nData form ID: {data_form['id']}")
    print(f"Data form type: {data_form['type']}")
    print(f"on_completion in data_form: {data_form.get('on_completion', 'NOT FOUND')}")
    
    # Load reference tracking
    ref_file = Path("generated/data_forms/reference_tracking.json")
    with open(ref_file) as f:
        ref_tracking = json.load(f)
    
    # Find the reference for on_completion
    original_id = data_form['id']
    if original_id in ref_tracking:
        refs = ref_tracking[original_id]
        print(f"\nReferences for this object:")
        for field_name, ref_info in refs.items():
            print(f"  {field_name}: {ref_info}")
            if field_name == 'on_completion':
                ref_id = ref_info['ref_id']
                print(f"    → This should map to new UUID for: {ref_id}")
    
    # Load ID mapping from reconstitution
    mapping_file = Path("generated/reconstituted_objects/id_mapping.json")
    if mapping_file.exists():
        with open(mapping_file) as f:
            id_mapping = json.load(f)
        
        # Check if the on_completion reference is in the mapping
        if original_id in ref_tracking and 'on_completion' in ref_tracking[original_id]:
            ref_id = ref_tracking[original_id]['on_completion']['ref_id']
            if ref_id in id_mapping:
                print(f"\n✅ Mapping exists: {ref_id} → {id_mapping[ref_id]}")
            else:
                print(f"\n❌ NO MAPPING for: {ref_id}")
                print(f"   Available mappings ({len(id_mapping)} total):")
                for old_id, new_id in sorted(id_mapping.items())[:5]:
                    print(f"     {old_id} → {new_id}")
                print(f"   ...")
    else:
        print(f"\n⚠️  ID mapping file not found: {mapping_file}")
    
    # Now let's actually trace through the restore_references_to_data_form logic
    print("\n" + "=" * 80)
    print("SIMULATING restore_references_to_data_form")
    print("=" * 80)
    
    # Simulate what should happen
    if original_id in ref_tracking:
        refs = ref_tracking[original_id]
        for field_name, ref_info in refs.items():
            original_ref = ref_info['ref_id']
            ref_type = ref_info['ref_type']
            
            print(f"\nProcessing reference: {field_name}")
            print(f"  Original ref: {original_ref}")
            print(f"  Ref type: {ref_type}")
            
            if ref_type == 'single':
                # This is what get_mapped_uuid should do
                if original_ref in id_mapping:
                    new_uuid = id_mapping[original_ref]
                    print(f"  ✅ Found in mapping: {new_uuid}")
                else:
                    print(f"  ❌ NOT in mapping - would generate new UUID")
                    
            elif ref_type == 'embedded':
                print(f"  🔍 Embedded reference - needs path navigation")
                embed_info = ref_info.get('embedded_info', {})
                print(f"     Path: {embed_info.get('path', 'UNKNOWN')}")

if __name__ == "__main__":
    test_restoration_with_logging()
