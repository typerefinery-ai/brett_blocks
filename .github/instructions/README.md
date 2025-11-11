# AI Assistant Instructions for Brett Blocks System - **Validated & Optimized**

## 🚀 QUICK START - READ THIS FIRST

**NEW:** Complete AI Assistant Guide with Smart Indexing available at:
### 📖 [COMPLETE-GUIDE.md](COMPLETE-GUIDE.md) - Your Primary Reference

The complete guide includes:
- ✅ Smart indexed table of contents (5/15/30/60 min sections)
- ✅ Critical rules and common mistakes
- ✅ Data forms & reconstitution (NEW Nov 2025)
- ✅ **Testing system achieving 100% pass rate (NEW Nov 2025)**
- ✅ Complete STIX object analysis (all 88 objects)
- ✅ Round-trip workflows with 99.3%+ accuracy
- ✅ Notebook development patterns
- ✅ Full utility function reference
- ✅ Quick decision tree

**Use COMPLETE-GUIDE.md for all new development work.**

---

## 🧪 TESTING & VALIDATION - **100% Pass Rate Achieved (Nov 2025)**

### StixORM Testing System
**Production-ready testing infrastructure** validating the entire Brett Blocks architecture:

**Key Achievements:**
- ✅ **100% pass rate** (53/53 objects tested across 15 STIX types)
- ✅ **100% execution success** using STIXReconstitutionEngine
- ✅ **All 18 test cases passing**
- ✅ **<1 second execution time**
- ✅ **Validates complete round-trip**: STIX → Data Forms → Reconstitution → Verification

**What Testing Validates:**
1. **Template-Driven Architecture** - All make_*.py blocks execute with correct signatures
2. **Data Form Pipeline** - 100% conversion success via convert_object_list_to_data_forms.py
3. **Reconstitution Engine** - Production-proven engine (99.3% → 100% focused accuracy)
4. **STIX Compliance** - Structural comparison confirms specification adherence
5. **System Integration** - End-to-end pipeline proves all components work together

**Running Tests:**
```bash
# Run complete test suite
poetry run pytest tests/

# Run specific phases
poetry run pytest tests/test_1_discovery.py
poetry run pytest tests/test_2_data_form_generation.py
poetry run pytest tests/test_3_block_execution.py
poetry run pytest tests/test_4_verification.py
poetry run pytest tests/test_5_reporting.py

# Check test reports
cat tests/generated/reports/test_summary.md
```

**See:** `architecture/stixorm-testing-system-design.md` for complete testing architecture.

---

## 🎯 LEARNING OBJECTIVES - **ALWAYS READ FIRST**

You are an expert AI assistant for the **Brett Blocks cybersecurity intelligence system**. Your mission is to help developers create, modify, and orchestrate Python blocks using **validated architectural patterns** discovered through comprehensive testing.

### 🧠 Critical Knowledge Framework
1. **Template-Driven Architecture**: Three-file pattern with automatic parameter generation
2. **Testing & Validation**: Production-ready testing system achieving 100% pass rate (53/53 objects)
3. **Comprehensive STIX Analysis**: Complete pattern analysis of all 88 available STIX objects (15 implemented, 73 available)
4. **Automatic STIX Routing**: Intelligent object categorization eliminates manual parameters
5. **Context Memory Evolution**: Multi-step workflow progression through validated notebook sequences
6. **Mathematical Equivalence**: NEW optimized notebooks produce identical results to legacy implementations
7. **File Path Patterns**: Brett Blocks functions create files WITHOUT .json extensions
8. **Round-Trip Conversion**: STIX → Data Forms → Reconstitution with 99.3%+ accuracy

## 📊 STIX Object Implementation Status

**Current Capability**: 15 implemented objects across SDO (8), SCO (5), SRO (2)
**Expansion Potential**: 88 total objects available (5.8x growth potential)
- **Standard STIX 2.1**: 29 objects ready for immediate implementation
- **Dialect Objects**: 44 objects requiring StixORM library upgrade (MITRE ATT&CK, OCA, IBM Security)

**Complexity Distribution** (from comprehensive analysis):
- **MINIMAL (0-1 params)**: 47% of objects → High automation feasibility
- **EXTREME (6-7 params)**: 13% of objects → Require manual integration testing

See `architecture/stix-object-generation-patterns.md` for complete analysis.

## ⚡ RAPID ABSORPTION GUIDE - **CRITICAL PATTERNS ONLY**

### 🔥 INSTANT REFERENCE - **Most Critical Discoveries**

**Automatic STIX Object Routing** (PARADIGM SHIFT):
```python
# save_incident_context.py automatically routes by stix_object["type"]
# ELIMINATION: context_type parameters largely redundant
# RULE: Let the system route automatically, don't force categorization
```

**File Path Pattern** (CRITICAL RULE):
```python
# ✅ CORRECT: Brett Blocks output
results_path = "step3/observation_anecdote"  # NO .json extension
save_path = results_base + results_path      # Direct path usage

# ❌ WRONG: Common error causing PermissionError  
save_path = results_base + results_path + ".json"  # DON'T ADD .json
```

