# STIX Object Reconstitution Testing Framework

This directory contains a comprehensive testing framework for validating the STIX object reconstitution process. The framework tests the complete round-trip conversion: STIX objects → data forms → STIX objects.

## Directory Structure

```
temporary_reconstitution_testing/
├── reconstitute_object_list.py    # Core reconstitution module
├── runner.py                      # Test runner with DeepDiff comparison
├── requirements.txt               # Dependencies
├── README.md                      # This file
└── generated/                     # Generated test files (auto-created)
    ├── input_objects/             # Original STIX objects for comparison
    ├── data_forms/                # Generated data forms and reconstitution data
    └── output_objects/            # Reconstituted STIX objects
```

## Components

### 1. `reconstitute_object_list.py`
The core reconstitution module that handles:
- Loading STIX objects from input directories
- Converting to data forms using `create_data_forms_from_stix_objects`
- Reconstituting STIX objects from data forms with proper dependency sequencing
- Managing UUID generation and reference restoration

**Key Features:**
- Preserves object structure while generating new UUIDs
- Handles complex reference patterns and dependencies
- Maintains creation sequence based on dependency graph
- Supports both single objects and collections

### 2. `runner.py`
Comprehensive test runner that:
- Clears generated directories before each test
- Runs full reconstitution pipeline on `Block_Families/examples`
- Compares original vs reconstituted objects using DeepDiff
- Generates detailed reports on successes/failures
- Saves test results in JSON and text formats

**Comparison Strategy:**
- Normalizes objects to ignore expected differences (UUIDs, timestamps)
- Groups objects by type and content for intelligent pairing
- Reports structural differences while allowing UUID changes
- Provides detailed failure analysis

## Usage

### Basic Testing
```bash
# Run the complete test suite
cd temporary_reconstitution_testing
python runner.py
```

### Module Testing
```bash
# Test reconstitution module directly
python reconstitute_object_list.py
```

### Custom Input Directory
```python
from reconstitute_object_list import reconstitute_object_list

# Use custom input directory
original_objects, reconstituted_objects, report = reconstitute_object_list(
    input_directory="/path/to/stix/objects",
    generated_directory="./generated"
)
```

## Test Results

The framework generates several output files:

1. **`generated/test_results.json`** - Complete test results in JSON format
2. **`generated/test_report.txt`** - Human-readable test report
3. **`generated/input_objects/`** - Original objects for comparison
4. **`generated/data_forms/`** - Generated data forms and reconstitution metadata
5. **`generated/output_objects/`** - Reconstituted objects

## Success Criteria

The test suite considers the reconstitution successful when:
- **Structural Integrity**: Objects maintain same structure and content
- **Reference Preservation**: All references are correctly restored with new UUIDs
- **Type Consistency**: Object types and properties remain unchanged
- **Dependency Resolution**: Objects are created in correct dependency order

## Expected Differences

The following differences are **expected** and **ignored** during comparison:
- **UUIDs**: All object IDs and references get new UUIDs
- **Timestamps**: `created` and `modified` fields get new timestamps
- **Field Order**: JSON field ordering may differ

## Validation Process

1. **Input Loading**: Load STIX objects from examples directory
2. **Data Form Generation**: Convert to data forms using Mode 2
3. **Reference Extraction**: Extract and track all object references
4. **Dependency Mapping**: Build dependency graph for creation sequence
5. **Object Reconstitution**: Create new STIX objects from data forms
6. **Reference Restoration**: Restore references with new UUIDs
7. **Deep Comparison**: Compare structures while ignoring UUID differences

## Error Handling

The framework handles various error conditions:
- Missing template files for object types
- Circular dependencies in object references
- Malformed input objects
- File I/O errors
- Reference resolution failures

## Dependencies

- **deepdiff**: For intelligent object comparison
- **Standard library**: json, uuid, pathlib, shutil, typing
- **Project modules**: `convert_object_list_to_data_forms`

## Example Output

```
🚀 Starting STIX Reconstitution Test Suite

📂 Using examples directory: /path/to/Block_Families/examples
📁 Generated files directory: /path/to/generated

🧹 Clearing generated directories...
📂 Loading STIX objects from: /path/to/examples
   ✅ Loaded 15 STIX objects
   📋 Copied 15 objects to input_objects directory

🔄 Generating data forms for 15 objects...
   ✅ Data forms generation completed
   📊 Success rate: 100.0%
   📁 Created 15 data form files
   🔗 Reference tracking entries: 15

🔄 Reconstituting STIX objects from data forms...
   📋 Processing 15 objects in dependency order
   ✅ Reconstituted: identity -> identity_a1b2c3d4_reconstituted.json
   ✅ Reconstituted: indicator -> indicator_e5f6g7h8_reconstituted.json
   ...
   🎯 Successfully reconstituted 15 objects

🔍 Running comparison tests...
   ✅ identity: Objects are structurally identical
   ✅ indicator: Objects are structurally identical
   ...

🎉 TEST SUITE PASSED! Success rate: 100.0%
```

This framework provides comprehensive validation that the STIX object reconstitution process maintains data integrity while properly handling the complex reference relationships inherent in STIX data structures.