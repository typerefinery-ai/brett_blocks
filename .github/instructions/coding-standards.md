# Brett Blocks Coding Standards - **Template-Driven Implementation**

## 🎯 Code Quality Mission - **Template-Driven Architecture**

**High-quality, maintainable code** is essential for the Brett Blocks cybersecurity intelligence system. **Template-driven architecture** ensures consistency, reliability, and automatic code generation with the OS Threat platform using **validated three-file patterns**.

## 🔧 Development Framework Standards - **✅ Template-Driven Patterns**

### Template-Driven Architecture Framework - **Critical Implementation Pattern**

**Validated Discovery**: Development uses **template-driven architecture** where class templates automatically generate Python function signatures and imports.

**Three-File Pattern** (confirmed working across all StixORM directories):

```python
# ✅ VALIDATED TEMPLATE-DRIVEN PATTERN
# 1. Class Template (ClassName_template.json) - Defines structure and auto-generation rules
# 2. Data Template (objectname_variant.json) - Provides instance data  
# 3. Python Block (make_objecttype.py) - Auto-generated function signature

# Example: Identity template drives automatic function parameter generation
# Identity_template.json ReferenceProperty → make_identity.py function parameters
```

**Property Type Auto-Generation Rules** (validated through execution):

```python
# ✅ CRITICAL: Template property types determine Python function structure
# ReferenceProperty → Optional function parameter with None default
# OSThreatReference → Auto-generated parameter for foreign key relationships
# EmbeddedObjectProperty → Required imports and conditional creation logic

# Identity_template.json example:
# "identity_class" property → identity_class parameter in make_identity.py
# "contact_information" (EmbeddedObjectProperty) → conditional contact info creation
```

**Template-to-Python Translation Rules** (validated through execution):

```python
# ✅ CORRECT: Template-driven parameter generation
# Template: "belongs_to_ref": {"type": "ReferenceProperty"}
# Result: def make_email_addr_block(..., usr_account=None):

# Template: "sequence_start_refs": {"type": "OSThreatReference"}  
# Result: def make_incident_block(..., sequence_start_refs=None):

# ❌ INCORRECT: Manual parameter definition that ignores template structure
# Always use template-driven auto-generation, never manual parameter lists
```

### Context Memory Integration - **Validated Dual-Pattern**

**User Context Pattern** (confirmed working):

```python
# ✅ USER CONTEXT - Simple array-based storage
# Location: context_mem/usr/cache_me.json, cache_team.json
user_context = [
    {
        "id": "user-account--uuid",
        "type": "user-account", 
        "original": { /* STIX data */ },
        /* UI metadata */
    }
]
```

**Company Context Pattern** (confirmed working):

```python
# ✅ COMPANY CONTEXT - Category-based organization
# Location: context_mem/identity--{company-uuid}/
context_type = {
    "context_type": "users"  # Store in users.json category
}

# Required: Use context type for proper categorization
result = invoke_save_company_context_block(
    object_path, 
    context_path, 
    context_type  # ✅ Critical for category-based storage
)
```

### STIX Object Creation - **Validated Dual-Layer Format**

**Required Object Structure** (confirmed through execution):

```python
# ✅ VALIDATED DUAL-LAYER STIX OBJECT FORMAT
def create_stix_object(template_data: dict, stix_type: str) -> dict:
    """Create STIX object with validated dual-layer format"""
    
    # Generate STIX-compliant UUID
    stix_id = f"{stix_type}--{str(uuid.uuid4())}"
    template_data['id'] = stix_id
    
    # Set STIX timestamps
    current_time = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%fZ')
    template_data['created'] = current_time
    template_data['modified'] = current_time
    
    # ✅ REQUIRED: Create dual-layer format
    dual_layer_object = {
        "id": stix_id,                    # Top-level routing
        "type": stix_type,                # Top-level type
        "original": template_data,        # ✅ PURE STIX 2.1 DATA
        # ✅ UI METADATA for visualization
        "icon": stix_type,
        "name": stix_type.title().replace('-', ' '),
        "heading": stix_type.title().replace('-', ' '),
        "description": f"<br>/* Generate description from object data */",
        "object_form": stix_type,
        "object_group": f"{object_category}-forms",  # sdo-forms, sco-forms, sro-forms
        "object_family": "stix-forms"
    }
    
    return dual_layer_object
```

## 🧱 Block Development Standards - **Updated with Findings**

### Error Handling Standards - **✅ Critical Fixes Discovered**

**Variable Scope Bug Fix** (discovered in `make_user_account.py`):

