# Template-Driven Architecture

## 🎯 Overview

The Brett Blocks StixORM system implements a sophisticated **template-driven architecture** where class templates define both STIX object structure and Python function interfaces. This architecture ensures consistent, scalable object creation with automatic foreign key parameter generation, validated through practical execution.

## 🏗️ Three-File Architecture Pattern

### File Type Roles

Each StixORM block directory contains exactly three file types that work together:

```text
BlockType/
├── ClassName_template.json      # Class Template - defines structure & interface
├── objectname_variant1.json     # Data Template - provides actual values
├── objectname_variant2.json     # Data Template - additional sample data
├── objectname_variantN.json     # Data Template - multiple variants available
└── make_objecttype.py          # Python Block - processes data using template
```

**Actual Pattern Examples**:

```text
Identity/
├── Identity_template.json       # Class definition with property types
├── identity_IT_user1.json       # Sample IT user identity
├── identity_IT_user2.json       # Another IT user variant
├── identity_Exchange.json       # Exchange server identity
├── identity_TR_user.json        # Threat research user
├── identity_team1.json          # Team identity
└── make_identity.py            # Python processor

Email_Addr/
├── EmailAddress_template.json   # Class definition
├── email_addr_IT_user1.json     # IT user email address
├── email_addr_THREAT.json       # Threat actor email
├── email_addr_TR_user.json      # Researcher email
└── make_email_addr.py          # Python processor
```

#### 1. Class Template (`*_template.json`)

**Purpose**: Defines object structure with property types that drive code generation

**Key Characteristics**:
- Always named `ClassName_template.json` (e.g., `Identity_template.json`, `EmailAddress_template.json`)
- Contains property type definitions that generate function parameters
- Defines the complete structure including extensions and sub-objects
- Single template per object type

**Structure**: Contains six sections defining the complete object architecture:

```json
{
  "class_name": "Identity",
  "Identity_template": {
    "_type": "identity",
    "base_required": {
      "type": {"property": "TypeProperty", "parameters": {"value": "_type"}},
      "id": {"property": "IDProperty", "parameters": {"value": "_type"}}
    },
    "base_optional": {
      "created_by_ref": {"property": "ReferenceProperty", "parameters": {"valid_types": ["identity"]}}
    },
    "object": {
      "name": {"property": "StringProperty", "parameters": {"required": true}},
      "identity_class": {"property": "OpenVocabProperty", "parameters": {"vocab": "IDENTITY_CLASS"}}
    },
    "extensions": {
      "extension-definition--66e2492a-bbd3-4be6-88f5-cc91a017a498": {
        "email_addresses": {"collection": "ListProperty", "property": "EmbeddedObjectProperty", "parameters": {"type": "EmailContact"}}
      }
    },
    "sub": {
      "EmailContact": {
        "email_address_ref": {"property": "ReferenceProperty", "parameters": {"valid_types": ["email-addr"]}}
      }
    }
  }
}
```

#### 2. Data Template (`*.json`)

**Purpose**: Provides actual values that populate the class template structure

**Key Characteristics**:
- Multiple files per object type with descriptive names (e.g., `identity_IT_user1.json`, `identity_Exchange.json`)
- Contains the same structure as class template but with actual values instead of property definitions
- Named to indicate the specific use case or variant
- Used for testing, examples, and data population

**Structure**: Mirrors class template structure but with actual data values:

```json
{
  "identity_form": {
    "base_required": {
      "type": "identity",
      "id": "",
      "created": "",
      "modified": ""
    },
    "base_optional": {
      "created_by_ref": "",
      "labels": []
    },
    "object": {
      "name": "John Smith",
      "identity_class": "individual"
    },
    "extensions": {
      "extension-definition--66e2492a-bbd3-4be6-88f5-cc91a017a498": {
        "email_addresses": []
      }
    },
    "sub": {
      "email_addresses": [
        {"digital_contact_type": "work"}
      ]
    }
  }
}
```

**Data Template Naming Patterns**:
- `identity_IT_user1.json` - IT department user identity
- `identity_Exchange.json` - Microsoft Exchange server identity  
- `identity_team1.json` - Team or group identity
- `email_addr_THREAT.json` - Threat actor email address
- `phishing_incident.json` - Phishing investigation incident

#### 3. Python Block (`make_*.py`)

**Purpose**: Processes data templates using class template definitions

**Key Characteristics**:
- Always named `make_objecttype.py` (e.g., `make_identity.py`, `make_email_addr.py`)
- Function signature automatically determined by foreign key properties in class template
- Contains the logic to process data templates and create STIX objects
- Single Python file per object type

**Class Template Drives Python File Structure**: The class template directly explains and determines the structure of each Python file through several mechanisms:

##### Function Signature Generation

**Template ReferenceProperty entries** → **Python function parameters**

