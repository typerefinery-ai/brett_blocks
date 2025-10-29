# Brett Blocks System Architecture - AI Learning Framework

## AI Learning Mission

**Primary Objective**: Become an expert architect and developer of Python blocks within the **OS Threat low-code cybersecurity intelligence system**.

**System Context**: This system uses Python blocks as middleware between content management and security services, orchestrated through Total.js Flow platform with custom Python capabilities.

**Starting Point**: Sophisticated Python developer with zero knowledge of this specific system.

**End Goal**: Achieve architectural mastery sufficient to design and implement advanced cybersecurity intelligence capabilities.

## Learning Framework Structure

### Phase 1: Foundation (Understanding)
1. **Architectural Comprehension**: Master block structure, context memory, orchestration patterns
2. **STIX Expertise**: Deep knowledge of STIX 2.1 object management and transformations
3. **Documentation Creation**: Build comprehensive markdown docs in `./architecture/`
4. **Visual Mapping**: Create diagrams and system flow charts

### Phase 2: Exploration (Application)
5. **Hands-On Execution**: Run notebooks, observe context data generation
6. **Block Interaction Study**: Understand inter-block communication via context memory
7. **Data Flow Analysis**: Document complete STIX object lifecycle
8. **Pattern Recognition**: Identify reusable architectural patterns

### Phase 3: Development (Innovation)
9. **New Block Creation**: Design enhanced block capabilities
10. **Workflow Innovation**: Create sophisticated orchestration notebooks
11. **System Enhancement**: Architect improvements to existing components
12. **Integration Testing**: Validate new capabilities within ecosystem

### Phase 4: Mastery (Synthesis)
13. **Knowledge Consolidation**: Synthesize insights into coherent documentation
14. **Instruction Updates**: Refresh `.github/instructions/` with comprehensive guidance
15. **Best Practices**: Document patterns, anti-patterns, optimization strategies
16. **Future Roadmap**: Define architectural evolution paths

## Learning Success Metrics

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

## Key Learning Principles

**Continuous Documentation**: Document discoveries immediately in `./architecture/`
**Interactive Feedback**: Request clarification when concepts are unclear
**Hypothesis Testing**: Propose theories for validation
**Practical Application**: Test understanding through hands-on development
**Iterative Learning**: Periodically revise the instructions at .github\instructions to reflect newfound understanding

# System Architecture Overview

## Core System Concept

**Brett Blocks Repository** = Development and testing environment for Python blocks that integrate with **OS Threat cybersecurity intelligence platform**.

**Architecture Pattern**: Microservice-style architecture where individual Python blocks provide specialized STIX 2.1 capabilities.

## Dual-Sided Architecture

### Side 1: Block Definition (This Repository)
- 🔧 **Development Environment**: Python block creation and testing
- 📊 **STIX Object Management**: Form definitions and transformations
- 💾 **Context Memory Simulation**: Local JSON-based data management  
- 📝 **Orchestration Prototyping**: Jupyter notebook workflows

### Side 2: Production Orchestration (Target Application)  
- 🚀 **Total.js Flow Integration**: Real-time block execution platform
- 🔗 **Workflow Management**: Visual designer for block composition
- 🌐 **API Generation**: Convert Python blocks to REST endpoints
- ⚡ **Live Context Memory**: Production-grade state management

## Design Principles (Critical to Understand)

1. **Atomic Functionality**: Each block = one well-defined function
2. **Stateless Execution**: Blocks communicate ONLY via input/output JSON files
3. **STIX 2.1 Compliance**: All data structures follow STIX specifications exactly
4. **Context Isolation**: Blocks run in separate, restricted execution environments
5. **Orchestration Flexibility**: Blocks compose into complex workflows via Total.js Flow


# Block Architecture Deep Dive

## Block Categories (Location: `Block_Families/`)

### Category 1: OS_Triage Blocks (Operational Workflows)

**Purpose**: Cybersecurity operations and UI interactions

