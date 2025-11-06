#!/usr/bin/env python3
"""
Roundtrip Test: Which Method Works Better?
Test both prompt and notebook generated data forms with actual Brett Blocks functions
"""

import json
import os
import sys
from pathlib import Path
from typing import Dict, Any

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

def test_data_form_with_brett_blocks(data_form_path: str, output_path: str, test_type: str) -> Dict[str, Any]:
    """Test a data form with the actual Brett Blocks make functions"""
    
    try:
        if test_type == 'identity':
            from Block_Families.StixORM.SDO.Identity.make_identity import main as make_identity
            make_identity(data_form_path, output_path)
        elif test_type == 'email_addr':
            from Block_Families.StixORM.SCO.Email_Addr.make_email_addr import main as make_email_addr
            make_email_addr(data_form_path, output_path)
        else:
            return {'success': False, 'error': f'Unknown test type: {test_type}'}
        
        # Check if output was created
        if os.path.exists(output_path):
            with open(output_path, 'r', encoding='utf-8') as f:
                generated_obj = json.load(f)
            return {
                'success': True,
                'generated_object': generated_obj,
                'output_path': output_path
            }
        else:
            return {'success': False, 'error': 'No output file created'}
            
    except Exception as e:
        return {'success': False, 'error': str(e)}