```json
// In Identity_template.json sub section:
"EmailContact": {
  "email_address_ref": {"property": "ReferenceProperty", "parameters": {"valid_types": ["email-addr"]}}
},
"SocialMediaContact": {
  "user_account_ref": {"property": "ReferenceProperty", "parameters": {"valid_types": ["user-account"]}}
}
```

**Automatically generates**:
```python
def make_identity(identity_form, email_addr=None, user_account=None):
```

##### Import Requirements

**Template property types** → **Required Python imports**

```json
// Template references these types:
"property": "EmbeddedObjectProperty", "parameters": {"type": "ContactNumber"}
"property": "EmbeddedObjectProperty", "parameters": {"type": "EmailContact"}
"property": "EmbeddedObjectProperty", "parameters": {"type": "SocialMediaContact"}
```

**Requires these imports**:
```python
from stixorm.module.definitions.os_threat import (
    ContactNumber, EmailContact, SocialMediaContact, IdentityContact
)
```

##### Processing Logic Structure

**Template sections** → **Python processing steps**

```json
// Template has 6 sections:
{
  "_type": "identity",
  "base_required": {...},
  "base_optional": {...},
  "object": {...},
  "extensions": {...},
  "sub": {...}
}
```

**Python follows this exact structure**:
```python
def make_identity(identity_form, email_addr=None, user_account=None):
    # 1. Extract the components matching template sections
    required = identity_form["base_required"]
    optional = identity_form["base_optional"] 
    main = identity_form["object"]
    extensions = identity_form["extensions"]
    sub = identity_form["sub"]
    
    # 2. Process each section in order
    for k, v in main.items():        # Process "object" section
        contents[k] = v
    for k, v in optional.items():    # Process "base_optional" section
        contents[k] = v
    for k,v in sub.items():          # Process "sub" section
        if k == "contact_numbers":   # Handle EmbeddedObjectProperty
            stix_list.append(ContactNumber(**val))
        if k == "email_addresses":   # Handle ReferenceProperty assignment
            if email_addr:
                val["email_address_ref"] = email_addr["id"]
```

##### Sub-object Handling

**Template sub-objects** → **Python sub-object creation logic**

```json
// Template defines sub-objects:
"sub": {
  "ContactNumber": {...},
  "EmailContact": {...},
  "SocialMediaContact": {...}
}
```

**Python creates them in order**:
```python
# Each sub-object becomes a conditional processing block
for k,v in sub.items():
    if k == "contact_numbers":
        stix_list.append(ContactNumber(**val))
    if k == "email_addresses": 
        stix_list.append(EmailContact(**val))
    if k == "social_media_accounts":
        stix_list.append(SocialMediaContact(**val))
```

##### Timestamp Handling

**Template TimestampProperty** → **Python timestamp conversion**

```json
// Template has timestamp properties:
"created": {"property": "TimestampProperty", "parameters": {...}},
"modified": {"property": "TimestampProperty", "parameters": {...}}
```

**Python includes timestamp conversion**:
```python
def convert_dt(dt_stamp_string):
    # Conversion logic for millisecond precision
    
# Applied to timestamp fields
time_list = ["created", "modified"]
for tim in time_list:
    if tim in stix_dict:
        temp_string = convert_dt(stix_dict[tim])
        stix_dict[tim] = temp_string
```

**Complete Template-to-Python Mapping**:
1. **Template property types** → **Python import statements**
2. **Template ReferenceProperty** → **Python function parameters**
3. **Template sections** → **Python processing order**
4. **Template sub-objects** → **Python sub-object creation logic**
5. **Template extensions** → **Python extension handling**
6. **Template TimestampProperty** → **Python timestamp conversion**

This demonstrates that the class template is not just a data definition - it's a **complete specification** for the Python file structure, imports, function signature, and processing logic.

```python
def make_identity(identity_form, email_addr=None, user_account=None):
    # Function signature automatically determined by template foreign keys
    # email_addr parameter comes from ReferenceProperty in sub.EmailContact
    # user_account parameter comes from ReferenceProperty in sub.SocialMediaContact
    
    required = identity_form["base_required"]
    optional = identity_form["base_optional"]
    main = identity_form["object"]
    extensions = identity_form["extensions"]
    sub = identity_form["sub"]
    
    # Process sub-objects with foreign key assignment
    for k, v in sub.items():
        if k == "email_addresses":
            for i, val in enumerate(v):
                if email_addr:
                    val["email_address_ref"] = email_addr["id"]  # Foreign key assignment
                stix_list.append(EmailContact(**val))
    
    # Create main object
    stix_obj = Identity(**empties_removed)
    return stix_obj.serialize()
```

## 🔗 Foreign Key Parameter Generation

### Property Types That Generate Parameters

**Critical Understanding**: The StixORM system automatically scans class templates and generates Python function parameters based on specific property types.

#### ReferenceProperty

Standard STIX foreign key references that become function parameters:

```json
"created_by_ref": {"property": "ReferenceProperty", "parameters": {"valid_types": ["identity"]}}
"belongs_to_ref": {"property": "ReferenceProperty", "parameters": {"valid_types": ["user-account"]}}
"email_address_ref": {"property": "ReferenceProperty", "parameters": {"valid_types": ["email-addr"]}}
```

