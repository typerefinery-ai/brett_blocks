#!/usr/bin/env python3
"""
Simplified Brett Blocks Test Runner
Focus on core roundtrip testing using existing Orchestration patterns
"""

import json
import os
import sys
from pathlib import Path
from typing import Dict, Any, List, Tuple

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Import existing utilities
from Orchestration.Utilities.util import emulate_ports, unwind_ports, conv
from Orchestration.conv import conv


def load_test_data():
    """Load test data from creation results - both original and skipped objects"""
    all_test_data = []
    
    # Load original test data
    try:
        with open('test_output/data_form_creation_results.json', 'r', encoding='utf-8') as f:
            original_results = json.load(f)
        original_successful = [r for r in original_results if r.get('success')]
        all_test_data.extend(original_successful)
        print(f"📄 Loaded {len(original_successful)} original test objects")
    except FileNotFoundError:
        print("❌ Original test data not found.")
    
    # Load skipped test data
    try:
        with open('test_output/skipped_data_form_results.json', 'r', encoding='utf-8') as f:
            skipped_results = json.load(f)
        skipped_successful = [r for r in skipped_results if r.get('success')]
        all_test_data.extend(skipped_successful)
        print(f"📄 Loaded {len(skipped_successful)} skipped test objects")
    except FileNotFoundError:
        print("❌ Skipped test data not found.")
    
    if not all_test_data:
        print("❌ No test data found. Run create_data_forms.py and create_skipped_data_forms.py first.")
    
    return all_test_data


def simple_object_comparison(original: Dict[str, Any], generated: Dict[str, Any]) -> Tuple[bool, List[str]]:
    """
    Simple comparison ignoring UUIDs and timestamps
    """
    differences = []
    
    # Check basic fields
    for field in ['type', 'spec_version']:
        if original.get(field) != generated.get(field):
            differences.append(f"Field '{field}': {original.get(field)} != {generated.get(field)}")
    
    # Check content fields (name, value, etc.)
    content_fields = ['name', 'value', 'description', 'pattern', 'labels']
    for field in content_fields:
        if field in original:
            if original.get(field) != generated.get(field):
                differences.append(f"Content field '{field}': {original.get(field)} != {generated.get(field)}")
    
    is_equivalent = len(differences) == 0
    return is_equivalent, differences


def test_identity_roundtrip(test_data: Dict[str, Any]) -> Dict[str, Any]:
    """Test Identity object roundtrip"""
    from Block_Families.StixORM.SDO.Identity.make_identity import main as make_identity
    
    try:
        # Prepare file paths
        data_form_path = Path("tests/temp_data") / Path(test_data['data_form_path']).name
        result_path = "tests/results/identity_test_result.json"
        
        # Copy data form to temp location
        with open(test_data['data_form_path'], 'r', encoding='utf-8') as f:
            data_form = json.load(f)
        
        with open(data_form_path, 'w', encoding='utf-8') as f:
            json.dump(data_form, f, indent=2)
        
        # Run make_identity
        make_identity(str(data_form_path), result_path)
        
        # Load result
        if os.path.exists(result_path):
            with open(result_path, 'r', encoding='utf-8') as f:
                generated_obj = json.load(f)
            
            # Compare
            original = test_data['original_stix']
            is_equivalent, differences = simple_object_comparison(original, generated_obj)
            
            return {
                'success': True,
                'equivalent': is_equivalent,
                'differences': differences,
                'generated_object': generated_obj
            }
        else:
            return {'success': False, 'error': 'Result file not created'}
            
    except Exception as e:
        return {'success': False, 'error': str(e)}


