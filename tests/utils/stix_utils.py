"""
STIX Utilities for Brett Blocks Testing
Provides utilities for working with STIX objects and conversions
"""

import json
import uuid
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple
from deepdiff import DeepDiff


def load_stix_object(file_path: str) -> Tuple[Dict[str, Any], int]:
    """
    Load a STIX object from a JSON file
    
    Args:
        file_path: Path to the JSON file
        
    Returns:
        Tuple of (stix_object, object_index)
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    if isinstance(data, list):
        return data[0], 0
    else:
        return data, 0


def extract_stix_references(stix_obj: Dict[str, Any]) -> Dict[str, Any]:
    """
    Extract reference fields from a STIX object
    
    Args:
        stix_obj: The STIX object to analyze
        
    Returns:
        Dictionary of reference field names and their values
    """
    refs = {}
    for key, value in stix_obj.items():
        if key.endswith('_ref') or key.endswith('_refs'):
            refs[key] = value
    return refs


def normalize_stix_for_comparison(stix_obj: Dict[str, Any]) -> Dict[str, Any]:
    """
    Normalize a STIX object for comparison by removing/standardizing variable fields
    
    Args:
        stix_obj: The STIX object to normalize
        
    Returns:
        Normalized STIX object
    """
    normalized = stix_obj.copy()
    
    # Remove or normalize fields that vary between instances
    if 'id' in normalized:
        # Keep the type part, replace the UUID part with a placeholder
        stix_type = normalized['id'].split('--')[0]
        normalized['id'] = f"{stix_type}--00000000-0000-0000-0000-000000000000"
    
    # Remove timestamp fields that will differ
    for time_field in ['created', 'modified']:
        if time_field in normalized:
            del normalized[time_field]
    
    return normalized


def compare_stix_objects(original: Dict[str, Any], generated: Dict[str, Any], 
                        ignore_paths: Optional[List[str]] = None) -> Dict[str, Any]:
    """
    Compare two STIX objects using DeepDiff, ignoring UUID differences
    
    Args:
        original: The original STIX object
        generated: The generated STIX object
        ignore_paths: Additional paths to ignore in comparison
        
    Returns:
        DeepDiff result dictionary
    """
    # Default paths to ignore (UUIDs and timestamps)
    default_ignore = [
        "root['id']",
        "root['created']", 
        "root['modified']"
    ]
    
    if ignore_paths:
        default_ignore.extend(ignore_paths)
    
    # Perform the comparison
    diff = DeepDiff(
        original, 
        generated,
        ignore_order=True,
        exclude_paths=default_ignore,
        verbose_level=2
    )
    
    return diff


def get_stix_type_mapping() -> Dict[str, str]:
    """
    Get the mapping from STIX types to typeql form names
    
    Returns:
        Dictionary mapping STIX types to form names
    """
    return {
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


def is_stix_equivalent(original: Dict[str, Any], generated: Dict[str, Any]) -> bool:
    """
    Check if two STIX objects are equivalent (ignoring UUIDs and timestamps)
    
    Args:
        original: The original STIX object
        generated: The generated STIX object
        
    Returns:
        True if objects are equivalent, False otherwise
    """
    diff = compare_stix_objects(original, generated)
    
    # Objects are equivalent if there are no significant differences
    # We only care about changes in values, not additions/removals of UUID fields
    significant_changes = [
        'values_changed',
        'type_changes',
        'iterable_item_added',
        'iterable_item_removed'
    ]
    
    for change_type in significant_changes:
        if change_type in diff and diff[change_type]:
            # Filter out UUID-related changes
            filtered_changes = {}
            for path, change in diff[change_type].items():
                if not any(uuid_field in path for uuid_field in ['id', 'created', 'modified']):
                    filtered_changes[path] = change
            
            if filtered_changes:
                return False
    
    return True


def generate_test_stix_id(stix_type: str) -> str:
    """
    Generate a test STIX ID with a predictable UUID
    
    Args:
        stix_type: The STIX object type
        
    Returns:
        Test STIX ID string
    """
    test_uuid = str(uuid.uuid4())
    return f"{stix_type}--{test_uuid}"


def validate_stix_object(stix_obj: Dict[str, Any]) -> List[str]:
    """
    Validate a STIX object for required fields and structure
    
    Args:
        stix_obj: The STIX object to validate
        
    Returns:
        List of validation errors (empty if valid)
    """
    errors = []
    
    # Check required fields
    required_fields = ['type', 'spec_version', 'id']
    for field in required_fields:
        if field not in stix_obj:
            errors.append(f"Missing required field: {field}")
    
    # Check spec_version
    if 'spec_version' in stix_obj and stix_obj['spec_version'] != '2.1':
        errors.append(f"Invalid spec_version: {stix_obj['spec_version']} (expected 2.1)")
    
    # Check ID format
    if 'id' in stix_obj:
        id_parts = stix_obj['id'].split('--')
        if len(id_parts) != 2:
            errors.append(f"Invalid ID format: {stix_obj['id']}")
        elif id_parts[0] != stix_obj.get('type'):
            errors.append(f"ID type mismatch: {id_parts[0]} != {stix_obj.get('type')}")
    
    return errors