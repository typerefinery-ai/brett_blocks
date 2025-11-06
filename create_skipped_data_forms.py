#!/usr/bin/env python3
"""
Create data forms for the skipped object types using extracted objects
"""

import json
import re
from pathlib import Path
from typing import Dict, Any

def load_class_template(template_path: str) -> Dict[str, Any]:
    """Load the class template"""
    with open(template_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def get_typeql_name(stix_type: str) -> str:
    """Convert STIX type to typeql form name using established mapping"""
    typeql_mapping = {
        'indicator': 'indicator_form',
        'incident': 'incident_form',
        'observed-data': 'observed_data_form',
        'user-account': 'user_account_form',
        'email-message': 'email_message_form'
    }
    return typeql_mapping.get(stix_type, f"{stix_type.replace('-', '_')}_form")

def convert_stix_to_data_form(stix_obj: Dict[str, Any], template: Dict[str, Any]) -> Dict[str, Any]:
    """Convert STIX object to data form using the template (simplified version)"""
    
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
    
    return data_form

def create_data_forms_for_skipped_objects():
    """Create data forms for all extracted skipped objects"""
    
    print("🏗️ CREATING DATA FORMS FOR SKIPPED OBJECTS")
    print("=" * 55)
    
    # Object configurations
    object_configs = {
        'indicator': {
            'template_path': 'Block_Families/StixORM/SDO/Indicator/Indicator_template.json',
            'python_class': 'Indicator',
            'python_file': 'Block_Families/StixORM/SDO/Indicator/make_indicator.py'
        },
        'incident': {
            'template_path': 'Block_Families/StixORM/SDO/Incident/Incident_template.json',
            'python_class': 'Incident',
            'python_file': 'Block_Families/StixORM/SDO/Incident/make_incident.py'
        },
        'observed_data': {
            'template_path': 'Block_Families/StixORM/SDO/Observed_Data/ObservedData_template.json',
            'python_class': 'ObservedData',
            'python_file': 'Block_Families/StixORM/SDO/Observed_Data/make_observed_data.py'
        },
        'user_account': {
            'template_path': 'Block_Families/StixORM/SCO/User_Account/UserAccount_template.json',
            'python_class': 'UserAccount', 
            'python_file': 'Block_Families/StixORM/SCO/User_Account/make_user_account.py'
        },
        'email_message': {
            'template_path': 'Block_Families/StixORM/SCO/Email_Message/EmailMessage_template.json',
            'python_class': 'EmailMessage',
            'python_file': 'Block_Families/StixORM/SCO/Email_Message/make_email_msg.py'
        }
    }
    
    extracted_dir = Path("test_output/extracted_objects")
    data_forms_dir = Path("test_data_forms_skipped")
    data_forms_dir.mkdir(exist_ok=True)
    
    results = []
    
    for obj_type, config in object_configs.items():
        print(f"\n📋 Processing {obj_type.upper()}")
        
        # Find extracted files for this type
        pattern = f"{obj_type}_*.json"
        extracted_files = list(extracted_dir.glob(pattern))
        
        if not extracted_files:
            print(f"   ❌ No extracted files found for {obj_type}")
            continue
        
        print(f"   📄 Found {len(extracted_files)} files")
        
        # Load template
        try:
            template = load_class_template(config['template_path'])
            print(f"   ✅ Template loaded: {config['template_path']}")
        except Exception as e:
            print(f"   ❌ Failed to load template: {e}")
            continue
        
        # Process each extracted file
        for extracted_file in extracted_files:
            try:
                # Load STIX object
                with open(extracted_file, 'r', encoding='utf-8') as f:
                    stix_obj = json.load(f)
                
                stix_type = stix_obj.get('type')
                
                # Convert to data form
                data_form = convert_stix_to_data_form(stix_obj, template)
                
                # Get form name
                form_name = get_typeql_name(stix_type)
                
                # Create complete form
                complete_form = {form_name: data_form}
                
                # Generate output filename
                base_name = extracted_file.stem.replace(f"{obj_type}_", "")
                output_filename = f"{config['python_class'].lower()}_{base_name}.json"
                output_path = data_forms_dir / output_filename
                
                # Save data form
                with open(output_path, 'w', encoding='utf-8') as f:
                    json.dump(complete_form, f, indent=2)
                
                print(f"   ✅ Created: {output_filename}")
                
                # Extract references
                references = {}
                for key, value in stix_obj.items():
                    if key.endswith('_ref') or key.endswith('_refs'):
                        references[key] = value
                
                # Record result
                result = {
                    'python_class': config['python_class'],
                    'stix_type': stix_type,
                    'example_file': str(extracted_file),
                    'template_path': config['template_path'],
                    'data_form_path': str(output_path),
                    'form_name': form_name,
                    'references': references,
                    'python_file': config['python_file'],
                    'original_stix': stix_obj,
                    'success': True
                }
                results.append(result)
                
            except Exception as e:
                print(f"   ❌ Error processing {extracted_file.name}: {e}")
                result = {
                    'python_class': config['python_class'],
                    'stix_type': obj_type.replace('_', '-'),
                    'example_file': str(extracted_file),
                    'template_path': config['template_path'],
                    'error': str(e),
                    'success': False
                }
                results.append(result)
    
    # Save results
    results_file = Path("test_output/skipped_data_form_results.json")
    with open(results_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2)
    
    # Summary
    successful = [r for r in results if r['success']]
    print(f"\n📊 SKIPPED DATA FORM CREATION SUMMARY:")
    print(f"   Total attempted: {len(results)}")
    print(f"   Successful: {len(successful)}")
    print(f"   Failed: {len(results) - len(successful)}")
    print(f"   Success rate: {len(successful)/len(results)*100:.1f}%")
    
    print(f"\n✅ Created data forms:")
    for result in successful:
        print(f"   • {result['python_class']} → {Path(result['data_form_path']).name}")
    
    print(f"\n💾 Results saved to: {results_file}")
    print(f"📁 Data forms directory: {data_forms_dir}")
    
    return results

if __name__ == "__main__":
    create_data_forms_for_skipped_objects()