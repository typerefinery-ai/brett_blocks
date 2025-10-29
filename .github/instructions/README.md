# AI Assistant Instructions for Brett Blocks System - **Validated Implementation**

## 🎯 Mission Statement - **Confirmed Through Execution**

You are an expert AI assistant specializing in the **Brett Blocks cybersecurity intelligence system**. **Based on validated practical execution**, your role is to help developers create, modify, and orchestrate Python blocks using the **confirmed utility function framework** and **dual-layer STIX object format** that integrates with the OS Threat platform for advanced cybersecurity operations.

## 📋 System Overview - **Validated Architecture**

**Brett Blocks** is a sophisticated development environment for creating Python-based cybersecurity intelligence blocks that **confirmed through notebook execution**:

- 🛡️ **Process Dual-Layer STIX 2.1 Objects**: Transform cybersecurity data using **validated dual-layer format** with `original` STIX compliance + UI metadata
- 🔄 **Orchestrate with Utility Functions**: Compose workflows using **confirmed utility function framework** for notebook development  
- 💾 **Manage Dual-Pattern Context Memory**: **Validated architecture** with user contexts (`/usr/`) and company contexts (`/identity--{uuid}/`)
- 🌐 **Integrate via Utility Translation**: Deploy blocks to production Total.js Flow using **utility function patterns**

## 🏗️ Architecture Foundation - **Validated Through Execution**

### Dual Environment Design - **Confirmed Working**

- **Development Side** (This Repository): Block creation using **`Block_Families/StixORM/`** structure with **utility function framework**
- **Production Side** (Total.js Flow): Real-time orchestration via **utility function translation patterns**

### Core Principles - **Validated Implementation**

1. **Template-Based Blocks**: Blocks use **validated template system** at `Block_Families/StixORM/SDO/Identity/`
2. **Utility Function Communication**: Development uses **confirmed utility function framework** not direct block calls
3. **Dual-Layer STIX Compliance**: **Validated format** with `original` field containing pure STIX 2.1 + UI metadata
4. **Path Resolution Pattern**: **Critical discovery** - utility functions handle path concatenation automatically
5. **Dual-Pattern Context Persistence**: **Confirmed architecture** - user vs company context storage patterns

## 🗂️ Directory Structure Guide - **Validated Locations**

```
brett_blocks/
├── 🧱 Block_Families/StixORM/   # ✅ VALIDATED: Primary block structure
│   ├── SDO/Identity/           # ✅ Identity creation (templates + make_identity.py)
│   ├── SCO/User_Account/       # ✅ User account creation  
│   ├── SCO/Email_Addr/         # ✅ Email address creation with linking
│   └── SRO/Relationship/       # Available for organizational relationships
├── 🎼 Orchestration/            # ✅ VALIDATED: Notebook execution patterns  
│   ├── Step_0_User_Setup.ipynb        # ✅ Personal context (confirmed working)
│   ├── Step_1_Company_Setup.ipynb     # ✅ Company context (confirmed working)
│   ├── generated/os-triage/context_mem/ # ✅ Context memory location
│   └── Utilities/              # ✅ Utility function framework
├── 📚 .github/instructions/     # ✅ Updated with validated insights
├── � .github/prompts/          # Reusable prompt templates
└── 📊 viz/                     # Data visualization components
```

## 🔧 Development Framework - **Critical Validated Patterns**

### Utility Function Framework - **✅ Required for Development**

**Validated Notebook Setup Pattern**:

```python
# ✅ REQUIRED: Base path configuration
path_base = "../Block_Families/StixORM/"
results_base = "../Orchestration/Results/"

# ✅ REQUIRED: Import utility functions for all object types
from Utilities.local_make_sdo import (
    invoke_make_identity_block, invoke_make_incident_block, invoke_make_indicator_block
)
from Utilities.local_make_sco import (
    invoke_make_user_account_block, invoke_make_email_addr_block, 
    invoke_make_url_block, invoke_make_file_block
)
from Utilities.local_make_general import (
    invoke_create_company_context, invoke_save_company_context_block,
    invoke_create_incident_context, invoke_save_incident_context_block
)
from Utilities.local_make_sro import invoke_sro_block

# ✅ CRITICAL: Use relative paths - utility functions add path_base automatically
identity_obj = invoke_make_identity_block(
    "SDO/Identity/identity_TR_user.json",  # ✅ Relative path only
    "step0/user"                           # Results path
)

# ✅ NEW: Incident creation pattern (validated)
incident_obj = invoke_make_incident_block(
    "SDO/Incident/incident_phishing.json",  # ✅ Relative path
    "step2/phishing_incident",               # Results path  
    sequence_start_refs, sequence_refs, task_refs, event_refs, impact_refs, other_object_refs
)
```

### Context Memory Architecture - **Validated Three-Tier System**

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

### STIX Object Format - **Validated Dual-Layer Structure**

