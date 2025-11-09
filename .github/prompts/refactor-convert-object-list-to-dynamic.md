# Refactor Convert Object List to Dynamic Decisions on Objects

I want you to use sequential-thinking to plan out the following refactoring taks. First prepare the detailed report, then once it is approved, proceed to implement the code changes.

## Background

Consider the module Orchestration\Utilities\convert_object_list_to_data_forms.py, and in particular its function that processes a list of STIX objects and converts them into corresponding data forms (create_data_forms_from_stix_objects).

The currrent implementation relies on two specific static lists where an object is simplistically checked by its stix type against pre-defined lists to get the key data needed to process it:
1. List 1: Converting between the object and its directory path - get_stix_type_mapping - line 20
2. List 2: Converting between the object and its data form key - get_typeql_name - line 117

Originally the names in the Block_Families\StixORM\SCO and Block_Families\StixORM\SDO directories were customised, and so we recently changed all of them so that they now match the Python class names exactly.

Thus, the current static records are now incorrect anyway. so the current code would not work as intended.

## Problem

The problem with the current approach is two-fold:
1. **Static Lists**: The use of hardcoded lists means that any addition of new object types requires manual updates to these lists, which is error-prone and not scalable.
2. **Uses Stix Type to Identify Objects**: The current method uses the Stix Type to identify objects, however the stix type is not unique, and only the Python class or TypeQL name can uniquely identify an object.


## Objective

We want to refactor the existing code that converts a list of objects into a set of data forms, from using static references for deciding about objects to a more dynamic approach that can handle various object types flexibly.

The updated approach is to use the determine_content_object_from_list_by_tests function from the Block_Families\General\_library\parse.py module to dynamically identify the object type based on tests of its properties and characteristics, rather than relying on static lists.

## Details

The determine_content_object_from_list_by_tests function takes a stix dict, and returns a ParseContent Oydantic class instance that contains detailed information about the object, including its TypeQL name and the information needed to determine its directory path.

### Directory Path Determination for Each Object

Now that the directory names match the Python class names, we can derive the directory path directly from the TypeQL name provided by the ParseContent instance. In essence, the directory path can be constructed as follows:
- Base Path:  `Block_Families\StixORM\`
- Object Group: ParseContent.group (SRO, Meta, SDO or SCO)
- Object Directory: ParseContent.python_class (which matches the class name)

### Data Form Key Determination for Each Object

The data form key can also be directly obtained from the ParseContent instance using the TypeQL name attribute. The data form key name is the same as the typeql name, except it swaps underscores for dashes. Following this key name is the term `_form` This eliminates the need for a separate static mapping, as the TypeQL name uniquely identifies the object type.

### Summary of Changes

By using the determine_content_object_from_list_by_tests function, we can refactor the convert_object_list_to_data_forms function to dynamically determine both the directory path and the data form key for each object based on its properties, rather than relying on static lists. This makes the code more flexible, maintainable, and scalable for future additions of new object types.

## Testing the Changes

Once the refactoring is complete, we will need to run comprehensive tests to ensure that the new dynamic approach correctly identifies and processes all existing object types, and that it can handle any new types added in the future without requiring further code changes. Use the existing testing system by running the temporary_reconstitution_testing\runner.py file