**Template Parameter Generation** (OPTIMIZATION):
```python
# Template properties automatically become function parameters
# "event_refs": {"property": "OSThreatReference"} → event_refs=None parameter
# BENEFIT: 30-40% fewer manual parameters required
```

### 🏗️ VALIDATED ARCHITECTURE - **PROVEN PATTERNS**

**Context Memory Structure** (MATHEMATICAL EQUIVALENCE PROVEN):
```text
Step 0: usr/                     → 3 files (user context)
Step 1: identity--{uuid}/        → 5 files (company context)  
Step 2: incident--{uuid}/        → 10 files (incident context)
Step 3: Enhanced incident        → 6 updated + 1 new (anecdote collection)
```

**Utility Function Framework** (REQUIRED PATTERN):
```python
# ✅ STANDARD IMPORT PATTERN
from Utilities.local_make_sdo import invoke_make_identity_block
from Utilities.local_make_general import invoke_save_incident_context_block

# ✅ STANDARD USAGE PATTERN  
path_base = "../Block_Families/StixORM/"  # Base path for templates
results_base = "../Orchestration/Results/"  # Results storage

# ✅ RELATIVE PATH RULE - utility functions add path_base automatically
obj = invoke_make_identity_block("SDO/Identity/template.json", "step1/result")
```

**NEW vs OLD Notebook Equivalence** (PRODUCTION READY):
- ✅ NEW: 4 modular notebooks (Step_0_User, Step_1_Company, Step_2_Incident, Step_3_Anecdote)
- ✅ OLD: 3 monolithic notebooks (legacy implementation)
- ✅ PROVEN: Mathematical byte-for-byte equivalence in final context memory
- ✅ OPTIMIZED: 30-40% fewer parameters, improved maintainability

## 📋 OPERATIONAL QUICK REFERENCE - **ESSENTIAL COMMANDS**

### Context Memory Operations
```python
# Clear context memory (SAFE METHOD)
# ✅ DELETE: All files and subdirectories within context_mem/
# ❌ NEVER: Delete context_mem/ directory itself

# Monitor context evolution  
import os
files = os.listdir("../Orchestration/generated/os-triage/context_mem/")
```

### STIX Object Creation
```python
# Identity creation (MOST COMMON)
identity = invoke_make_identity_block(
    "SDO/Identity/identity_user.json",    # Template path (relative)
    "step1/user_identity",                # Results path
    email_results=email_obj,              # Optional: link to email
    acct_results=account_obj              # Optional: link to account
)

# Incident creation (ADVANCED)  
incident = invoke_make_incident_block(
    "SDO/Incident/incident_phishing.json",  # Template path
    "step2/phishing_incident",               # Results path
    event_refs=events,                       # Auto-generated parameter
    task_refs=tasks,                         # Auto-generated parameter
    other_object_refs=observables            # Auto-generated parameter
)
```

### Context Storage (AUTOMATIC ROUTING)
```python
# SIMPLIFIED: Let automatic routing handle categorization
result = invoke_save_incident_context_block(
    object_file_path,                        # File path (no .json)
    context_file_path,                       # Context storage path
    {"context_type": "unattached"}           # Often redundant now
)
```

## 🚨 CRITICAL RULES - **MEMORIZE THESE**

### File Path Rules
- ✅ **Use results_path directly** in save operations
- ❌ **Never append .json** to Brett Blocks function output paths
- ✅ **Templates are relative** to Block_Families/StixORM/
- ✅ **Results paths are relative** to Orchestration/Results/

### Context Memory Rules  
- ✅ **DELETE files within** context_mem/ to clear
- ❌ **NEVER delete** the context_mem/ directory itself
- ✅ **Monitor file evolution** through workflow steps
- ✅ **Trust automatic STIX routing** for categorization

### Development Rules
- ✅ **Use NEW notebook sequence** (4 notebooks) for all development
- ✅ **Template properties** automatically generate function parameters
- ✅ **Test mathematical equivalence** when optimizing code
- ❌ **Don't force manual categorization** - let automatic routing work

## 🗂️ DIRECTORY MAP - **VALIDATED LOCATIONS**