#### OSThreatReference

OS-Threat specific foreign key references for complex relationships:

```json
"sequence_start_refs": {"property": "OSThreatReference", "parameters": {"valid_types": ["sequence"]}}
"event_refs": {"property": "OSThreatReference", "parameters": {"valid_types": ["event"]}}
"impact_refs": {"property": "OSThreatReference", "parameters": {"valid_types": ["impact"]}}
```

### Template Scanning Process

The system scans all template sections to identify foreign key properties:

1. **base_required**: Standard STIX required properties
2. **base_optional**: Standard STIX optional properties  
3. **object**: Object-specific properties
4. **extensions**: Extension properties (within extension definitions)
5. **sub**: Sub-object properties (embedded objects)

### Function Signature Examples

**Simple Case** (Email Address):
```json
// Template has: "belongs_to_ref": {"property": "ReferenceProperty"}
```
```python
def make_email_addr(email_addr_form, usr_account=None):
```

**Complex Case** (Incident):
```json
// Template has multiple OSThreatReference properties
```
```python
def make_incident(incident_form, sequence_start_refs=None, sequence_refs=None, 
                 task_refs=None, event_refs=None, impact_refs=None, other_object_refs=None):
```

## 🏛️ Template Structure Specification

### Six Core Sections

Every class template contains exactly six sections:

#### 1. `_type` (Required)
Valid STIX type identifier
```json
"_type": "identity"
```

#### 2. `base_required` (Required)
Fixed properties for all STIX objects in the group (SDO, SRO, SCO, Meta)
```json
"base_required": {
  "type": {"property": "TypeProperty", "parameters": {"value": "_type"}},
  "spec_version": {"property": "StringProperty", "parameters": {"fixed": "2.1"}},
  "id": {"property": "IDProperty", "parameters": {"value": "_type"}}
}
```

#### 3. `base_optional` (Optional)
Optional properties common to all STIX objects
```json
"base_optional": {
  "created_by_ref": {"property": "ReferenceProperty", "parameters": {"valid_types": ["identity"]}},
  "labels": {"collection": "ListProperty", "property": "StringProperty", "parameters": {}},
  "external_references": {"collection": "ListProperty", "property": "ExternalReference", "parameters": {}}
}
```

#### 4. `object` (Required)
Object-specific properties including simple and composite types
```json
"object": {
  "name": {"property": "StringProperty", "parameters": {"required": true}},
  "description": {"property": "StringProperty", "parameters": {}},
  "identity_class": {"property": "OpenVocabProperty", "parameters": {"vocab": "IDENTITY_CLASS"}}
}
```

#### 5. `extensions` (Optional)
Extension definitions with their own property sets
```json
"extensions": {
  "extension-definition--66e2492a-bbd3-4be6-88f5-cc91a017a498": {
    "extension_type": {"property": "StringProperty", "parameters": {"fixed": "property-extension"}},
    "contact_numbers": {"collection": "ListProperty", "property": "EmbeddedObjectProperty", "parameters": {"type": "ContactNumber"}}
  }
}
```

#### 6. `sub` (Optional)
Sub-object definitions called by EmbeddedObjectProperty
```json
"sub": {
  "ContactNumber": {
    "contact_number_type": {"property": "StringProperty", "parameters": {"required": true}},
    "contact_number": {"property": "StringProperty", "parameters": {"required": true}}
  },
  "EmailContact": {
    "digital_contact_type": {"property": "StringProperty", "parameters": {"required": true}},
    "email_address_ref": {"property": "ReferenceProperty", "parameters": {"valid_types": ["email-addr"]}}
  }
}
```

## 🔄 Data Flow Process

### 1. Template Analysis
System scans class template for ReferenceProperty and OSThreatReference types

### 2. Function Generation
Python function signature automatically includes parameters for each foreign key property

### 3. Data Processing
Data template values are processed using the class template structure

### 4. Foreign Key Assignment
Foreign key parameters are assigned to appropriate object properties

### 5. Object Creation
StixORM creates the final STIX object with all relationships intact

## 🎯 Architecture Benefits

### Template-Driven Consistency
- **Single Source of Truth**: Class templates define both structure and interface
- **Automatic Code Generation**: Function signatures generated from templates
- **Type Safety**: Property types ensure correct foreign key handling

### Scalability
- **Modular Design**: Each object type is self-contained
- **Extensible Pattern**: New objects follow the same three-file pattern
- **Foreign Key Automation**: No manual parameter management required

### Maintainability
- **Clear Separation**: Structure (template) vs. data (values) vs. logic (Python)
- **Consistent Patterns**: All blocks follow identical architecture
- **Validation**: Template structure ensures proper STIX compliance

This template-driven architecture provides the foundation for scalable, maintainable cybersecurity intelligence operations with automatic foreign key relationship management.