# STIX Data Form Creation Analysis

## Note: Updated Documentation Available

**⚠️ This document has been superseded by the complete analysis document.**

**Current Documentation**: See `stix-data-form-conversion-complete-analysis.md` for:
- Comprehensive directory analysis across all 15 working implementations
- Enhanced reference extraction with STIX ID pattern detection
- Utility function implementation details
- Validation results across 24 objects and 14 STIX types

**Critical Enhancement (November 2025)**: Reference detection now includes both field name patterns (`_ref`/`_refs`) AND STIX ID patterns (`type--uuid`) to handle objects like Sequence with non-standard reference field names.

---

## Understanding the Pattern Between Class Templates and Data Forms

After systematic examination of class templates and their corresponding data form examples across SDO, SCO, and SRO directories, I have identified the consistent conversion pattern used in the Brett Blocks template-driven architecture.

## Key Findings

### 1. Class Template Structure
Every class template follows a fixed structure:
- `class_name`: The Python class name
- `{ClassName}_template`: Contains the template structure with:
  - `_type`: The STIX object type
  - `base_required`: Required base properties (type, spec_version, id, created, modified)
  - `base_optional`: Optional base properties (created_by_ref, revoked, labels, etc.)
  - `object`: Main STIX object properties specific to this type
  - `extensions`: STIX extensions (may be empty)
  - `sub`: Sub-object definitions for EmbeddedObjectProperty types

### 2. Data Form Structure  
Every data form follows this structure:
- `{typeql_name}_form`: Contains the actual data values with:
  - `base_required`: Same keys as template, but with actual values
  - `base_optional`: Same keys as template, but with actual values
  - `object`: Same keys as template, but with actual values
  - `extensions`: Same keys as template, but with actual values
  - `sub`: Contains actual instances of sub-objects (not definitions)

### 3. Critical Conversion Rules

#### Rule 1: Preserve Structure, Replace Property Definitions with Values
- **Template**: `"name": {"property": "StringProperty", "parameters": {"required": true}}`
- **Data Form**: `"name": "Paolo"`

#### Rule 2: Handle Reference Properties Carefully
- **Template**: `"belongs_to_ref": {"property": "ReferenceProperty", "parameters": {"valid_types": ["user-account"], "spec_version": "2.1"}}`
- **Data Form**: `"belongs_to_ref": ""` (empty string, to be filled by Python block)

#### Rule 3: Handle Collections/Lists
- **Template**: `"roles": {"collection": "ListProperty", "property": "StringProperty", "parameters": {}}`
- **Data Form**: `"roles": ["security-point-of-contact"]`

#### Rule 4: Handle Sub-Objects
- **Template**: In `sub` section as definitions with property types
- **Data Form**: In `sub` section as actual data instances (without property definitions)

#### Rule 5: Auto-Generated Fields
- For `base_required` properties like `id`, `created`, `modified`: Use empty strings if they will be auto-generated
- Keep `type` and `spec_version` with actual values

#### Rule 6: Extensions Handling
- **Template**: Extension properties are defined with property types
- **Data Form**: Extension properties contain actual values
- Empty collections in extensions should be empty arrays `[]`

## Systematic Directory Analysis Results

I will examine each working implementation (those with make_object.py files) to validate the pattern:

### SDO Make Files Analysis (Currently Implemented)

Let me examine each SDO that has working implementations: