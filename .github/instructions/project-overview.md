# Brett Blocks System - Template-Driven Architecture Specification

## 🎯 System Mission - **Validated Through Execution**

**Brett Blocks** is a sophisticated cybersecurity intelligence platform implementing a **template-driven architecture** where class templates define both STIX object structure and Python function interfaces. **Validated through practical execution**, the system enables creation, testing, and deployment of atomic Python functions that process STIX 2.1 cybersecurity objects using **automatic foreign key parameter generation** and **confirmed dual-layer object format**.

## 🏗️ Template-Driven Architecture - **Critical Understanding**

### StixORM Template System - **Revolutionary Discovery**

**The core architectural insight**: Brett Blocks uses a sophisticated **three-file pattern** where class templates serve as complete specifications for Python file structure, not just data definitions.

#### Three-File Pattern Per Block

**Every StixORM block directory contains exactly**:

```text
BlockType/
├── ClassName_template.json      # Class Template - defines structure & auto-generates interface
├── objectname_variant1.json     # Data Template - actual values for testing
├── objectname_variant2.json     # Data Template - additional examples  
├── objectname_variantN.json     # Data Template - multiple variants
└── make_objecttype.py          # Python Block - auto-generated structure
```

**Real Examples** (validated in codebase):
- `Identity/`: `Identity_template.json`, `identity_IT_user1.json`, `identity_Exchange.json`, `make_identity.py`
- `Email_Addr/`: `EmailAddress_template.json`, `email_addr_THREAT.json`, `make_email_addr.py`
- `Incident/`: `Incident_template.json`, `phishing_incident.json`, `make_incident.py`

#### Foreign Key Parameter Auto-Generation

**Critical Discovery**: The system automatically scans class templates and generates Python function parameters based on property types.

**Property Types That Generate Parameters**:
- **ReferenceProperty**: Standard STIX foreign key references  
- **OSThreatReference**: OS-Threat specific foreign key references

**Template Example**:
```json
{
  "sub": {
    "EmailContact": {
      "email_address_ref": {"property": "ReferenceProperty", "parameters": {"valid_types": ["email-addr"]}}
    },
    "SocialMediaContact": {
      "user_account_ref": {"property": "ReferenceProperty", "parameters": {"valid_types": ["user-account"]}}
    }
  }
}
```

**Automatically Generates Function Signature**:
```python
def make_identity(identity_form, email_addr=None, user_account=None):
```

#### Template-to-Python Mapping

**Class templates serve as complete Python file specifications**:
1. **Property types** → **Python import statements**
2. **ReferenceProperty entries** → **Function parameters**  
3. **Template sections** → **Python processing order**
4. **Sub-objects** → **Sub-object creation logic**
5. **Extensions** → **Extension handling code**
6. **TimestampProperty** → **Timestamp conversion inclusion**

### Dual Architecture Design - **Validated Implementation**

### Development Environment (This Repository) - **Confirmed Structure**
**Purpose**: Block creation, testing, and workflow prototyping with **validated file structure**

**Components** (confirmed working):
- 🧱 **Block Families**: Organized Python blocks at **`Block_Families/StixORM/`** with **SDO/SCO/SRO** categories
- 🎼 **Orchestration**: Jupyter notebooks for workflow testing using **utility function framework**
- 💾 **Context Memory Simulation**: **Dual-pattern architecture** with user (`/usr/`) and company (`/identity--{uuid}/`) contexts
- 📊 **Visualization**: Data visualization components for UI generation with **dual-layer metadata**

### Production Environment (Total.js Flow Platform) - **Target Integration**
**Purpose**: Real-time block orchestration via **utility function translation**

**Components**:
- 🚀 **Flow Designer**: Visual workflow composition interface
- ⚡ **Block Registry**: Deployed Python blocks translated from **utility function patterns**
- 🌐 **API Generation**: Automatic REST endpoint creation from workflows
- 🔄 **Live Context Memory**: Production-grade state management using **validated storage patterns**

## 🧩 Block Architecture Fundamentals - **Validated Structure**

