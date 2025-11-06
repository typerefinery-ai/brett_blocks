#!/usr/bin/env python3
"""
Manual validation of create-data-forms prompt accuracy
Compares manual prompt results vs automated conversion function
"""

import json
import os
from pathlib import Path

def main():
    # Setup paths
    base_path = Path('c:/projects/brett_blocks')
    examples_path = base_path / 'Block_Families' / 'examples'
    
    print("🧪 CREATE-DATA-FORMS PROMPT ACCURACY VALIDATION")
    print("=" * 55)
    
    # Test cases
    test_cases = [
        {
            'name': 'Identity (Adversary Bravo)',
            'example_file': 'aaa_identity.json',
            'manual_file': 'generated_identity_adversary_bravo.json',
            'object_index': 0,
            'expected_form': 'identity_form',
            'stix_type': 'identity'
        },
        {
            'name': 'EmailAddress (John Doe)',
            'example_file': 'email_basic_addr.json', 
            'manual_file': 'generated_email_addr_john.json',
            'object_index': 0,
            'expected_form': 'email_addr_form',
            'stix_type': 'email-addr'
        },
        {
            'name': 'File (foo.dll)',
            'example_file': 'file_basic.json',
            'manual_file': 'generated_file_foo_dll.json',
            'object_index': 0,
            'expected_form': 'file_form',
            'stix_type': 'file'
        }
    ]
    
    results = []
    
    for test_case in test_cases:
        print(f"\n📋 Testing: {test_case['name']}")
        
        try:
            # Load original example
            example_file = examples_path / test_case['example_file']
            with open(example_file, 'r', encoding='utf-8') as f:
                example_data = json.load(f)
            
            # Get the specific STIX object
            if isinstance(example_data, list):
                stix_obj = example_data[test_case['object_index']]
            else:
                stix_obj = example_data
            
            print(f"   📄 Source: {test_case['example_file']}")
            print(f"   🔍 STIX Type: {stix_obj.get('type')}")
            
            # Load manually generated form (from prompt)
            manual_file = base_path / 'test_output' / test_case['manual_file']
            if manual_file.exists():
                with open(manual_file, 'r', encoding='utf-8') as f:
                    manual_result = json.load(f)
                
                expected_form = test_case['expected_form']
                
                # Check if form exists
                has_expected_form = expected_form in manual_result
                print(f"   🤖 Manual form generated: {has_expected_form}")
                print(f"   📊 Expected form name: {expected_form}")
                print(f"   ✅ Form name correct: {has_expected_form}")
                
                if has_expected_form:
                    form = manual_result[expected_form]
                    
                    # Check structure
                    required_sections = ['base_required', 'base_optional', 'object', 'extensions', 'sub']
                    structure_check = {}
                    
                    for section in required_sections:
                        exists = section in form
                        structure_check[section] = exists
                        status = "✅" if exists else "❌"
                        field_count = len(form.get(section, {})) if exists and isinstance(form.get(section), dict) else 0
                        print(f"      {status} {section}: {field_count} fields")
                    
                    # Check key fields
                    all_sections_present = all(structure_check.values())
                    
                    # Validate base_required fields
                    base_req_valid = False
                    if 'base_required' in form:
                        base_req = form['base_required']
                        # SCO objects only need 3 base fields, SDO objects need 5
                        if test_case['stix_type'] in ['email-addr', 'file', 'url', 'domain-name', 'ipv4-addr', 'ipv6-addr', 'mac-addr', 'windows-registry-key', 'x509-certificate', 'mutex', 'artifact', 'autonomous-system', 'directory', 'network-traffic', 'process', 'software', 'user-account']:
                            # SCO (Cyber Observable Object) - only needs type, spec_version, id
                            expected_base_fields = ['type', 'spec_version', 'id']
                        else:
                            # SDO (STIX Domain Object) - needs type, spec_version, id, created, modified  
                            expected_base_fields = ['type', 'spec_version', 'id', 'created', 'modified']
                        
                        base_req_valid = all(field in base_req for field in expected_base_fields)
                        print(f"      🔍 Base required fields complete ({len(expected_base_fields)} expected): {base_req_valid}")
                    
                    # Check for reference extraction
                    has_references = False
                    if 'object' in form:
                        obj_fields = form['object']
                        ref_fields = [k for k in obj_fields.keys() if k.endswith('_ref') or k.endswith('_refs')]
                        has_references = len(ref_fields) > 0
                        if ref_fields:
                            print(f"      🔗 Reference fields found: {ref_fields}")
                    
                    result = {
                        'name': test_case['name'],
                        'stix_type': test_case['stix_type'],
                        'form_name_correct': has_expected_form,
                        'structure_complete': all_sections_present,
                        'base_required_valid': base_req_valid,
                        'has_references': has_references,
                        'manual_result': manual_result
                    }
                    
                else:
                    result = {
                        'name': test_case['name'],
                        'stix_type': test_case['stix_type'],
                        'form_name_correct': False,
                        'structure_complete': False,
                        'base_required_valid': False,
                        'has_references': False,
                        'error': 'Expected form not found'
                    }
            else:
                print(f"   ❌ Manual result file not found: {manual_file}")
                result = {
                    'name': test_case['name'],
                    'stix_type': test_case['stix_type'],
                    'form_name_correct': False,
                    'structure_complete': False,
                    'base_required_valid': False,
                    'has_references': False,
                    'error': 'Manual result file not found'
                }
            
            results.append(result)
            
        except Exception as e:
            print(f"   ❌ Error: {e}")
            results.append({
                'name': test_case['name'],
                'error': str(e)
            })
    
    # Summary
    print(f"\n📊 VALIDATION SUMMARY")
    print(f"   Total tests: {len(results)}")
    
    successful = [r for r in results if r.get('form_name_correct') and r.get('structure_complete') and r.get('base_required_valid')]
    print(f"   Fully successful: {len(successful)}")
    
    form_name_correct = [r for r in results if r.get('form_name_correct')]
    structure_complete = [r for r in results if r.get('structure_complete')]
    base_valid = [r for r in results if r.get('base_required_valid')]
    
    print(f"   Form name accuracy: {len(form_name_correct)}/{len(results)} ({len(form_name_correct)/len(results)*100:.1f}%)")
    print(f"   Structure accuracy: {len(structure_complete)}/{len(results)} ({len(structure_complete)/len(results)*100:.1f}%)")
    print(f"   Base fields accuracy: {len(base_valid)}/{len(results)} ({len(base_valid)/len(results)*100:.1f}%)")
    print(f"   Overall success rate: {len(successful)}/{len(results)} ({len(successful)/len(results)*100:.1f}%)")
    
    # Detailed results
    print(f"\n📋 DETAILED RESULTS:")
    for result in results:
        if 'error' not in result:
            print(f"   {result['name']}: ✅ Form Name: {result['form_name_correct']}, ✅ Structure: {result['structure_complete']}, ✅ Base Fields: {result['base_required_valid']}")
        else:
            print(f"   {result['name']}: ❌ {result['error']}")

if __name__ == "__main__":
    main()