**Key Functions**:
- 💾 **Context Management**: [Save context data](Block_Families/OS_Triage/Save_Context/save_unattached_context.py) 
- 📊 **Data Visualization**: [Generate UI data](Block_Families/OS_Triage/Viz_Dataviews/sighting_index.py)
- 🔄 **Workflow Orchestration**: Multi-step security analysis
- 📋 **Form Processing**: Input validation and handling
- ⏱️ **Event Processing**: Incident timeline management

### Category 2: StixORM Blocks (STIX Object Transformation)

**Purpose**: Convert data templates → Valid STIX 2.1 objects

**Supported STIX Dialects**:
- 🏛️ **STIX v2.1**: Core cybersecurity specifications
- ⚔️ **MITRE ATT&CK**: Tactics, techniques, procedures
- 🔗 **MITRE CTI Attack Flow**: Attack sequence modeling
- 🛡️ **OASIS OCA**: Open Cybersecurity Alliance
- 🦠 **Malware MBC**: Malware behavior catalog
- 🔧 **Custom Extensions**: Organization-specific objects

**STIX Object Types**:
- 📍 **SDO** (Domain Objects): Primary threat entities
- 👁️ **SCO** (Cyber Observable Objects): Observable phenomena  
- 🔗 **SRO** (Relationship Objects): Inter-object connections

## Universal Block Structure (MEMORIZE THIS)

**Block Execution Signature**: 
```python
def main(input_file: str, output_file: str) -> None:
```

**Standard Block Template**:
```python
################################################################################
## IMMUTABLE HEADER - DO NOT CHANGE
################################################################################
import os.path
where_am_i = os.path.dirname(os.path.abspath(__file__))
################################################################################

##############################################################################
# Title: [Block Purpose]
# Author: OS-Threat  
# Description: [What this block does]
# Inputs: [Input requirements]
# Outputs: [Output format]
##############################################################################

# BLOCK-SPECIFIC IMPORTS
from stixorm.module.authorise import import_type_factory
import json, sys, importlib.util, logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
import_type = import_type_factory.get_all_imports()

def process_block_logic(input_data: Dict[str, Any]) -> Dict[str, Any]:
    """Block-specific processing logic - CUSTOMIZE THIS"""
    pass

def main(input_file: str, output_file: str) -> None:
    """Standard entry point - DO NOT CHANGE SIGNATURE"""
    with open(input_file, 'r') as f:
        input_data = json.load(f)
    
    result = process_block_logic(input_data)
    
    with open(output_file, 'w') as f:
        json.dump(result, f, indent=2)

################################################################################
## IMMUTABLE FOOTER - DO NOT CHANGE  
################################################################################
if __name__ == '__main__':
    args = getArgs()
    main(args.inputfile, args.outputfile)
################################################################################
```

## Block Execution Constraints (CRITICAL)

**Isolation Requirements**:
- ❌ **No Shared Memory**: Blocks cannot share variables/state
- ❌ **No Direct Calls**: Blocks cannot call each other directly
- ❌ **Limited Imports**: Restricted to approved libraries only
- ✅ **File Communication**: JSON input/output files ONLY

**Input/Output Patterns**:
- 🔄 **No-Input Blocks**: Context memory readers (data slice generators)
- 📝 **Form-Input Blocks**: STIX creators needing structured templates
- 🔄 **Processing Blocks**: Data transformation operations
- 💾 **Output-Only Blocks**: Context memory writers

## Shared Resources Management

**Common Files Location**: `Orchestration/generated/os-triage/common_files/`

**Key Shared Resources**:
- 🔄 **Node/Edge Converter**: [convert_n_and_e.py](Orchestration/generated/os-triage/common_files/convert_n_and_e.py)
- 🎨 **Icon Registry**: STIX object icons for UI
- 📋 **Schema Definitions**: STIX validation schemas
- ⚙️ **Configuration Files**: System-wide settings

