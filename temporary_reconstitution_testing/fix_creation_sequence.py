#!/usr/bin/env python3
"""
Fix the creation sequence in reconstitution_data.json

This script recomputes the creation sequence with the fixed algorithm
that excludes self-references when determining dependencies.
"""

import json
from pathlib import Path
from collections import defaultdict


def fix_creation_sequence(recon_data_path):
    """Recompute creation sequence excluding self-references"""
    
    # Load existing reconstitution data
    with open(recon_data_path, 'r', encoding='utf-8') as f:
        recon_data = json.load(f)
    
    print(f"📂 Loaded reconstitution data with {len(recon_data['detailed_reference_extraction'])} objects")
    
    # Build dependency graph excluding self-references
    dependency_graph = {}
    objects_without_dependencies = []
    
    for ref_info in recon_data['detailed_reference_extraction']:
        obj_id = ref_info['object_id']
        referenced_ids = ref_info['referenced_object_ids']
        
        # Exclude self-references (object's own ID) from dependencies
        # An object referencing itself via the 'id' field is not a real dependency
        external_dependencies = [ref_id for ref_id in referenced_ids if ref_id != obj_id]
        
        dependency_graph[obj_id] = {
            'depends_on': external_dependencies,
            'filename': ref_info['filename'],
            'form_name': ref_info['form_name'],
            'object_type': ref_info['object_type']
        }
        
        if not external_dependencies:
            objects_without_dependencies.append(obj_id)
    
    print(f"📊 Objects with NO external dependencies: {len(objects_without_dependencies)}")
    print(f"   First 5: {[obj_id.split('--')[0] + '--' + obj_id.split('--')[1][:8] for obj_id in objects_without_dependencies[:5]]}")
    
    # Calculate creation sequence (topological sort)
    creation_sequence = []
    remaining_objects = set(dependency_graph.keys())
    available_objects = set(objects_without_dependencies)
    
    while remaining_objects:
        # Find objects whose dependencies are all satisfied
        ready_objects = []
        for obj_id in remaining_objects:
            deps = dependency_graph[obj_id]['depends_on']
            if all(dep in available_objects or dep not in dependency_graph for dep in deps):
                ready_objects.append(obj_id)
        
        if not ready_objects:
            # Circular dependency or missing references - add remaining objects
            print(f"⚠️  Warning: {len(remaining_objects)} objects have circular/missing dependencies")
            ready_objects = list(remaining_objects)
        
        # Sort for deterministic ordering
        ready_objects.sort()
        
        for obj_id in ready_objects:
            creation_sequence.append({
                'sequence_order': len(creation_sequence) + 1,
                'object_id': obj_id,
                'filename': dependency_graph[obj_id]['filename'],
                'form_name': dependency_graph[obj_id]['form_name'],
                'object_type': dependency_graph[obj_id]['object_type'],
                'dependencies': dependency_graph[obj_id]['depends_on']
            })
            available_objects.add(obj_id)
            remaining_objects.remove(obj_id)
    
    print(f"✅ Created sequence of {len(creation_sequence)} objects")
    
    # Update the reconstitution data
    recon_data['creation_sequence'] = creation_sequence
    recon_data['dependency_graph'] = dependency_graph
    
    # Save the updated file
    with open(recon_data_path, 'w', encoding='utf-8') as f:
        json.dump(recon_data, f, indent=2, ensure_ascii=False)
    
    print(f"💾 Saved updated reconstitution data")
    
    # Also save just the creation sequence
    sequence_path = recon_data_path.parent / "creation_sequence.json"
    with open(sequence_path, 'w', encoding='utf-8') as f:
        json.dump(creation_sequence, f, indent=2, ensure_ascii=False)
    
    print(f"💾 Saved updated creation sequence")
    
    # Show example: anecdote dependency chain
    print("\n📋 Example: Anecdote dependency chain")
    anecdote_id = "anecdote--e1298bc0-818e-5cdb-9154-eac37c8e260f"
    
    for seq_item in creation_sequence:
        if seq_item['object_id'] == anecdote_id:
            print(f"   Anecdote: sequence_order={seq_item['sequence_order']}, deps={len(seq_item['dependencies'])}")
            for dep in seq_item['dependencies']:
                dep_type = dep.split('--')[0]
                dep_short = dep.split('--')[1][:8]
                # Find this dependency in the sequence
                for dep_item in creation_sequence:
                    if dep_item['object_id'] == dep:
                        print(f"      → {dep_type}--{dep_short}: sequence_order={dep_item['sequence_order']}")
                        break


if __name__ == "__main__":
    recon_data_path = Path(__file__).parent / "generated" / "data_forms" / "reconstitution_data.json"
    
    if not recon_data_path.exists():
        print(f"❌ Reconstitution data not found: {recon_data_path}")
        exit(1)
    
    fix_creation_sequence(recon_data_path)
    print("\n✅ Creation sequence fixed!")
