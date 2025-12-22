"""
1. Parse STIX object metadata from icon_registry.csv. 
2. Analyses objects for Visualisation and generate the wrapper using the parser

This module reads the CSV registry containing STIX object metadata including:
- Object identification (stix_type, protocol, group)
- Python class mapping
- Condition testing fields (condition1/2, field1/2, value1/2)
- Display formatting fields (icon, form, head, prior_string/post_field pairs)
"""

from pydantic import  BaseModel, field_validator, Field
from typing import List, Dict, Union, Optional, Any
import logging
import copy
import csv
import os
import re
import uuid
import json


logger = logging.getLogger(__name__)


class ParseContent(BaseModel):
	"""
	ParseContent is a Pydantic model that represents the ORM content used for parsing.
	Reads from icon_registry.csv with 27 columns including display formatting fields.
	"""
	# Core identification fields
	stix_type: str
	protocol: str
	group: str
	python_class: str
	typeql: str
	
	# Condition testing fields
	condition1: Optional[str] = ""
	field1: Optional[str] = ""
	value1: Optional[str] = ""
	condition2: Optional[str] = ""
	field2: Optional[str] = ""
	value2: Optional[str] = ""
	
	# Display metadata fields
	icon: Optional[str] = ""
	form: Optional[str] = ""
	head: Optional[str] = ""
	
	# Display formatting fields (prior_string/post_field pairs)
	prior_string0: Optional[str] = ""
	post_field0: Optional[str] = ""
	prior_string1: Optional[str] = ""
	post_field1: Optional[str] = ""
	prior_string2: Optional[str] = ""
	post_field2: Optional[str] = ""
	prior_string3: Optional[str] = ""
	post_field3: Optional[str] = ""
	prior_string4: Optional[str] = ""
	post_field4: Optional[str] = ""
	prior_string5: Optional[str] = ""
	post_field5: Optional[str] = ""
	prior_string6: Optional[str] = ""
	post_field6: Optional[str] = ""

	def __str__(self):
		return f"ParseContent(stix_type={self.stix_type}, protocol={self.protocol}, group={self.group}, python_class={self.python_class}, typeql={self.typeql}, condition1={self.condition1}, field1={self.field1}, value1={self.value1}, condition2={self.condition2}, field2={self.field2}, value2={self.value2})"
	

def read_icon_registry() -> List[Dict]:
    """
    Read icon_registry.csv from the same directory as this module.
    
    Returns:
        List[Dict]: List of dictionaries with registry data, or empty list if file not found.
    """
    try:
        # Get the directory of the current file
        current_dir = os.path.dirname(os.path.abspath(__file__))
        # Construct the path to the icon_registry.csv file
        file_path = os.path.join(current_dir, "icon_registry.csv")
        
        if not os.path.exists(file_path):
            logger.error(f"icon_registry.csv file not found at {file_path}")
            return []
        
        result = []
        # Try different encodings to handle potential non-UTF-8 characters
        encodings = ['utf-8-sig', 'utf-8', 'latin-1', 'cp1252']
        
        for encoding in encodings:
            try:
                with open(file_path, 'r', encoding=encoding, errors='ignore') as f:
                    reader = csv.DictReader(f)
                    
                    for row_num, row in enumerate(reader, start=2):  # Start at 2 (after header)
                        # Rename 'class' to 'python_class' to avoid Python reserved keyword
                        if 'class' in row:
                            row['python_class'] = row.pop('class')
                        
                        result.append(row)
                
                logger.debug(f"Successfully loaded {len(result)} entries from icon_registry.csv using {encoding} encoding")
                return result
                
            except Exception as e:
                logger.debug(f"Failed to read with {encoding}: {e}")
                continue
        
        logger.error(f"Could not read {file_path} with any encoding")
        return []
        
    except Exception as e:
        logger.error(f"Error reading icon_registry.csv file: {e}")
        return []




###################################################################################
#
# Base - Get Content Record from List Based on Dict Loop
#
###################################################################################

