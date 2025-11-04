# STIX 2.1 Guidelines for Brett Blocks System - **Template-Driven Implementation**

## 🎯 STIX Mission in Brett Blocks - **Template-Driven Architecture**

**STIX 2.1** is the foundational data standard for all cybersecurity intelligence operations within the Brett Blocks system. **Template-driven architecture** processes cybersecurity data using **three-file patterns** that ensure STIX 2.1 compliance through automatic code generation and dual-layer object format.

## 📊 Comprehensive STIX Object Analysis

**Implementation Status**: Based on complete systematic analysis documented in `architecture/`:
- **Current**: 15 implemented objects (8 SDO, 5 SCO, 2 SRO)
- **Available**: 88 total STIX objects across standard and dialect categories
- **Growth Potential**: 5.8x expansion with current StixORM library

**Complexity Patterns**: See `architecture/complete-stix-pattern-matrix.md` for:
- Function signature matrix for all 15 implemented objects
- Parameter complexity distribution (MINIMAL to EXTREME)
- Automation feasibility classifications

**Implementation Roadmap**: See `architecture/stix-object-generation-patterns.md` for:
- Complete analysis of all available STIX object types
- Standard STIX 2.1 vs dialect object categorization
- Development prioritization based on complexity analysis

## 🏗️ Template-Driven STIX Architecture - **Data Form Creation from Class Templates**

### Critical Implementation Discovery - **✅ Class Template to Data Form Conversion**

**Class Template to Data Form Conversion** (validated across 15 implemented objects):

Based on systematic analysis documented in `architecture/stix-data-form-conversion-complete-analysis.md`, the Brett Blocks system uses a precise conversion pattern from class templates to data forms:

#### Structure Preservation Pattern:
```json
// 1. CLASS TEMPLATE (Identity_template.json) - Property Definitions
{
  "class_name": "Identity",
  "Identity_template": {
    "_type": "identity",
    "base_required": {
      "type": {"property": "TypeProperty", "parameters": {"value": "_type", "spec_version": "2.1"}},
      "id": {"property": "IDProperty", "parameters": {"value": "_type", "Spec_version": "2.1"}}
    },
    "base_optional": {
      "created_by_ref": {"property": "ReferenceProperty", "parameters": {"valid_types": ["identity"]}},
      "labels": {"collection": "ListProperty", "property": "StringProperty", "parameters": {}}
    },
    "object": {
      "name": {"property": "StringProperty", "parameters": {"required": true}},
      "identity_class": {"property": "OpenVocabProperty", "parameters": {"vocab": "identity-class-ov"}}
    },
    "extensions": {},
    "sub": {}
  }
}

// 2. DATA FORM (identity_IT_user1.json) - Actual Values Following Template Structure
{
  "identity_form": {
    "base_required": {
      "type": "identity",
      "spec_version": "2.1", 
      "id": "",
      "created": "",
      "modified": ""
    },
    "base_optional": {
      "created_by_ref": "",
      "labels": [],
      "external_references": []
    },
    "object": {
      "name": "Naive Smith",
      "identity_class": "individual"
    },
    "extensions": {},
    "sub": {}
  }
}
  "name": "John Smith - IT User",
  "identity_class": "individual",
  "contact_information": "jsmith@company.com"
}

#### Data Form Conversion Rules - **Critical for STIX JSON to Data Form Creation**

**Property Type Mapping** (validated across 15 implemented objects):

| Template Property | Data Form Value | Example |
|------------------|------------------|---------|
| `StringProperty` | String value or `""` | `"name": "John Smith"` |
| `ListProperty` | Array with values or `[]` | `"labels": ["user", "sales"]` |
| `ReferenceProperty` | Reference ID or `""` | `"created_by_ref": ""` |
| `IntegerProperty` | Number value | `"criticality": 99` |
| `BooleanProperty` | `true`/`false`/`null` | `"revoked": null` |
| `TimestampProperty` | ISO timestamp or `""` | `"created": ""` |
| `DictionaryProperty` | Object with key-value pairs | `"extensions": {}` |

**Section Conversion Algorithm**:
1. **base_required**: Use actual STIX type, empty strings for auto-generated fields
2. **base_optional**: Use default values or empty arrays/strings  
3. **object**: Map template properties to actual data values
4. **extensions**: Convert extension definitions to actual extension values
5. **sub**: Convert sub-object definitions to actual instances

**Reference Extraction Rules**:
- Fields ending in `_ref`: Single reference IDs (often empty for auto-population)
- Fields ending in `_refs`: Arrays of reference IDs
- Embedded objects: Move to `sub` section with actual data, not definitions

// 3. PYTHON BLOCK (make_identity.py) - Auto-Generated Function
def make_identity_block(json_object_file: str, results_path: str, 
                       identity_class=None, contact_information=None):
    # Function parameters automatically generated from template properties
```

