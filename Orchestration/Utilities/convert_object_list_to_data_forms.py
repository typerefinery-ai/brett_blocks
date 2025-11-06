#!/usr/bin/env python3
"""
Convert Object List to Data Forms Utility

This utility refactors the data form creation logic from the notebook into a reusable 
Python function that can be called from anywhere in the codebase.

Based on the requirements from .github/prompts/convert-create-data-forms-notebook-to-python-utility.md
and the conversion logic in .github/prompts/create-data-forms.md
"""

import json
import copy
from pathlib import Path
from typing import Dict, List, Any, Optional
from collections import defaultdict


def get_stix_type_mapping():
    """Map STIX types to their expected directory structure"""
    
    # Load the inventory from the documentation
    inventory = {
        # SDO types (currently implemented)
        'identity': 'SDO/Identity',
        'indicator': 'SDO/Indicator', 
        'impact': 'SDO/Impact',
        'incident': 'SDO/Incident',
        'event': 'SDO/Event',
        'observed-data': 'SDO/Observed_Data',
        'sequence': 'SDO/Sequence',
        'task': 'SDO/Task',
        
        # SCO types (currently implemented)
        'anecdote': 'SCO/Anecdote',
        'email-addr': 'SCO/Email_Addr',
        'user-account': 'SCO/User_Account',
        'url': 'SCO/URL',
        'email-message': 'SCO/Email_Message',
        
        # SRO types (currently implemented)
        'relationship': 'SRO/Relationship',
        'sighting': 'SRO/Sighting',
        
        # Standard STIX 2.1 SDO types (templates exist)
        'attack-pattern': 'SDO/Attack_Pattern',
        'campaign': 'SDO/Campaign',
        'course-of-action': 'SDO/Course_of_Action',
        'grouping': 'SDO/Grouping',
        'infrastructure': 'SDO/Infrastructure',
        'intrusion-set': 'SDO/Instrusion_Set',
        'location': 'SDO/Location',
        'malware-analysis': 'SDO/Malware_Analysis',
        'note': 'SDO/Note',
        'opinion': 'SDO/Opinion',
        'report': 'SDO/Report',
        'threat-actor': 'SDO/Threat_Actor',
        'vulnerability': 'SDO/Vulnerability',
        
        # Standard STIX 2.1 SCO types (templates exist)
        'artifact': 'SCO/Artifact',
        'autonomous-system': 'SCO/Autonomous_System',
        'directory': 'SCO/Directory',
        'domain-name': 'SCO/Domain_Name',
        'file': 'SCO/File',
        'ipv4-addr': 'SCO/IPv4_Addr',
        'ipv6-addr': 'SCO/IPv6_Addr',
        'mac-addr': 'SCO/MAC_Address',
        'mutex': 'SCO/Mutex',
        'software': 'SCO/Software',
        'x509-certificate': 'SCO/X509_Cert'
    }
    
    return inventory


def discover_class_templates(stixorm_path: Path) -> Dict[str, Any]:
    """Discover all class templates in the StixORM directory structure"""
    templates = {}
    
    # Search SDO, SCO, and SRO directories
    for category in ['SDO', 'SCO', 'SRO']:
        category_path = stixorm_path / category
        if not category_path.exists():
            continue
            
        for obj_dir in category_path.iterdir():
            if not obj_dir.is_dir() or obj_dir.name.startswith('_'):
                continue
                
            # Look for template files
            for file in obj_dir.glob('*_template.json'):
                try:
                    with open(file, 'r', encoding='utf-8') as f:
                        template_data = json.load(f)
                    
                    class_name = template_data.get('class_name')
                    if class_name:
                        template_key = f"{class_name}_template"
                        if template_key in template_data:
                            stix_type = template_data[template_key].get('_type')
                            templates[stix_type] = {
                                'class_name': class_name,
                                'template_path': file,
                                'template_data': template_data,
                                'category': category,
                                'directory': obj_dir
                            }
                        
                except Exception as e:
                    continue
    
    return templates


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


def get_template_default(template_def: Any, field_name: str = "", section: str = "") -> Any:
    """Get appropriate default value for a template field definition"""
    if isinstance(template_def, dict):
        if 'collection' in template_def or template_def.get('collection'):
            return []
        else:
            # Use section-specific logic to match prompt method exactly
            if section == "base_optional":
                return None  # base_optional uses None for non-collections
            else:
                return ""  # object and other sections use empty strings
    else:
        # Handle direct value definitions
        if section == "base_optional":
            return None
        else:
            return ""