**Dynamic Loading Pattern** (Use This):
```python
# Load common files from shared directory
module_path = TR_Common_Files + '/' + common[0]["file"]
spec = importlib.util.spec_from_file_location('convert_n_and_e', module_path)
convert_n_and_e = importlib.util.module_from_spec(spec)
spec.loader.exec_module(convert_n_and_e)
```

## Block Development Guidelines

- 🔧 **Extract Common Logic**: Move reusable code to common_files/
- ⚠️ **Comprehensive Error Handling**: Validate inputs, handle failures gracefully
- ✅ **Input Validation**: Check against expected schemas
- 📋 **Consistent Output**: Follow standard metadata structure
- 📚 **Clear Documentation**: Include docstrings and usage examples



## Orchestration Side

The orchestration side is responsible for managing the execution of the blocks and coordinating their interactions. This side is responsible for managing the execution of the blocks and coordinating their interactions. This involves:

1. Triggering the execution of blocks based on events or conditions
2. Managing the flow of data between blocks
3. Handling errors and retries
4. Providing a user interface for monitoring and controlling the execution

There are 3 key aspects:

1. Context Memory: This is a storage area where data can be saved and retrieved by blocks. It allows blocks to share data and maintain state across executions.
2. Orchestration Notebooks: These are Jupyter notebooks that define the sequence of blocks to be executed and the data flow between them. They provide a visual representation of the orchestration logic and allow for easy modification and testing.
3. Utilities: These are the helper functions that assist in converting instructions provided by the notebooks into the saved files and file location paths needed by the blocks.

### Context Memory Architecture

Context Memory serves as the **persistent data layer** that enables stateful interactions between stateless blocks. It provides a structured storage system for STIX objects, relationships, and operational metadata.

#### Data Structure Format

Context Memory uses a **dual-layer object structure** combining STIX compliance with system metadata:

```json
{
    "id": "user-account--5aaaa4e2-0974-5ab4-9069-41a16197f0ff",
    "type": "user-account", 
    "original": {
        "type": "user-account",
        "spec_version": "2.1", 
        "id": "user-account--5aaaa4e2-0974-5ab4-9069-41a16197f0ff",
        "account_login": "dguy",
        "account_type": "unix",
        "display_name": "dumbo guy"
    },
    "icon": "user-account",
    "name": "User Account",
    "heading": "User Account", 
    "description": "<br>Display Name -> dumbo guy<br>Account Type -> unix<br>Login String ->dguy",
    "object_form": "user-account",
    "object_group": "sco-forms",
    "object_family": "stix-forms"
}
```

**Structure Components**:

- **Core Identity**: `id`, `type` - Object identification and classification
- **STIX Compliance**: `original` - Pure STIX 2.1 object data  
- **UI Metadata**: `icon`, `name`, `heading` - Display and visualization data
- **System Classification**: `object_form`, `object_group`, `object_family` - Internal categorization
- **Presentation**: `description` - Human-readable object summary

#### Directory Organization

Context Memory follows a **hierarchical multi-tenancy model**:

```
Orchestration/generated/os-triage/context_mem/
├── context_map.json                          # Global context routing
├── usr/                                      # Single user workspace  
│   ├── global_variables_dict.json           # User-global settings
│   ├── cache_me.json                        # Personal identity cache
│   ├── cache_team.json                      # Team member cache
│   └── [relationship files]                 # User-level relationships
├── identity--{company-uuid}/                # Company-specific context
│   ├── company.json                         # Company identity object
│   ├── users.json                          # Company user roster  
│   ├── assets.json                         # Company asset inventory
│   ├── systems.json                        # Company system catalog
│   └── [relationship files]                # Company-level relationships  
└── incident--{incident-uuid}/               # Incident-specific context
    ├── incident.json                       # Core incident object
    ├── sequence_start_refs.json            # Initial attack vectors
    ├── sequence_refs.json                  # Attack progression chain
    ├── impact_refs.json                    # Damage and consequences  
    ├── event_refs.json                     # Timeline events
    ├── task_refs.json                      # Response tasks
    ├── other_object_refs.json              # Supporting objects
    ├── unattached_objs.json               # Objects pending classification
    ├── unattached_relation.json           # Unclassified relationships
    └── [relationship files]                # Incident-level relationships
```

