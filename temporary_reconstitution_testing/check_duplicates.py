"""
Check for duplicate IDs in the examples directory
"""
import json
from pathlib import Path
from collections import defaultdict

examples_dir = Path("../Block_Families/examples")
id_to_objects = defaultdict(list)

for json_file in examples_dir.glob("*.json"):
    try:
        with open(json_file) as f:
            content = f.read()
        
        # Handle STIX bundles
        if content.strip().startswith('['):
            objects = json.loads(content)
        else:
            obj = json.loads(content)
            if obj.get('type') == 'bundle':
                objects = obj.get('objects', [])
            else:
                objects = [obj]
        
        for obj in objects:
            obj_id = obj.get('id')
            if obj_id:
                id_to_objects[obj_id].append({
                    'file': json_file.name,
                    'type': obj.get('type'),
                    'content': obj
                })
    except Exception as e:
        print(f"Error processing {json_file.name}: {e}")

# Find duplicates
duplicates = {obj_id: objs for obj_id, objs in id_to_objects.items() if len(objs) > 1}

print(f"=" * 80)
print(f"Found {len(duplicates)} IDs with multiple instances")
print(f"=" * 80)

for obj_id, instances in sorted(duplicates.items())[:10]:
    print(f"\n{obj_id}: {len(instances)} instances")
    for idx, inst in enumerate(instances, 1):
        print(f"  [{idx}] {inst['file']} - type: {inst['type']}")
        if inst['type'] == 'relationship':
            print(f"      relationship_type: {inst['content'].get('relationship_type')}")
            print(f"      source_ref: {inst['content'].get('source_ref', 'N/A')[:50]}")
            print(f"      target_ref: {inst['content'].get('target_ref', 'N/A')[:50]}")

# Check specifically for relationship--44298a74-ba52-4f0c-87a3-1824e67d7fad
target_ids = [
    "relationship--44298a74-ba52-4f0c-87a3-1824e67d7fad",
    "note--0c7b5b88-8ff7-4a4d-aa9d-feb398cd0061",
    "observed-data--b67d30ff-02ac-498a-92f9-32f845f448cf",
    "file--9a1f834d-2506-5367-baec-7aa63996ac43",
    "sighting--ee20065d-2555-424f-ad9e-0f8428623c75"
]

for target_id in target_ids:
    if target_id in id_to_objects:
        print(f"\n{'=' * 80}")
        print(f"Details for {target_id}:")
        print(f"{'=' * 80}")
        for idx, inst in enumerate(id_to_objects[target_id], 1):
            print(f"\n[{idx}] File: {inst['file']}")
            obj = inst['content']
            print(f"    Type: {obj.get('type')}")
            if obj.get('type') == 'relationship':
                print(f"    Relationship Type: {obj.get('relationship_type')}")
                print(f"    Source: {obj.get('source_ref')}")
                print(f"    Target: {obj.get('target_ref')}")
            elif obj.get('type') == 'note':
                print(f"    Content: {obj.get('content', 'N/A')[:80]}")
                print(f"    Authors: {obj.get('authors', [])}")
            elif obj.get('type') == 'file':
                print(f"    Name: {obj.get('name', 'N/A')}")
                print(f"    Contains refs: {obj.get('contains_refs', [])}")
            elif obj.get('type') == 'observed-data':
                print(f"    First observed: {obj.get('first_observed')}")
                print(f"    Last observed: {obj.get('last_observed')}")
                print(f"    Object refs: {obj.get('object_refs', [])}")
    else:
        print(f"\n{target_id}: NOT FOUND (only 1 instance)")