def extract_references_from_object(obj: Dict[str, Any], path: str = "") -> Dict[str, Any]:
    """
    Recursively extract reference fields from any part of a STIX object.
    
    This implements the critical reference extraction rules from create-data-forms.md:
    - Properties ending in `_ref`: Extract as separate parameter, leave empty string "" 
    - Properties ending in `_refs`: Extract as separate parameter, leave empty array []
    - All stix-id values: Extract as separate parameters
    """
    extracted_refs = {}
    
    def extract_from_dict(d: Dict[str, Any], current_path: str = ""):
        nonlocal extracted_refs
        keys_to_remove = []
        
        for key, value in d.items():
            field_path = f"{current_path}.{key}" if current_path else key
            
            # Rule 1: Fields ending in _ref or _refs
            if key.endswith('_ref') or key.endswith('_refs'):
                if value:  # Only extract if not empty
                    extracted_refs[field_path] = value
                    keys_to_remove.append(key)
            
            # Rule 2: Check for STIX ID patterns (type--uuid format)
            elif isinstance(value, str) and '--' in value and len(value.split('--')) == 2:
                # This looks like a STIX ID
                type_part, uuid_part = value.split('--', 1)
                if len(uuid_part) >= 36:  # UUID-like length
                    extracted_refs[field_path] = value
                    keys_to_remove.append(key)
            
            # Rule 3: Arrays of STIX IDs
            elif isinstance(value, list) and value:
                stix_ids = []
                for item in value:
                    if isinstance(item, str) and '--' in item and len(item.split('--')) == 2:
                        type_part, uuid_part = item.split('--', 1)
                        if len(uuid_part) >= 36:
                            stix_ids.append(item)
                
                if stix_ids:
                    extracted_refs[field_path] = stix_ids
                    keys_to_remove.append(key)
            
            # Rule 4: Recursively check nested objects and arrays
            elif isinstance(value, dict):
                extract_from_dict(value, field_path)
            elif isinstance(value, list):
                for i, item in enumerate(value):
                    if isinstance(item, dict):
                        extract_from_dict(item, f"{field_path}[{i}]")
        
        # Remove the extracted reference fields from the original object
        for key in keys_to_remove:
            if key.endswith('_refs'):
                d[key] = []  # Empty array for _refs fields
            else:
                d[key] = ""  # Empty string for _ref fields and STIX IDs
    
    # Create a deep copy to avoid modifying the original
    obj_copy = copy.deepcopy(obj)
    extract_from_dict(obj_copy)
    
    return extracted_refs, obj_copy