def get_content_list_for_type(type: str, content_type: str) -> List[ParseContent]:
    """
    Get the list of ParseContent models for a specific type from the class registry.
    
    Args:
        type (str): The STIX type to filter by.
        content_type (str): The type of content to retrieve ("class" is currently supported).
    
    Returns:
        List[ParseContent]: List of ParseContent models matching the type, or empty list if none found.
    """
    if content_type != "class":
        logger.warning(f"Content type '{content_type}' is not supported. Only 'class' is currently supported.")
        return []
    
    try:
        # Read the icon registry data
        registry_data = read_icon_registry()
        
        # Filter by the specified type and convert to ParseContent models
        filtered_data = [item for item in registry_data if item.get("stix_type") == type]
        
        # Convert dictionaries to ParseContent models
        parse_content_list = []
        for item in filtered_data:
            try:
                parse_content_list.append(ParseContent(**item))
            except Exception as e:
                logger.error(f"Error creating ParseContent from item {item}: {e}")
                continue
        
        logger.debug(f"Found {len(parse_content_list)} ParseContent entries for type '{type}'")
        return parse_content_list
        
    except Exception as e:
        logger.error(f"Error getting content list for type '{type}': {e}")
        return []

def process_exists_condition(stix_dict, field_list):
    """
    Process the EXISTS condition for the given field list.

    Args:
        stix_dict (Dict[str, Any]): The STIX dictionary object.
        field_list (List[str]): The list of fields to check for existence.

    Returns:
        bool: True if all fields exist in the STIX dictionary, False otherwise.
    """
    local_dict = copy.deepcopy(stix_dict)
    correct = False
    length = len(field_list)
    for i, field in enumerate(field_list):
        if length == i+1:
            if field in local_dict:
                correct = True
                return correct
            else:
                correct = False
                return correct
        else:
            if field in local_dict:
                local_dict = local_dict[field]
            else:
                correct = False
                return correct

def process_starts_with_condition(stix_dict, value):
    """
    Process the STARTS_WITH condition for the given field list.

    Args:
        stix_dict (Dict[str, Any]): The STIX dictionary to check against.
        field_list (List[str]): The list of fields to check for existence.
        value (str): The value to check for.

    Returns:
        bool: True if it is not an attack object, and any field starts with the given value, False otherwise.
    """
    correct = False
    local_dict = copy.deepcopy(stix_dict)
    if "x_mitre_attack_spec_version" in local_dict:
        return correct
    for field_name, field_value in local_dict.items():
        if isinstance(field_name, str) and field_name.startswith(value):
            correct = True
            return correct
    return correct

def process_equals_condition(stix_dict, field_list, value):
    """
    Process the EQUALS condition for the given field and value.

    Args:
        stix_dict (Dict[str, Any]): The STIX dictionary to check against.
        field (str): The field to check for equality.
        value (str): The value to check against.

    Returns:
        bool: True if the field exists and it equals the value, False otherwise.
    """
    local_dict = copy.deepcopy(stix_dict)
    correct = False
    length = len(field_list)
    for i, field in enumerate(field_list):
        if length == i+1:
            if field in local_dict:
                if local_dict[field] == value:
                    correct = True
                    return correct
        else:
            if field in local_dict:
                local_dict = local_dict[field]
    return correct

def test_object_by_condition(item: ParseContent, stix_dict: Dict[str, Any]) -> bool:
    """
    Test the ParseContent condition against the STIX dictionary .

    Args:
        item (ParseContent): The ParseContent condition to test.
        stix_dict (Dict[str, Any]): The STIX dictionary to match against.

    Returns:
        bool: True if the dict matches the conditions, False otherwise.
    """
    correct = False
    # Check each condition in the STIX dictionary
    if item.condition1 == "EXISTS" and item.field1:
        field_list = item.field1.split(".")
        correct = process_exists_condition(stix_dict, field_list)
    elif item.condition1 == "STARTS_WITH" and item.value1:
        correct = process_starts_with_condition(stix_dict, item.value1)
    elif item.condition1 == "EQUALS" and item.field1 and item.value1:
        field_list = item.field1.split(".")
        correct = process_equals_condition(stix_dict, field_list, item.value1)
    # Check the second condition if it exists
    if item.condition2 and correct:
        if item.condition2 == "EQUALS" and item.field2 and item.value2:
            field_list = item.field2.split(".")
            correct = process_equals_condition(stix_dict, field_list, item.value2)
    return bool(correct)