### Block Categories - **Template-Driven Implementation**

#### StixORM Blocks (`Block_Families/StixORM/`) - **✅ Template-Driven Architecture**

**Purpose**: STIX 2.1 cybersecurity object creation using template-driven automatic code generation

**Template-Driven Structure** (validated across all directories):

**SDO/** (STIX Domain Objects) - **✅ Confirmed Template Pattern**
- `Identity/` - **✅ Complete template system validated**
  - `Identity_template.json` - Class template with ReferenceProperty auto-generation
  - `identity_IT_user1.json`, `identity_Exchange.json`, `identity_team1.json` - Data templates
  - `make_identity.py` - Python block with auto-generated function signature
  
- `Incident/` - **✅ Complex foreign key template validated**  
  - `Incident_template.json` - Multiple OSThreatReference properties
  - `phishing_incident.json` - Phishing investigation data template
  - `make_incident.py` - Auto-generated parameters: `sequence_start_refs`, `event_refs`, `impact_refs`

**SCO/** (STIX Cyber Observable Objects) - **✅ Confirmed Template Pattern**
- `Email_Addr/` - **✅ Simple template pattern validated**
  - `EmailAddress_template.json` - ReferenceProperty for belongs_to_ref
  - `email_addr_IT_user1.json`, `email_addr_THREAT.json` - Data templates  
  - `make_email_addr.py` - Auto-generated parameter: `usr_account=None`

- `User_Account/` - **✅ Confirmed working (fixed variable scope bug)**
  - Complete three-file template pattern implemented

**SRO/** (STIX Relationship Objects) - **Available for Implementation**
- `Relationship/` - Template pattern available for complex relationship modeling

**Critical Template Discoveries**:
1. **Property Type Auto-Generation**: `ReferenceProperty` and `OSThreatReference` automatically become function parameters
2. **Import Requirements**: `EmbeddedObjectProperty` types automatically determine required Python imports  
3. **Processing Order**: Template sections directly map to Python processing logic
4. **Sub-object Creation**: Template sub-objects become conditional Python creation blocks

#### OS_Triage Blocks (`Block_Families/OS_Triage/`) - **Operational Workflows**

**Purpose**: Cybersecurity investigation workflows and UI interactions

**Capabilities**:
- 💾 **Context Management**: Save and retrieve investigation data using dual-pattern architecture
- 📊 **Data Visualization**: Generate UI components with dual-layer metadata  
- 🔄 **Workflow Orchestration**: Coordinate multi-step security analysis
- 📋 **Form Processing**: Handle user input validation and processing
- ⏱️ **Event Processing**: Manage incident timelines and relationships

#### General Blocks (`Block_Families/General/`) - **Utility Framework**

**Purpose**: Common utilities and cross-cutting concerns

**Capabilities**:
- 📦 **Import Management**: Handle external data imports
- 🔄 **Data Transformation**: Generic data processing utilities  
- 📊 **Object Management**: STIX object manipulation helpers

## 🔧 Development Framework - **Validated Utility Functions**

### Utility Function Framework - **✅ Confirmed Working Pattern**

**Critical Discovery**: Development uses **utility function framework** that translates block calls for notebook execution while maintaining Total.js Flow compatibility.

**Validated Path Resolution Pattern**:
```python
# ✅ CONFIRMED WORKING PATTERN
path_base = "../Block_Families/StixORM/"  # Base path set in notebooks
results_base = "../Orchestration/Results/"

# Utility functions automatically prepend path_base to relative paths
# Block calls use RELATIVE paths only:
invoke_make_identity_block("SDO/Identity/identity_TR_user.json", "step0/user")
# Utility function translates to: path_base + "SDO/Identity/identity_TR_user.json"
```

**Key Utility Functions** (validated through execution):

```python
# ✅ STIX Domain Object Creation
from Utilities.local_make_sdo import invoke_make_identity_block

# ✅ STIX Cyber Observable Creation  
from Utilities.local_make_sco import invoke_make_user_account_block, invoke_make_email_addr_block

# ✅ Context Memory Management
from Utilities.local_make_general import invoke_create_company_context
from Utilities.local_make_general import invoke_save_company_context_block

# ✅ Data Processing Utilities
from Utilities.util import emulate_ports, unwind_ports, conv
```

### Context Memory Architecture - **Validated Dual-Pattern**

**User Context Pattern** (confirmed working):
```
context_mem/usr/
├── cache_me.json      # Personal identity objects (array format)
└── cache_team.json    # Team member identities (array format)
```

**Company Context Pattern** (confirmed working):
```
context_mem/identity--{company-uuid}/
├── company.json       # Company identity object
├── users.json         # Employee identities (categorized)
├── systems.json       # IT system identities (categorized)
├── assets.json        # Hardware asset identities (categorized)
└── edges.json         # Organizational relationships
```

**Critical Implementation**: 
- **User contexts**: Simple setup, array-based storage
- **Company contexts**: Requires initialization, category-based organization
- **Context routing**: Global `context_map.json` for multi-tenant support

### STIX Object Creation - **Validated Dual-Layer Format**

**Confirmed Object Structure** (discovered through execution):
```json
{
  "id": "identity--f431f809-377b-45e0-aa1c-6a4751cae5ff",
  "type": "identity",
  "original": {
    // ✅ PURE STIX 2.1 DATA - what blocks process
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

**Key Benefits**:
- **STIX Compliance**: `original` field contains pure STIX 2.1 specification data
- **UI Integration**: Metadata enables rich visualization and interface generation
- **External Compatibility**: Perfect integration with STIX tools and platforms

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

### Block Execution Constraints (CRITICAL)

**Isolation Requirements**:
- ❌ **No Shared Memory**: Blocks cannot share variables or state
- ❌ **No Direct Calls**: Blocks cannot call each other directly  
- ❌ **Limited Imports**: Restricted to approved libraries only
- ✅ **File Communication**: JSON input/output files ONLY

**Input/Output Patterns**:
- 🔄 **No-Input Blocks**: Context memory readers (data slice generators)
- 📝 **Form-Input Blocks**: STIX creators needing structured templates
- 🔄 **Processing Blocks**: Data transformation operations
- 💾 **Output-Only Blocks**: Context memory writers

## 🎼 Orchestration System

### Notebook-Based Workflow Development (`Orchestration/`)

**Purpose**: Design, test, and validate block workflows using Jupyter notebooks

#### Core Workflow Notebooks

1. **Step_0_Build_Initial_Identities.ipynb**
   - **Purpose**: Initialize identity objects for companies and users
   - **Capabilities**: Create foundational STIX identity objects
   - **Context Operations**: Establish baseline identity context
   - **Output**: Identity objects ready for incident association

2. **Step_1_Create_Incident_with_an_Alert.ipynb**
   - **Purpose**: Establish incident context and initial alerting
   - **Capabilities**: Create incident objects, indicators, sighting relationships
   - **Context Operations**: Initialize incident directory structure
   - **Output**: Active incident context ready for investigation workflows

3. **Step_2_Get_the_Anecdote.ipynb**
   - **Purpose**: Develop incident narrative and relationship analysis
   - **Capabilities**: Build complex object relationships, timeline construction
   - **Context Operations**: Populate incident with detailed investigative data
   - **Output**: Comprehensive incident context with rich relationship data

#### Development and Testing Notebooks

**Utility Notebooks**:
- **Test Form Actions.ipynb**: Block capability testing and validation
- **create_tab_dataslice.ipynb**: UI data generation and visualization support
- **Test_Diff.ipynb**: Context memory comparison and analysis
- **vizdata_examples.ipynb**: Visualization data structure examples

**Known Issues**:
- **Step_3 - Create_more_data_for_unattached.ipynb**: Non-compliant format (scheduled for refactoring)
- **try.ipynb**: Experimental template requiring improvement

### Orchestration Utilities (`Orchestration/Utilities/`)

**Purpose**: Abstraction layer between notebook-level operations and block execution

**Core Utility Functions**:

**Path Management**:
```python
def resolve_context_path(context_type: str, object_id: str) -> str:
    """Generate absolute paths to context memory files"""
    
def get_current_context() -> Dict[str, str]:
    """Load and return current context routing information"""
```

**Data Transformation**:
```python  
def prepare_block_input(notebook_data: Dict, block_config: Dict) -> str:
    """Transform notebook data into block-compatible input file"""
    
def parse_block_output(output_file: str) -> Dict:
    """Parse block output and return structured data to notebook"""
```

**Batch Operations**:
```python
def aggregate_inputs(input_list: List[Dict]) -> str:
    """Combine multiple data sources into single block input"""
    
def distribute_outputs(output_data: Dict) -> List[str]:
    """Split block output into multiple context destinations"""
```

## 💾 Context Memory Management (Validated Implementation)

### Storage Architecture (Actual Implementation)

**Location**: `Orchestration/context_mem/` directory (validated structure)
**Persistence**: JSON files with dual-layer object storage
**Structure**: Dual-pattern architecture with user vs company contexts

### Memory Component Hierarchy (From Step_0 Execution)

```
context_mem/
├── context_map.json                         # Global context routing
├── usr/                                     # Single user workspace
│   ├── cache_me.json                       # User identity objects
│   ├── cache_team.json                     # Team member objects
│   ├── edges.json                          # User-level relationships
│   ├── relations.json                      # User relationships
│   ├── relation_edges.json                 # Relationship edge data
│   └── relation_replacement_edges.json     # Relationship replacements
├── identity--{company-uuid}/                # Company-specific contexts
│   ├── company.json                        # Company identity object
│   ├── users.json                          # Employee objects
│   ├── systems.json                        # IT system objects
│   ├── assets.json                         # Hardware/asset objects
│   ├── edges.json                          # Company relationships
│   ├── relations.json                      # Company relationships
│   ├── relation_edges.json                 # Relationship edge data
│   └── relation_replacement_edges.json     # Relationship replacements
└── incident--{incident-uuid}/               # Incident-specific contexts
    ├── incident.json                       # Core incident object
    ├── sequence_start_refs.json            # Initial attack vectors
    ├── sequence_refs.json                  # Attack progression chain
    ├── impact_refs.json                    # Damage and consequences
    ├── event_refs.json                     # Timeline events
    ├── task_refs.json                      # Response tasks
    ├── other_object_refs.json              # Supporting objects
    ├── unattached_objs.json               # Objects pending classification
    ├── unattached_relation.json           # Unclassified relationships
    └── [various relationship files]        # Incident relationships
```

### Dual-Pattern Architecture (Validated)

**User Context Pattern** (`/usr/`)
- **Initialization**: No setup required - direct object storage
- **Usage**: Personal identity objects and team member data
- **Storage Format**: Array-based JSON files with dual-layer objects
- **Functions**: `invoke_save_user_context_block()`, `invoke_save_team_context_block()`

**Company Context Pattern** (`/identity--{uuid}/`)
- **Initialization**: Explicit creation using `invoke_create_company_context()`
- **Categorization**: Objects stored in category-specific files
- **Multi-Tenant**: Support for multiple company contexts
- **Functions**: `invoke_save_company_context_block()` with `context_type` parameter

### Object Storage Structure (Validated)

Each STIX object stored with **dual-layer metadata**:

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

**Key Implementation Features**:
- **`original`** field contains pure STIX 2.1 data (what blocks process)
- **UI metadata** provides display information for visualization
- **Array storage** enables multiple objects per context file
- **Append pattern** preserves object history and relationships

### Data Flow Patterns

#### Pattern 1: Context → Slice → Process → Update
```
🗂️ [Full Context] → 📋 [Data Slice] → ⚙️ [Block Processing] → 💾 [Context Update]
```

#### Pattern 2: Form → Validate → STIX → Store
```
📝 [User Form] → ✅ [Validation] → 🔧 [STIX Creation] → 📊 [Object Storage]
```

#### Pattern 3: STIX → Relationships → Visualization → UI
```
📊 [STIX Objects] → 🔗 [Relationship Analysis] → 📈 [Data Visualization] → 🖥️ [UI Display]
```

### Shared Resources Management

**Common Files Location**: `Orchestration/generated/os-triage/common_files/`

**Key Shared Resources**:
- 🔄 **Node/Edge Converter**: Convert STIX objects to graph representation
- 🎨 **Icon Registry**: STIX object icons for UI components
- 📋 **Schema Definitions**: STIX validation schemas
- ⚙️ **Configuration Files**: System-wide settings

**Dynamic Loading Pattern**:
```python
# Load common files from shared directory
module_path = TR_Common_Files + '/' + common[0]["file"]
spec = importlib.util.spec_from_file_location('convert_n_and_e', module_path)
convert_n_and_e = importlib.util.module_from_spec(spec)
spec.loader.exec_module(convert_n_and_e)
```

## 🚀 System Integration & Deployment

### Development-to-Production Pipeline

**Development Phase** (This Repository):
- Block development and testing in isolated Python environment
- Orchestration workflow design using Jupyter notebooks
- Context memory simulation with local JSON file storage
- Integration testing and validation using utility functions

**Production Deployment** (Total.js Flow):
- Block registration in Total.js Flow platform
- Workflow translation to Total.js Flow visual designer
- Context memory integration with production data stores
- API endpoint generation for external system integration

### Scalability Considerations

**Horizontal Scaling**:
- **Block Parallelization**: Stateless blocks enable concurrent execution
- **Context Partitioning**: Multi-tenant context memory design
- **Load Distribution**: Workflow orchestration across multiple execution nodes

**Vertical Scaling**:
- **Memory Optimization**: Efficient STIX object processing and caching
- **I/O Performance**: Optimized context memory access patterns
- **Processing Efficiency**: Block execution optimization and resource management

## 🎯 Use Cases and Applications

### Primary Use Cases

1. **Demo Context Development**: Produce sufficient data for development purposes
   - Generate data for two companies and two incidents
   - Create detailed user and team information
   - Execute Step 0, Step 1, Step 2 notebooks systematically

2. **Block Development and Testing**: Create and validate new Python blocks
   - Develop blocks in `Block_Families/` directory structure
   - Test functionality using orchestration notebooks
   - Validate integration with context memory system

3. **Workflow Prototyping**: Design complex security operations
   - Compose multi-block workflows for incident response
   - Test data flow and transformation patterns
   - Validate STIX object relationships and dependencies

4. **Intelligence Analysis**: Process cybersecurity threat data
   - Transform raw security data into STIX objects
   - Analyze attack patterns and malware behaviors
   - Generate threat intelligence reports and visualizations

### Success Metrics

**Foundation Level**:
- ✅ Complete block architecture and lifecycle comprehension
- ✅ STIX object management and transformation mastery
- ✅ Context memory structure and data flow understanding

**Advanced Level**:
- ✅ Design new block types and capabilities
- ✅ Orchestrate complex workflows
- ✅ System optimization and performance knowledge

**Expert Level**:
- ✅ Propose system-wide improvements
- ✅ Understand scalability and extensibility patterns
- ✅ Security and data integrity expertise

## 🔄 Evolution and Roadmap

### Immediate Development Priorities

1. **Architecture Documentation**: Complete system documentation enhancement
2. **Block Standardization**: Refactor problematic notebooks and establish patterns
3. **Utility Enhancement**: Expand orchestration utilities and error handling
4. **Testing Framework**: Develop comprehensive test suites for blocks and workflows

### Long-term Architectural Goals

1. **Advanced Workflow Capabilities**: Complex multi-stage incident response workflows
2. **Enhanced STIX Support**: Extended dialect support and custom object types
3. **Performance Optimization**: Advanced caching, indexing, and search capabilities
4. **Integration Expansion**: Additional external system connectors and API integrations

This specification serves as the definitive guide for understanding, developing, and extending the Brett Blocks cybersecurity intelligence system. Every component, pattern, and constraint described here is essential for maintaining system integrity and achieving advanced cybersecurity capabilities.