```
📁 Block_Families/StixORM/     # Template library (STABLE)
├── SDO/Identity/              # Identity objects
├── SDO/Incident/              # Incident objects  
├── SCO/User_Account/          # User accounts
├── SCO/Email_Addr/            # Email addresses
└── SRO/Sighting/              # Relationships

📁 Orchestration/              # Workflow execution (ACTIVE DEVELOPMENT)
├── Step_0_User_Setup.ipynb           # ✅ NEW: User context creation
├── Step_1_Company_Setup.ipynb        # ✅ NEW: Company context creation
├── Step_2_Create_Incident.ipynb      # ✅ NEW: Incident context creation
├── Step_3_Get_Anecdote.ipynb         # ✅ NEW: Anecdote collection
├── generated/os-triage/context_mem/  # Context memory storage
├── Results/                          # Intermediate file storage
└── Utilities/                        # Utility function framework
    ├── convert_object_list_to_data_forms.py   # Data form generation (99.3% success)
    ├── reconstitute_object_list.py            # STIXReconstitutionEngine
    └── local_make_*.py                        # Block wrapper utilities

📁 tests/                      # Testing infrastructure (NEW Nov 2025)
├── generated/                 # Test artifacts (100+ files generated)
│   ├── reports/               # Test reports (JSON & Markdown)
│   ├── input_objects/         # Original STIX objects (53 files)
│   └── *_data_form.json       # Generated data forms (53 files)
├── utils/                     # Testing utilities
│   ├── discovery.py           # Object discovery (53 testable objects found)
│   ├── data_form_generator.py # Data form wrapper
│   ├── comparator.py          # DeepDiff comparison with UUID normalization
│   └── reporter.py            # Report generation
└── test_*.py                  # 18 test cases (all passing)

📁 architecture/               # Updated documentation (REFERENCE)
├── system-interaction-map.md         # ✅ NEW: Complete component interaction guide
├── stixorm-testing-system-design.md  # ✅ NEW: Testing system architecture (100% pass rate)
├── reconstitution-and-notebook-generation.md  # ✅ UPDATED: Testing validation added
├── context-memory-architecture.md    # ✅ UPDATED: Automatic routing
├── orchestration-architecture.md     # ✅ UPDATED: Notebook validation  
└── new-knowledge-summary.md          # ✅ UPDATED: October 2025 discoveries
```

## 🎯 WORKFLOW PATTERNS - **TESTED & VALIDATED**

### Standard Workflow Execution
```python
# 1. Setup (EVERY notebook)
path_base = "../Block_Families/StixORM/"
results_base = "../Orchestration/Results/"

# 2. Create objects (template-driven)
obj = invoke_make_*_block(template_path, results_path, **auto_params)

# 3. Save to context (automatic routing)
result = invoke_save_*_context_block(obj_path, context_path, context_type)

# 4. Monitor context evolution (optional)
files = monitor_context_memory()
```

### Multi-Step Investigation Workflow
```text
Step 0: User Setup      → Personal identities and team context
Step 1: Company Setup   → Organizational infrastructure 
Step 2: Incident Setup  → Evidence collection and threat modeling
Step 3: Anecdote Collection → Impact assessment and narrative generation
```

## 📚 DOCUMENTATION INDEX - **ORGANIZED BY URGENCY**

### 🔥 **IMMEDIATE REFERENCE** (Read for every session)
- `.github/instructions/README.md` (THIS FILE) - Core operational patterns
- `architecture/new-knowledge-summary.md` - October 2025 breakthrough discoveries
- `architecture/system-interaction-map.md` - **NEW**: Complete component interaction guide

### 🧪 **TESTING & VALIDATION** (Understand system quality)
- `architecture/stixorm-testing-system-design.md` - **NEW**: Testing achieving 100% pass rate
- `architecture/reconstitution-and-notebook-generation.md` - Data forms & round-trip conversion (99.3%+ accuracy)

### 📖 **DETAILED ARCHITECTURE** (Read for complex tasks)
- `architecture/context-memory-architecture.md` - Context storage and automatic routing
- `architecture/orchestration-architecture.md` - Notebook validation and equivalence
- `architecture/template-driven-architecture.md` - Template system and parameter generation

### 🛠️ **IMPLEMENTATION GUIDES** (Read for specific tasks)
- `architecture/block-architecture.md` - Python block design patterns
- `architecture/stix-object-architecture.md` - STIX 2.1 object specifications

### 📊 **REFERENCE MATERIALS** (Consult as needed)
- `architecture/system-overview.md` - High-level system design
- `architecture/stix-object-generation-patterns.md` - Complete STIX object analysis

This instruction set provides **maximum efficiency** for AI assistants working with Brett Blocks, prioritizing critical discoveries and proven patterns while maintaining comprehensive reference materials for complex scenarios.

## 🚀 **QUICK START FOR AI ASSISTANTS**

1. **Absorb Core Patterns**: Read the RAPID ABSORPTION GUIDE above first
2. **Master Critical Rules**: Memorize the file path and context memory rules
3. **Understand Testing**: Review testing system achieving 100% validation
4. **Reference Architecture**: Use the DOCUMENTATION INDEX for detailed guidance
5. **Apply Validated Patterns**: Follow the tested workflow patterns
6. **Trust Automatic Systems**: Let STIX routing and template generation work
7. **Monitor Progress**: Use context memory evolution tracking
8. **Validate Changes**: Run `poetry run pytest tests/` to verify code quality

Your expertise in this system directly enables advanced cybersecurity intelligence capabilities while leveraging the most efficient, validated patterns discovered through comprehensive testing and optimization.

**System Quality Assurance:**
- ✅ 100% pass rate on 53 testable objects across 15 STIX types
- ✅ Complete round-trip validation: STIX → Data Forms → Reconstitution
- ✅ All 18 test cases passing with <1 second execution time
- ✅ Production-proven utilities with 99.3%+ accuracy
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
7. **Testing System**: Production-ready testing validates all components (100% pass rate)
8. **Data Forms**: Round-trip conversion STIX → Data Forms → STIX achieves 99.3%+ accuracy
9. **Reconstitution Engine**: STIXReconstitutionEngine handles automatic reference restoration

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