#### Context Routing System

**Context Map Structure** (`context_map.json`):
```json
{
    "current_incident": "incident--145eb841-90db-4526-8407-b25fd2d705c1",
    "current_company": "identity--42aba91a-14cd-4a36-a0b7-c6bfc9240212", 
    "company_list": [
        "identity--42aba91a-14cd-4a36-a0b7-c6bfc9240212"
    ],
    "incident_list": [
        "incident--145eb841-90db-4526-8407-b25fd2d705c1"
    ]
}
```

**Context Resolution Process**:
1. **Load Context Map**: Determine active incident and company contexts
2. **Resolve File Paths**: Construct absolute paths to data files
3. **Load Context Data**: Read relevant JSON files based on operation type
4. **Process Operations**: Execute block logic using context data
5. **Update Context**: Write modified data back to appropriate files`


#### Context Memory Files

The context memory is a series of small lists stored on file that are used to store data that needs to be shared between blocks. Each block can read from and write to the context memory, allowing them to share data and maintain state across executions. The context memory is structured as follows:

```python
TR_Context_Memory_Dir = "./generated/os-triage/context_mem"
TR_User_Dir = "/usr"
context_map = "context_map.json"
user_data = {
    "global": "/global_variables_dict.json",
    "me": "/cache_me.json",
    "team": "/cache_team.json",
    "relations" : "/relations.json",
    "edges" : "/edges.json",
    "relation_edges" : "/relation_edges.json",
    "relation_replacement_edges" : "/relation_replacement_edges.json"
}
comp_data = {
    "users": "/users.json",
    "company" : "/company.json",
    "assets" : "/assets.json",
    "systems" : "/systems.json",
    "relations" : "/relations.json",
    "edges" : "/edges.json",
    "relation_edges" : "/relation_edges.json",
    "relation_replacement_edges" : "/relation_replacement_edges.json"
}
incident_data = {
    "incident" : "/incident.json",
    "start" : "/sequence_start_refs.json",
    "sequence" : "/sequence_refs.json",
    "impact" : "/impact_refs.json",
    "event" : "/event_refs.json",
    "task" : "/task_refs.json",
    "other" : "/other_object_refs.json",
    "unattached" : "/unattached_objs.json",
    "unattached_relations" : "/unattached_relation.json",
    "relations" : "/incident_relations.json",
    "edges" : "/incident_edges.json",
    "relation_edges" : "/relation_edges.json",
    "relation_replacement_edges" : "/relation_replacement_edges.json"
}
```

The context map file includes four fields:

- current_incident: The current incident being processed
- current_company: The current company being processed
- company_list: A list of all companies in the context memory
- incident_list: A list of all incidents in the context memory

When a block needs to read or write data to the context memory, it first loads the context map file to determine the current incident and company. It then constructs the appropriate file paths based on this information and reads or writes the data as needed.

### Orchestration Notebooks

Orchestration notebooks serve as **workflow definition and testing environments** for complex multi-block operations. They simulate the production Total.js Flow environment while providing interactive development capabilities.

#### Production-Ready Notebooks

**Core Workflow Notebooks** (Verified and Production-Ready):

1. **Step_0_Build_Initial_Identities.ipynb**
   - **Purpose**: Initialize foundational identity objects and team structures
   - **Capabilities**: Create user accounts, email addresses, organizational identities
   - **Context Operations**: Populate user and company context directories
   - **Output**: Established identity baseline for incident operations

2. **Step_1_Create_Incident_with_an_Alert.ipynb** 
   - **Purpose**: Establish incident context and initial alerting
   - **Capabilities**: Create incident objects, initial indicators, sighting relationships
   - **Context Operations**: Initialize incident directory structure and baseline objects
   - **Output**: Active incident context ready for investigation workflows

3. **Step_2_Get_the_Anecdote.ipynb**
   - **Purpose**: Develop incident narrative and relationship analysis  
   - **Capabilities**: Build complex object relationships, timeline construction
   - **Context Operations**: Populate incident with detailed investigative data
   - **Output**: Comprehensive incident context with rich relationship data

#### Development and Testing Notebooks

**Utility and Testing Notebooks**:

- **Test Form Actions.ipynb**: Block capability testing and validation
- **create_tab_dataslice.ipynb**: UI data generation and visualization support
- **try.ipynb**: Experimental notebook template (requires improvement)

**Known Issues**:
- **Step_3 - Create_more_data_for_unattached.ipynb**: Non-compliant format, generates erroneous data (scheduled for refactoring)

#### Notebook Development Standards

**Architecture Requirements**:
- **Block Integration**: Proper input/output file handling for block execution
- **Context Management**: Appropriate context map loading and updates  
- **Error Handling**: Comprehensive error checking and graceful failure recovery
- **Data Validation**: STIX 2.1 compliance validation for all generated objects
- **Documentation**: Clear markdown documentation of workflow steps and objectives

### Orchestration Utilities

The utilities layer provides **abstraction and normalization services** between notebook-level operations and block-level execution requirements.

#### Core Utility Functions

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

#### Integration Architecture

The utilities serve as the **normalization layer** enabling seamless communication between:

- **Notebook Environment**: Interactive Python with rich data structures and visualization
- **Block Environment**: Isolated JSON-based input/output with restricted imports  
- **Context Memory**: Persistent file-based storage with hierarchical organization
- **Production System**: Total.js Flow platform with real-time execution requirements

**Key Responsibilities**:

1. **Data Format Translation**: Convert between notebook objects and JSON files
2. **Context Path Resolution**: Map logical operations to physical file locations  
3. **Batch Processing Coordination**: Orchestrate multi-block workflows
4. **Error Recovery and Validation**: Ensure data integrity across the system
5. **Performance Optimization**: Minimize file I/O and optimize data transfer patterns

This abstraction layer is essential for maintaining **development agility** while ensuring **production compatibility** with the target Total.js Flow environment.

# Context Memory Management System

## Storage Architecture

**Location**: All context data stored in JSON files within the workspace
**Persistence**: Survives across orchestration sessions (development ↔ production)
**Structure**: Hierarchical data organization with standardized schemas

## Memory Components (What AI Assistants Work With)

### Core Data Types

**🗂️ Context Slices** (`_slice.json` files):
- **Purpose**: Focused data views extracted from full context
- **Usage**: Input for specific block operations
- **Lifecycle**: Created → Consumed → Archived
- **Examples**: sighting-data slice, incident-timeline slice

**📊 STIX Objects** (`.json` files):
- **Purpose**: Validated cybersecurity intelligence entities
- **Structure**: Conforms to STIX 2.1 specifications
- **Examples**: malware entities, attack-pattern objects, indicators

**🔄 Form Data** (`form_*.json` files):
- **Purpose**: User input templates for STIX object creation
- **Structure**: Pre-validated data ready for transformation
- **Examples**: incident forms, malware analysis forms

### Context Memory Hierarchy (MEMORIZE THIS)

```
📁 Context Root/
├── 📊 **STIX Objects/**           # Valid cybersecurity entities
│   ├── incident--[uuid].json      # Incident reports
│   ├── malware--[uuid].json       # Malware entities  
│   ├── indicator--[uuid].json     # Threat indicators
│   └── attack-pattern--[uuid].json # Attack techniques
│
├── 🗂️ **Data Slices/**           # Extracted context views
│   ├── anecdote_slice.json        # Narrative data 
│   ├── sighting_slice.json        # Observation data
│   ├── timeline_slice.json        # Temporal sequences
│   └── identity_slice.json        # Entity relationships
│
├── 📋 **Form Templates/**         # User input structures
│   ├── form_incident.json         # Incident creation forms
│   ├── form_malware.json          # Malware analysis forms
│   └── form_indicator.json        # Indicator definition forms
│
└── ⚙️ **Configuration/**          # System settings
    ├── ui_metadata.json           # Interface configuration
    ├── workflow_config.json       # Process definitions
    └── schema_registry.json       # Validation schemas
```

## Memory Operations (For AI Development)

### Read Operations (Data Access)

**Context Slice Generation**:
```python
# Extract specific data slice from full context
def generate_data_slice(context_type: str, filter_criteria: Dict) -> Dict:
    """Creates focused data view for block processing"""
    pass
```

**STIX Object Retrieval**:
```python
# Load existing STIX objects by type/UUID
def load_stix_objects(object_type: str, uuid_list: List[str]) -> List[Dict]:
    """Retrieves validated cybersecurity objects"""
    pass
```

### Write Operations (Data Storage)

**Context Memory Updates**:
```python
# Save processed results to context memory
def save_to_context(data: Dict, context_type: str, metadata: Dict) -> str:
    """Persists data with proper categorization"""
    pass
```

**STIX Object Creation**:
```python
# Transform templates into valid STIX objects
def create_stix_object(template: Dict, object_type: str) -> Dict:
    """Validates and stores new cybersecurity entities"""
    pass
```

## Data Flow Patterns (CRITICAL FOR AI)

### Pattern 1: Context → Slice → Process → Update
```
🗂️ [Full Context] → 📋 [Data Slice] → ⚙️ [Block Processing] → 💾 [Context Update]
```

### Pattern 2: Form → Validate → STIX → Store
```
📝 [User Form] → ✅ [Validation] → 🔧 [STIX Creation] → 📊 [Object Storage]
```

### Pattern 3: STIX → Relationships → Visualization → UI
```
📊 [STIX Objects] → 🔗 [Relationship Analysis] → 📈 [Data Visualization] → 🖥️ [UI Display]
```

## Memory Management Rules (AI MUST FOLLOW)

### ✅ Required Practices
- **UUID Consistency**: Always preserve STIX object UUIDs across operations
- **Schema Validation**: Validate all data against STIX 2.1 specifications
- **Metadata Preservation**: Maintain creation timestamps and versioning
- **Relationship Integrity**: Ensure all STIX relationships remain valid

### ❌ Prohibited Actions
- **Direct File Deletion**: Never delete context memory files directly
- **Schema Violations**: Never create malformed STIX objects
- **Circular References**: Avoid infinite loops in object relationships
- **Timestamp Manipulation**: Never modify creation/update timestamps

## Memory Troubleshooting Guide

**Common Issues**:
- 🔍 **Missing Objects**: Check UUID formatting and file existence
- ⚠️ **Schema Errors**: Validate against STIX 2.1 specifications
- 🔗 **Broken Relationships**: Verify target object existence
- 📁 **File Conflicts**: Check for duplicate UUIDs or naming conflicts

**Diagnostic Commands**:
```python
# Check context memory integrity
def validate_context_memory() -> Dict[str, Any]:
    """Comprehensive memory validation report"""
    pass

# Repair broken relationships
def repair_stix_relationships() -> bool:
    """Fix orphaned or invalid STIX relationships"""
    pass
```

## System Integration & Deployment

### Development-to-Production Pipeline

The Brett Blocks system serves as a **comprehensive development environment** that mirrors the production Total.js Flow platform:

**Development Phase**:
- Block development and testing in isolated Python environment
- Orchestration workflow design using Jupyter notebooks  
- Context memory simulation with local JSON file storage
- Integration testing and validation using utility functions

**Production Deployment**:
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

## Next Steps & Evolution

### Immediate Development Priorities

1. **Architecture Documentation**: Complete system documentation in `./architecture/` directory
2. **Block Standardization**: Refactor problematic notebooks and establish consistent patterns
3. **Utility Enhancement**: Expand orchestration utility functions and error handling
4. **Testing Framework**: Develop comprehensive test suites for blocks and workflows

### Long-term Architectural Goals

1. **Advanced Workflow Capabilities**: Complex multi-stage incident response workflows
2. **Enhanced STIX Support**: Extended dialect support and custom object types
3. **Performance Optimization**: Advanced caching, indexing, and search capabilities  
4. **Integration Expansion**: Additional external system connectors and API integrations

### Knowledge Development Framework

This seed architecture document establishes the foundation for systematic exploration and mastery of the Brett Blocks system. Through iterative learning, hands-on experimentation, and comprehensive documentation, the goal is to achieve **architectural expertise** sufficient to design and implement advanced cybersecurity intelligence capabilities.

**Success Metrics**:
- **Comprehensive Understanding**: Complete mastery of block architecture and orchestration patterns
- **Innovation Capability**: Ability to design novel blocks and workflows for emerging requirements  
- **System Optimization**: Expertise in performance tuning and scalability enhancement
- **Documentation Excellence**: Creation of definitive architectural guidance and best practices

The journey from **functional understanding** to **architectural mastery** requires systematic exploration of each system component, hands-on experimentation with real workflows, and continuous refinement of knowledge through practical application.

---

# 🎯 AI Assistant Quick Reference Card

## Essential System Facts (Memorize This)

**System Purpose**: 🛡️ Cybersecurity intelligence platform using Python blocks + STIX 2.1 objects
**Architecture**: 🔄 Development environment (this repo) ↔ Production environment (Total.js Flow)
**Communication**: 📄 JSON files only (no shared memory, no direct calls between blocks)
**Data Standard**: 🔒 STIX 2.1 compliance required for all cybersecurity objects

## Block Execution Pattern (Never Deviate)

```python
def main(input_file: str, output_file: str) -> None:
    """STANDARD SIGNATURE - DO NOT CHANGE"""
    with open(input_file, 'r') as f:
        input_data = json.load(f)
    
    result = process_block_logic(input_data)  # ← CUSTOMIZE THIS
    
    with open(output_file, 'w') as f:
        json.dump(result, f, indent=2)
```

## Critical Directories (Know Where Everything Lives)

- 🧱 **Block_Families/**: All executable Python blocks
  - 🚨 **OS_Triage/**: Operational workflows
  - 📊 **StixORM/**: STIX object creators
- 🎼 **Orchestration/**: Jupyter notebooks for testing workflows
- 📁 **Context Memory**: JSON files containing all persistent data

## AI Development Rules (MUST FOLLOW)

### ✅ Always Do This
- Validate STIX objects against 2.1 specifications
- Use JSON for all inter-block communication
- Preserve UUIDs and metadata in STIX objects
- Load common files dynamically from shared directory
- Test blocks using Jupyter notebooks in Orchestration/

### ❌ Never Do This
- Create blocks that share memory or state
- Generate malformed STIX objects
- Delete context memory files directly
- Call blocks directly from other blocks
- Skip input/output file validation

## Workflow Patterns (Use These Templates)

**Data Processing**: Context → Slice → Block → Result → Context Update
**STIX Creation**: Form → Validation → STIX Object → Storage
**Analysis**: STIX Objects → Relationships → Visualization → UI Data

## Common AI Tasks

1. **Creating New Blocks**: Use standard template, focus on `process_block_logic()`
2. **Debugging Workflows**: Check JSON file formats and STIX validation
3. **Context Analysis**: Examine slice generation and memory structure
4. **STIX Operations**: Transform templates to valid objects with proper relationships

---


## Use Cases for the Repo

This repo can be used for a variety of processes:

1. Developing a demo context memory to be used for development purposes in the OS Threat platform. Ideally, we produce sufficient data for two companies and two incidents, as well as good details about the user and team. Thus we probably need to run Step 0, Step 1, and Step 2 notebooks, and then Step 1 and Step 2 again to produce this data.
2. Testing and developing new Python blocks that can be integrated into the OS Threat platform. Developers can create new blocks in the `Block_Families/` directory, test them using the orchestration notebooks, and validate their functionality with the context memory.