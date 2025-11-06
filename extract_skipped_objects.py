#!/usr/bin/env python3
"""
Extract specific objects from block_output.json for the skipped object types
"""

import json
from pathlib import Path

def extract_skipped_objects():
    """Extract indicator, incident, observed-data, user-account, and email-message objects"""
    
    block_output_file = Path("Block_Families/examples/block_output.json")
    
    print("🔍 EXTRACTING SKIPPED OBJECTS FROM BLOCK_OUTPUT.JSON")
    print("=" * 55)
    
    if not block_output_file.exists():
        print(f"❌ File not found: {block_output_file}")
        return
    
    with open(block_output_file, 'r', encoding='utf-8') as f:
        objects = json.load(f)
    
    # Target object types we need
    target_types = {
        'indicator': 'indicator',
        'incident': 'incident', 
        'observed-data': 'observed_data',
        'user-account': 'user_account',
        'email-message': 'email_message'
    }
    
    extracted_objects = {}
    
    for obj in objects:
        obj_type = obj.get('type')
        if obj_type in target_types:
            type_key = target_types[obj_type]
            if type_key not in extracted_objects:
                extracted_objects[type_key] = []
            extracted_objects[type_key].append(obj)
    
    # Save individual files for each type
    output_dir = Path("test_output/extracted_objects")
    output_dir.mkdir(exist_ok=True)
    
    print(f"📁 Creating individual object files...")
    
    for type_key, objects_list in extracted_objects.items():
        print(f"\n📋 {type_key.upper()}: Found {len(objects_list)} objects")
        
        for i, obj in enumerate(objects_list):
            # Create descriptive filename
            obj_name = obj.get('name', obj.get('value', obj.get('id', f'object_{i}'))[:30])
            safe_name = obj_name.replace('/', '_').replace('\\', '_').replace(':', '_').replace('--', '_')
            filename = f"{type_key}_{safe_name}.json"
            
            output_file = output_dir / filename
            
            # Save as single object (not array)
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(obj, f, indent=2)
            
            print(f"   ✅ Created: {filename}")
            print(f"      ID: {obj.get('id', 'N/A')}")
            print(f"      Name: {obj.get('name', obj.get('value', 'N/A'))}")
    
    # Save summary
    summary = {
        'total_objects_found': sum(len(objs) for objs in extracted_objects.values()),
        'by_type': {k: len(v) for k, v in extracted_objects.items()},
        'extracted_objects': extracted_objects
    }
    
    summary_file = output_dir / "extraction_summary.json"
    with open(summary_file, 'w', encoding='utf-8') as f:
        json.dump(summary, f, indent=2)
    
    print(f"\n📊 EXTRACTION SUMMARY:")
    print(f"   Total objects extracted: {summary['total_objects_found']}")
    for obj_type, count in summary['by_type'].items():
        print(f"   {obj_type}: {count} objects")
    
    print(f"\n💾 Files saved to: {output_dir}")
    print(f"📄 Summary saved to: {summary_file}")
    
    return extracted_objects

if __name__ == "__main__":
    extract_skipped_objects()