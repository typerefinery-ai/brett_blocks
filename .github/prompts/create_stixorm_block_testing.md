# Refactor the Test Setup into two testing systems, Testing of StixORM and OS_Triage Blocks

All of the details to do with all testing, including scripts and generated files should be maintained in the `tests` directory.

## StixORM Testing

1. **Directory Structure**:
   - Cleaning of directories must be done before running tests, which requires emptying contents of data_forms, input_objects, and output_objects directories.
   - Directory structure should be:
      - `tests/stixorm/`: Contains all tests related to StixORM blocks
      - `tests/stixorm/fixtures/`: Contains any fixtures needed for testing StixORM blocks
      - `tests/stixorm/generated/data_forms/`: Contains generated data forms used for testing StixORM blocks
      - `tests/stixorm/generated/input_objects/`: Contains the input STIX objects used for generating the data forms for testing StixORM blocks
      - `tests/stixorm/generated/output_objects`: Contains the outputs of the StixORM blocks

2. **Testing Framework**:
   - Use `pytest` for all StixORM tests
   - Include a `conftest.py` file in the `tests/stixorm/` directory for shared fixtures

3. **Test Organization**:
   - Organize tests by feature or functionality
   - Use descriptive names for test files and test functions

4. **Test Input Data**:
   - Open all of the lists of stix objects from `Block_Families/StixORM/examples/` for use as a single input
   - Select those data objects where there is a make_object.py file in the same directory as the template
   - To decide this, first use the get_parse_content_for_objectfunction in Orchestration\Utilities\convert_object_list_to_data_forms.py to retrieve the ParseContent metadata for each object
   - Then the ParseContent  metadata is then used to create the object direcory path, so you can determine if the make_object.py file exists in the `object_path`. Essentially you only need to search for a *.py file in the `object_path` but ideally it should be named as shown in the variable `make_object_file` below:
   ```python
   metadata = get_parse_content_for_object(stix_obj)
   object_dir = metadata.python_class
   path_base = "Block_Families/StixORM"
   group_dir = metadata.group.upper()  # Convert to uppercase for directory structure
   object_path = Path(path_base) / group_dir / object_dir
   make_object_file = object_path / f"make_{metadata.typeql.replace("-", "_")}.py
   ```
   - Using this approach, you can filter the input STIX objects to only those that have a corresponding StixORM block for testing.

5. **Identical Test Sequence for Each Block**: 
   - For each StixORM block, follow this sequence:
    1. **Input Object Preparation**: Copy the STIX input objects into `tests/stixorm/generated/input_objects/`.
    2. **Data Form Generation**: Generate the corresponding data forms and store them in `tests/stixorm/generated/data_forms/`.
    3. **Block Sequence Reconstitution**: Reconstitute the input embedded references using the Orchestration\Utilities\reconstitute_object_list.py script to ensure all references are properly handled.
    4. **Output Verification**: Compare the output of the block against the expected output stored in `tests/stixorm/generated/output_objects/` using DeepDiff, ensuring you use the poetry system to find the current DeepDiff import.
    5. **Report**: Write a report on each block's test results, including any discrepancies found.


6. Write a summary report of all StixORM block tests, including pass/fail status for each block and any issues encountered.





## OS_Triage Blocks Testing

**TODO: Fill in the details for OS_Triage block testing similar to StixORM testing. Below is an embryonic structure, to be filled out at a later time, only setup the directories and prototype files. Do not create any code yet**

1. **Directory Structure**:
   - `tests/os_triage/`: Contains all tests related to OS_Triage blocks
   - `tests/os_triage/fixtures/`: Contains any fixtures needed for testing OS_Triage blocks

2. **Testing Framework**:
   - Use `pytest` for all OS_Triage tests
   - Include a `conftest.py` file in the `tests/os_triage/` directory for shared fixtures

3. **Test Organization**:
   - Organize tests by feature or functionality
   - Use descriptive names for test files and test functions
