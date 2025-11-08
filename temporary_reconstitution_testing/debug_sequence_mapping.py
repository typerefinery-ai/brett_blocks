#!/usr/bin/env python3
"""Debug the sequence on_completion UUID mapping"""

import json
from pathlib import Path

# Load reconstitution data
with open('generated/data_forms/reconstitution_data.json', 'r') as f:
    recon_data = json.load(f)

# Find the two sequence objects involved
seq1_id = "sequence--5ced78bf-aab8-4650-9c9e-a6914d68b46e"  # The failing one
seq2_id = "sequence--4c9100f2-06a1-4570-ba51-7dabde2371b8"  # The referenced one

# Find their filenames
id_to_filename = recon_data['id_to_filename_mapping']
print(f"Sequence 1 (failing): {seq1_id}")
print(f"  Filename: {id_to_filename.get(seq1_id, 'NOT FOUND')}")
print(f"\nSequence 2 (referenced): {seq2_id}")
print(f"  Filename: {id_to_filename.get(seq2_id, 'NOT FOUND')}")

# Check creation sequence
creation_seq = recon_data['creation_sequence']
print("\n" + "=" * 80)
print("CREATION SEQUENCE FOR BOTH:")
print("=" * 80)

for entry in creation_seq:
    if entry['object_id'] in [seq1_id, seq2_id]:
        print(f"\nObject: {entry['object_id']}")
        print(f"  Sequence order: {entry['sequence_order']}")
        print(f"  Filename: {entry['filename']}")
        print(f"  Dependencies: {entry['dependencies']}")

# Now check the reconstituted outputs to see what UUIDs they got
print("\n" + "=" * 80)
print("RECONSTITUTED OBJECTS:")
print("=" * 80)

output_dir = Path('generated/output_objects')
for f in output_dir.glob('sequence_*_reconstituted.json'):
    with open(f, 'r') as file:
        obj = json.load(file)
        obj_id = obj.get('id')
        # Check if this is one of our sequences by checking on_completion
        if 'on_completion' in obj and obj['on_completion']:
            print(f"\nFile: {f.name}")
            print(f"  ID: {obj_id}")
            print(f"  on_completion: {obj['on_completion']}")