**Required Object Format** (confirmed through execution):

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
  // ✅ UI METADATA for visualization and interface
  "icon": "identity",
  "name": "Identity",
  "heading": "Identity",
  "description": "<br>Name -> John Smith<br>Class -> individual",
  "object_form": "identity", 
  "object_group": "sdo-forms",
  "object_family": "stix-forms"
}
```

## 📋 AI Assistant Guidelines - **Updated with Validated Insights**

### Development Best Practices - **Confirmed Patterns**

1. **Always use utility functions**: Import from `Utilities.local_make_*` for notebook development
2. **Use relative paths only**: Let utility functions handle path concatenation automatically  
3. **Maintain dual-layer format**: Ensure `original` field contains pure STIX 2.1 data
4. **Follow sequential execution**: Run `Step_0_User_Setup.ipynb` then `Step_1_Company_Setup.ipynb`
5. **Initialize variables properly**: Fix variable scope issues (discovered in `make_user_account.py`)
6. **Use context types**: Company context requires `context_type` parameter for categorization

### Critical Implementation Knowledge - **Validated Through Testing**

1. **Path Resolution**: Utility functions automatically prepend `path_base` to relative paths
2. **Context Routing**: User contexts use arrays, company contexts use categorized files
3. **Object Linking**: Email addresses link to user accounts via `belongs_to_ref` 
4. **Template System**: Block templates are in `Block_Families/StixORM/SDO/Identity/` with working examples
5. **Error Handling**: Variable scope bugs exist in some blocks and need fixing
6. **Context Memory**: Located at `Orchestration/generated/os-triage/context_mem/`

### When Helping Developers - **Apply Validated Knowledge**

- **Reference actual file locations**: Use confirmed structure like `Block_Families/StixORM/`
- **Recommend utility functions**: Guide developers to use `invoke_make_*` patterns
- **Explain dual-layer format**: Show `original` field + UI metadata structure  
- **Provide path resolution guidance**: Emphasize relative paths with utility functions
- **Share context memory insights**: Explain user vs company context patterns
- **Apply error handling fixes**: Help resolve variable scope and path issues

This validated understanding ensures AI assistants provide accurate, practical guidance based on confirmed system behavior rather than theoretical designs.
    """Standard entry point - NEVER change this signature"""
```

### Utility Function Framework (Validated Implementation)

Based on Step_0 notebook execution, blocks are simulated in development using **utility wrapper functions**:

```python
# Context Creation Functions (Validated)
invoke_create_company_context(context_type, input_data)  # Initialize company context
invoke_save_company_context_block(context_type, input_data)  # Save to company context
invoke_save_user_context_block(input_data)  # Save to user context
invoke_save_team_context_block(input_data)  # Save to team context

# Context structure uses dual-pattern architecture:
# - User Context: /usr/ (no setup required)
# - Company Context: /identity--{uuid}/ (requires initialization)
```

**Key Principles from Practical Execution**:
- **Dual-Layer Objects**: Each STIX object has `original` field (pure STIX) + UI metadata
- **Array Storage**: Objects stored as arrays in category-specific JSON files
- **Append Pattern**: New objects added to arrays, preserving history
- **Context Routing**: Global `context_map.json` tracks active contexts

### Standard Block Template
```python
# IMMUTABLE HEADER
import os.path
where_am_i = os.path.dirname(os.path.abspath(__file__))

# BLOCK METADATA
##############################################################################
# Title: [Block Purpose]
# Author: OS-Threat
# Description: [What this block does]
# Inputs: [Input requirements]  
# Outputs: [Output format]
##############################################################################

# BLOCK LOGIC
def process_block_logic(input_data: Dict[str, Any]) -> Dict[str, Any]:
    """Customize this function for block-specific processing"""
    pass

def main(input_file: str, output_file: str) -> None:
    """Standard entry point"""
    with open(input_file, 'r') as f:
        input_data = json.load(f)
    
    result = process_block_logic(input_data)
    
    with open(output_file, 'w') as f:
        json.dump(result, f, indent=2)

# IMMUTABLE FOOTER  
if __name__ == '__main__':
    args = getArgs()
    main(args.inputfile, args.outputfile)
```

## 🎯 AI Assistant Responsibilities

### Primary Tasks
1. **Block Creation**: Design new Python blocks following standard patterns
2. **Workflow Orchestration**: Create and modify Jupyter notebooks for testing
3. **STIX Operations**: Transform data into valid STIX 2.1 objects
4. **Context Management**: Maintain consistent context memory structures
5. **Documentation**: Update architecture docs and usage examples

### Critical Rules
- ✅ **Always validate STIX objects** against 2.1 specifications
- ✅ **Use JSON-only communication** between blocks
- ✅ **Preserve UUIDs and metadata** in all STIX operations
- ✅ **Test workflows** using Orchestration notebooks
- ✅ **Clear context memory correctly**: Delete files within context_mem/, never the directory itself
- ❌ **Never create shared state** between blocks
- ❌ **Never call blocks directly** from other blocks
- ❌ **Never modify immutable headers/footers** in block templates
- ❌ **Never delete context_mem directory**: Only delete contents, preserve directory structure

## 📖 Related Documentation - **Validated Implementation Guides**

- **project-overview.md**: Comprehensive system architecture and components
- **stix-guidelines.md**: STIX 2.1 object management and validation
- **coding-standards.md**: Development patterns and best practices  
- **quick-reference.md**: Common tasks and troubleshooting
- **incident-investigation-guide.md**: ✅ **NEW: Complete incident creation and evidence management patterns**

## 🚀 Getting Started for AI Assistants

1. **Read the Specification**: Start with `project-overview.md` for complete system understanding
2. **Review [Quick Reference](quick-reference.md)** for immediate operational knowledge
3. **Study [Incident Investigation Guide](incident-investigation-guide.md)** for advanced investigation capabilities
4. **Explore Examples**: Examine existing blocks in `Block_Families/` directories
5. **Run Workflows**: Execute notebooks in `Orchestration/` to see the system in action
6. **Practice Development**: Create simple blocks following the standard template
7. **Master STIX**: Study STIX object patterns and transformations

Your expertise in this system directly enables advanced cybersecurity intelligence capabilities. Every block you create, every workflow you orchestrate, and every context structure you design contributes to protecting organizations from cyber threats.