"""
Fix duplicate STIX IDs in examples directory.

For SCO objects: Generate UUIDv5 based on contributing properties
For SDO/SRO objects: Generate UUIDv4
"""

import json
import uuid
import hashlib
from pathlib import Path
from collections import defaultdict

# STIX namespace for SCO UUIDv5 generation
STIX_NAMESPACE = uuid.UUID('00abedb4-aa42-466c-9c01-fed23315a9b7')

# Define contributing properties for each SCO type
SCO_CONTRIBUTING_PROPERTIES = {
    'network-traffic': ['start', 'end', 'src_ref', 'dst_ref', 'src_port', 'dst_port', 'protocols', 'extensions'],
    'ipv4-addr': ['value'],
    'ipv6-addr': ['value'],
}

def generate_sco_uuid(obj_type, obj_data):
    """Generate UUIDv5 for SCO based on contributing properties."""
    contributing_props = SCO_CONTRIBUTING_PROPERTIES.get(obj_type)
    
    if not contributing_props:
        # Not an SCO we're handling, use UUIDv4
        return str(uuid.uuid4())
    
    # Extract contributing properties in sorted order
    props_dict = {}
    for prop in sorted(contributing_props):  # Sort for consistency
        if prop in obj_data:
            props_dict[prop] = obj_data[prop]
    
    # If no contributing properties present, use UUIDv4
    if not props_dict:
        return str(uuid.uuid4())
    
    # Create canonical JSON string (sorted keys, no whitespace)
    canonical_json = json.dumps(props_dict, sort_keys=True, separators=(',', ':'), ensure_ascii=True)
    
    # Generate UUIDv5
    new_uuid = uuid.uuid5(STIX_NAMESPACE, canonical_json)
    
    return str(new_uuid)

def generate_uuid_for_object(obj):
    """Generate appropriate UUID based on object type."""
    obj_type = obj.get('type')
    
    # Check if it's an SCO we need to handle specially
    if obj_type in SCO_CONTRIBUTING_PROPERTIES:
        new_uuid = generate_sco_uuid(obj_type, obj)
    else:
        # SDO/SRO/etc - use UUIDv4
        new_uuid = str(uuid.uuid4())
    
    return f"{obj_type}--{new_uuid}"

def load_json_file(file_path):
    """Load JSON file."""
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_json_file(file_path, data):
    """Save JSON file with pretty formatting."""
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
        f.write('\n')  # Add trailing newline

def collect_all_objects():
    """Collect all STIX objects from examples directory."""
    examples_dir = Path(r'C:\projects\brett_blocks\Block_Families\examples')
    
    all_objects = []
    
    for json_file in examples_dir.rglob('*.json'):
        try:
            data = load_json_file(json_file)
            
            # Handle different file structures
            if isinstance(data, dict):
                if 'objects' in data:
                    # Bundle format
                    for obj in data['objects']:
                        all_objects.append({
                            'file': json_file,
                            'object': obj,
                            'id': obj.get('id')
                        })
                elif 'id' in data:
                    # Single object
                    all_objects.append({
                        'file': json_file,
                        'object': data,
                        'id': data.get('id')
                    })
            elif isinstance(data, list):
                # Array of objects
                for obj in data:
                    if isinstance(obj, dict) and 'id' in obj:
                        all_objects.append({
                            'file': json_file,
                            'object': obj,
                            'id': obj.get('id')
                        })
        except Exception as e:
            print(f"   ⚠️  Error reading {json_file}: {e}")
    
    return all_objects

def find_duplicates(all_objects):
    """Find objects with duplicate IDs but different content."""
    id_to_objects = defaultdict(list)
    
    for item in all_objects:
        id_to_objects[item['id']].append(item)
    
    duplicates = {}
    for obj_id, items in id_to_objects.items():
        if len(items) > 1:
            # Check if content is actually different
            contents = []
            for item in items:
                # Create a normalized version for comparison (exclude 'modified' timestamp)
                obj_copy = item['object'].copy()
                obj_copy.pop('modified', None)
                contents.append(json.dumps(obj_copy, sort_keys=True))
            
            # If contents differ, it's a real duplicate problem
            if len(set(contents)) > 1:
                duplicates[obj_id] = items
    
    return duplicates

def fix_duplicate_ids():
    """Main function to fix duplicate IDs."""
    print("🔍 Scanning examples directory for duplicate IDs...")
    
    all_objects = collect_all_objects()
    print(f"   ✅ Found {len(all_objects)} STIX objects")
    
    duplicates = find_duplicates(all_objects)
    print(f"   ⚠️  Found {len(duplicates)} IDs with different content (real duplicates)")
    
    if not duplicates:
        print("   🎉 No duplicates to fix!")
        return
    
    print("\n📋 Duplicate IDs found:")
    examples_base = Path(r'C:\projects\brett_blocks\Block_Families\examples')
    for obj_id, items in duplicates.items():
        print(f"\n   ID: {obj_id}")
        print(f"   Type: {items[0]['object'].get('type')}")
        print(f"   Occurrences: {len(items)}")
        for i, item in enumerate(items, 1):
            rel_path = item['file'].relative_to(examples_base)
            print(f"      #{i}: {rel_path}")
    
    print("\n🔧 Fixing duplicates...")
    
    fixes_applied = 0
    
    for obj_id, items in duplicates.items():
        obj_type = items[0]['object'].get('type')
        print(f"\n   Processing {obj_type} ({obj_id})...")
        
        # Keep the first occurrence, fix the rest
        for i, item in enumerate(items):
            if i == 0:
                print(f"      ✓ Keeping first occurrence: {item['file'].name}")
                continue
            
            # Generate new ID
            new_id = generate_uuid_for_object(item['object'])
            old_id = item['object']['id']
            
            print(f"      🔄 Fixing occurrence #{i+1}: {item['file'].name}")
            print(f"         Old ID: {old_id}")
            print(f"         New ID: {new_id}")
            
            # Update the object
            item['object']['id'] = new_id
            
            # Save the file
            file_path = item['file']
            file_data = load_json_file(file_path)
            
            # Update the object in the file structure
            if isinstance(file_data, dict):
                if 'objects' in file_data:
                    # Bundle format - find and update the object
                    for j, obj in enumerate(file_data['objects']):
                        if obj.get('id') == old_id:
                            file_data['objects'][j] = item['object']
                            break
                elif file_data.get('id') == old_id:
                    # Single object file
                    file_data = item['object']
            elif isinstance(file_data, list):
                # Array of objects
                for j, obj in enumerate(file_data):
                    if isinstance(obj, dict) and obj.get('id') == old_id:
                        file_data[j] = item['object']
                        break
            
            save_json_file(file_path, file_data)
            fixes_applied += 1
            print(f"         ✅ Saved {file_path.name}")
    
    print(f"\n🎉 Fixed {fixes_applied} duplicate IDs!")
    print("\n✅ All duplicates have been resolved.")

if __name__ == '__main__':
    fix_duplicate_ids()
