#!/usr/bin/env python3
"""
Match target objects with available examples from Block_Families/examples directory
"""

import json
from pathlib import Path

def load_target_objects():
    """Load the target objects from the extracted JSON"""
    target_file = Path('c:/projects/brett_blocks/test_output/target_objects.json')
    with open(target_file, 'r', encoding='utf-8') as f:
        return json.load(f)

def find_example_matches():
    """Find matching examples for each target object"""
    
    target_data = load_target_objects()
    examples_dir = Path('c:/projects/brett_blocks/Block_Families/examples')
    
    # Get all available example files
    example_files = list(examples_dir.glob('*.json'))
    example_names = [f.stem for f in example_files]
    
    print("🔍 MATCHING TARGET OBJECTS WITH EXAMPLES")
    print("=" * 50)
    
    matches = {}
    
    # Define mapping strategies for finding examples
    type_mappings = {
        'identity': ['aaa_identity', 'identity'],
        'indicator': ['aaa_indicator', 'indicator'],
        'impact': ['impact'],
        'incident': ['incident'],
        'event': ['event'],
        'observed-data': ['observed'],
        'sequence': ['sequence'],
        'task': ['task'],
        'anecdote': ['anecdote'],
        'email-addr': ['email_basic_addr', 'email'],
        'user-account': ['user_account_unix_basic', 'user_account_twitter_basic', 'user_account'],
        'url': ['url'],
        'email-message': ['email_simple', 'email_headers', 'email_mime'],
        'relationship': ['relationship'],
        'sighting': ['sighting']
    }
    
    all_targets = []
    for category in ['sdo_make_files', 'sco_make_files', 'sro_make_files']:
        for obj in target_data.get(category, []):
            all_targets.append((category, obj))
    
    print(f"🎯 Target objects: {len(all_targets)}")
    print(f"📁 Available examples: {len(example_files)}")
    print()
    
    for category, target_obj in all_targets:
        stix_type = target_obj['stix_type']
        python_class = target_obj['python_class']
        
        print(f"🔎 Matching {python_class} ({stix_type})...")
        
        # Try to find matching examples
        possible_matches = type_mappings.get(stix_type, [])
        found_examples = []
        
        for pattern in possible_matches:
            matching_files = [f for f in example_files if pattern in f.stem.lower()]
            found_examples.extend(matching_files)
        
        # Remove duplicates
        found_examples = list(set(found_examples))
        
        if found_examples:
            print(f"   ✅ Found {len(found_examples)} example(s):")
            for example in found_examples:
                print(f"      • {example.name}")
            
            # Use the first/best match
            chosen_example = found_examples[0]
            matches[python_class] = {
                'category': category,
                'target_object': target_obj,
                'example_file': str(chosen_example),
                'all_matches': [str(f) for f in found_examples]
            }
        else:
            print(f"   ❌ No examples found for {stix_type}")
            matches[python_class] = {
                'category': category,
                'target_object': target_obj,
                'example_file': None,
                'all_matches': []
            }
        print()
    
    # Save the matches
    matches_file = Path('c:/projects/brett_blocks/test_output/object_example_matches.json')
    with open(matches_file, 'w', encoding='utf-8') as f:
        json.dump(matches, f, indent=2)
    
    # Summary
    successful_matches = [k for k, v in matches.items() if v['example_file']]
    print(f"📊 MATCHING SUMMARY:")
    print(f"   Total targets: {len(matches)}")
    print(f"   Successful matches: {len(successful_matches)}")
    print(f"   Success rate: {len(successful_matches)/len(matches)*100:.1f}%")
    print()
    
    print("✅ Successful matches:")
    for obj_class in successful_matches:
        match = matches[obj_class]
        example_file = Path(match['example_file']).name
        print(f"   • {obj_class} → {example_file}")
    
    unmatched = [k for k, v in matches.items() if not v['example_file']]
    if unmatched:
        print(f"\n❌ Unmatched objects ({len(unmatched)}):")
        for obj_class in unmatched:
            match = matches[obj_class]
            stix_type = match['target_object']['stix_type']
            print(f"   • {obj_class} ({stix_type})")
    
    print(f"\n💾 Matches saved to: {matches_file}")
    
    return matches

def main():
    return find_example_matches()

if __name__ == "__main__":
    main()