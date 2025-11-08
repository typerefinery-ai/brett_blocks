#!/usr/bin/env python3
"""
Comprehensive comparison of input vs output STIX objects
Maps objects by their STIX ID and reports all differences
"""

import json
import os
from pathlib import Path
from deepdiff import DeepDiff
from collections import defaultdict

def load_json_file(filepath):
    """Load and return JSON content from file."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"❌ Error loading {filepath}: {e}")
        return None

def get_stix_objects_from_directory(directory):
    """Load all STIX objects from a directory and map by ID."""
    objects_by_id = {}
    directory = Path(directory)
    
    print(f"📂 Scanning directory: {directory}")
    
    for json_file in directory.glob("*.json"):
        if json_file.name == "all_reconstituted_objects.json":
            continue
            
        content = load_json_file(json_file)
        if content:
            # Handle both single objects and lists
            if isinstance(content, list):
                for obj in content:
                    if isinstance(obj, dict) and 'id' in obj:
                        objects_by_id[obj['id']] = obj
                        print(f"   📋 Loaded list object: {obj['id']} from {json_file.name}")
            elif isinstance(content, dict) and 'id' in content:
                objects_by_id[content['id']] = content
                print(f"   📋 Loaded object: {content['id']} from {json_file.name}")
            else:
                print(f"   ⚠️  Invalid STIX object in {json_file.name}")
    
    print(f"   ✅ Total objects loaded: {len(objects_by_id)}")
    return objects_by_id

def normalize_stix_id(stix_id):
    """
    Normalize a STIX ID by replacing UUID with placeholder while keeping type.
    Example: 'identity--ce31dd38-f69b-45ba-9bcd-2a208bbf8017' -> 'identity--UUID'
    """
    if isinstance(stix_id, str) and '--' in stix_id:
        parts = stix_id.split('--')
        if len(parts) == 2:
            return f"{parts[0]}--UUID"
    return stix_id

def normalize_stix_value(value):
    """
    Normalize a value that might be a STIX ID, list of STIX IDs, dict, or primitive.
    Preserves list order and structure while normalizing UUIDs.
    """
    if value is None:
        return None
    elif isinstance(value, str):
        # Check if it's a STIX ID (type--uuid format)
        return normalize_stix_id(value)
    elif isinstance(value, list):
        # Preserve order while normalizing each element
        return [normalize_stix_value(item) for item in value]
    elif isinstance(value, dict):
        # Recursively normalize dictionary
        return {k: normalize_stix_value(v) for k, v in value.items()}
    else:
        # Return primitives as-is (int, float, bool, etc.)
        return value

def normalize_stix_object(obj):
    """
    Normalize STIX object for comparison by:
    1. Removing timestamp fields that will naturally differ
    2. Normalizing all STIX IDs to type--UUID format (preserving type)
    3. Preserving list order and structure
    4. Recursively handling nested objects
    """
    if not isinstance(obj, dict):
        return obj
        
    normalized = {}
    
    # Fields to completely remove from comparison
    fields_to_remove = ['created', 'modified']
    
    for key, value in obj.items():
        # Skip fields that should be removed
        if key in fields_to_remove:
            continue
            
        # Normalize the value
        normalized[key] = normalize_stix_value(value)
    
    return normalized

def map_objects_by_content(input_objects, output_objects):
    """
    Map input objects to output objects by comparing normalized content.
    Returns dict mapping input_id -> output_id for matching objects.
    """
    mapping = {}
    
    # Normalize all input objects
    normalized_inputs = {}
    for input_id, input_obj in input_objects.items():
        normalized_inputs[input_id] = normalize_stix_object(input_obj)
    
    # Normalize all output objects
    normalized_outputs = {}
    for output_id, output_obj in output_objects.items():
        normalized_outputs[output_id] = normalize_stix_object(output_obj)
    
    # Try to match each input to an output by normalized content
    used_output_ids = set()
    
    for input_id, norm_input in normalized_inputs.items():
        best_match = None
        best_match_score = 0
        
        for output_id, norm_output in normalized_outputs.items():
            if output_id in used_output_ids:
                continue
                
            # Must be same type
            if norm_input.get('type') != norm_output.get('type'):
                continue
            
            # Compare normalized objects
            diff = DeepDiff(norm_input, norm_output, ignore_order=False)
            
            # Calculate similarity score (inverse of difference count)
            if not diff:
                # Perfect match
                mapping[input_id] = output_id
                used_output_ids.add(output_id)
                break
            else:
                # Calculate similarity score based on differences
                diff_count = sum(len(v) if isinstance(v, (dict, set)) else 1 
                               for v in diff.values())
                similarity = 1.0 / (1.0 + diff_count)
                
                if similarity > best_match_score:
                    best_match_score = similarity
                    best_match = output_id
        
        # If we found a reasonable match (>50% similar), use it
        if best_match and best_match_score > 0.5:
            mapping[input_id] = best_match
            used_output_ids.add(best_match)
    
    return mapping

def compare_objects():
    """Compare input and output objects comprehensively."""
    
    print("🔍 COMPREHENSIVE STIX OBJECT COMPARISON")
    print("=" * 60)
    
    # Load objects from both directories
    input_dir = "C:/projects/brett_blocks/temporary_reconstitution_testing/generated/input_objects"
    output_dir = "C:/projects/brett_blocks/temporary_reconstitution_testing/generated/output_objects"
    
    print("\n📥 Loading input objects...")
    input_objects = get_stix_objects_from_directory(input_dir)
    
    print("\n📤 Loading output objects...")  
    output_objects = get_stix_objects_from_directory(output_dir)
    
    print("\n📊 SUMMARY:")
    print(f"   📥 Input objects: {len(input_objects)}")
    print(f"   📤 Output objects: {len(output_objects)}")
    
    # Map objects by normalized content
    print("\n🔗 Mapping objects by content similarity...")
    object_mapping = map_objects_by_content(input_objects, output_objects)
    
    print(f"   ✅ Successfully mapped: {len(object_mapping)} object pairs")
    
    # Identify unmapped objects
    mapped_input_ids = set(object_mapping.keys())
    mapped_output_ids = set(object_mapping.values())
    
    unmapped_inputs = set(input_objects.keys()) - mapped_input_ids
    unmapped_outputs = set(output_objects.keys()) - mapped_output_ids
    
    print(f"   ❌ Unmapped input objects: {len(unmapped_inputs)}")
    print(f"   ➕ Unmapped output objects: {len(unmapped_outputs)}")
    
    if unmapped_inputs:
        print("\n❌ UNMAPPED INPUT OBJECTS:")
        for obj_id in sorted(unmapped_inputs)[:10]:  # Show first 10
            obj_type = input_objects[obj_id].get('type', 'unknown')
            print(f"   - {obj_type}: {obj_id}")
        if len(unmapped_inputs) > 10:
            print(f"   ... and {len(unmapped_inputs) - 10} more")
    
    if unmapped_outputs:
        print("\n➕ UNMAPPED OUTPUT OBJECTS:")
        for obj_id in sorted(unmapped_outputs)[:10]:  # Show first 10
            obj_type = output_objects[obj_id].get('type', 'unknown')
            print(f"   + {obj_type}: {obj_id}")
        if len(unmapped_outputs) > 10:
            print(f"   ... and {len(unmapped_outputs) - 10} more")
    
    # Compare mapped objects in detail
    print(f"\n🔍 DETAILED COMPARISON OF MAPPED OBJECTS ({len(object_mapping)} pairs):")
    print("-" * 60)
    
    identical_count = 0
    structural_identical_count = 0
    different_count = 0
    
    differences_by_type = defaultdict(list)
    common_difference_patterns = defaultdict(int)
    detailed_examples = []
    
    for input_id, output_id in sorted(object_mapping.items()):
        input_obj = input_objects[input_id]
        output_obj = output_objects[output_id]
        obj_type = input_obj.get('type', 'unknown')
        
        # Normalized comparison (ignoring UUIDs and timestamps)
        normalized_input = normalize_stix_object(input_obj)
        normalized_output = normalize_stix_object(output_obj)
        normalized_diff = DeepDiff(normalized_input, normalized_output, ignore_order=False)
        
        if not normalized_diff:
            print(f"✅ PERFECT MATCH: {obj_type}")
            print(f"   Input:  {input_id}")
            print(f"   Output: {output_id}")
            identical_count += 1
        else:
            print(f"❌ DIFFERENCES FOUND: {obj_type}")
            print(f"   Input:  {input_id}")
            print(f"   Output: {output_id}")
            different_count += 1
            differences_by_type[obj_type].append((input_id, output_id))
            
            # Analyze difference patterns
            if 'values_changed' in normalized_diff:
                for path in normalized_diff['values_changed'].keys():
                    common_difference_patterns[path] += 1
            
            if 'dictionary_item_added' in normalized_diff:
                for path in normalized_diff['dictionary_item_added']:
                    common_difference_patterns[f"ADDED: {path}"] += 1
                    
            if 'dictionary_item_removed' in normalized_diff:
                for path in normalized_diff['dictionary_item_removed']:
                    common_difference_patterns[f"REMOVED: {path}"] += 1
            
            if 'iterable_item_added' in normalized_diff:
                for path in normalized_diff['iterable_item_added'].keys():
                    common_difference_patterns[f"LIST ITEM ADDED: {path}"] += 1
                    
            if 'iterable_item_removed' in normalized_diff:
                for path in normalized_diff['iterable_item_removed'].keys():
                    common_difference_patterns[f"LIST ITEM REMOVED: {path}"] += 1
            
            # Store detailed example for first few differences
            if len(detailed_examples) < 5:
                detailed_examples.append({
                    'type': obj_type,
                    'input_id': input_id,
                    'output_id': output_id,
                    'diff': normalized_diff,
                    'input_obj': input_obj,
                    'output_obj': output_obj
                })
    
    # Show detailed examples
    if detailed_examples:
        print("\n" + "=" * 60)
        print("📋 DETAILED DIFFERENCE EXAMPLES (First 5)")
        print("=" * 60)
        
        for idx, example in enumerate(detailed_examples, 1):
            print(f"\n🔍 Example {idx}: {example['type']}")
            print(f"   Input ID:  {example['input_id']}")
            print(f"   Output ID: {example['output_id']}")
            print(f"   Differences:")
            
            if 'values_changed' in example['diff']:
                print("   📝 Changed Values:")
                for path, change in list(example['diff']['values_changed'].items())[:5]:
                    print(f"      {path}:")
                    print(f"         Was: {change['old_value']}")
                    print(f"         Now: {change['new_value']}")
                if len(example['diff']['values_changed']) > 5:
                    print(f"      ... and {len(example['diff']['values_changed']) - 5} more changed values")
            
            if 'dictionary_item_removed' in example['diff']:
                print("   ➖ Removed Fields:")
                for path in list(example['diff']['dictionary_item_removed'])[:5]:
                    print(f"      {path}")
                if len(example['diff']['dictionary_item_removed']) > 5:
                    print(f"      ... and {len(example['diff']['dictionary_item_removed']) - 5} more")
            
            if 'dictionary_item_added' in example['diff']:
                print("   ➕ Added Fields:")
                for path in list(example['diff']['dictionary_item_added'])[:5]:
                    print(f"      {path}")
                if len(example['diff']['dictionary_item_added']) > 5:
                    print(f"      ... and {len(example['diff']['dictionary_item_added']) - 5} more")
            
            if 'iterable_item_removed' in example['diff']:
                print("   📤 Removed List Items:")
                for path, items in list(example['diff']['iterable_item_removed'].items())[:3]:
                    print(f"      {path}: {items}")
            
            if 'iterable_item_added' in example['diff']:
                print("   📥 Added List Items:")
                for path, items in list(example['diff']['iterable_item_added'].items())[:3]:
                    print(f"      {path}: {items}")
    
    # Summary statistics
    print("\n" + "=" * 60)
    print("📊 COMPARISON SUMMARY:")
    print("=" * 60)
    total_compared = len(object_mapping)
    if total_compared > 0:
        print(f"   ✅ Perfect matches: {identical_count} ({identical_count/total_compared*100:.1f}%)")
        print(f"   ❌ Objects with differences: {different_count} ({different_count/total_compared*100:.1f}%)")
        print(f"   📊 Total compared: {total_compared}")
    print(f"   ❌ Unmapped inputs: {len(unmapped_inputs)}")
    print(f"   ➕ Unmapped outputs: {len(unmapped_outputs)}")
    
    if differences_by_type:
        print("\n❌ DIFFERENCES BY OBJECT TYPE:")
        for obj_type, pairs in sorted(differences_by_type.items()):
            print(f"   {obj_type}: {len(pairs)} objects with differences")
    
    if common_difference_patterns:
        print("\n🔍 MOST COMMON DIFFERENCE PATTERNS:")
        sorted_patterns = sorted(common_difference_patterns.items(), 
                               key=lambda x: x[1], reverse=True)
        for pattern, count in sorted_patterns[:15]:  # Show top 15 patterns
            print(f"   [{count:3d}x] {pattern}")

if __name__ == "__main__":
    compare_objects()
