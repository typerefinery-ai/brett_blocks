#!/usr/bin/env python3
"""
Extract target object lists from a_seed/2_initial_set_of_blocks.md
"""

import json
import re
from pathlib import Path

def extract_object_lists():
    """Extract sdo_make_files, sco_make_files, and sro_make_files from the seed file"""
    
    seed_file = Path('c:/projects/brett_blocks/a_seed/2_initial_set_of_blocks.md')
    
    with open(seed_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extract the JSON block containing the three dictionaries
    # Look for the pattern starting with "sdo_make_files" and ending with the closing brace
    json_pattern = r'"sdo_make_files":\s*\[(.*?)\]\s*}\s*```'
    
    # Find the start of sdo_make_files
    sdo_start = content.find('"sdo_make_files": [')
    if sdo_start == -1:
        raise ValueError("Could not find sdo_make_files in seed file")
    
    # Find the end of the JSON block (look for the closing brace and triple backticks)
    json_end = content.find('}\n```', sdo_start)
    if json_end == -1:
        raise ValueError("Could not find end of JSON block in seed file")
    
    # Extract the JSON content
    json_start = content.rfind('{', 0, sdo_start)  # Find the opening brace before sdo_make_files
    json_content = content[json_start:json_end + 1]
    
    try:
        data = json.loads(json_content)
        return data
    except json.JSONDecodeError as e:
        print(f"JSON decode error: {e}")
        print(f"Extracted content: {json_content[:500]}...")
        raise

def main():
    """Main function to extract and display object lists"""
    
    print("🔍 EXTRACTING TARGET OBJECT LISTS")
    print("=" * 40)
    
    try:
        data = extract_object_lists()
        
        # Display the extracted data
        for category in ['sdo_make_files', 'sco_make_files', 'sro_make_files']:
            if category in data:
                objects = data[category]
                print(f"\n📋 {category.upper()}: {len(objects)} objects")
                for obj in objects:
                    print(f"   • {obj['python_class']} ({obj['stix_type']})")
                    print(f"     Python: {obj['python']}")
                    print(f"     Template: {obj['template']}")
                    print(f"     Example: {obj['data_example']}")
                    print()
        
        # Save the extracted data
        output_file = Path('c:/projects/brett_blocks/test_output/target_objects.json')
        output_file.parent.mkdir(exist_ok=True)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)
        
        print(f"✅ Target objects saved to: {output_file}")
        
        # Summary
        total_objects = sum(len(data.get(cat, [])) for cat in ['sdo_make_files', 'sco_make_files', 'sro_make_files'])
        print(f"\n📊 SUMMARY: {total_objects} total target objects across 3 categories")
        
        return data
        
    except Exception as e:
        print(f"❌ Error extracting object lists: {e}")
        return None

if __name__ == "__main__":
    main()