"""
Find Embedded References in STIX Objects

This module provides functionality to parse STIX objects and extract all embedded 
references (STIX IDs) found in their properties, validating them against the STIX 2.1 
specification format: object-type--UUID (lowercase type, RFC 4122 UUID).
"""

from pydantic import BaseModel, field_validator, Field
from typing import List, Dict, Any, Union
import re
import uuid
import json


class EmbeddedReferences(BaseModel):
    """Collection of embedded STIX references grouped by property name."""
    
    references: Dict[str, List[str]] = Field(
        default_factory=dict,
        description="Property names mapped to lists of STIX IDs"
    )
    
    @field_validator('references')
    @classmethod
    def validate_stix_ids(cls, v: Dict[str, List[str]]) -> Dict[str, List[str]]:
        """Validate all STIX IDs in the references dictionary."""
        # STIX ID pattern: object-type--UUID (lowercase type, RFC 4122 UUID)
        stix_id_pattern = re.compile(
            r'^[a-z][a-z0-9-]*--[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$'
        )
        
        for prop_name, id_list in v.items():
            if not isinstance(id_list, list):
                raise ValueError(f'Property "{prop_name}" must map to a list of STIX IDs')
            
            for stix_id in id_list:
                if not isinstance(stix_id, str):
                    raise ValueError(f'STIX ID must be string, got {type(stix_id).__name__}: {stix_id}')
                
                if not stix_id_pattern.match(stix_id):
                    raise ValueError(
                        f'Invalid STIX ID in "{prop_name}": {stix_id}. '
                        'Must be object-type--UUID (lowercase, RFC 4122)'
                    )
                
                # Validate UUID portion
                try:
                    uuid_part = stix_id.split('--')[1]
                    uuid.UUID(uuid_part, version=4)
                except (IndexError, ValueError):
                    raise ValueError(f'Invalid UUID in STIX ID: {stix_id}')
        
        return v


def is_valid_stix_id(value: str) -> bool:
    """
    Check if a string is a valid STIX ID.
    
    Args:
        value: String to validate
        
    Returns:
        True if the value matches STIX ID format, False otherwise
    """
    if not isinstance(value, str):
        return False
    
    pattern = re.compile(
        r'^[a-z][a-z0-9-]*--[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$'
    )
    
    if not pattern.match(value):
        return False
    
    # Validate UUID portion
    try:
        uuid_part = value.split('--')[1]
        uuid.UUID(uuid_part, version=4)
        return True
    except (IndexError, ValueError):
        return False


def find_embedded_references(stix_object: Dict[str, Any]) -> EmbeddedReferences:
    """
    Parse a STIX object and extract all embedded references.
    
    This function recursively searches through all properties of a STIX object
    to find embedded references (STIX IDs). It identifies them by validating
    the format (object-type--UUID) rather than by property name, as reference
    properties can have various names (_ref, _refs, or custom names).
    
    Args:
        stix_object: Dictionary representing a STIX object
        
    Returns:
        EmbeddedReferences instance containing all found references grouped by property name
        
    Example:
        >>> obj = {
        ...     "id": "incident--123...",
        ...     "type": "incident",
        ...     "created_by_ref": "identity--456...",
        ...     "object_refs": ["indicator--789...", "malware--abc..."]
        ... }
        >>> refs = find_embedded_references(obj)
        >>> print(refs.references)
        {'created_by_ref': ['identity--456...'], 'object_refs': ['indicator--789...', 'malware--abc...']}
    """
    found_refs: Dict[str, List[str]] = {}
    
    def extract_refs_from_value(value: Any, property_path: str) -> None:
        """
        Recursively extract STIX IDs from a value.
        
        Args:
            value: The value to examine (could be str, list, dict, etc.)
            property_path: Dot-notation path to this property for tracking nested properties
        """
        # Extract only the final property name (after last dot)
        final_property_name = property_path.split('.')[-1] if property_path else property_path
        
        # Check if it's a single STIX ID string
        if isinstance(value, str):
            if is_valid_stix_id(value):
                if final_property_name not in found_refs:
                    found_refs[final_property_name] = []
                found_refs[final_property_name].append(value)
        
        # Check if it's a list of STIX IDs
        elif isinstance(value, list):
            for item in value:
                if isinstance(item, str) and is_valid_stix_id(item):
                    if final_property_name not in found_refs:
                        found_refs[final_property_name] = []
                    found_refs[final_property_name].append(item)
                # Recursively check nested objects/lists
                elif isinstance(item, (dict, list)):
                    extract_refs_from_value(item, property_path)
        
        # Check if it's a nested dictionary
        elif isinstance(value, dict):
            for nested_key, nested_value in value.items():
                nested_path = f"{property_path}.{nested_key}" if property_path else nested_key
                extract_refs_from_value(nested_value, nested_path)
    
    # Start extraction from root level (skip 'id' property as it's the object's own ID)
    for prop_name, prop_value in stix_object.items():
        if prop_name == 'id':
            continue
        extract_refs_from_value(prop_value, prop_name)
    
    # Create and return validated EmbeddedReferences instance
    return EmbeddedReferences(references=found_refs)


def main():
    """Test the find_embedded_references function with example data."""
    
    # Load example file
    example_file = r"Block_Families\General\_library\example_foreign_keys.json"
    
    try:
        with open(example_file, 'r', encoding='utf-8') as f:
            stix_objects = json.load(f)
        
        print(f"Loaded {len(stix_objects)} STIX objects from {example_file}\n")
        print("="*80)
        
        # Process each object
        for i, obj in enumerate(stix_objects, 1):
            obj_type = obj.get('type', 'unknown')
            obj_id = obj.get('id', 'no-id')
            
            print(f"\n{i}. Object: {obj_type}")
            print(f"   ID: {obj_id}")
            
            # Find embedded references
            refs = find_embedded_references(obj)
            
            if refs.references:
                print(f"   Found {sum(len(ids) for ids in refs.references.values())} embedded reference(s):")
                for prop_name, id_list in refs.references.items():
                    print(f"     - {prop_name}: {len(id_list)} reference(s)")
                    for ref_id in id_list:
                        ref_type = ref_id.split('--')[0]
                        print(f"         • {ref_type} → {ref_id}")
            else:
                print("   No embedded references found")
            
            print("-"*80)
        
        print("\n" + "="*80)
        print("Test completed successfully!")
        
    except FileNotFoundError:
        print(f"Error: Could not find file {example_file}")
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in file - {e}")
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