def convert_stix_to_data_form(stix_obj: Dict[str, Any], class_template: Dict[str, Any]) -> Dict[str, Any]:
    """
    Convert a STIX object to a data form using the class template as reference.
    
    This implements the conversion rules from .github/prompts/create-data-forms.md:
    - Structure preservation from template
    - Reference extraction (no embedded references in data forms)
    - Proper type handling and auto-generated field management
    - Extension and sub-object handling
    
    Args:
        stix_obj: The STIX JSON object to convert
        class_template: The corresponding class template
        
    Returns:
        Dict containing the data form and extracted references
    """
    
    # Get template data
    class_name = class_template['class_name']
    template_key = f"{class_name}_template"
    template_data = class_template[template_key]
    
    # Get the form name using established mapping
    stix_type = stix_obj.get('type')
    form_name = get_typeql_name(stix_type)
    
    # Extract all references first
    extracted_refs, cleaned_obj = extract_references_from_object(stix_obj)
    
    # Create the data form structure following template
    data_form = {
        'base_required': {},
        'base_optional': {},
        'object': {},
        'extensions': {},
        'sub': {}
    }
    
    # Auto-generated fields that should be empty strings
    auto_generated_fields = {'id', 'created', 'modified'}
    
    # Process base_required section
    if 'base_required' in template_data:
        for field, template_def in template_data['base_required'].items():
            if field in cleaned_obj:
                if field in auto_generated_fields:
                    data_form['base_required'][field] = ""
                elif field == 'type':
                    data_form['base_required'][field] = cleaned_obj[field]
                elif field == 'spec_version':
                    data_form['base_required'][field] = "2.1"
                else:
                    data_form['base_required'][field] = cleaned_obj[field]
            else:
                # Add defaults for missing required fields
                if field == 'type':
                    data_form['base_required'][field] = stix_type
                elif field == 'spec_version':
                    data_form['base_required'][field] = "2.1"
                elif field in auto_generated_fields:
                    data_form['base_required'][field] = ""
                else:
                    data_form['base_required'][field] = get_template_default(template_def, field, "base_required")
    
    # Process base_optional section
    if 'base_optional' in template_data:
        for field, template_def in template_data['base_optional'].items():
            if field in cleaned_obj:
                data_form['base_optional'][field] = cleaned_obj[field]
            else:
                data_form['base_optional'][field] = get_template_default(template_def, field, "base_optional")
    
    # Process object section
    if 'object' in template_data:
        for field, template_def in template_data['object'].items():
            if field in cleaned_obj:
                data_form['object'][field] = cleaned_obj[field]
            else:
                data_form['object'][field] = get_template_default(template_def, field, "object")
    
    # Process extensions section - only process extensions that exist in the STIX object
    if 'extensions' in template_data and 'extensions' in cleaned_obj:
        obj_extensions = cleaned_obj.get('extensions', {})
        
        for ext_id, ext_data in obj_extensions.items():
            processed_ext = {}
            
            # Extract references from extension first
            ext_refs, cleaned_ext = extract_references_from_object(ext_data)
            extracted_refs.update(ext_refs)
            
            # Process the cleaned extension data
            for key, value in cleaned_ext.items():
                if not isinstance(value, (dict, list)) or (isinstance(value, list) and not value):
                    processed_ext[key] = value
                elif isinstance(value, list) and value:
                    # Check if it's embedded objects - move to sub section
                    if isinstance(value[0], dict):
                        processed_ext[key] = []  # Empty array in extension
                        # Extract references from embedded objects before moving to sub
                        cleaned_sub_objects = []
                        for sub_obj in value:
                            sub_refs, cleaned_sub_obj = extract_references_from_object(sub_obj)
                            extracted_refs.update(sub_refs)
                            cleaned_sub_objects.append(cleaned_sub_obj)
                        # Move cleaned embedded objects to sub section
                        if 'sub' not in data_form:
                            data_form['sub'] = {}
                        data_form['sub'][key] = cleaned_sub_objects
                    else:
                        processed_ext[key] = value
                else:
                    processed_ext[key] = value
            
            data_form['extensions'][ext_id] = processed_ext
    
    # Process sub section (embedded objects) 
    # NOTE: Sub section should only contain actual embedded object data,
    # not template placeholders. Data comes from extensions processing or original STIX object.
    if 'sub' in cleaned_obj:
        obj_sub = cleaned_obj.get('sub', {})
        for key, value in obj_sub.items():
            # Remove any remaining references from sub-objects
            sub_refs, cleaned_sub = extract_references_from_object(value)
            extracted_refs.update(sub_refs)
            if 'sub' not in data_form:
                data_form['sub'] = {}
            data_form['sub'][key] = cleaned_sub
    
    # Create the result structure
    result = {
        form_name: data_form
    }
    
    if extracted_refs:
        result['extracted_references'] = extracted_refs
    
    return result


