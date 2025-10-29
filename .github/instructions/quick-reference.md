# Brett Blocks Quick Reference Guide - **Template-Driven Implementation**

## 🎯 Essential System Facts - **Template-Driven Architecture**

**System Purpose**: 🛡️ Cybersecurity intelligence platform using **template-driven automatic code generation** + **validated dual-layer STIX 2.1 objects**
**Architecture**: 🔄 **Three-file patterns** (class template + data template + Python block) with automatic function parameter generation
**Communication**: 📄 **Template-generated JSON objects** with `original` STIX data + UI metadata
**Data Standard**: 🔒 **STIX 2.1 compliance in `original` field** + property type auto-generation

## 🔧 Template-Driven Architecture Framework - **✅ Critical Pattern**

**Validated Three-File Pattern**:

```python
# ✅ TEMPLATE-DRIVEN DEVELOPMENT PATTERN
# 1. CLASS TEMPLATE: Identity_template.json - Defines structure and auto-generation
# 2. DATA TEMPLATE: identity_IT_user1.json - Provides instance data
# 3. PYTHON BLOCK: make_identity.py - Auto-generated function signature

# ✅ PROPERTY TYPE AUTO-GENERATION (Real examples):
# Template: "identity_class": {"type": "OpenVocabProperty"}
# Result: identity_class=None parameter in make_identity.py

# Template: "belongs_to_ref": {"type": "ReferenceProperty"} 
# Result: usr_account=None parameter in make_email_addr.py

# Template: "sequence_start_refs": {"type": "OSThreatReference"}
# Result: sequence_start_refs=None parameter in make_incident.py

# ✅ CRITICAL: Function parameters automatically generated from template properties
identity_obj = invoke_make_identity_block(
    "SDO/Identity/identity_IT_user1.json",  # ✅ Data template path
    "step0/user"                            # Results path
)
```

## 📁 Critical Template Directories - **Validated Three-File Patterns**