```python
# ❌ INCORRECT: Variable scope issue found during testing
def process_user_account(input_data):
    if some_condition:
        result_data = process_condition()
    # Bug: result_data undefined if condition false
    return result_data  # ❌ UnboundLocalError

# ✅ CORRECT: Proper variable initialization
def process_user_account(input_data):
    result_data = None  # ✅ Initialize variables
    if some_condition:
        result_data = process_condition()
    else:
        result_data = default_processing()
    return result_data  # ✅ Always defined
```

**Template Loading Error Handling** (validated pattern):

```python
# ✅ REQUIRED: Robust template loading with path validation
def load_template_safely(template_path: str, path_base: str) -> dict:
    """Load template with proper error handling"""
    try:
        full_path = path_base + template_path
        if not os.path.exists(full_path):
            raise FileNotFoundError(f"Template not found: {full_path}")
        
        with open(full_path, 'r') as f:
            template_data = json.load(f)
        
        # Validate required STIX fields
        required_fields = ['type', 'spec_version']
        for field in required_fields:
            if field not in template_data:
                raise ValueError(f"Missing required field '{field}' in template: {template_path}")
        
        return template_data
    
    except Exception as e:
        logger.error(f"Error loading template {template_path}: {str(e)}")
        raise
```

### File Path Management - **Critical Validated Patterns**

**Path Resolution Requirements** (discovered during execution):

```python
# ✅ VALIDATED: Utility function path pattern
# Notebooks set base paths, utility functions handle concatenation
path_base = "../Block_Families/StixORM/"
results_base = "../Orchestration/Results/"

# ✅ REQUIRED: Always use relative paths with utility functions
def create_object_with_utility(template_name: str, results_name: str):
    # Utility function automatically prepends path_base
    return invoke_make_identity_block(
        f"SDO/Identity/{template_name}",  # ✅ Relative path
        f"step0/{results_name}"           # Results path
    )

# ❌ INCORRECT: Manual path concatenation breaks utility pattern
def create_object_manual(template_name: str):
    full_path = path_base + f"SDO/Identity/{template_name}"  # ❌ Breaks pattern
    # This bypasses utility function path management
```

**File Existence Validation** (required pattern):

```python
# ✅ REQUIRED: Validate files exist before processing  
def validate_template_exists(template_path: str, path_base: str) -> bool:
    """Validate template file exists before processing"""
    full_path = path_base + template_path
    if not os.path.exists(full_path):
        logger.error(f"Template file not found: {full_path}")
        return False
    return True

# ✅ Use validation in block logic
if not validate_template_exists(template_path, path_base):
    raise FileNotFoundError(f"Required template missing: {template_path}")
```

### JSON Processing Standards - **Validated Patterns**

**Safe JSON Operations** (required for STIX data):