def test_email_addr_roundtrip(test_data: Dict[str, Any]) -> Dict[str, Any]:
    """Test EmailAddress object roundtrip"""
    from Block_Families.StixORM.SCO.Email_Addr.make_email_addr import main as make_email_addr
    
    try:
        # Prepare file paths
        data_form_path = Path("tests/temp_data") / Path(test_data['data_form_path']).name
        result_path = "tests/results/email_addr_test_result.json"
        
        # Copy data form to temp location
        with open(test_data['data_form_path'], 'r', encoding='utf-8') as f:
            data_form = json.load(f)
        
        with open(data_form_path, 'w', encoding='utf-8') as f:
            json.dump(data_form, f, indent=2)
        
        # Run make_email_addr
        make_email_addr(str(data_form_path), result_path)
        
        # Load result
        if os.path.exists(result_path):
            with open(result_path, 'r', encoding='utf-8') as f:
                generated_obj = json.load(f)
            
            # Compare
            original = test_data['original_stix']
            is_equivalent, differences = simple_object_comparison(original, generated_obj)
            
            return {
                'success': True,
                'equivalent': is_equivalent,
                'differences': differences,
                'generated_object': generated_obj
            }
        else:
            return {'success': False, 'error': 'Result file not created'}
            
    except Exception as e:
        return {'success': False, 'error': str(e)}


def test_url_roundtrip(test_data: Dict[str, Any]) -> Dict[str, Any]:
    """Test URL object roundtrip"""
    from Block_Families.StixORM.SCO.URL.make_url import main as make_url
    
    try:
        # Prepare file paths
        data_form_path = Path("tests/temp_data") / Path(test_data['data_form_path']).name
        result_path = "tests/results/url_test_result.json"
        
        # Copy data form to temp location
        with open(test_data['data_form_path'], 'r', encoding='utf-8') as f:
            data_form = json.load(f)
        
        with open(data_form_path, 'w', encoding='utf-8') as f:
            json.dump(data_form, f, indent=2)
        
        # Run make_url
        make_url(str(data_form_path), result_path)
        
        # Load result
        if os.path.exists(result_path):
            with open(result_path, 'r', encoding='utf-8') as f:
                generated_obj = json.load(f)
            
            # Compare
            original = test_data['original_stix']
            is_equivalent, differences = simple_object_comparison(original, generated_obj)
            
            return {
                'success': True,
                'equivalent': is_equivalent,
                'differences': differences,
                'generated_object': generated_obj
            }
        else:
            return {'success': False, 'error': 'Result file not created'}
            
    except Exception as e:
        return {'success': False, 'error': str(e)}


def test_indicator_roundtrip(test_data: Dict[str, Any]) -> Dict[str, Any]:
    """Test Indicator object roundtrip"""
    from Block_Families.StixORM.SDO.Indicator.make_indicator import main as make_indicator
    
    try:
        # Prepare file paths
        data_form_path = Path("tests/temp_data") / Path(test_data['data_form_path']).name
        result_path = "tests/results/indicator_test_result.json"
        
        # Copy data form to temp location
        with open(test_data['data_form_path'], 'r', encoding='utf-8') as f:
            data_form = json.load(f)
        
        with open(data_form_path, 'w', encoding='utf-8') as f:
            json.dump(data_form, f, indent=2)
        
        # Run make_indicator
        make_indicator(str(data_form_path), result_path)
        
        # Load result
        if os.path.exists(result_path):
            with open(result_path, 'r', encoding='utf-8') as f:
                generated_obj = json.load(f)
            
            # Compare
            original = test_data['original_stix']
            is_equivalent, differences = simple_object_comparison(original, generated_obj)
            
            return {
                'success': True,
                'equivalent': is_equivalent,
                'differences': differences,
                'generated_object': generated_obj
            }
        else:
            return {'success': False, 'error': 'Result file not created'}
            
    except Exception as e:
        return {'success': False, 'error': str(e)}


