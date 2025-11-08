# Refactor the Test Setup into two testing systems, Testing of StixORM and OS_Triage Blocks

All of the details to do with all testing, including scripts and generated files should be maintained in the `tests` directory.

## StixORM Testing

1. **Directory Structure**:
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
   - Open all directories using 
   - Only use data objects where there is a make_object.py file in the same directory as the template

5. **Identical Test Sequence for Each Block**: 
   - For each StixORM block, follow this sequence:
     1. **Input Object Preparation**: Copy the STIX input objects into `tests/stixorm/generated/input_objects/`.
     2. **Data Form Generation**: Generate the corresponding data forms and store them in `tests/stixorm/generated/data_forms/`.
     3. **Block Sequence Execution**: Execute the StixORM block using the generated data forms as input.
     4. **Output Verification**: Compare the output of the block against the expected output stored in `tests/stixorm/generated/output_objects/` using DeepDiff.
     5. **Report**: Ensure any temporary files or data created during testing are cleaned up after tests run.








## OS_Triage Blocks Testing

**TODO: Fill in the details for OS_Triage block testing similar to StixORM testing. Below is an embryonic structure.**

1. **Directory Structure**:
   - `tests/os_triage/`: Contains all tests related to OS_Triage blocks
   - `tests/os_triage/fixtures/`: Contains any fixtures needed for testing OS_Triage blocks

2. **Testing Framework**:
   - Use `pytest` for all OS_Triage tests
   - Include a `conftest.py` file in the `tests/os_triage/` directory for shared fixtures

3. **Test Organization**:
   - Organize tests by feature or functionality
   - Use descriptive names for test files and test functions