def determine_content_object_from_list_by_tests(stix_dict: Dict[str, Any], content_type:str) -> Optional[ParseContent]:
    """
    Determine the content object from the list by matching the STIX dictionary.

    Args:
        stix_dict (Dict[str, Any]): The STIX dictionary to match against.
        content_type (str): The type of content to match against "class" or "icon".

    Returns:
        ParseContent: The matching ParseContent object, or None if not found.
    """
    content_list: List[ParseContent] = get_content_list_for_type(stix_dict.get("type", ""), content_type)
    if not content_list:
        return None
    elif len(content_list) == 1:
        return content_list[0]
    else:
        correct = False
        # Split the list
        default = [item for item in content_list if item.condition1 == ""]
        specialisation = [item for item in content_list if item.condition1 != ""]
        # First check the specialisation list for test matches
        for item in specialisation:
            correct = test_object_by_condition(item, stix_dict)
            if correct:
                return item

        # Else return the default, or worst case the first in the specialisation list
        return default[0] if default else specialisation[0]
    

###################################################################################################
#
# Specific - Get TQL Name from Content by Type and Protocol
#
####################################################################################################

def get_tqlname_from_type_and_protocol(stix_type, protocol=None) -> Union[str, None]:
    """
    Get the TypeQL name from the type and protocol.

    Args:
        stix_type (str): The type of the object.
        protocol (str): The protocol to use.

    Returns:
        tql_name (str): The TypeQL name of the object.
    """
    content_list: List[ParseContent] = get_content_list_for_type(stix_type, "class")
    if not content_list:
        return None
    elif len(content_list) == 1:
        content = content_list[0]
        return content.typeql
    else:
        # find the default option, with the empty condition
        for item in content_list:
            if item.condition1 == "":
                return item.typeql
    return content_list[0].typeql

def get_group_from_type(stix_type) -> Union[str, None]:
    """
    Get the group from the type.

    Args:
        stix_type (str): The type of the object.

    Returns:
        group (str): The Stix group of the object.
    """
    content_list: List[ParseContent] = get_content_list_for_type(stix_type, "class")
    if not content_list:
        return None
    elif len(content_list) == 1:
        content = content_list[0]
        return content.group
    else:
        # find the default option, with the empty condition
        for item in content_list:
            if item.condition1 == "":
                return item.group
    return content_list[0].group


    
###################################################################################################
#
# Find the Embedded References
#
####################################################################################################

# find_embedded_references


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
    
    def to_json_dict(self) -> Dict[str, List[str]]:
        """
        Convert the EmbeddedReferences to a JSON-serializable dictionary.
        
        Returns:
            Dict[str, List[str]]: The references dictionary ready for json.dumps()
        """
        return self.references


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

    
###################################################################################################
#
# Get the Stix Object Wrapper
#
####################################################################################################

# wrap the object

class Wrapper(BaseModel):
    """
    Wrapper model to hold the Generated Details and EmbeddedReferences for a STIX object.
    """
    id: str
    type: str
    icon: str
    name: str
    heading: str
    description: str
    object_form: str
    object_group: str
    object_family: str
    original: Dict[str, Union[str, List, Dict]] = Field(default_factory=dict)
    references: EmbeddedReferences

def parse_path_part(part: str) -> Optional[tuple[Optional[str], Optional[int]]]:
    """
    Parse a path segment to extract either a field name or a list index.
    
    ONLY supports Format 2 notation:
    - Plain field names: "field_name" → ("field_name", None)
    - Separate index notation: "[0]" → (None, 0)
    
    Invalid formats (returns None and logs error):
    - Attached index: "field[0]", "[0]field"
    - Empty brackets: "[]"
    - Non-numeric index: "[abc]"
    
    Args:
        part: A single path segment after splitting by "."
        
    Returns:
        Tuple of (field_name, index) or None if invalid format
        - (field_name, None) for plain field
        - (None, index) for list index
        - None for invalid format
    """
    # Check for standalone bracket notation: [N]
    standalone_index_pattern = re.compile(r'^\[(\d+)\]$')
    match = standalone_index_pattern.match(part)
    
    if match:
        # Valid standalone index like [0], [1], etc.
        index = int(match.group(1))
        return (None, index)
    
    # Check for invalid patterns with brackets
    if '[' in part or ']' in part:
        # Invalid: field[0], [0]field, [], [abc], etc.
        logger.warning(f"Invalid path notation '{part}'. Only standalone bracket notation like '[0]' is supported. "
                      f"Use format: 'field.[0].subfield' not 'field[0].subfield'")
        return None
    
    # Plain field name (no brackets)
    return (part, None)