def test_incident_roundtrip(test_data: Dict[str, Any]) -> Dict[str, Any]:
    """Test Incident object roundtrip"""
    from Block_Families.StixORM.SDO.Incident.make_incident import main as make_incident
    
    try:
        # Prepare file paths
        data_form_path = Path("tests/temp_data") / Path(test_data['data_form_path']).name
        result_path = "tests/results/incident_test_result.json"
        
        # Copy data form to temp location
        with open(test_data['data_form_path'], 'r', encoding='utf-8') as f:
            data_form = json.load(f)
        
        with open(data_form_path, 'w', encoding='utf-8') as f:
            json.dump(data_form, f, indent=2)
        
        # Run make_incident
        make_incident(str(data_form_path), result_path)
        
        # Load result
        if os.path.exists(result_path):
            with open(result_path, 'r', encoding='utf-8') as f:
                generated_obj = json.load(f)
            
            # Compare
            original = test_data['original_stix']
            is_equivalent, differences = simple_object_comparison(original, generated_obj)
            
            return {
                'success': True,
                'equivalent': is_equivalent,
                'differences': differences,
                'generated_object': generated_obj
            }
        else:
            return {'success': False, 'error': 'Result file not created'}
            
    except Exception as e:
        return {'success': False, 'error': str(e)}


def test_observed_data_roundtrip(test_data: Dict[str, Any]) -> Dict[str, Any]:
    """Test ObservedData object roundtrip"""
    from Block_Families.StixORM.SDO.Observed_Data.make_observed_data import main as make_observed_data
    
    try:
        # Prepare file paths
        data_form_path = Path("tests/temp_data") / Path(test_data['data_form_path']).name
        result_path = "tests/results/observed_data_test_result.json"
        
        # Copy data form to temp location
        with open(test_data['data_form_path'], 'r', encoding='utf-8') as f:
            data_form = json.load(f)
        
        with open(data_form_path, 'w', encoding='utf-8') as f:
            json.dump(data_form, f, indent=2)
        
        # Run make_observed_data
        make_observed_data(str(data_form_path), result_path)
        
        # Load result
        if os.path.exists(result_path):
            with open(result_path, 'r', encoding='utf-8') as f:
                generated_obj = json.load(f)
            
            # Compare
            original = test_data['original_stix']
            is_equivalent, differences = simple_object_comparison(original, generated_obj)
            
            return {
                'success': True,
                'equivalent': is_equivalent,
                'differences': differences,
                'generated_object': generated_obj
            }
        else:
            return {'success': False, 'error': 'Result file not created'}
            
    except Exception as e:
        return {'success': False, 'error': str(e)}


def test_user_account_roundtrip(test_data: Dict[str, Any]) -> Dict[str, Any]:
    """Test UserAccount object roundtrip"""
    from Block_Families.StixORM.SCO.User_Account.make_user_account import main as make_user_account
    
    try:
        # Prepare file paths
        data_form_path = Path("tests/temp_data") / Path(test_data['data_form_path']).name
        result_path = "tests/results/user_account_test_result.json"
        
        # Copy data form to temp location
        with open(test_data['data_form_path'], 'r', encoding='utf-8') as f:
            data_form = json.load(f)
        
        with open(data_form_path, 'w', encoding='utf-8') as f:
            json.dump(data_form, f, indent=2)
        
        # Run make_user_account
        make_user_account(str(data_form_path), result_path)
        
        # Load result
        if os.path.exists(result_path):
            with open(result_path, 'r', encoding='utf-8') as f:
                generated_obj = json.load(f)
            
            # Compare
            original = test_data['original_stix']
            is_equivalent, differences = simple_object_comparison(original, generated_obj)
            
            return {
                'success': True,
                'equivalent': is_equivalent,
                'differences': differences,
                'generated_object': generated_obj
            }
        else:
            return {'success': False, 'error': 'Result file not created'}
            
    except Exception as e:
        return {'success': False, 'error': str(e)}


