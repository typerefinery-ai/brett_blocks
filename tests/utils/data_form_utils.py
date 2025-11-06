"""
Data Form Utilities for Brett Blocks Testing
Extends the existing Orchestration utilities for comprehensive testing
"""

import json
import sys
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple

# Add the project root to Python path for imports
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

# Import existing Orchestration utilities
from Orchestration.conv import conv
from Orchestration.Utilities.util import emulate_ports, unwind_ports


def load_data_form(file_path: str) -> Tuple[str, Dict[str, Any]]:
    """
    Load a data form from a JSON file
    
    Args:
        file_path: Path to the data form JSON file
        
    Returns:
        Tuple of (form_name, form_data)
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Data forms have a single root key which is the form name
    form_name = list(data.keys())[0]
    form_data = data[form_name]
    
    return form_name, form_data


def load_class_template(template_path: str) -> Dict[str, Any]:
    """
    Load a class template from a JSON file
    
    Args:
        template_path: Path to the template file
        
    Returns:
        Template data dictionary
    """
    with open(template_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def validate_data_form_structure(form_data: Dict[str, Any]) -> List[str]:
    """
    Validate that a data form has the expected structure
    
    Args:
        form_data: The data form to validate
        
    Returns:
        List of validation errors (empty if valid)
    """
    errors = []
    
    # Check required sections
    required_sections = ['base_required', 'base_optional', 'object', 'extensions', 'sub']
    for section in required_sections:
        if section not in form_data:
            errors.append(f"Missing required section: {section}")
    
    # Check that base_required has essential fields
    if 'base_required' in form_data:
        base_req = form_data['base_required']
        essential_fields = ['type', 'spec_version', 'id']
        for field in essential_fields:
            if field not in base_req:
                errors.append(f"Missing essential field in base_required: {field}")
    
    return errors


def extract_data_form_references(form_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Extract reference fields from a data form
    
    Args:
        form_data: The data form to analyze
        
    Returns:
        Dictionary of reference field names and their values
    """
    refs = {}
    
    # Check all sections for reference fields
    for section_name, section_data in form_data.items():
        if isinstance(section_data, dict):
            for key, value in section_data.items():
                if key.endswith('_ref') or key.endswith('_refs'):
                    refs[key] = value
    
    return refs


def convert_data_form_to_stix_input(form_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Convert a data form back to STIX-like structure for object creation
    
    Args:
        form_data: The data form to convert
        
    Returns:
        STIX-like object dictionary
    """
    stix_obj = {}
    
    # Combine all sections into a single object
    for section_name, section_data in form_data.items():
        if isinstance(section_data, dict):
            stix_obj.update(section_data)
    
    return stix_obj


def get_python_module_path(python_file_path: str) -> str:
    """
    Convert a file path to a Python module path for importing
    
    Args:
        python_file_path: File system path to the Python file
        
    Returns:
        Python module path string
    """
    # Convert Block_Families/StixORM/SDO/Identity/make_identity.py
    # to Block_Families.StixORM.SDO.Identity.make_identity
    
    path = Path(python_file_path)
    
    # Remove .py extension
    module_parts = path.with_suffix('').parts
    
    # Join with dots
    return '.'.join(module_parts)


def import_make_function(python_file_path: str):
    """
    Dynamically import the main function from a make_object.py file
    
    Args:
        python_file_path: Path to the Python file containing the make function
        
    Returns:
        The main function from the module
    """
    import importlib.util
    import importlib
    
    try:
        # Try module import first
        module_path = get_python_module_path(python_file_path)
        module = importlib.import_module(module_path)
        
        # Look for the main function (usually called 'main')
        if hasattr(module, 'main'):
            return module.main
        else:
            # Look for other potential function names
            for attr_name in dir(module):
                if not attr_name.startswith('_') and callable(getattr(module, attr_name)):
                    attr = getattr(module, attr_name)
                    if hasattr(attr, '__code__') and attr.__code__.co_argcount > 0:
                        return attr
        
        raise AttributeError(f"No suitable function found in {module_path}")
        
    except ImportError:
        # Try direct file import
        full_path = project_root / python_file_path
        spec = importlib.util.spec_from_file_location("make_module", full_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        
        if hasattr(module, 'main'):
            return module.main
        else:
            raise AttributeError(f"No main function found in {python_file_path}")


def create_dependency_order(test_objects: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Order test objects based on their dependencies (references)
    
    Args:
        test_objects: List of test object configurations
        
    Returns:
        Ordered list of test objects
    """
    # Simple ordering: put objects with no references first
    no_refs = []
    has_refs = []
    
    for obj in test_objects:
        if 'references' in obj and obj['references']:
            has_refs.append(obj)
        else:
            no_refs.append(obj)
    
    # Return objects with no references first, then objects with references
    return no_refs + has_refs


def generate_test_inputs_for_references(refs: Dict[str, Any], available_objects: Dict[str, Dict[str, Any]]) -> Dict[str, Any]:
    """
    Generate test input objects for satisfying reference dependencies
    
    Args:
        refs: Dictionary of reference fields and their types
        available_objects: Dictionary of available created objects by type
        
    Returns:
        Dictionary of input objects to satisfy references
    """
    inputs = {}
    
    for ref_field, ref_value in refs.items():
        if ref_field.endswith('_ref'):
            # Single reference
            if ref_value and ref_value != "":
                ref_type = ref_value.split('--')[0] if '--' in ref_value else ref_value
                if ref_type in available_objects:
                    inputs[ref_field] = available_objects[ref_type]
        elif ref_field.endswith('_refs'):
            # Multiple references
            if ref_value and isinstance(ref_value, list) and ref_value:
                ref_objects = []
                for ref_id in ref_value:
                    if ref_id and '--' in ref_id:
                        ref_type = ref_id.split('--')[0]
                        if ref_type in available_objects:
                            ref_objects.append(available_objects[ref_type])
                if ref_objects:
                    inputs[ref_field] = ref_objects
    
    return inputs