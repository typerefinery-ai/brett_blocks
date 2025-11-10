#!/usr/bin/env python3
"""
Comprehensive Method Comparison: Notebook vs Prompt Method
Compare data form creation between Convert_Examples_to_DataForms.ipynb and create-data-forms.md prompt
"""

import json
import os
import sys
from pathlib import Path
from typing import Dict, Any, List, Tuple
import shutil

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

def setup_test_environment():
    """Setup test environment with sample STIX objects"""
    
    print("🏗️ SETTING UP METHOD COMPARISON TEST")
    print("=" * 50)
    
    # Create test directories
    test_dirs = [
        "temp_method_comparison/input_objects",
        "temp_method_comparison/notebook_results", 
        "temp_method_comparison/prompt_results",
        "temp_method_comparison/comparison_results"
    ]
    
    for test_dir in test_dirs:
        os.makedirs(test_dir, exist_ok=True)
    
    # Select test objects from existing examples
    test_objects = []
    
    # 1. Identity object
    identity_path = "Block_Families/examples/aaa_identity.json"
    if os.path.exists(identity_path):
        with open(identity_path, 'r', encoding='utf-8') as f:
            identity_data = json.load(f)
        # Handle array of objects
        identity_obj = identity_data[0] if isinstance(identity_data, list) else identity_data
        test_objects.append({
            'type': 'identity',
            'source_file': identity_path,
            'stix_object': identity_obj,
            'python_class': 'Identity',
            'template_path': 'Block_Families/StixORM/SDO/Identity/Identity_template.json'
        })
    
    # 2. Indicator object  
    indicator_path = "Block_Families/examples/aaa_indicator.json"
    if os.path.exists(indicator_path):
        with open(indicator_path, 'r', encoding='utf-8') as f:
            indicator_data = json.load(f)
        # Handle array of objects
        indicator_obj = indicator_data[0] if isinstance(indicator_data, list) else indicator_data
        test_objects.append({
            'type': 'indicator',
            'source_file': indicator_path,
            'stix_object': indicator_obj,
            'python_class': 'Indicator',
            'template_path': 'Block_Families/StixORM/SDO/Indicator/Indicator_template.json'
        })
    
    # 3. EmailAddress object
    email_path = "Block_Families/examples/email_basic_addr.json"
    if os.path.exists(email_path):
        with open(email_path, 'r', encoding='utf-8') as f:
            email_data = json.load(f)
        # Handle array of objects
        email_obj = email_data[0] if isinstance(email_data, list) else email_data
        test_objects.append({
            'type': 'email-addr',
            'source_file': email_path,
            'stix_object': email_obj,
            'python_class': 'EmailAddress',
            'template_path': 'Block_Families/StixORM/SCO/EmailAddress/EmailAddress_template.json'
        })
    
    # Save test objects to input directory
    for i, obj in enumerate(test_objects):
        input_file = f"temp_method_comparison/input_objects/test_{i+1}_{obj['type'].replace('-', '_')}.json"
        with open(input_file, 'w', encoding='utf-8') as f:
            json.dump(obj, f, indent=2)
    
    print(f"✅ Created {len(test_objects)} test objects")
    for obj in test_objects:
        print(f"   • {obj['python_class']} from {obj['source_file']}")
    
    return test_objects