def test_email_message_roundtrip(test_data: Dict[str, Any]) -> Dict[str, Any]:
    """Test EmailMessage object roundtrip"""
    from Block_Families.StixORM.SCO.Email_Message.make_email_msg import main as make_email_msg
    
    try:
        # Prepare file paths
        data_form_path = Path("tests/temp_data") / Path(test_data['data_form_path']).name
        result_path = "tests/results/email_message_test_result.json"
        
        # Copy data form to temp location
        with open(test_data['data_form_path'], 'r', encoding='utf-8') as f:
            data_form = json.load(f)
        
        with open(data_form_path, 'w', encoding='utf-8') as f:
            json.dump(data_form, f, indent=2)
        
        # Run make_email_msg
        make_email_msg(str(data_form_path), result_path)
        
        # Load result
        if os.path.exists(result_path):
            with open(result_path, 'r', encoding='utf-8') as f:
                generated_obj = json.load(f)
            
            # Compare
            original = test_data['original_stix']
            is_equivalent, differences = simple_object_comparison(original, generated_obj)
            
            return {
                'success': True,
                'equivalent': is_equivalent,
                'differences': differences,
                'generated_object': generated_obj
            }
        else:
            return {'success': False, 'error': 'Result file not created'}
            
    except Exception as e:
        return {'success': False, 'error': str(e)}


def run_simplified_tests():
    """Run simplified roundtrip tests"""
    
    print("🧪 SIMPLIFIED BRETT BLOCKS ROUNDTRIP TESTS")
    print("=" * 55)
    
    # Setup
    os.makedirs("tests/temp_data", exist_ok=True)
    os.makedirs("tests/results", exist_ok=True)
    
    # Load test data
    test_data_list = load_test_data()
    if not test_data_list:
        return
    
    # Test mapping
    test_functions = {
        'Identity': test_identity_roundtrip,
        'EmailAddress': test_email_addr_roundtrip,
        'URL': test_url_roundtrip,
        'Indicator': test_indicator_roundtrip,
        'Incident': test_incident_roundtrip,
        'ObservedData': test_observed_data_roundtrip,
        'UserAccount': test_user_account_roundtrip,
        'EmailMessage': test_email_message_roundtrip,
    }
    
    results = []
    
    for test_data in test_data_list:
        python_class = test_data['python_class']
        
        print(f"\n🔬 Testing {python_class}")
        print(f"   📄 Data form: {Path(test_data['data_form_path']).name}")
        
        if python_class in test_functions:
            test_result = test_functions[python_class](test_data)
            test_result['python_class'] = python_class
            test_result['test_data'] = test_data
            
            if test_result.get('success'):
                if test_result.get('equivalent'):
                    print("   ✅ PASSED - Objects are equivalent")
                else:
                    print("   ❌ FAILED - Objects differ")
                    for diff in test_result.get('differences', []):
                        print(f"      • {diff}")
            else:
                print(f"   ❌ ERROR - {test_result.get('error')}")
            
            results.append(test_result)
        else:
            print(f"   ⏭️  SKIPPED - No test function for {python_class}")
            results.append({
                'python_class': python_class,
                'success': False,
                'error': 'No test function available'
            })
    
    # Summary
    successful_tests = [r for r in results if r.get('success')]
    equivalent_tests = [r for r in results if r.get('equivalent')]
    
    print(f"\n📊 TEST SUMMARY")
    print(f"   Total tests attempted: {len(results)}")
    print(f"   Successfully executed: {len(successful_tests)}")
    print(f"   Equivalent objects: {len(equivalent_tests)}")
    print(f"   Success rate: {len(equivalent_tests)/len(results)*100:.1f}%")
    
    # Save results
    results_file = "tests/results/simplified_test_results.json"
    with open(results_file, 'w', encoding='utf-8') as f:
        json.dump({
            'summary': {
                'total_tests': len(results),
                'successful_tests': len(successful_tests),
                'equivalent_tests': len(equivalent_tests),
                'success_rate': len(equivalent_tests)/len(results)*100 if results else 0
            },
            'detailed_results': results
        }, f, indent=2)
    
    print(f"\n💾 Results saved to: {results_file}")
    
    return results


if __name__ == "__main__":
    run_simplified_tests()