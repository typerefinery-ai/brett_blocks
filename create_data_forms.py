#!/usr/bin/env python3
"""
Create data forms for matched target objects using the create-data-forms prompt methodology
"""

import json
from pathlib import Path
from typing import Dict, Any, List, Tuple

def load_matches():
    """Load the object-example matches"""
    matches_file = Path('c:/projects/brett_blocks/test_output/object_example_matches.json')
    with open(matches_file, 'r', encoding='utf-8') as f:
        return json.load(f)

def load_example_stix_object(example_path: str) -> Tuple[Dict[str, Any], int]:
    """Load STIX object from example file, returning object and its index"""
    with open(example_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Most examples are arrays, some may be single objects
    if isinstance(data, list):
        return data[0], 0  # Return first object and its index
    else:
        return data, 0

def load_class_template(template_path: str) -> Dict[str, Any]:
    """Load the class template"""
    with open(template_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def extract_references(stix_obj: Dict[str, Any]) -> List[str]:
    """Extract reference fields (_ref and _refs) from STIX object"""
    refs = []
    for key, value in stix_obj.items():
        if key.endswith('_ref') or key.endswith('_refs'):
            refs.append(key)
    return refs

def get_typeql_name(stix_type: str) -> str:
    """Convert STIX type to typeql form name using established mapping"""
    typeql_mapping = {
        'identity': 'identity_form',
        'indicator': 'indicator_form', 
        'incident': 'incident_form',
        'observed-data': 'observed_data_form',
        'email-addr': 'email_addr_form',
        'user-account': 'user_account_form',
        'url': 'url_form',
        'email-message': 'email_message_form',
        'impact': 'impact_form',
        'event': 'event_form',
        'sequence': 'sequence_form',
        'task': 'task_form',
        'anecdote': 'anecdote_form',
        'relationship': 'relationship_form',
        'sighting': 'sighting_form'
    }
    return typeql_mapping.get(stix_type, f"{stix_type.replace('-', '_')}_form")

def convert_stix_to_data_form(stix_obj: Dict[str, Any], template: Dict[str, Any]) -> Dict[str, Any]:
    """Convert STIX object to data form using the template"""
    
    # Get the class template (nested inside the outer structure)
    class_name = template['class_name']
    template_data = template[f"{class_name}_template"]
    
    # Determine if this is SDO or SCO based on required fields
    stix_type = stix_obj.get('type')
    is_sdo = 'created' in stix_obj or 'modified' in stix_obj
    
    # Create the data form structure
    data_form = {
        'base_required': {},
        'base_optional': {},
        'object': {},
        'extensions': {},
        'sub': {}
    }
    
    # Process base_required fields
    if 'base_required' in template_data:
        for field, definition in template_data['base_required'].items():
            if field in stix_obj:
                if field in ['id', 'created', 'modified']:
                    # Auto-generated fields get empty strings
                    data_form['base_required'][field] = ""
                else:
                    data_form['base_required'][field] = stix_obj[field]
            else:
                # Add default values for missing required fields
                if field == 'type':
                    data_form['base_required'][field] = stix_type
                elif field == 'spec_version':
                    data_form['base_required'][field] = "2.1"
                else:
                    data_form['base_required'][field] = ""
    
    # Process base_optional fields
    if 'base_optional' in template_data:
        for field, definition in template_data['base_optional'].items():
            if field in stix_obj:
                data_form['base_optional'][field] = stix_obj[field]
            else:
                # Add appropriate defaults for missing optional fields
                if 'collection' in definition and definition['collection'] == 'ListProperty':
                    data_form['base_optional'][field] = []
                elif 'property' in definition and definition['property'] == 'BooleanProperty':
                    data_form['base_optional'][field] = None
                else:
                    data_form['base_optional'][field] = None
    
    # Process object-specific fields
    if 'object' in template_data:
        for field, definition in template_data['object'].items():
            if field in stix_obj:
                data_form['object'][field] = stix_obj[field]
            else:
                # Handle missing object fields based on definition
                if 'collection' in definition and definition['collection'] == 'ListProperty':
                    data_form['object'][field] = []
                elif field.endswith('_ref') or field.endswith('_refs'):
                    # Reference fields get empty strings or empty lists
                    if field.endswith('_refs'):
                        data_form['object'][field] = []
                    else:
                        data_form['object'][field] = ""
                else:
                    data_form['object'][field] = ""
    
    # Process extensions (usually empty for basic objects)
    # Extensions would be populated if the STIX object has extension properties
    
    # Process sub-objects (embedded objects within the main object)
    # Sub-objects are typically empty for simple conversions
    
    return data_form

def create_data_forms():
    """Create data forms for all matched objects"""
    
    matches = load_matches()
    successful_matches = {k: v for k, v in matches.items() if v['example_file']}
    
    print("🏗️ CREATING DATA FORMS FROM MATCHED OBJECTS")
    print("=" * 55)
    
    results = []
    data_forms_dir = Path('c:/projects/brett_blocks/test_data_forms')
    data_forms_dir.mkdir(exist_ok=True)
    
    for python_class, match_data in successful_matches.items():
        target_obj = match_data['target_object']
        example_file = match_data['example_file']
        
        print(f"\n📋 Creating data form for {python_class}")
        print(f"   📄 Example: {Path(example_file).name}")
        print(f"   🔧 Template: {target_obj['template']}")
        
        try:
            # Load the STIX example
            stix_obj, obj_index = load_example_stix_object(example_file)
            stix_type = stix_obj.get('type')
            
            # Load the class template
            template_path = Path('c:/projects/brett_blocks') / target_obj['template']
            template = load_class_template(template_path)
            
            # Extract references
            references = extract_references(stix_obj)
            
            # Convert to data form
            data_form = convert_stix_to_data_form(stix_obj, template)
            
            # Get the proper form name
            form_name = get_typeql_name(stix_type)
            
            # Create the complete data form file
            complete_form = {form_name: data_form}
            
            # Generate a descriptive filename
            obj_name = stix_obj.get('name', stix_obj.get('value', stix_obj.get('id', 'unknown')))
            if isinstance(obj_name, str):
                safe_name = obj_name.replace(' ', '_').replace('/', '_').replace('\\', '_')[:30]
            else:
                safe_name = str(obj_name)[:30]
            
            filename = f"{python_class.lower()}_{safe_name}.json"
            output_path = data_forms_dir / filename
            
            # Save the data form
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(complete_form, f, indent=2)
            
            print(f"   ✅ Created: {output_path.name}")
            print(f"   📊 Form name: {form_name}")
            print(f"   🔗 References found: {len(references)} ({references})")
            
            # Record the result
            result = {
                'python_class': python_class,
                'stix_type': stix_type,
                'example_file': example_file,
                'template_path': str(template_path),
                'data_form_path': str(output_path),
                'form_name': form_name,
                'references': references,
                'python_file': target_obj['python'],
                'original_stix': stix_obj,
                'success': True
            }
            results.append(result)
            
        except Exception as e:
            print(f"   ❌ Error: {e}")
            result = {
                'python_class': python_class,
                'stix_type': target_obj['stix_type'],
                'example_file': example_file,
                'template_path': target_obj['template'],
                'error': str(e),
                'success': False
            }
            results.append(result)
    
    # Save the results
    results_file = Path('c:/projects/brett_blocks/test_output/data_form_creation_results.json')
    with open(results_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2)
    
    # Summary
    successful = [r for r in results if r['success']]
    print(f"\n📊 DATA FORM CREATION SUMMARY:")
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

def main():
    return create_data_forms()

if __name__ == "__main__":
    main()