def run_roundtrip_comparison():
    """Compare both methods by running actual Brett Blocks functions"""
    
    print("🔄 ROUNDTRIP COMPARISON TEST")
    print("Testing which method works better with Brett Blocks")
    print("=" * 55)
    
    # Create test directory
    os.makedirs("temp_method_comparison/roundtrip_test", exist_ok=True)
    
    test_cases = [
        {
            'name': 'Identity',
            'type': 'identity',
            'prompt_file': 'temp_method_comparison/direct_comparison/Identity_prompt.json',
            'notebook_file': 'temp_method_comparison/direct_comparison/Identity_notebook.json'
        },
        {
            'name': 'EmailAddress', 
            'type': 'email_addr',
            'prompt_file': 'temp_method_comparison/direct_comparison/EmailAddress_prompt.json',
            'notebook_file': 'temp_method_comparison/direct_comparison/EmailAddress_notebook.json'
        }
    ]
    
    results = []
    
    for test_case in test_cases:
        print(f"\n🧪 Testing {test_case['name']}")
        
        # Test prompt method
        prompt_output = f"temp_method_comparison/roundtrip_test/{test_case['name']}_prompt_result.json"
        prompt_result = test_data_form_with_brett_blocks(
            test_case['prompt_file'], 
            prompt_output, 
            test_case['type']
        )
        
        # Test notebook method
        notebook_output = f"temp_method_comparison/roundtrip_test/{test_case['name']}_notebook_result.json"
        notebook_result = test_data_form_with_brett_blocks(
            test_case['notebook_file'], 
            notebook_output, 
            test_case['type']
        )
        
        # Compare results
        comparison = {
            'test_case': test_case['name'],
            'type': test_case['type'],
            'prompt_success': prompt_result['success'],
            'notebook_success': notebook_result['success'],
            'prompt_error': prompt_result.get('error'),
            'notebook_error': notebook_result.get('error')
        }
        
        if prompt_result['success'] and notebook_result['success']:
            # Both worked - compare outputs
            prompt_obj = prompt_result['generated_object']
            notebook_obj = notebook_result['generated_object']
            
            # Simple comparison
            objects_match = prompt_obj == notebook_obj
            comparison.update({
                'both_successful': True,
                'objects_match': objects_match,
                'prompt_output': prompt_output,
                'notebook_output': notebook_output
            })
            
            print(f"   ✅ Prompt method: SUCCESS")
            print(f"   ✅ Notebook method: SUCCESS") 
            print(f"   📊 Generated objects match: {objects_match}")
            
        elif prompt_result['success'] and not notebook_result['success']:
            comparison['winner'] = 'prompt'
            print(f"   ✅ Prompt method: SUCCESS")
            print(f"   ❌ Notebook method: {notebook_result['error']}")
            
        elif not prompt_result['success'] and notebook_result['success']:
            comparison['winner'] = 'notebook'
            print(f"   ❌ Prompt method: {prompt_result['error']}")
            print(f"   ✅ Notebook method: SUCCESS")
            
        else:
            comparison['winner'] = 'neither'
            print(f"   ❌ Prompt method: {prompt_result['error']}")
            print(f"   ❌ Notebook method: {notebook_result['error']}")
        
        results.append(comparison)
    
    # Generate summary
    print(f"\n📊 ROUNDTRIP TEST SUMMARY")
    
    prompt_successes = sum(1 for r in results if r['prompt_success'])
    notebook_successes = sum(1 for r in results if r['notebook_success'])
    both_successful = sum(1 for r in results if r.get('both_successful', False))
    objects_matching = sum(1 for r in results if r.get('objects_match', False))
    
    print(f"   Total tests: {len(results)}")
    print(f"   Prompt method successes: {prompt_successes}/{len(results)}")
    print(f"   Notebook method successes: {notebook_successes}/{len(results)}")
    print(f"   Both successful: {both_successful}/{len(results)}")
    if both_successful > 0:
        print(f"   Generated objects match: {objects_matching}/{both_successful}")
    
    # Determine winner
    if prompt_successes > notebook_successes:
        winner = "Prompt Method"
        print(f"\n🏆 WINNER: {winner}")
    elif notebook_successes > prompt_successes:
        winner = "Notebook Method"
        print(f"\n🏆 WINNER: {winner}")
    elif prompt_successes == notebook_successes and both_successful == len(results):
        if objects_matching == both_successful:
            winner = "TIE - Both methods work perfectly"
        else:
            winner = "TIE - Both work but generate different objects"
        print(f"\n🏆 RESULT: {winner}")
    else:
        winner = "INCONCLUSIVE"
        print(f"\n🏆 RESULT: {winner}")
    
    # Save detailed results
    final_results = {
        'summary': {
            'total_tests': len(results),
            'prompt_successes': prompt_successes,
            'notebook_successes': notebook_successes,
            'both_successful': both_successful,
            'objects_matching': objects_matching,
            'winner': winner
        },
        'detailed_results': results
    }
    
    with open("temp_method_comparison/roundtrip_test/roundtrip_results.json", 'w', encoding='utf-8') as f:
        json.dump(final_results, f, indent=2)
    
    # Create final report
    report = f"""# Roundtrip Test Results

## Executive Summary
**Winner: {winner}**

## Test Results
- **Total Tests:** {len(results)}
- **Prompt Method Success Rate:** {prompt_successes}/{len(results)} ({prompt_successes/len(results)*100:.1f}%)
- **Notebook Method Success Rate:** {notebook_successes}/{len(results)} ({notebook_successes/len(results)*100:.1f}%)
- **Both Methods Successful:** {both_successful}/{len(results)}
- **Generated Objects Match:** {objects_matching}/{both_successful if both_successful > 0 else 1}

## Method Evaluation

### Prompt Method (create-data-forms.md)
- **Compatibility:** {'High' if prompt_successes == len(results) else 'Medium' if prompt_successes > 0 else 'Low'}
- **Success Rate:** {prompt_successes/len(results)*100:.1f}%
- **Key Finding:** Uses empty strings for missing fields

### Notebook Method (Convert_Examples_to_DataForms.ipynb)
- **Compatibility:** {'High' if notebook_successes == len(results) else 'Medium' if notebook_successes > 0 else 'Low'}
- **Success Rate:** {notebook_successes/len(results)*100:.1f}%
- **Key Finding:** Uses null values for missing fields

## Detailed Results
"""
    
    for result in results:
        report += f"""
### {result['test_case']}
- **Prompt Method:** {'✅ SUCCESS' if result['prompt_success'] else f"❌ {result.get('prompt_error', 'FAILED')}"}
- **Notebook Method:** {'✅ SUCCESS' if result['notebook_success'] else f"❌ {result.get('notebook_error', 'FAILED')}"}
"""
        if result.get('objects_match') is not None:
            report += f"- **Objects Match:** {'✅ YES' if result['objects_match'] else '❌ NO'}\n"
    
    report += f"""
## Recommendation

"""
    
    if winner == "Prompt Method":
        report += "**Use the Prompt Method** - Better compatibility with Brett Blocks infrastructure."
    elif winner == "Notebook Method":
        report += "**Use the Notebook Method** - Better compatibility with Brett Blocks infrastructure."
    elif "TIE - Both methods work perfectly" in winner:
        report += "**Either method works** - Both are fully compatible. Choose based on your workflow preference."
    elif "TIE" in winner:
        report += "**Either method works** - Both are compatible but generate slightly different outputs. Standardize on one approach."
    else:
        report += "**Further investigation needed** - Results are inconclusive."
    
    with open("temp_method_comparison/roundtrip_test/roundtrip_report.md", 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(f"\n✅ Roundtrip test complete!")
    print(f"📁 Results: temp_method_comparison/roundtrip_test/")
    print(f"📊 Report: temp_method_comparison/roundtrip_test/roundtrip_report.md")
    
    return final_results

if __name__ == "__main__":
    run_roundtrip_comparison()