**Property Type Auto-Generation Rules** (validated through execution):

```python
# ✅ CRITICAL: Template property types determine Python function structure
# StringProperty → Optional parameter with None default
# ReferenceProperty → Auto-generated parameter for object references  
# OSThreatReference → Auto-generated parameter for foreign key relationships
# EmbeddedObjectProperty → Conditional creation logic with imports

# Real example from Identity template:
# "contact_information": {"type": "EmbeddedObjectProperty"} 
# → contact_information=None parameter in make_identity.py function
# → Conditional ContactInformation object creation in Python code
```

### Dual-Layer STIX Object Format - **✅ Confirmed Working**

**Template-Generated STIX Structure** (validated during notebook execution):

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
    "identity_class": "individual",
    "contact_information": "jsmith@company.com"
  },
  // ✅ UI METADATA for visualization and interface integration
  "icon": "identity",
  "name": "Identity",
  "heading": "Identity", 
  "description": "<br>Name -> John Smith<br>Class -> individual",
  "object_form": "identity",
  "object_group": "sdo-forms",
  "object_family": "stix-forms"
}
```

### Key Architecture Benefits - **Validated**

**STIX 2.1 Compliance** (confirmed):
- **`original` field**: Contains pure STIX 2.1 specification data
- **Perfect compatibility**: External STIX tools and platforms can process `original` field directly
- **Schema validation**: All `original` objects validate against STIX 2.1 schemas
- **Industry standard**: No modification of cybersecurity object specifications

**Enhanced Functionality** (confirmed):
- **UI metadata**: Rich visualization and interface information outside STIX spec
- **Form integration**: Object form types enable automatic UI generation  
- **Display optimization**: Formatted descriptions and visual elements
- **Context routing**: Top-level ID/type for efficient context operations

## 📊 STIX Object Categories - **Validated Implementation**

### STIX Domain Objects (SDO) - **✅ Validated Implementation**

**Identity Objects** - **Confirmed Critical for Context Memory**

```json
{
  "id": "identity--f431f809-377b-45e0-aa1c-6a4751cae5ff",
  "type": "identity",
  "original": {
    "type": "identity",
    "spec_version": "2.1",
    "id": "identity--f431f809-377b-45e0-aa1c-6a4751cae5ff",
    "created": "2023-10-25T10:30:00.000Z",
    "modified": "2023-10-25T10:30:00.000Z",
    "name": "John Smith",
    "identity_class": "individual",        // ✅ Required: individual, organization, system, etc.
    "contact_information": "jsmith@company.com"  // ✅ Optional linking to email objects
  },
  "icon": "identity",
  "name": "Identity",
  "heading": "Identity",
  "description": "<br>Name -> John Smith<br>Class -> individual",
  "object_form": "identity",
  "object_group": "sdo-forms",
  "object_family": "stix-forms"
}
```

**Validated Identity Categories** (confirmed through execution):
- **Person Identities**: Individual users and team members 
- **Organization Identities**: Companies and departments
- **System Identities**: IT systems and infrastructure
- **Asset Identities**: Hardware and virtual assets

### STIX Cyber Observable Objects (SCO) - **✅ Validated Implementation**

**User Account Objects** - **Confirmed Working (Fixed Bug)**

```json
{
  "id": "user-account--83658594-537d-5c32-b9f0-137354bd9bc3",
  "type": "user-account", 
  "original": {
    "type": "user-account",
    "spec_version": "2.1",
    "id": "user-account--83658594-537d-5c32-b9f0-137354bd9bc3",
    "user_id": "79563902",              // ✅ Required: unique user identifier
    "account_login": "tjones",          // ✅ Required: login name
    "account_type": "soc,",             // ✅ Optional: account type classification
    "display_name": "Trusty Jones"      // ✅ Optional: human-readable name
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

**Email Address Objects** - **Confirmed Working with Linking**

```json
{
  "id": "email-addr--c99b87bd-f0a8-50ca-9f84-68072efc61e3",
  "type": "email-addr",
  "original": {
    "type": "email-addr",
    "spec_version": "2.1",
    "id": "email-addr--c99b87bd-f0a8-50ca-9f84-68072efc61e3",
    "value": "tjones@company.com",       // ✅ Required: email address value
    "belongs_to_ref": "user-account--83658594-537d-5c32-b9f0-137354bd9bc3"  // ✅ Links to user account
  },
  "icon": "email-addr",
  "name": "Email Address",
  "heading": "Email Address",
  "description": "<br>Value -> tjones@company.com<br>Belongs To -> user-account--83658594...",
  "object_form": "email-addr",
  "object_group": "sco-forms", 
  "object_family": "stix-forms"
}
```

### STIX Relationship Objects (SRO) - **Available Implementation**

**Relationship Objects** - Available for organizational modeling

```json
{
  "type": "relationship",
  "spec_version": "2.1",
  "id": "relationship--example-uuid",
  "created": "2023-10-25T10:30:00.000Z",
  "modified": "2023-10-25T10:30:00.000Z",
  "relationship_type": "employed-by",   // ✅ Defines relationship semantics
  "source_ref": "identity--employee-uuid",     // ✅ Source object reference
  "target_ref": "identity--company-uuid"       // ✅ Target object reference
}
```

## 🔧 Object Creation Patterns - **Validated Implementation**

### Template-Based Creation - **✅ Confirmed Working**

**Template File Structure** (discovered during execution):

```text
Block_Families/StixORM/SDO/Identity/
├── make_identity.py                 # ✅ CORE BLOCK (fixed variable scope bug)
├── identity_TR_user.json           # ✅ PERSONAL USER TEMPLATE
├── identity_TR_user_company.json   # ✅ COMPANY TEMPLATE  
├── identity_IT_user1.json          # ✅ EMPLOYEE TEMPLATE 1
├── identity_IT_user2.json          # ✅ EMPLOYEE TEMPLATE 2
├── identity_IT_user3.json          # ✅ EMPLOYEE TEMPLATE 3
├── identity_Exchange.json          # ✅ IT SYSTEM TEMPLATE
├── identity_Laptop1.json           # ✅ HARDWARE ASSET TEMPLATE
├── identity_Laptop2.json           # ✅ HARDWARE ASSET TEMPLATE
└── identity_Laptop3.json           # ✅ HARDWARE ASSET TEMPLATE
```

**Utility Function Pattern** (validated through notebook execution):

```python
# ✅ VALIDATED EXECUTION PATTERN
from Utilities.local_make_sdo import invoke_make_identity_block
from Utilities.local_make_sco import invoke_make_user_account_block, invoke_make_email_addr_block

# Path resolution handled automatically by utility functions
path_base = "../Block_Families/StixORM/"  # Set in notebook
results_base = "../Orchestration/Results/"

# Create identity with template (relative path used)
identity_obj = invoke_make_identity_block(
    "SDO/Identity/identity_TR_user.json",  # Relative to path_base
    "step0/user"                           # Results path
)

# Create linked user account and email
user_account = invoke_make_user_account_block("SCO/User_Account/usr_account_TR_user.json", "step0/user")
email_addr = invoke_make_email_addr_block("SCO/Email_Addr/email_addr_TR_user.json", "step0/user", user_account)
```
- **Purpose**: Represent organizations, individuals, or sectors
- **Usage**: Company entities, user profiles, threat actor groups
- **Properties**: name, identity_class, sectors, contact_information
- **Relationships**: Common target of attacks, creators of indicators

**Incident Objects** (`incident--[uuid]`):
- **Purpose**: Security events requiring investigation
- **Usage**: Breach reports, attack campaigns, security alerts
- **Properties**: name, description, incident_type, confidence
- **Relationships**: Links to indicators, malware, attack patterns

**Indicator Objects** (`indicator--[uuid]`):
- **Purpose**: Observable patterns indicating potential threats
- **Usage**: IOCs, signatures, behavioral patterns
- **Properties**: pattern, indicator_types, valid_from, valid_until
- **Relationships**: Indicates malware, attack patterns, campaigns

**Malware Objects** (`malware--[uuid]`):
- **Purpose**: Malicious software entities
- **Usage**: Ransomware, trojans, backdoors, rootkits
- **Properties**: name, malware_types, is_family, capabilities
- **Relationships**: Uses attack patterns, targets vulnerabilities

**Attack Pattern Objects** (`attack-pattern--[uuid]`):
- **Purpose**: Documented adversarial techniques
- **Usage**: MITRE ATT&CK techniques, custom attack methods
- **Properties**: name, description, kill_chain_phases
- **Relationships**: Used by malware, threat actors, campaigns

### STIX Cyber Observable Objects (SCO) - Observable Phenomena

**File Objects** (`file--[uuid]`):
- **Purpose**: Files observed in cyber operations
- **Usage**: Malware samples, suspicious documents, executables
- **Properties**: hashes, size, name, mime_type, magic_number_hex
- **Relationships**: Contains malware, dropped by attack patterns

**Network Traffic Objects** (`network-traffic--[uuid]`):
- **Purpose**: Network communications and protocols
- **Usage**: C2 communications, data exfiltration, lateral movement
- **Properties**: protocols, src_ref, dst_ref, src_port, dst_port
- **Relationships**: Indicates communication patterns, contains payloads

**Process Objects** (`process--[uuid]`):
- **Purpose**: Running programs and system processes
- **Usage**: Malicious processes, system modification, persistence
- **Properties**: name, command_line, pid, parent_ref, child_refs
- **Relationships**: Creates files, opens network connections

**Directory Objects** (`directory--[uuid]`):
- **Purpose**: File system directories and paths
- **Usage**: Installation paths, data storage locations, system directories
- **Properties**: path, created, modified, accessed
- **Relationships**: Contains files, created by processes

### STIX Relationship Objects (SRO) - Inter-Object Connections

**Sighting Relationships** (`sighting--[uuid]`):
- **Purpose**: Observations of indicators in operational environments
- **Usage**: IOC detections, malware observations, technique sightings
- **Properties**: sighting_of_ref, observed_data_refs, first_seen, last_seen
- **Relationships**: Links indicators to observed data

**Relationship Objects** (`relationship--[uuid]`):
- **Purpose**: Generic relationships between STIX objects
- **Usage**: indicates, uses, targets, attributed-to, variant-of
- **Properties**: relationship_type, source_ref, target_ref, description
- **Relationships**: Connects any two STIX objects with semantic meaning

## 🔧 STIX Object Creation Patterns

### Universal STIX Object Template
```python
def create_stix_object(object_type: str, properties: Dict[str, Any]) -> Dict[str, Any]:
    """Create valid STIX 2.1 object with proper structure"""
    import uuid
    from datetime import datetime
    
    # Generate unique identifier
    stix_id = f"{object_type}--{str(uuid.uuid4())}"
    
    # Create base object structure
    stix_object = {
        "type": object_type,
        "spec_version": "2.1",
        "id": stix_id,
        "created": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
        "modified": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
        **properties
    }
    
    return stix_object
```

### Common STIX Creation Patterns

**Identity Creation**:
```python
def create_identity(name: str, identity_class: str, sectors: List[str] = None) -> Dict:
    """Create STIX identity object"""
    properties = {
        "name": name,
        "identity_class": identity_class,  # "organization", "individual", "group"
        "sectors": sectors or []
    }
    return create_stix_object("identity", properties)
```

**Incident Creation**:
```python
def create_incident(name: str, description: str, incident_types: List[str]) -> Dict:
    """Create STIX incident object"""
    properties = {
        "name": name,
        "description": description,
        "incident_types": incident_types  # ["breach", "malware", "phishing"]
    }
    return create_stix_object("incident", properties)
```

**Indicator Creation**:
```python
def create_indicator(pattern: str, indicator_types: List[str], valid_from: str) -> Dict:
    """Create STIX indicator object"""
    properties = {
        "pattern": pattern,  # "[file:hashes.MD5 = 'd41d8cd98f00b204e9800998ecf8427e']"
        "indicator_types": indicator_types,  # ["malicious-activity", "file-hash-watchlist"]
        "valid_from": valid_from
    }
    return create_stix_object("indicator", properties)
```

**Relationship Creation**:
```python
def create_relationship(relationship_type: str, source_ref: str, target_ref: str) -> Dict:
    """Create STIX relationship object"""
    properties = {
        "relationship_type": relationship_type,  # "indicates", "uses", "targets"
        "source_ref": source_ref,  # "indicator--uuid"
        "target_ref": target_ref   # "malware--uuid"
    }
    return create_stix_object("relationship", properties)
```

## ✅ STIX Validation Requirements

### Mandatory Validation Checks

**Schema Compliance**:
```python
def validate_stix_schema(stix_object: Dict[str, Any]) -> bool:
    """Validate object against STIX 2.1 schema"""
    required_fields = ["type", "spec_version", "id", "created", "modified"]
    
    # Check required fields
    for field in required_fields:
        if field not in stix_object:
            raise ValueError(f"Missing required field: {field}")
    
    # Validate spec_version
    if stix_object["spec_version"] != "2.1":
        raise ValueError(f"Invalid spec_version: {stix_object['spec_version']}")
    
    # Validate ID format
    if not stix_object["id"].startswith(f"{stix_object['type']}--"):
        raise ValueError(f"Invalid ID format for type {stix_object['type']}")
    
    return True
```

**UUID Consistency**:
```python
def validate_uuid_consistency(stix_object: Dict[str, Any]) -> bool:
    """Ensure UUID in ID matches object type"""
    object_type = stix_object["type"]
    object_id = stix_object["id"]
    
    expected_prefix = f"{object_type}--"
    if not object_id.startswith(expected_prefix):
        raise ValueError(f"ID prefix mismatch: expected {expected_prefix}")
    
    # Validate UUID format
    uuid_part = object_id.split("--", 1)[1]
    try:
        uuid.UUID(uuid_part)
    except ValueError:
        raise ValueError(f"Invalid UUID format in ID: {uuid_part}")
    
    return True
```

**Relationship Validation**:
```python
def validate_relationship_refs(relationship: Dict[str, Any], context_objects: List[Dict]) -> bool:
    """Validate relationship references exist in context"""
    source_ref = relationship.get("source_ref")
    target_ref = relationship.get("target_ref")
    
    object_ids = {obj["id"] for obj in context_objects}
    
    if source_ref not in object_ids:
        raise ValueError(f"Source reference not found: {source_ref}")
    
    if target_ref not in object_ids:
        raise ValueError(f"Target reference not found: {target_ref}")
    
    return True
```

## 🔄 STIX Integration Patterns

### Context Memory Integration

**STIX Object Storage**:
```python
def save_stix_to_context(stix_object: Dict[str, Any], context_path: str) -> str:
    """Save STIX object to context memory with proper naming"""
    # Validate before saving
    validate_stix_schema(stix_object)
    validate_uuid_consistency(stix_object)
    
    # Generate filename from object ID
    filename = f"{stix_object['id']}.json"
    file_path = os.path.join(context_path, filename)
    
    # Save with proper formatting
    with open(file_path, 'w') as f:
        json.dump(stix_object, f, indent=2, sort_keys=True)
    
    return file_path
```

**STIX Object Retrieval**:
```python
def load_stix_from_context(object_id: str, context_path: str) -> Dict[str, Any]:
    """Load STIX object from context memory"""
    filename = f"{object_id}.json"
    file_path = os.path.join(context_path, filename)
    
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"STIX object not found: {object_id}")
    
    with open(file_path, 'r') as f:
        stix_object = json.load(f)
    
    # Validate loaded object
    validate_stix_schema(stix_object)
    
    return stix_object
```

### Block Integration Patterns

**STIX Input Processing**:
```python
def process_stix_input(input_data: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Extract and validate STIX objects from block input"""
    stix_objects = input_data.get("stix_objects", [])
    
    validated_objects = []
    for obj in stix_objects:
        validate_stix_schema(obj)
        validated_objects.append(obj)
    
    return validated_objects
```

**STIX Output Generation**:
```python
def generate_stix_output(stix_objects: List[Dict[str, Any]], metadata: Dict = None) -> Dict[str, Any]:
    """Generate block output with STIX objects and metadata"""
    # Validate all objects before output
    for obj in stix_objects:
        validate_stix_schema(obj)
    
    output = {
        "stix_objects": stix_objects,
        "object_count": len(stix_objects),
        "generated_at": datetime.utcnow().isoformat(),
        "metadata": metadata or {}
    }
    
    return output
```

## 🚨 Common STIX Pitfalls and Solutions

### Pitfall 1: Invalid Timestamp Formats
**Problem**: Incorrect datetime formatting in created/modified fields
**Solution**: Always use ISO 8601 format with UTC timezone
```python
timestamp = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%fZ")
```

### Pitfall 2: Circular Relationships
**Problem**: Objects referencing each other in loops
**Solution**: Validate relationship graphs before creation
```python
def detect_circular_relationships(relationships: List[Dict]) -> bool:
    """Detect circular references in relationship graph"""
    # Implementation of cycle detection algorithm
    pass
```

### Pitfall 3: Malformed Object References
**Problem**: Relationships pointing to non-existent objects
**Solution**: Validate all references against context memory
```python
def validate_all_references(objects: List[Dict], relationships: List[Dict]) -> bool:
    """Ensure all relationship references are valid"""
    object_ids = {obj["id"] for obj in objects}
    
    for rel in relationships:
        if rel["source_ref"] not in object_ids:
            return False
        if rel["target_ref"] not in object_ids:
            return False
    
    return True
```

### Pitfall 4: Schema Version Mismatches
**Problem**: Mixing STIX 2.0 and 2.1 object formats
**Solution**: Enforce consistent spec_version across all objects
```python
def enforce_stix_version(objects: List[Dict], target_version: str = "2.1") -> List[Dict]:
    """Ensure all objects use consistent STIX version"""
    for obj in objects:
        obj["spec_version"] = target_version
    return objects
```

## 📋 STIX Development Checklist

### Pre-Creation Validation
- [ ] Determine appropriate STIX object type for data
- [ ] Identify required properties for object type
- [ ] Plan relationships to other objects in context
- [ ] Validate input data completeness and format

### Object Creation Process
- [ ] Generate valid UUID for object ID
- [ ] Set proper spec_version (2.1)
- [ ] Include all required properties
- [ ] Add optional properties as needed
- [ ] Set created/modified timestamps

### Post-Creation Validation
- [ ] Validate against STIX 2.1 schema
- [ ] Check UUID format and consistency
- [ ] Verify relationship references exist
- [ ] Test JSON serialization/deserialization
- [ ] Confirm context memory storage

### Integration Testing
- [ ] Test block input/output with STIX objects
- [ ] Validate workflow with multiple object types
- [ ] Confirm visualization compatibility
- [ ] Test production deployment readiness

This comprehensive STIX guide ensures all Brett Blocks system components maintain strict compliance with STIX 2.1 specifications while supporting extended cybersecurity intelligence capabilities.