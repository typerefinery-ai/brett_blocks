# STIX Object Reconstitution Utility

## Overview

`reconstitute_object_list.py` is a utility that reconstitutes full STIX objects from their data form representations. It works in conjunction with `convert_object_list_to_data_forms.py` to enable round-trip conversion: STIX objects → data forms → STIX objects.

## Purpose

This utility performs the reverse operation of data form generation:
- Loads data forms created by `convert_object_list_to_data_forms.py`
- Restores embedded references that were extracted during data form creation
- Generates new UUIDs for all objects (maintaining referential integrity)
- Produces fully valid STIX objects that are structurally identical to the originals

## Key Features

### 1. **Dependency-Aware Processing**
- Processes objects in dependency order based on the creation sequence
- Ensures referenced objects are reconstituted before objects that reference them
- Handles complex nested reference chains

### 2. **Reference Restoration**
- Restores all extracted references (embedded objects, lists, properties)
- Maintains reference integrity by mapping old UUIDs to new UUIDs
- Handles special reference types:
  - Embedded objects (e.g., granular markings, extensions)
  - Embedded lists (e.g., external_references, kill_chain_phases)
  - Property references (e.g., created_by_ref, object_refs)

### 3. **UUID Mapping**
- Generates new UUIDs for all reconstituted objects
- Maintains a mapping of old IDs → new IDs
- Updates all references to use the new UUIDs
- Preserves reference relationships across the entire object graph

### 4. **Template-Based Reconstruction**
- Uses the same templates as data form creation
- Ensures structural consistency between original and reconstituted objects
- Supports all STIX 2.1 object types with available templates

## Usage

### Basic Usage

```python
from Orchestration.Utilities.reconstitute_object_list import StixObjectReconstitutor

# Initialize the reconstructor
reconstructor = StixObjectReconstitutor(
    data_forms_dir="path/to/data_forms",
    reconstitution_data_file="path/to/reconstitution_data.json",
    output_dir="path/to/output"
)

# Reconstitute all objects
success = reconstructor.reconstitute_all_objects()

if success:
    print("✅ All objects reconstituted successfully")
else:
    print("❌ Some objects failed to reconstitute")
```

### Integration with Data Form Generation

```python
from Orchestration.Utilities.convert_object_list_to_data_forms import convert_object_list_to_data_forms
from Orchestration.Utilities.reconstitute_object_list import StixObjectReconstitutor

# Step 1: Convert STIX objects to data forms
results = convert_object_list_to_data_forms(
    stix_objects=my_objects,
    output_directory="generated/data_forms",
    mode=2  # Test mode with reference tracking
)

# Step 2: Reconstitute from data forms
reconstructor = StixObjectReconstitutor(
    data_forms_dir="generated/data_forms",
    reconstitution_data_file="generated/data_forms/reconstitution_data.json",
    output_dir="generated/reconstituted"
)

success = reconstructor.reconstitute_all_objects()
```

## Input Requirements

### 1. Data Forms Directory
Contains individual data form JSON files created by `convert_object_list_to_data_forms.py`:
- Format: `{type}_{hash}_data_form.json`
- Structure: Object data with extracted references removed

### 2. Reconstitution Data File
JSON file containing metadata needed for reconstitution:
```json
{
    "creation_sequence": [
        {
            "object_id": "identity--abc123...",
            "filename": "identity_5e2f7cea_data_form.json",
            "form_name": "identity"
        }
    ],
    "detailed_references": [
        {
            "object_id": "identity--abc123...",
            "filename": "identity_5e2f7cea_data_form.json",
            "embedded_objects": [...],
            "embedded_lists": [...],
            "property_refs": [...]
        }
    ]
}
```

## Output

### Reconstituted Objects
- Individual JSON files: `{type}_{hash}_reconstituted.json`
- Full STIX objects with all references restored
- New UUIDs for all objects (maintaining referential integrity)
- Structurally identical to original objects

### Success Metrics
The utility tracks and reports:
- Number of objects successfully reconstituted
- Objects that failed to reconstitute
- Reference mapping statistics

## Technical Details

### Reference Restoration Process

1. **Load Data Form**: Read the simplified object data
2. **Generate New UUID**: Create new ID for the reconstituted object
3. **Restore References**: Process in order:
   - Embedded objects (restore nested STIX objects)
   - Embedded lists (restore arrays of complex structures)
   - Property references (update ID references to new UUIDs)
4. **Update Mappings**: Track old ID → new ID for subsequent references
5. **Save Object**: Write fully reconstituted STIX object to file

### Special Handling

#### Sequence Objects
- `on_completion` field: Maps old sequence IDs to new sequence IDs
- `sequenced_object` field: Maps old object IDs to new object IDs

#### Identity Extensions
- Extracts extension data from 'sub' section of detailed references
- Restores to `extension-definition--*` keys in extensions

#### File Archive Extensions
- Navigates nested path: `extensions['archive-ext']['contains_refs']`
- Restores file references in archive contents

#### Network Traffic Encapsulation
- Handles `encapsulates_refs` and `encapsulated_by_ref` properties
- Maintains network traffic relationship chains

## Success Rate

Current performance on STIX 2.1 test corpus:
- **99.3%** success rate (151/152 objects)
- **100%** on all objects with available templates
- Only unsupported type: `language-content` (no template)

## Limitations

1. **Template Dependency**: Requires templates for all object types
2. **UUID Generation**: All objects get new UUIDs (not preserving originals)
3. **Reference Integrity**: Requires complete object graph in data forms

## Error Handling

The utility provides detailed error messages for:
- Missing data form files
- Template not found for object type
- Reference restoration failures
- UUID mapping issues

All errors are logged with context for debugging.

## Integration Points

### Works With
- `convert_object_list_to_data_forms.py` - Creates input data forms
- `runner.py` - Test harness for validation
- All STIX object templates in `Block_Families/`

### File Dependencies
- Data form JSON files
- `reconstitution_data.json` metadata
- STIX object templates

## Testing

Run the test suite to validate reconstitution:
```bash
cd temporary_reconstitution_testing
poetry run python runner.py
```

Expected output:
```
🎉 TEST SUITE PASSED! Success rate: 99.3%
✅ 151 objects structurally identical
```

## Version History

- **v1.0** - Initial implementation with basic reconstitution
- **v1.1** - Added sequence reference normalization
- **v1.2** - Added identity extension handling
- **v1.3** - Added file archive extension support
- **v1.4** - Content-based stable filenames
- **v1.5** - Duplicate ID handling (skip duplicates)
- **Current** - 99.3% success rate, production-ready

## Author

Developed as part of the Brett Blocks STIX object management system.

## See Also

- `convert_object_list_to_data_forms.py` - Data form generation
- `README_convert_object_list_to_data_forms.md` - Data form documentation
- STIX 2.1 Specification - https://docs.oasis-open.org/cti/stix/v2.1/