def load_class_template(template_path: str) -> Dict[str, Any]:
    """Load the class template"""
    with open(template_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def get_typeql_name(stix_type: str) -> str:
    """Convert STIX type to typeql form name"""
    typeql_mapping = {
        'identity': 'identity_form',
        'indicator': 'indicator_form', 
        'email-addr': 'email_addr_form',
        'user-account': 'user_account_form',
        'url': 'url_form'
    }
    return typeql_mapping.get(stix_type, f"{stix_type.replace('-', '_')}_form")

def create_data_form_prompt_method(stix_obj: Dict[str, Any], template: Dict[str, Any]) -> Dict[str, Any]:
    """Create data form using the prompt method (simplified implementation)"""
    
    class_name = template['class_name']
    template_key = f"{class_name}_template"
    template_data = template[template_key]
    
    # Create the data form structure
    data_form = {
        'base_required': {},
        'base_optional': {},
        'object': {},
        'extensions': {},
        'sub': {}
    }
    
    # Auto-generated fields that get empty strings
    auto_generated_fields = {'id', 'created', 'modified'}
    
    # Process base_required section
    if 'base_required' in template_data:
        for prop, template_def in template_data['base_required'].items():
            if prop in stix_obj:
                if prop in auto_generated_fields:
                    data_form['base_required'][prop] = ""
                elif prop == 'type':
                    data_form['base_required'][prop] = stix_obj[prop]
                elif prop == 'spec_version':
                    data_form['base_required'][prop] = "2.1"
                else:
                    data_form['base_required'][prop] = stix_obj[prop]
            else:
                # Add defaults
                if prop == 'type':
                    data_form['base_required'][prop] = template_data.get('_type', stix_obj.get('type'))
                elif prop == 'spec_version':
                    data_form['base_required'][prop] = "2.1"
                else:
                    data_form['base_required'][prop] = ""
    
    # Process base_optional section
    if 'base_optional' in template_data:
        for prop, template_def in template_data['base_optional'].items():
            if prop in stix_obj:
                data_form['base_optional'][prop] = stix_obj[prop]
            else:
                # Add appropriate defaults
                if isinstance(template_def, dict) and 'collection' in template_def:
                    data_form['base_optional'][prop] = []
                else:
                    data_form['base_optional'][prop] = None
    
    # Process object section
    if 'object' in template_data:
        for prop, template_def in template_data['object'].items():
            if prop in stix_obj:
                data_form['object'][prop] = stix_obj[prop]
            else:
                # Add appropriate defaults
                if isinstance(template_def, dict) and 'collection' in template_def:
                    data_form['object'][prop] = []
                elif prop.endswith('_ref') or prop.endswith('_refs'):
                    if prop.endswith('_refs'):
                        data_form['object'][prop] = []
                    else:
                        data_form['object'][prop] = ""
                else:
                    data_form['object'][prop] = ""
    
    # Process extensions section
    if 'extensions' in stix_obj:
        data_form['extensions'] = stix_obj['extensions']
    
    return data_form

def extract_notebook_data_forms():
    """Extract data forms created by the notebook method"""
    
    print("\n📓 EXTRACTING NOTEBOOK METHOD RESULTS")
    print("-" * 40)
    
    # Check if notebook has been run and created data forms
    notebook_outputs = []
    
    # Look for generated files from notebook
    generated_dirs = [
        "Orchestration/generated",
        "data_forms_generated", 
        "test_data_forms"
    ]
    
    for gen_dir in generated_dirs:
        if os.path.exists(gen_dir):
            for file in os.listdir(gen_dir):
                if file.endswith('.json'):
                    file_path = os.path.join(gen_dir, file)
                    print(f"   Found: {file_path}")
                    
                    with open(file_path, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                    
                    # Copy to notebook results directory
                    result_file = f"temp_method_comparison/notebook_results/{file}"
                    with open(result_file, 'w', encoding='utf-8') as f:
                        json.dump(data, f, indent=2)
                    
                    notebook_outputs.append({
                        'file': file,
                        'source_path': file_path,
                        'result_path': result_file,
                        'data': data
                    })
    
    print(f"✅ Extracted {len(notebook_outputs)} notebook-generated data forms")
    return notebook_outputs

def create_prompt_method_results(test_objects: List[Dict[str, Any]]):
    """Create data forms using the prompt method"""
    
    print("\n📝 CREATING PROMPT METHOD RESULTS")
    print("-" * 40)
    
    prompt_results = []
    
    for i, test_obj in enumerate(test_objects):
        try:
            # Load template
            template = load_class_template(test_obj['template_path'])
            
            # Create data form using prompt method
            data_form = create_data_form_prompt_method(test_obj['stix_object'], template)
            
            # Get form name
            form_name = get_typeql_name(test_obj['stix_object']['type'])
            
            # Create complete form
            complete_form = {form_name: data_form}
            
            # Save result
            result_file = f"temp_method_comparison/prompt_results/test_{i+1}_{test_obj['type'].replace('-', '_')}_prompt.json"
            with open(result_file, 'w', encoding='utf-8') as f:
                json.dump(complete_form, f, indent=2)
            
            prompt_results.append({
                'test_object': test_obj,
                'result_file': result_file,
                'data_form': complete_form,
                'form_name': form_name
            })
            
            print(f"   ✅ Created: {test_obj['python_class']} → {Path(result_file).name}")
            
        except Exception as e:
            print(f"   ❌ Error creating {test_obj['python_class']}: {e}")
            prompt_results.append({
                'test_object': test_obj,
                'error': str(e)
            })
    
    return prompt_results

def compare_methods(test_objects: List[Dict[str, Any]], notebook_results: List[Dict[str, Any]], prompt_results: List[Dict[str, Any]]):
    """Compare the two methods"""
    
    print("\n🔍 COMPARING METHODS")
    print("-" * 40)
    
    comparison_results = {
        'summary': {},
        'detailed_comparisons': [],
        'notebook_files': [r['file'] for r in notebook_results],
        'prompt_files': [r.get('result_file', '') for r in prompt_results if 'result_file' in r]
    }
    
    # For each test object, try to find matching results
    for test_obj in test_objects:
        obj_type = test_obj['type']
        python_class = test_obj['python_class']
        
        print(f"\n📋 Comparing {python_class} ({obj_type})")
        
        # Find notebook result
        notebook_match = None
        for nb_result in notebook_results:
            if any(obj_type.replace('-', '_') in nb_result['file'].lower() or 
                   python_class.lower() in nb_result['file'].lower() for check in [True]):
                notebook_match = nb_result
                break
        
        # Find prompt result  
        prompt_match = None
        for pr_result in prompt_results:
            if 'test_object' in pr_result and pr_result['test_object']['type'] == obj_type:
                prompt_match = pr_result
                break
        
        comparison = {
            'object_type': obj_type,
            'python_class': python_class,
            'notebook_result': notebook_match['file'] if notebook_match else None,
            'prompt_result': Path(prompt_match['result_file']).name if prompt_match and 'result_file' in prompt_match else None,
            'has_notebook': notebook_match is not None,
            'has_prompt': prompt_match is not None and 'result_file' in prompt_match
        }
        
        if notebook_match and prompt_match and 'data_form' in prompt_match:
            # Detailed comparison
            nb_data = notebook_match['data']
            pr_data = prompt_match['data_form']
            
            # Compare structure
            nb_keys = set(nb_data.keys()) if isinstance(nb_data, dict) else set()
            pr_keys = set(pr_data.keys()) if isinstance(pr_data, dict) else set()
            
            comparison.update({
                'structure_match': nb_keys == pr_keys,
                'notebook_keys': list(nb_keys),
                'prompt_keys': list(pr_keys),
                'missing_in_notebook': list(pr_keys - nb_keys),
                'missing_in_prompt': list(nb_keys - pr_keys)
            })
            
            print(f"   📊 Structure match: {comparison['structure_match']}")
            if not comparison['structure_match']:
                print(f"      Missing in notebook: {comparison['missing_in_notebook']}")
                print(f"      Missing in prompt: {comparison['missing_in_prompt']}")
        else:
            print(f"   ❌ Cannot compare - Notebook: {comparison['has_notebook']}, Prompt: {comparison['has_prompt']}")
        
        comparison_results['detailed_comparisons'].append(comparison)
    
    # Save comparison results
    with open("temp_method_comparison/comparison_results/method_comparison.json", 'w', encoding='utf-8') as f:
        json.dump(comparison_results, f, indent=2)
    
    # Summary
    total_objects = len(test_objects)
    notebook_count = len([c for c in comparison_results['detailed_comparisons'] if c['has_notebook']])
    prompt_count = len([c for c in comparison_results['detailed_comparisons'] if c['has_prompt']])
    both_count = len([c for c in comparison_results['detailed_comparisons'] if c['has_notebook'] and c['has_prompt']])
    
    print(f"\n📊 COMPARISON SUMMARY")
    print(f"   Total test objects: {total_objects}")
    print(f"   Notebook results: {notebook_count}/{total_objects}")
    print(f"   Prompt results: {prompt_count}/{total_objects}")
    print(f"   Both methods: {both_count}/{total_objects}")
    
    comparison_results['summary'] = {
        'total_objects': total_objects,
        'notebook_count': notebook_count,
        'prompt_count': prompt_count,
        'both_count': both_count,
        'notebook_coverage': notebook_count / total_objects * 100 if total_objects > 0 else 0,
        'prompt_coverage': prompt_count / total_objects * 100 if total_objects > 0 else 0
    }
    
    return comparison_results

def run_method_comparison():
    """Run the complete method comparison"""
    
    print("🔬 BRETT BLOCKS METHOD COMPARISON")
    print("Notebook vs Prompt Method for Data Form Creation")
    print("=" * 60)
    
    # Setup test environment
    test_objects = setup_test_environment()
    
    # Extract notebook results
    notebook_results = extract_notebook_data_forms()
    
    # Create prompt method results
    prompt_results = create_prompt_method_results(test_objects)
    
    # Compare methods
    comparison_results = compare_methods(test_objects, notebook_results, prompt_results)
    
    # Generate final report
    print("\n📝 GENERATING FINAL REPORT")
    print("-" * 40)
    
    report = f"""# Method Comparison Report
## Notebook vs Prompt Method for Data Form Creation

### Test Summary
- **Total Objects Tested:** {comparison_results['summary']['total_objects']}
- **Notebook Coverage:** {comparison_results['summary']['notebook_coverage']:.1f}% ({comparison_results['summary']['notebook_count']}/{comparison_results['summary']['total_objects']})
- **Prompt Coverage:** {comparison_results['summary']['prompt_coverage']:.1f}% ({comparison_results['summary']['prompt_count']}/{comparison_results['summary']['total_objects']})
- **Both Methods:** {comparison_results['summary']['both_count']}/{comparison_results['summary']['total_objects']}

### Detailed Results
"""
    
    for comp in comparison_results['detailed_comparisons']:
        report += f"""
#### {comp['python_class']} ({comp['object_type']})
- **Notebook Result:** {comp['notebook_result'] or 'Not found'}
- **Prompt Result:** {comp['prompt_result'] or 'Not found'}
- **Available in Both:** {comp['has_notebook'] and comp['has_prompt']}
"""
        if 'structure_match' in comp:
            report += f"- **Structure Match:** {comp['structure_match']}\n"
    
    report += f"""
### Files Generated
**Notebook Method Files:**
{chr(10).join(f"- {f}" for f in comparison_results['notebook_files'])}

**Prompt Method Files:**
{chr(10).join(f"- {f}" for f in comparison_results['prompt_files'])}

### Conclusion
The comparison shows the coverage and accuracy of both methods for creating Brett Blocks data forms.
"""
    
    with open("temp_method_comparison/comparison_results/final_report.md", 'w', encoding='utf-8') as f:
        f.write(report)
    
    print("✅ Comparison complete!")
    print(f"📁 Results saved in: temp_method_comparison/")
    print(f"📊 Final report: temp_method_comparison/comparison_results/final_report.md")
    
    return comparison_results

if __name__ == "__main__":
    run_method_comparison()