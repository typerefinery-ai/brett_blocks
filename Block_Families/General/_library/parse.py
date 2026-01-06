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
from typing import List, Dict, Union, Optional
import logging
import copy
import csv
import os
import re
import uuid
from embedded_references import EmbeddedReferences, find_embedded_references


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
        stix_dict (Dict[str, str]): The STIX dictionary object.
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
        stix_dict (Dict[str, str]): The STIX dictionary to check against.
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
        stix_dict (Dict[str, str]): The STIX dictionary to check against.
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

def test_object_by_condition(item: ParseContent, stix_dict: Dict[str, str]) -> bool:
    """
    Test the ParseContent condition against the STIX dictionary .

    Args:
        item (ParseContent): The ParseContent condition to test.
        stix_dict (Dict[str, str]): The STIX dictionary to match against.

    Returns:
        bool: True if the dict matches the conditions, False otherwise.
    """
    correct = False
    # Check each condition in the STIX dictionary
    if item.condition1 == "EXISTS":
        field_list = item.field1.split(".")
        correct = process_exists_condition(stix_dict, field_list)
    elif item.condition1 == "STARTS_WITH":
        correct = process_starts_with_condition(stix_dict, item.value1)
    elif item.condition1 == "EQUALS":
        field_list = item.field1.split(".")
        correct = process_equals_condition(stix_dict, field_list, item.value1)
    # Check the second condition if it exists
    if item.condition2 and correct:
        if item.condition2 == "EQUALS":
            field_list = item.field2.split(".")
            correct = process_equals_condition(stix_dict, field_list, item.value2)
    return correct

def determine_content_object_from_list_by_tests(stix_dict: Dict[str, str], content_type:str) -> ParseContent:
    """
    Determine the content object from the list by matching the STIX dictionary.

    Args:
        stix_dict (Dict[str, str]): The STIX dictionary to match against.
        content_type (str): The type of content to match against "class" or "icon".

    Returns:
        ParseContent: The matching ParseContent object, or None if not found.
    """
    content_list: List[ParseContent] = get_content_list_for_type(stix_dict.get("type"), content_type)
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
# Get the Stix Object Wrapper
#
####################################################################################################

# find_embedded_references

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

def make_description(content: ParseContent) -> str:
    """
    Make the description string for the Wrapper.

    Args:
        content (ParseContent): The ParseContent object.

    Returns:
        str: The generated description string with HTML breaks between lines.
    """
    description_parts = []
    for i in range(7):
        prior_string = getattr(content, f"prior_string{i}")
        post_field = getattr(content, f"post_field{i}")
        if prior_string and post_field:
            # Add HTML break before second and subsequent lines
            prefix = "<br>" if i > 0 else ""
            description_parts.append(f"{prefix}{prior_string}{post_field}")
    description = "".join(description_parts).strip()
    return description


def wrap_stix_dict(stix_dict: Dict[str, str]) -> Wrapper:
    """
    Generate the Wrapper for a given STIX dictionary object.

    Args:
        stix_dict (Dict[str, str]): The STIX dictionary object.
    
    Returns:
        Wrapper: The generated Wrapper object.
    """
    content = determine_content_object_from_list_by_tests(stix_dict, "class")
    if not content:
        raise ValueError(f"No content found for STIX type: {stix_dict.get('type')}")


    description = make_description(stix_dict, content)
    
    # Find embedded references
    embedded_refs = find_embedded_references(stix_dict)
    
    wrapped = Wrapper(
        id=stix_dict.get("id"),
        type=stix_dict.get("type"),
        icon=content.icon,
        name=stix_dict.get("name", ""),
        heading=content.head,
        description=description,
        object_form=content.form,
        object_group=content.group,
        object_family=content.protocol,
        original=stix_dict,
        references=embedded_refs
    )
    
    return wrapped