```python
# ✅ REQUIRED: Safe JSON loading with error handling
def load_json_safely(file_path: str) -> dict:
    """Load JSON with proper error handling and validation"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        if not isinstance(data, dict):
            raise ValueError(f"Expected JSON object, got {type(data)}")
        
        return data
    
    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON in {file_path}: {str(e)}")
        raise
    except Exception as e:
        logger.error(f"Error loading JSON from {file_path}: {str(e)}")
        raise

# ✅ REQUIRED: Safe JSON saving with formatting
def save_json_safely(data: dict, file_path: str) -> None:
    """Save JSON with proper formatting and error handling"""
    try:
        # Ensure directory exists
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Successfully saved JSON to {file_path}")
    
    except Exception as e:
        logger.error(f"Error saving JSON to {file_path}: {str(e)}")
        raise
```
    """
    # Implementation varies per block type
    # Always validate inputs
    # Always handle errors gracefully
    # Always return consistent output structure
    pass

def main(input_file: str, output_file: str) -> None:
    """
    Standard entry point - DO NOT CHANGE SIGNATURE
    
    Args:
        input_file: Path to JSON input file
        output_file: Path to JSON output file
    """
    try:
        # Load input data
        with open(input_file, 'r') as f:
            input_data = json.load(f)
        
        # Process data using block-specific logic  
        result = process_block_logic(input_data)
        
        # Write output data
        with open(output_file, 'w') as f:
            json.dump(result, f, indent=2, sort_keys=True)
            
    except Exception as e:
        logger.error(f"Block execution failed: {str(e)}")
        # Write error output
        error_output = {
            "success": False,
            "error": str(e),
            "block": os.path.basename(__file__)
        }
        with open(output_file, 'w') as f:
            json.dump(error_output, f, indent=2)
        raise

################################################################################
## IMMUTABLE FOOTER - DO NOT CHANGE  
################################################################################
import argparse

def getArgs():
    parser = argparse.ArgumentParser(description="Script params",
                                  formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("inputfile", nargs='?', default=f"{os.path.basename(__file__)}.input", 
                       help="input file (default: %(default)s)")
    parser.add_argument("outputfile", nargs='?', default=f"{os.path.basename(__file__)}.output", 
                       help="output file (default: %(default)s)")
    return parser.parse_args()

if __name__ == '__main__':
    args = getArgs()
    main(args.inputfile, args.outputfile)
################################################################################
```

### Block Function Constraints

**Input/Output Requirements**:
- ✅ **JSON-only communication**: All inter-block communication via JSON files
- ✅ **Standard signature**: `main(input_file: str, output_file: str) -> None`
- ✅ **Error handling**: Comprehensive try/catch with error output
- ✅ **Logging**: Use Python logging module for debugging

**Prohibited Patterns**:
- ❌ **Direct block calls**: Never import or call other blocks directly
- ❌ **Shared state**: No global variables or shared memory
- ❌ **Print statements**: Use logging instead of print()
- ❌ **Hardcoded paths**: Use relative paths and configuration

## 🗂️ File and Directory Naming

### Directory Structure Conventions

**Block Organization**:
```
Block_Families/
├── OS_Triage/              # PascalCase for major categories
│   ├── Create_Context/     # PascalCase for functional groups
│   ├── Save_Context/       
│   └── Viz_Dataviews/      
├── StixORM/                # PascalCase for major categories
│   ├── SDO/                # Uppercase for STIX categories
│   ├── SCO/
│   └── SRO/
└── General/                # PascalCase for utilities
```

**File Naming Patterns**:
- **Python Blocks**: `snake_case.py` (e.g., `save_unattached_context.py`)
- **JSON Data**: `snake_case.json` (e.g., `incident_data.json`)
- **Notebooks**: `descriptive_name.ipynb` (e.g., `Step_1_Create_Incident.ipynb`)
- **Documentation**: `kebab-case.md` (e.g., `coding-standards.md`)

### STIX Object Naming

**STIX File Naming**:
```
[object-type]--[uuid].json
Examples:
- incident--d1cdb31f-8e54-4bdd-b3f9-ce9d0c94acc8.json
- malware--a1b2c3d4-5e6f-7890-abcd-ef1234567890.json
- indicator--12345678-90ab-cdef-1234-567890abcdef.json
```

**Form Data Naming**:
```
form_[object-type].json
Examples:
- form_incident.json
- form_malware.json
- form_indicator.json
```

## 📊 Data Handling Standards

### JSON Structure Conventions

**Standard Input Format**:
```json
{
  "stix_objects": [],           // Array of STIX objects
  "context_data": {},           // Context memory references
  "form_data": {},              // User input forms
  "configuration": {},          // Block-specific settings
  "metadata": {                 // Processing metadata
    "timestamp": "ISO-8601",
    "source": "block-name",
    "version": "1.0"
  }
}
```

**Standard Output Format**:
```json
{
  "success": true,              // Processing success indicator
  "stix_objects": [],           // Generated/modified STIX objects
  "data_slice": {},             // Context data slice
  "ui_data": {},                // Visualization data
  "relationships": [],          // STIX relationships
  "metadata": {                 // Output metadata
    "processed_at": "ISO-8601",
    "block": "block-name",
    "object_count": 5,
    "validation_status": "passed"
  }
}
```

### STIX Compliance Requirements

**Mandatory STIX Validation**:
```python
def validate_stix_object(stix_obj: Dict[str, Any]) -> bool:
    """Validate STIX object against 2.1 schema"""
    required_fields = ["type", "spec_version", "id", "created", "modified"]
    
    # Check required fields
    for field in required_fields:
        if field not in stix_obj:
            raise ValueError(f"Missing required field: {field}")
    
    # Validate spec_version
    if stix_obj["spec_version"] != "2.1":
        raise ValueError(f"Invalid spec_version: {stix_obj['spec_version']}")
    
    # Validate ID format
    expected_prefix = f"{stix_obj['type']}--"
    if not stix_obj["id"].startswith(expected_prefix):
        raise ValueError(f"Invalid ID format for {stix_obj['type']}")
    
    return True
```

**UUID Generation Standard**:
```python
import uuid

def generate_stix_id(object_type: str) -> str:
    """Generate valid STIX ID with proper format"""
    return f"{object_type}--{str(uuid.uuid4())}"
```

## 🔧 Import and Dependency Management

### Approved Import Categories

**Core Python Libraries** (Always Allowed):
```python
import os, sys, json, uuid, logging
from datetime import datetime
from typing import Dict, Any, List, Optional, Union
import importlib.util, argparse
```

**STIX Processing Libraries** (Required for STIX blocks):
```python
from stixorm.module.authorise import import_type_factory
import_type = import_type_factory.get_all_imports()
```

**Common File Loading Pattern**:
```python
# Dynamic loading of common utilities
def load_common_module(module_name: str, file_path: str):
    """Load common module dynamically"""
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

# Usage example
common_path = "Orchestration/generated/os-triage/common_files/convert_n_and_e.py"
converter = load_common_module('convert_n_and_e', common_path)
```

### Prohibited Imports

**Blocked Libraries**:
- ❌ **Network libraries**: requests, urllib (blocks run in isolated environment)
- ❌ **File system libraries**: shutil, pathlib (use os.path only)
- ❌ **Threading libraries**: threading, multiprocessing (blocks are stateless)
- ❌ **External APIs**: No external service calls allowed

## 🧪 Testing and Validation Standards

### Block Testing Requirements

**Unit Test Structure**:
```python
def test_block_functionality():
    """Test block with sample input data"""
    # Arrange
    test_input = {
        "stix_objects": [sample_stix_object],
        "context_data": {},
        "metadata": {"source": "test"}
    }
    
    # Act
    result = process_block_logic(test_input)
    
    # Assert
    assert result["success"] is True
    assert "stix_objects" in result
    assert len(result["stix_objects"]) > 0
    
    # Validate STIX compliance
    for obj in result["stix_objects"]:
        validate_stix_object(obj)
```

**Integration Testing Pattern**:
```python
def test_block_integration():
    """Test block with real input/output files"""
    import tempfile
    
    # Create temporary input file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        json.dump(test_input_data, f)
        input_file = f.name
    
    # Create temporary output file
    output_file = tempfile.mktemp(suffix='.json')
    
    try:
        # Execute block
        main(input_file, output_file)
        
        # Validate output
        with open(output_file, 'r') as f:
            result = json.load(f)
        
        assert result["success"] is True
        
    finally:
        # Cleanup
        os.unlink(input_file)
        if os.path.exists(output_file):
            os.unlink(output_file)
```

### Error Handling Standards

**Comprehensive Error Handling**:
```python
def process_block_logic(input_data: Dict[str, Any]) -> Dict[str, Any]:
    """Block processing with proper error handling"""
    try:
        # Validate input
        if not isinstance(input_data, dict):
            raise ValueError("Input must be a dictionary")
        
        # Process data
        result = perform_processing(input_data)

## 💾 Context Memory Operations (Validated Implementation)

### Context Memory Patterns from Step_0 Execution

**Dual-Pattern Architecture** (validated through notebook execution):

1. **User Context Pattern** (`/usr/` directory)
   - No initialization required
   - Direct object storage in array format
   - Used for personal identity and team member data

2. **Company Context Pattern** (`/identity--{uuid}/` directory)
   - Requires explicit initialization via `invoke_create_company_context()`
   - Category-specific storage (users.json, systems.json, assets.json, company.json)
   - Multi-tenant support with UUID-based directory naming

### Validated Utility Functions

**Context Creation Functions** (observed in Step_0):
```python
# Company context initialization
invoke_create_company_context(context_type="Company", input_data=company_data)

# Context storage operations
invoke_save_company_context_block(context_type="Company", input_data=company_object)
invoke_save_user_context_block(input_data=user_object)
invoke_save_team_context_block(input_data=team_object)
```

### Object Storage Structure (Validated)

**Dual-Layer Object Format** (actual implementation):
```json
{
  "id": "user-account--83658594-537d-5c32-b9f0-137354bd9bc3",
  "type": "user-account",
  "original": {
    "type": "user-account",
    "spec_version": "2.1",
    "id": "user-account--83658594-537d-5c32-b9f0-137354bd9bc3",
    "user_id": "79563902",
    "account_login": "tjones",
    "account_type": "soc,",
    "display_name": "Trusty Jones"
  },
  "icon": "user-account",
  "name": "User Account",
  "heading": "User Account",
  "description": "<br>Display Name -> Trusty Jones<br>Account Type -> soc,",
  "object_form": "user-account",
  "object_group": "sco-forms",
  "object_family": "stix-forms"
}
```

**Key Implementation Details**:
- **`original`** field contains pure STIX 2.1 compliant data (what blocks process)
- **UI metadata** provides display information for visualization components
- **Array storage** in JSON files enables multiple objects per context
- **Append pattern** preserves object history and relationships

### Context Directory Structure (From Execution)

**Validated Storage Layout**:
```
context_mem/
├── context_map.json                    # Global context routing
├── usr/                               # Single user workspace  
│   ├── cache_me.json                  # User identity objects
│   ├── cache_team.json                # Team member objects
│   └── edges.json                     # User relationships
├── identity--{company-uuid}/           # Company contexts
│   ├── company.json                   # Company identity
│   ├── users.json                     # Employee objects
│   ├── systems.json                   # IT system objects
│   ├── assets.json                    # Hardware/asset objects
│   └── edges.json                     # Company relationships
└── incident--{incident-uuid}/          # Incident contexts
    ├── incident.json                  # Core incident data
    ├── sequence_start_refs.json       # Attack vectors
    └── [relationship files]           # Various relationships
```
        
        # Validate output
        validate_output_structure(result)
        
        return result
        
    except ValueError as e:
        logger.error(f"Input validation error: {str(e)}")
        raise
        
    except KeyError as e:
        logger.error(f"Missing required data: {str(e)}")
        raise
        
    except Exception as e:
        logger.error(f"Unexpected error in block processing: {str(e)}")
        raise
```

## 📝 Documentation Standards

### Block Documentation Requirements

**Header Documentation** (Required for every block):
```python
##############################################################################
# Title: Clear, descriptive title of block purpose
# Author: OS-Threat  
# Organization Repo: https://github.com/typerefinery-ai/brett_blocks
# Contact Email: brett@osthreat.com
# Date: YYYY/MM/DD
#
# Description: 
# Detailed description of what this block does, including:
# - Primary purpose and use case
# - Input requirements and format
# - Processing methodology
# - Output structure and format
#
# Inputs:
# 1. input_file: JSON file containing:
#    - stix_objects: Array of STIX 2.1 objects
#    - context_data: Context memory references
#    - configuration: Block-specific settings
#
# Outputs:
# 1. output_file: JSON file containing:
#    - success: Boolean processing status
#    - stix_objects: Generated/modified objects
#    - metadata: Processing information
#
# Dependencies:
# - stixorm library for STIX processing
# - Common files: [list any shared utilities]
#
# Examples:
# Input: {"stix_objects": [incident_object]}
# Output: {"success": true, "ui_data": visualization_data}
#
# This code is licensed under the terms of the Apache 2.
##############################################################################
```

**Function Documentation**:
```python
def process_block_logic(input_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Process input data according to block-specific logic.
    
    This function implements the core processing logic for the block.
    It validates inputs, performs transformations, and generates outputs
    according to the block's specific purpose.
    
    Args:
        input_data (Dict[str, Any]): Input data containing:
            - stix_objects: List of STIX 2.1 objects to process
            - context_data: Context memory references and metadata
            - configuration: Block-specific configuration parameters
            
    Returns:
        Dict[str, Any]: Processing results containing:
            - success: Boolean indicating processing success
            - stix_objects: Generated or modified STIX objects
            - data_slice: Extracted context data if applicable
            - metadata: Processing metadata and statistics
            
    Raises:
        ValueError: If input data is malformed or missing required fields
        ValidationError: If STIX objects fail validation
        ProcessingError: If block-specific processing fails
        
    Example:
        >>> input_data = {"stix_objects": [incident_obj]}
        >>> result = process_block_logic(input_data)
        >>> assert result["success"] is True
    """
```

## 🚀 Performance and Optimization

### Efficiency Guidelines

**Memory Management**:
- ✅ **Process data in chunks** for large datasets
- ✅ **Clean up temporary variables** after use
- ✅ **Use generators** for large data processing
- ❌ **Avoid loading entire context** memory at once

**File I/O Optimization**:
```python
# Efficient JSON processing
def process_large_json(file_path: str) -> Dict[str, Any]:
    """Process large JSON files efficiently"""
    import ijson  # If available in environment
    
    # Stream parsing for large files
    with open(file_path, 'rb') as file:
        objects = ijson.items(file, 'stix_objects.item')
        for obj in objects:
            yield process_single_object(obj)
```

**Logging Best Practices**:
```python
# Configure logging appropriately
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Use appropriate log levels
logger.debug("Detailed debugging information")
logger.info("General processing information")
logger.warning("Warning conditions")
logger.error("Error conditions requiring attention")
logger.critical("Critical errors causing failure")
```

These coding standards ensure consistency, maintainability, and reliability across all Brett Blocks system components while maintaining strict compliance with STIX 2.1 specifications and OS Threat platform requirements.