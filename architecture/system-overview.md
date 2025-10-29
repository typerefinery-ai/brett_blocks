# Brett Blocks System Overview

## 🎯 System Purpose

Brett Blocks is a **cybersecurity intelligence platform** that combines Python-based atomic blocks with STIX 2.1 objects to create sophisticated threat analysis and incident response capabilities. The system operates in a **dual-environment architecture** enabling both development/testing and production deployment.

## 🏗️ Core Architecture

### Template-Driven StixORM System

**Critical Understanding**: Brett Blocks implements a sophisticated template-driven architecture where class templates define both STIX object structure and Python function interfaces, ensuring automatic foreign key parameter generation.

#### Three-File Pattern Per Block

```text
BlockType/
├── ClassName_template.json      # Defines structure & auto-generates function interface
├── objectname_variant.json      # Provides actual values for template population
└── make_objecttype.py          # Processes data using template-driven parameters
```

#### Three-File Pattern Per Block

Each StixORM block directory follows a consistent three-file pattern:

```text
BlockType/
├── ClassName_template.json      # Class Template - defines structure & interface
├── objectname_variant1.json     # Data Template - actual values for testing
├── objectname_variant2.json     # Data Template - additional examples
└── make_objecttype.py          # Python Block - processing logic
```

**Real Examples**:
- `Identity/` contains `Identity_template.json`, `identity_IT_user1.json`, `identity_Exchange.json`, `make_identity.py`
- `Email_Addr/` contains `EmailAddress_template.json`, `email_addr_IT_user1.json`, `email_addr_THREAT.json`, `make_email_addr.py`
- `Incident/` contains `Incident_template.json`, `phishing_incident.json`, `make_incident.py`

#### Foreign Key Parameter Generation

The system automatically scans class templates and generates Python function parameters:

- **ReferenceProperty**: Standard STIX foreign key references
- **OSThreatReference**: OS-Threat specific foreign key references

**Example**: Class template contains:

```json
"sequence_start_refs": {"property": "OSThreatReference", "parameters": {"valid_types": ["sequence"]}}
"event_refs": {"property": "OSThreatReference", "parameters": {"valid_types": ["event"]}}
```

**Automatically generates function signature**:

```python
def make_incident(incident_form, sequence_start_refs=None, event_refs=None, ...):
```

### Dual Environment Design

**Development Environment** (This Repository)

```text
brett_blocks/
├── Block_Families/StixORM/          # ✅ ACTUAL LOCATION - Atomic Python blocks
│   ├── SCO/                         # STIX Cyber Observable Objects  
│   ├── SDO/                         # STIX Domain Objects
│   └── SRO/                         # STIX Relationship Objects
├── Orchestration/                   # Jupyter notebooks for testing/workflows
│   ├── context_mem/                 # Local context memory simulation
│   ├── Utilities/                   # ✅ CRITICAL - Wrapper functions for development
│   └── Step_*.ipynb                 # Educational workflow notebooks
└── .github/instructions/            # AI assistant guidance system
```

**Production Environment** (Total.js Flow)

- Live block execution with real-time data processing
- Production-grade context memory with enterprise storage
- Visual flow orchestration and monitoring
- Enterprise integration capabilities

### Validated Implementation Patterns

**Path Resolution System** (Critical Discovery)

```python
# Utility functions automatically prepend path_base
path_base = "../Block_Families/StixORM/"

# Input paths must be relative to StixORM directory
user_account_path = "SCO/User_Account/usr_account_TR_user.json"  # ✅ CORRECT
# NOT: "../Block_Families/StixORM/SCO/User_Account/..."         # ❌ WRONG - double path
```

**Block Error Handling Issues** (Fixed During Testing)

- Variable scope bugs in block main() functions
- Missing file existence validation
- Inconsistent error reporting
- Need for standardized exception handling

## 🧱 Block Architecture (Validated)

### STIX Object Categories

**SCO (STIX Cyber Observable Objects)**

```text
SCO/
├── Email_Addr/           # Email address objects with user account linking
├── User_Account/         # User account objects with authentication details
├── File/                 # File system objects for malware analysis
├── Network_Traffic/      # Network communication observables
├── Process/              # Running process observables
└── [25+ other types]     # Complete STIX SCO coverage
```

**SDO (STIX Domain Objects)**

```text
SDO/
├── Identity/             # ✅ VERIFIED - Person, organization, system identities
├── Incident/             # Security incident objects
├── Malware/              # Malware family and variant objects
├── Attack_Pattern/       # MITRE ATT&CK technique objects
├── Indicator/            # Threat indicators and IOCs
└── [30+ other types]     # Complete STIX SDO coverage
```

**SRO (STIX Relationship Objects)**

```text
SRO/
├── Relationship/         # Standard STIX relationships
├── Sighting/            # Threat indicator sightings
└── [relationship types] # Custom relationship definitions
```

### Template System (Discovered)

Each block type includes:

- **Template files**: Standardized object creation patterns
- **Sample data files**: Complete test data sets for all object types
- **Validation schemas**: STIX 2.1 compliance checking

## 💾 Context Memory Architecture (Validated Implementation)

### Actual Storage Structure