def get_nested_value(stix_dict: Dict[str, Any], field_path: str) -> Any:
    """
    Extract a value from a nested dictionary using dot notation with optional list indexing.
    
    Supports Format 2 notation only:
    - Dictionary access: "extensions.availability.availability_impact"
    - List indexing (separate): "external_references.[0].external_id"
    - Nested lists: "extensions.ext.[0].field.[1].value"
    
    Invalid formats (returns None):
    - Attached indices: "field[0]" or "tags[2]"
    - Index before field: "[0]field"
    - Empty brackets: "[]"
    - Non-numeric indices: "[abc]"
    
    Args:
        stix_dict: The STIX dictionary to extract from
        field_path: Dot-separated path (e.g., "external_references.[0].external_id")
    
    Returns:
        The value at the specified path, or None if path doesn't exist or is invalid
    
    Examples:
        >>> get_nested_value({"name": "test"}, "name")
        "test"
        >>> get_nested_value({"extensions": {"availability": {"availability_impact": 99}}}, 
        ...                  "extensions.availability.availability_impact")
        99
        >>> get_nested_value({"external_references": [{"external_id": "CVE-2021-1234"}]}, 
        ...                  "external_references.[0].external_id")
        "CVE-2021-1234"
        >>> get_nested_value({"tags": ["malware", "trojan"]}, "tags.[1]")
        "trojan"
    """
    if not field_path:
        return None
    
    # Split the path into parts
    field_parts = field_path.split(".")
    current_value = stix_dict
    
    # Traverse the nested structure
    for part in field_parts:
        # Parse the part to get field name and/or index
        parsed = parse_path_part(part)
        
        if parsed is None:
            # Invalid format detected
            return None
        
        field_name, index = parsed
        
        # Handle field access (dictionary key)
        if field_name is not None:
            if isinstance(current_value, dict) and field_name in current_value:
                current_value = current_value[field_name]
            else:
                return None
        
        # Handle list index access
        if index is not None:
            if isinstance(current_value, list) and 0 <= index < len(current_value):
                current_value = current_value[index]
            else:
                return None
    
    return current_value

def make_description(stix_dict: Dict[str, Union[str, Dict, List]], content: ParseContent) -> str:
    """
    Make the description string for the Wrapper.

    Args:
        stix_dict: The STIX dictionary object
        content (ParseContent): The ParseContent object.

    Returns:
        str: The generated description string with HTML breaks between lines.
    """
    description_parts = []
    j = 0
    for i in range(7):
        prior_string = getattr(content, f"prior_string{i}")
        post_field = getattr(content, f"post_field{i}")
        
        # Handle both simple keys and dot-notation paths
        if "." in post_field:
            post_value = get_nested_value(stix_dict, post_field)
        else:
            post_value = stix_dict.get(post_field)
        
        # Only add to description if both prior_string and post_value exist and are not empty
        if prior_string and post_value not in (None, "", {}):
            # Add HTML break before second and subsequent lines
            prefix = "<br>" if j > 0 else ""
            description_parts.append(f"{prefix}{prior_string}{post_value}")
            j += 1
    description = "".join(description_parts).strip()
    return description


def wrap_stix_dict(stix_dict: Dict[str, Union[str, Dict, List]]) -> Dict[str, Union[str, Dict, List]]:
    """
    Generate the Wrapper for a given STIX dictionary object.

    Args:
        stix_dict (Dict[str, str]): The STIX dictionary object.
    
    Returns:
        Wrapper: The generated Wrapper object, as a dict.
    """
    content = determine_content_object_from_list_by_tests(stix_dict, "class")
    if not content:
        raise ValueError(f"No content found for STIX type: {stix_dict.get('type', '')}")


    description = make_description(stix_dict, content)
    
    # Find embedded references
    embedded_refs: EmbeddedReferences = find_embedded_references(stix_dict)
    
    # wrapped = Wrapper(
    #     id=stix_dict.get("id"),
    #     type=stix_dict.get("type"),
    #     icon=content.icon,
    #     name=stix_dict.get("name", ""),
    #     heading=content.head,
    #     description=description,
    #     object_form=content.form,
    #     object_group=content.group,
    #     object_family=content.protocol,
    #     original=stix_dict,
    #     references=embedded_refs
    # )

    wrap = {}
    wrap["id"] = stix_dict.get("id")
    wrap["type"] = stix_dict.get("type")
    wrap["icon"] = content.icon
    wrap["name"] = stix_dict.get(content.post_field0, "")
    wrap["heading"] = content.head
    wrap["description"] = description
    wrap["object_form"] = content.form
    wrap["object_group"] = content.group
    wrap["object_family"] = content.protocol
    wrap["original"] = stix_dict
    wrap["references"] = embedded_refs.to_json_dict()

    return wrap