- 🧱 **Block_Families/StixORM/** - **✅ Complete template-driven structure**
  - **SDO/Identity/** - ✅ Full template system (Identity_template.json + 7 data templates + make_identity.py)
  - **SDO/Incident/** - ✅ Complex foreign key template (OSThreatReference auto-generation)
  - **SDO/Indicator/** - ✅ Pattern template system validated
  - **SCO/User_Account/** - ✅ Simple template pattern (ReferenceProperty auto-generation)
  - **SCO/Email_Addr/** - ✅ Email template with belongs_to_ref auto-generation
  - **SCO/URL/** - ✅ URL evidence template pattern
  - **SCO/File/** - ✅ File evidence template pattern
  - **SRO/Relationship/** - Available template pattern for relationships
- 🎼 **Orchestration/** - **✅ Template usage patterns**
  - **Step_0_Build_Initial_Identities.ipynb** - ✅ Template-driven identity creation
  - **Step_1_Create_Incident_with_an_Alert.ipynb** - ✅ Complex template with foreign keys
  - **Results/** - Generated template-driven objects
  - **generated/os-triage/context_mem/** - **✅ Template-generated context storage**

## 🗂️ Context Memory Architecture - **Template-Driven Three-Tier System**

**User Context** (confirmed working):

```text
context_mem/usr/
├── cache_me.json      # Personal identity objects (array format)
└── cache_team.json    # Team member identities (array format)
```

**Company Context** (confirmed working):

```text
context_mem/identity--{company-uuid}/
├── company.json       # Company identity object
├── users.json         # Employee identities (categorized)
├── systems.json       # IT system identities (categorized)
├── assets.json        # Hardware asset identities (categorized)
└── edges.json         # Organizational relationships
```

**Incident Context** (✅ NEW - validated implementation):

```text
context_mem/incident--{incident-uuid}/
├── incident.json          # Primary incident STIX object
├── observables.json       # Evidence objects (email, URL, file)
├── indicators.json        # Threat detection patterns
├── relationships.json     # Evidence-to-incident linkages
├── sequence_start_refs.json # Attack vector initiation
├── sequence_refs.json     # Attack progression chain
├── impact_refs.json       # Business impact assessment
└── unattached_objs.json   # Evidence pending classification
```

## 🏗️ STIX Object Format - **Validated Dual-Layer**

**Required Object Structure** (confirmed through execution):

```json
{
  "id": "identity--f431f809-377b-45e0-aa1c-6a4751cae5ff",
  "type": "identity",
  "original": {
    // ✅ PURE STIX 2.1 DATA - industry standard compliance
    "type": "identity",
    "spec_version": "2.1",
    "id": "identity--f431f809-377b-45e0-aa1c-6a4751cae5ff",
    "created": "2023-10-25T10:30:00.000Z",
    "modified": "2023-10-25T10:30:00.000Z",
    "name": "John Smith",
    "identity_class": "individual"
  },
  // ✅ UI METADATA for visualization
  "icon": "identity",
  "name": "Identity",
  "heading": "Identity",
  "description": "<br>Name -> John Smith<br>Class -> individual",
  "object_form": "identity",
  "object_group": "sdo-forms",
  "object_family": "stix-forms"
}
```

## ✅ AI Development Rules - **Updated with Validated Insights**

### Always Do This - **Confirmed Patterns**

- **Use utility functions**: Import from `Utilities.local_make_*` for notebook development
- **Use relative paths**: Let utility functions handle path concatenation automatically
- **Validate dual-layer format**: Ensure `original` field contains pure STIX 2.1 data
- **Initialize variables**: Fix variable scope issues (discovered in `make_user_account.py`)
- **Handle path resolution**: Use `path_base` setup pattern in notebooks
- **Create incident contexts**: Use `invoke_create_incident_context()` for investigation setup
- **Specify context types**: Use proper context categories for evidence storage

### Never Do This - **Discovered Pitfalls**

- **Manual path concatenation**: Don't combine `path_base` with template paths
- **Absolute template paths**: Don't use full paths - utility functions expect relative
- **Skip context initialization**: Company and incident contexts require setup calls
- **Mix context patterns**: Don't store user objects in company contexts or vice versa
- **Ignore variable scope**: Initialize all variables before using in functions

## 🚨 Critical Implementation Patterns - **✅ Validated Through Execution**

### Context Memory Operations - **Important Definitions**

**CRITICAL**: When "deleting context memory" or "clearing context memory":

✅ **CORRECT**: Delete all FILES within context_mem/, preserve the directory:
```powershell
# Clear context data, keep directory structure
Remove-Item -Path "context_mem\*" -Recurse -Force
# Result: Empty context_mem/ directory remains (correct)
```

❌ **WRONG**: Never delete the context_mem directory itself:
```powershell  
# This breaks the system - DON'T DO THIS
Remove-Item -Path "context_mem" -Recurse -Force
# Result: No context_mem/ directory (system broken)
```

**Rationale**: The context memory directory is part of the system architecture. Deleting it breaks context storage operations.

### Template Path Resolution - **Critical Bug Fix**

```python
# ✅ CORRECT - Use relative paths only
incident_obj = invoke_make_incident_block(
    "SDO/Incident/incident_phishing.json",    # ✅ Relative from StixORM/
    "step2/phishing_incident",                # Results path
    sequence_start_refs, sequence_refs, task_refs, event_refs, impact_refs, other_object_refs
)

# ❌ WRONG - Double path concatenation causes "file not found"
incident_obj = invoke_make_incident_block(
    "../Block_Families/StixORM/SDO/Incident/incident_phishing.json",  # ❌ Double path
    "step2/phishing_incident",
    # ... parameters
)
```

### Context Type Specification - **✅ Validated Categories**

```python
# Incident evidence storage with proper context types
context_types = {
    "incident": "incident.json",           # Primary incident object
    "observables": "observables.json",     # Email, URL, file evidence
    "indicators": "indicators.json",       # Threat detection patterns  
    "relationships": "relationships.json", # Evidence linkages
    "evidence": "evidence.json",           # General investigation evidence
    "analysis": "analysis.json"            # Investigation findings
}

# Usage pattern for incident evidence storage
context_type = {"context_type": "observables"}  # Specify storage category
result = invoke_save_incident_context_block(obj_path, context_path, context_type)
```

### Incident Investigation Pattern - **✅ Validated Implementation**

```python
# Complete phishing incident creation pattern
# 1. Create incident context
result = invoke_create_incident_context(incident_obj_path, incident_context_path)

# 2. Create evidence objects with proper categorization
attacker_email = invoke_make_email_addr_block("SCO/Email_Addr/email_addr_malicious.json", "step2/attacker_email")
malicious_url = invoke_make_url_block("SCO/URL/url_malicious.json", "step2/malicious_url") 
suspicious_file = invoke_make_file_block("SCO/File/file_suspicious.json", "step2/malicious_file")

# 3. Store evidence in categorized context
context_type = {"context_type": "observables"}
invoke_save_incident_context_block(email_obj_path, email_context_path, context_type)
invoke_save_incident_context_block(url_obj_path, url_context_path, context_type)
invoke_save_incident_context_block(file_obj_path, file_context_path, context_type)

# 4. Create threat indicators for detection
email_indicator = invoke_make_indicator_block("SDO/Indicator/indicator_email_domain.json", "step2/email_indicator")
url_indicator = invoke_make_indicator_block("SDO/Indicator/indicator_url_pattern.json", "step2/url_indicator")

# 5. Store indicators in appropriate context
context_type = {"context_type": "indicators"}
invoke_save_incident_context_block(email_indicator_path, email_indicator_context, context_type)
invoke_save_incident_context_block(url_indicator_path, url_indicator_context, context_type)
```
- **Test sequentially**: Run `Step_0_User_Setup.ipynb` then `Step_1_Company_Setup.ipynb`

### Never Do This - **Validated Restrictions**

- **Manual path concatenation**: Breaks utility function pattern
- **Skip context type**: Company context requires `context_type` parameter
- **Modify `original` field**: Keep pure STIX 2.1 data unchanged
- **Use absolute paths**: Utility functions expect relative paths only
- **Skip variable initialization**: Causes UnboundLocalError in blocks

## 🔄 Workflow Patterns (Use These Templates)

**Data Processing**: Context → Slice → Block → Result → Context Update
**STIX Creation**: Form → Validation → STIX Object → Storage
**Analysis**: STIX Objects → Relationships → Visualization → UI Data

## 💾 Context Memory Operations (Validated Implementation)

### Utility Functions (From Step_0 Execution)
```python
# Context initialization (company contexts only)
invoke_create_company_context(context_type="Company", input_data=company_data)

# Context storage operations
invoke_save_company_context_block(context_type="Company", input_data=object_data)
invoke_save_user_context_block(input_data=user_data)
invoke_save_team_context_block(input_data=team_data)
```

### Dual-Pattern Architecture (Validated)
**User Context** (`/usr/`): No setup required, direct storage
**Company Context** (`/identity--{uuid}/`): Requires initialization, category-specific files

### Object Storage Format (Actual Implementation)
```json
{
  "id": "user-account--uuid",
  "type": "user-account", 
  "original": {                    // ← Pure STIX 2.1 data (what blocks process)
    "type": "user-account",
    "spec_version": "2.1",
    "id": "user-account--uuid",
    "user_id": "12345",
    "display_name": "User Name"
  },
  "icon": "user-account",          // ← UI metadata for visualization
  "name": "User Account",
  "description": "Display Name -> User Name"
}
```

**Key Facts**:
- Objects stored as **arrays** in JSON files
- **`original`** field = pure STIX data for block processing
- **UI metadata** = display information for visualization
- **Append pattern** = new objects added to arrays, history preserved

## 🏗️ Common Block Types

### OS_Triage Blocks (Operational Workflows)
**Create_Context/**: Initialize new security investigation contexts
**Save_Context/**: Persist investigation data to context memory
**Get_Context/**: Retrieve existing investigation data
**Update_Context/**: Modify investigation states
**Viz_Dataviews/**: Generate visualization data for UI components
**Form_Actions/**: Process user input forms

### StixORM Blocks (STIX Object Management)
**SDO/**: Domain object creators (incidents, malware, attack-patterns)
**SCO/**: Observable object creators (files, network traffic, processes)
**SRO/**: Relationship creators (sighting-of, indicates, uses)
**Common/**: Shared STIX utilities and validators

## 📊 STIX Object Quick Reference

### Core STIX Objects
```python
# Identity Object
{
  "type": "identity",
  "spec_version": "2.1",
  "id": "identity--uuid",
  "name": "Organization Name",
  "identity_class": "organization"
}

# Incident Object
{
  "type": "incident", 
  "spec_version": "2.1",
  "id": "incident--uuid",
  "name": "Security Incident",
  "incident_types": ["breach"]
}

# Indicator Object
{
  "type": "indicator",
  "spec_version": "2.1", 
  "id": "indicator--uuid",
  "pattern": "[file:hashes.MD5 = 'hash']",
  "indicator_types": ["malicious-activity"]
}
```

### STIX Validation Template
```python
def validate_stix_object(obj: Dict[str, Any]) -> bool:
    required = ["type", "spec_version", "id", "created", "modified"]
    for field in required:
        if field not in obj:
            raise ValueError(f"Missing: {field}")
    
    if obj["spec_version"] != "2.1":
        raise ValueError("Must use STIX 2.1")
    
    return True
```

## 🗂️ Context Memory Structure

```
Context Memory Root/
├── 📊 STIX Objects/             # Valid cybersecurity entities
│   ├── incident--[uuid].json    # Incident reports
│   ├── malware--[uuid].json     # Malware entities  
│   └── indicator--[uuid].json   # Threat indicators
├── 🗂️ Data Slices/             # Extracted context views
│   ├── anecdote_slice.json      # Narrative data 
│   └── sighting_slice.json      # Observation data
├── 📋 Form Templates/           # User input structures
│   └── form_incident.json       # Incident creation forms
└── ⚙️ Configuration/            # System settings
```

## 🚨 Common Issues and Solutions

### Block Execution Issues
**Problem**: Block won't execute or crashes
**Solution**: Check JSON input format, validate file paths, review logs

**Problem**: STIX validation errors
**Solution**: Verify spec_version is "2.1", check required fields, validate UUID format

**Problem**: Context memory not found
**Solution**: Verify file paths, check context directory structure, validate object IDs

### Development Issues
**Problem**: Block template doesn't work
**Solution**: Use exact immutable header/footer, don't modify main() signature

**Problem**: Import errors in blocks
**Solution**: Use approved imports only, load common files dynamically

**Problem**: Can't find shared utilities
**Solution**: Check `Orchestration/generated/os-triage/common_files/` directory

## 🎼 Orchestration Notebook Examples

### Step 0: Build Initial Identities
- Creates foundational STIX identity objects
- Establishes company and user entities
- Initializes baseline identity context

### Step 1: Create Incident with Alert
- Establishes incident context and alerting
- Creates incident objects and indicators
- Initializes incident directory structure

### Step 2: Get the Anecdote
- Develops incident narrative
- Builds complex object relationships
- Populates incident with investigative data

## 🔧 Block Creation Checklist

### Before Creating a Block
- [ ] Determine block purpose and category (OS_Triage vs StixORM)
- [ ] Identify input requirements and output format
- [ ] Plan STIX object types to be created/processed
- [ ] Choose appropriate subdirectory location

### During Block Development
- [ ] Use exact block template with immutable header/footer
- [ ] Implement `process_block_logic()` function
- [ ] Add comprehensive error handling
- [ ] Include proper logging and validation
- [ ] Test with sample input/output files

### After Block Creation
- [ ] Test block execution in isolation
- [ ] Validate STIX objects against 2.1 schema
- [ ] Test integration in Jupyter notebook
- [ ] Document block purpose and usage
- [ ] Verify context memory integration

## 🚀 Testing Quick Commands

### Test Block Execution
```bash
# Test individual block
python Block_Families/OS_Triage/Save_Context/save_context.py input.json output.json

# Validate output
python -c "import json; print(json.load(open('output.json')))"
```

### Validate STIX Objects
```python
# Quick validation
import json
with open('stix_object.json') as f:
    obj = json.load(f)
    
required = ["type", "spec_version", "id", "created", "modified"] 
assert all(field in obj for field in required)
assert obj["spec_version"] == "2.1"
```

## 💡 Pro Tips

1. **Start Simple**: Begin with existing block examples before creating new ones
2. **Test Frequently**: Run blocks in isolation before integrating into workflows
3. **Validate Early**: Check STIX compliance immediately after object creation
4. **Use Notebooks**: Jupyter notebooks are perfect for testing and development
5. **Follow Patterns**: Stick to established data flow and naming conventions
6. **Read Examples**: Study existing blocks in `Block_Families/` for patterns
7. **Check Context**: Always verify context memory structure before and after operations

This quick reference provides everything needed to develop, test, and deploy Brett Blocks effectively within the cybersecurity intelligence system.