```text
Orchestration/generated/os-triage/context_mem/
├── context_map.json                    # ✅ VERIFIED - Global context routing
├── usr/                                # Single user workspace (no setup required)
│   ├── cache_me.json                   # User identity objects
│   ├── cache_team.json                 # Team member objects
│   ├── edges.json                      # User relationships
│   ├── relations.json                  # User relationship data
│   ├── relation_edges.json             # Relationship edge data
│   └── relation_replacement_edges.json # Relationship replacements
├── identity--{company-uuid}/            # Company contexts (require initialization)
│   ├── company.json                    # Company identity object
│   ├── users.json                      # Employee objects (categorized)
│   ├── systems.json                    # IT system objects (categorized)
│   ├── assets.json                     # Hardware asset objects (categorized)
│   ├── edges.json                      # Company relationships
│   └── [relationship files]            # Various relationship types
└── incident--{incident-uuid}/           # Incident contexts
    ├── incident.json                   # Core incident object
    ├── sequence_start_refs.json        # Initial attack vectors
    ├── sequence_refs.json              # Attack progression
    ├── impact_refs.json                # Damage assessment
    ├── unattached_objs.json            # Pending classification
    └── [relationship files]            # Incident relationships
```

### Dual-Pattern Context Architecture (Validated)

**User Context Pattern** (`/usr/`)

- **No initialization required** - direct object storage
- **Single tenant** - one user workspace
- **Array-based storage** - multiple objects per file
- **Personal scope** - user identity and immediate team

**Company Context Pattern** (`/identity--{uuid}/`)

- **Explicit initialization required** - `invoke_create_company_context()`
- **Multi-tenant support** - UUID-based isolation
- **Category-based storage** - objects organized by type
- **Enterprise scope** - organizational infrastructure

### Object Storage Format (Validated)

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

**Key Features:**

- **`original` field**: Contains pure STIX 2.1 data (what blocks process)
- **UI metadata**: Provides display information for visualization
- **Array storage**: Multiple objects per context file
- **Append pattern**: Preserves object history and relationships

## 🔧 Utility Function Framework (Critical Discovery)

### Development Simulation Layer

The `Orchestration/Utilities/` directory contains **wrapper functions** that simulate production behavior:

**Context Management Functions**

```python
# Company context operations
invoke_create_company_context(context_type, input_data)     # Initialize company context
invoke_save_company_context_block(obj_path, context_path, context_type)  # Save with categorization

# User context operations  
invoke_save_user_context_block(obj_path, context_path)      # Save to user context
invoke_save_team_context_block(obj_path, context_path)      # Save to team context
```

**STIX Object Creation Functions**

```python
# Identity objects
invoke_make_identity_block(ident_path, results_path, email_results=None, acct_results=None)

# Observable objects
invoke_make_user_account_block(user_path, results_path)
invoke_make_email_addr_block(email_path, results_path, user_account_obj)

# Relationship objects
invoke_sro_block(sro_path, results_path)
invoke_update_company_relations_block(config_path, results_path)
```

### Path Management System

**Critical Pattern Discovery:**

```python
# Utility functions automatically prepend path_base
path_base = "../Block_Families/StixORM/"

# Input paths MUST be relative to StixORM directory
correct_path = "SCO/User_Account/usr_account_TR_user.json"     # ✅ WORKS
incorrect_path = "../Block_Families/StixORM/SCO/User_Account/..." # ❌ FAILS - double path
```

## 📊 Data Flow Patterns (Validated)

### Development Workflow

```text
Input Data Files → Utility Functions → Block Execution → STIX Objects → Context Memory
      ↓                    ↓                 ↓              ↓             ↓
Template Files    Path Resolution    JSON Processing   Validation    Persistent Storage
```

### Context Memory Operations

```text
Object Creation → Dual-Layer Format → Category Storage → Context Routing → Relationship Tracking
      ↓                 ↓                    ↓              ↓                  ↓
   STIX + UI       Array Append        users.json     context_map.json    edges.json
```

## 🎯 Educational Notebook System

### Step-Based Learning Progression

**Step_0_User_Setup.ipynb** - Personal identity and team setup

- User context creation (`/usr/` directory)
- Personal identity objects (account, email, identity)
- Team member identity objects
- No company setup required

**Step_1_Company_Setup.ipynb** - Organizational infrastructure

- Company context initialization (`/identity--{uuid}/` directory)
- Employee identity objects (categorized storage)
- IT system identities (infrastructure modeling)
- Hardware asset identities (physical security)

### Notebook Architecture Patterns

**Error Handling Discoveries:**

- Block code quality issues require fixes
- Path management critical for success
- File existence validation needed
- Comprehensive error reporting essential

**Documentation Integration:**

- Notebooks serve as executable documentation
- Step-by-step progression for learning
- Real system behavior demonstration
- Architecture validation through execution

## 🔍 Quality Assurance Findings

### Block Code Issues (Found & Fixed)

1. **Variable Scope Bugs**: Fixed `input_data` scope in `make_user_account.py`
2. **Error Handling Gaps**: Missing file existence checks
3. **Path Resolution**: Double path concatenation issues
4. **Naming Conventions**: Mixed camelCase/snake_case usage

### System Reliability Patterns

- **Defensive Programming**: All utility functions should validate inputs
- **Path Normalization**: Standardize relative path handling
- **Error Recovery**: Graceful handling of missing data files
- **Comprehensive Logging**: Track all operations for debugging

## 🚀 Operational Insights

### Ready-for-Use Components

- **Complete Sample Data**: All test data files exist and are properly formatted
- **Validated Context Memory**: Dual-pattern architecture works as designed
- **Functional Utility Layer**: Development simulation layer operational
- **Educational Materials**: Step-by-step learning notebooks complete

### Development Recommendations

1. **Standardize Error Handling**: Implement consistent error patterns across all blocks
2. **Path Management Library**: Create standardized path resolution utilities
3. **Validation Framework**: Comprehensive STIX object validation
4. **Testing Automation**: Automated testing of all block functionality
5. **Documentation Sync**: Keep documentation aligned with actual implementation

This system provides a robust foundation for cybersecurity intelligence operations with clear separation between development and production environments, comprehensive STIX 2.1 support, and sophisticated context memory management.