def create_data_forms_from_stix_objects(
    stix_objects: List[Dict],
    test_directory: Optional[str] = None
) -> Dict:
    """
    Create data forms from a list of STIX data objects using class templates.
    
    This function supports two modes of operation:
    
    Mode 1: Fill StixORM directory (test_directory=None):
        - Creates data forms from STIX objects
        - Saves them to appropriate StixORM directories based on object type  
        - Returns a report of created data forms
        
    Mode 2: Fill test directory (test_directory specified):
        - Creates data forms from STIX objects
        - Saves them to the specified test directory
        - Collects comprehensive documentation on extracted references
        - Returns report + reference documentation for reconstitution
        
    Args:
        stix_objects: List of STIX JSON objects to convert
        test_directory: Optional path to test directory for Mode 2
        
    Returns:
        Dict containing:
        - Mode 1: {'report': {...}, 'created_files': [...]}
        - Mode 2: {'report': {...}, 'created_files': [...], 'extracted_references': [...]}
        
    The function follows Brett Blocks template-driven architecture for proper
    handling of extensions, sub-objects, and reference extraction.
    """
    
    # Set up paths
    base_path = Path.cwd()
    if base_path.name == "Orchestration":
        base_path = base_path.parent
    
    stixorm_path = base_path / "Block_Families" / "StixORM"
    stix_type_mapping = get_stix_type_mapping()
    
    # Discover available templates
    available_templates = discover_class_templates(stixorm_path)
    
    # Initialize results
    results = {
        'report': {
            'total_objects': len(stix_objects),
            'processed': 0,
            'successful': 0,
            'failed': 0,
            'by_type': defaultdict(int),
            'errors': []
        },
        'created_files': []
    }
    
    # Mode 2: Add reference tracking
    if test_directory is not None:
        results['extracted_references'] = []
        # Create test directory if it doesn't exist
        test_path = Path(test_directory)
        test_path.mkdir(parents=True, exist_ok=True)
    
    # Process each STIX object
    for idx, stix_obj in enumerate(stix_objects):
        try:
            obj_type = stix_obj.get('type')
            obj_id = stix_obj.get('id', f'unknown_{idx}')
            
            results['report']['processed'] += 1
            results['report']['by_type'][obj_type] += 1
            
            # Check if we have a template for this type
            if obj_type not in available_templates:
                error_msg = f"No template available for type: {obj_type}"
                results['report']['errors'].append({
                    'object_id': obj_id,
                    'error': error_msg
                })
                results['report']['failed'] += 1
                continue
            
            # Get template
            template_info = available_templates[obj_type]
            template = template_info['template_data']
            
            # Convert to data form
            conversion_result = convert_stix_to_data_form(stix_obj, template)
            
            # Determine form name and data
            form_name = list(conversion_result.keys())[0]  # First key is the form name
            form_data = conversion_result[form_name]
            extracted_refs = conversion_result.get('extracted_references', {})
            
            # Generate filename
            obj_short_id = obj_id.split('--')[-1][:8] if '--' in obj_id else str(idx)
            filename = f"{obj_type}_{obj_short_id}_data_form.json"
            
            # Determine save path
            if test_directory is None:
                # Mode 1: Save to StixORM directory
                save_path = template_info['directory'] / filename
            else:
                # Mode 2: Save to test directory
                save_path = Path(test_directory) / filename
            
            # Save the data form
            save_data = {form_name: form_data}
            with open(save_path, 'w', encoding='utf-8') as f:
                json.dump(save_data, f, indent=2, ensure_ascii=False)
            
            results['created_files'].append({
                'object_id': obj_id,
                'object_type': obj_type,
                'filename': filename,
                'path': str(save_path),
                'form_name': form_name
            })
            
            # Mode 2: Track extracted references for reconstitution
            if test_directory is not None and extracted_refs:
                results['extracted_references'].append({
                    'object_id': obj_id,
                    'object_type': obj_type,
                    'object_index': idx,  # Preserve order for reconstitution
                    'filename': filename,
                    'form_name': form_name,
                    'extracted_references': extracted_refs,
                    'reference_fields': list(extracted_refs.keys())
                })
            
            results['report']['successful'] += 1
            
        except Exception as e:
            error_msg = f"Error processing object {obj_id}: {str(e)}"
            results['report']['errors'].append({
                'object_id': obj_id,
                'error': error_msg
            })
            results['report']['failed'] += 1
    
    # Add summary statistics
    results['report']['success_rate'] = (
        results['report']['successful'] / results['report']['total_objects'] * 100
        if results['report']['total_objects'] > 0 else 0
    )
    
    # Mode 2: Save comprehensive reference documentation
    if test_directory is not None and results['extracted_references']:
        reference_summary = {
            'total_objects': len(stix_objects),
            'objects_with_references': len(results['extracted_references']),
            'total_references': sum(len(item['extracted_references']) for item in results['extracted_references']),
            'by_type': defaultdict(int),
            'reference_patterns': defaultdict(int),
            'reconstitution_order': []
        }
        
        for ref_info in results['extracted_references']:
            reference_summary['by_type'][ref_info['object_type']] += 1
            reference_summary['reconstitution_order'].append({
                'index': ref_info['object_index'],
                'object_id': ref_info['object_id'],
                'object_type': ref_info['object_type'],
                'filename': ref_info['filename'],
                'form_name': ref_info['form_name'],
                'reference_count': len(ref_info['extracted_references'])
            })
            
            # Track reference patterns
            for ref_field in ref_info['reference_fields']:
                reference_summary['reference_patterns'][ref_field] += 1
        
        # Save reference summary
        summary_path = Path(test_directory) / "extracted_references_summary.json"
        with open(summary_path, 'w', encoding='utf-8') as f:
            json.dump(dict(reference_summary), f, indent=2, ensure_ascii=False)
    
    return results


if __name__ == "__main__":
    """
    Example usage of the utility function
    """
    # Example STIX objects for testing
    sample_objects = [
        {
            "type": "identity",
            "spec_version": "2.1",
            "id": "identity--example-uuid",
            "created": "2023-01-01T00:00:00.000Z",
            "modified": "2023-01-01T00:00:00.000Z",
            "name": "Example Identity",
            "identity_class": "individual"
        }
    ]
    
    # Test Mode 1: Save to StixORM directories
    print("Testing Mode 1: StixORM directory mode")
    result1 = create_data_forms_from_stix_objects(sample_objects)
    print(f"Mode 1 result: {result1['report']}")
    
    # Test Mode 2: Save to test directory with reference documentation
    print("\nTesting Mode 2: Test directory mode")
    result2 = create_data_forms_from_stix_objects(sample_objects, test_directory="test_output")
    print(f"Mode 2 result: {result2['report']}")