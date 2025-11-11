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

## 🔍 Quality Assurance & Testing

### StixORM Testing System (Nov 2025)

**Complete testing system achieving 100% pass rate** - validates the entire template-driven architecture from object discovery through reconstitution.

**See:** [stixorm-testing-system-design.md](stixorm-testing-system-design.md) for complete details.

#### 5-Phase Testing Pipeline

```
Discovery → Data Form Generation → Block Execution → Verification → Reporting
  53         100% success           100% success      100% pass    Reports
objects      (53/53)                (53/53)           (53/53)      Generated
```

**Key Achievements:**
- ✅ **100% pass rate** (53/53 objects across 15 STIX types)
- ✅ **100% execution success** using STIXReconstitutionEngine
- ✅ **All 18 test cases passing**
- ✅ **<1 second execution time**
- ✅ **Zero structural differences** in comparison

**Testing Validates:**
1. **Template-Driven Architecture** - All make_*.py blocks execute with correct signatures
2. **Data Form Generation** - 100% conversion success via convert_object_list_to_data_forms.py
3. **Reconstitution Engine** - Production-proven engine (99.3% → 100% focused accuracy)
4. **Reference Restoration** - Automatic ID mapping and dependency ordering
5. **STIX Compliance** - Structural comparison confirms specification adherence

**Integration Points:**
- Uses `Orchestration/Utilities/convert_object_list_to_data_forms.py` for data form generation
- Uses `Orchestration/Utilities/reconstitute_object_list.py` (STIXReconstitutionEngine) for execution
- Uses `Block_Families/General/_library/parse.py` for object metadata
- Validates all components working together in production-ready configuration

#### Performance Evolution

| Phase | Implementation | Pass Rate | Key Issue |
|-------|---------------|-----------|-----------|
| 1 | Custom BlockExecutor | 9.4% | Manual execution, missing dependencies |
| 2 | Engine + Type Matching | 49.1% | Type+name matching unreliable |
| 3 | Engine + Index Mapping | **100%** | **All issues resolved** |

**Critical Technical Decisions:**
1. Use STIXReconstitutionEngine (production-proven, not custom executor)
2. Deterministic index-based mapping via creation_sequence
3. Manual UUID normalization (portable across DeepDiff versions)
4. Session-scoped pytest fixtures for performance

### Block Code Quality (Historical Issues - Now Tested)

**Previous Issues Found & Fixed:**
1. **Variable Scope Bugs**: Fixed `input_data` scope in `make_user_account.py`
2. **Error Handling Gaps**: Missing file existence checks
3. **Path Resolution**: Double path concatenation issues
4. **Naming Conventions**: Mixed camelCase/snake_case usage

**Current State:**
- All 53 testable objects execute successfully (100% pass rate)
- Testing system catches regressions automatically
- Comprehensive error reporting via test reports
- Continuous validation of block code quality

### System Reliability Patterns

- **Automated Testing**: Complete test coverage via pytest framework
- **Defensive Programming**: All utility functions validate inputs
- **Path Normalization**: Standardized path handling in tests
- **Error Recovery**: Graceful handling validated through testing
- **Comprehensive Reporting**: JSON and Markdown test reports

## 🚀 Operational Insights

### Ready-for-Production Components

- **Complete Sample Data**: All test data files exist and are properly formatted
- **Validated Context Memory**: Dual-pattern architecture works as designed
- **Functional Utility Layer**: Development simulation layer operational
- **Educational Materials**: Step-by-step learning notebooks complete
- **Testing Infrastructure**: Production-ready testing achieving 100% pass rate
- **Data Form Pipeline**: Round-trip conversion validated (STIX → Forms → STIX)
- **Reconstitution Engine**: Proven accuracy (99.3% production, 100% focused testing)

### Development & Testing Recommendations

1. **Run Tests Regularly**: `poetry run pytest tests/` validates entire system
2. **Monitor Test Reports**: Check `tests/generated/reports/` for metrics
3. **Validate New Blocks**: Add to `Block_Families/examples/` for automatic testing
4. **Reference Testing Docs**: See [stixorm-testing-system-design.md](stixorm-testing-system-design.md)
5. **Use Proven Utilities**: Leverage tested utilities from `Orchestration/Utilities/`

### System Architecture Interactions

For a complete understanding of how all components interact, see:
- **[system-interaction-map.md](system-interaction-map.md)** - Complete data flow and component interactions
- **[template-driven-architecture.md](template-driven-architecture.md)** - Foundation of the entire system
- **[reconstitution-and-notebook-generation.md](reconstitution-and-notebook-generation.md)** - Data transformation pipeline
- **[stixorm-testing-system-design.md](stixorm-testing-system-design.md)** - Testing & validation architecture

This system provides a **robust, tested, production-ready foundation** for cybersecurity intelligence operations with:
- Clear separation between development and production environments
- Comprehensive STIX 2.1 support validated through testing
- Sophisticated context memory management with automatic routing
- Template-driven architecture ensuring consistency and scalability
- Complete round-trip data transformation with proven accuracy