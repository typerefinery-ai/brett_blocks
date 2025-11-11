# Brett Blocks System Interaction Map

**Document Version:** 1.0  
**Created:** 2025-11-10  
**Status:** ✅ Complete

## Table of Contents

1. [Overview](#overview)
2. [Complete Data Flow](#complete-data-flow)
3. [Component Interactions](#component-interactions)
4. [Utility Functions](#utility-functions)
5. [Testing Integration](#testing-integration)
6. [Cross-Document Reference Guide](#cross-document-reference-guide)

---

## Overview

This document provides a comprehensive map of how all Brett Blocks components interact, from template-driven block design through data form generation, reconstitution, and testing validation. It serves as a navigation guide connecting all architecture documents.

---

## Complete Data Flow

### Phase 1: Template-Driven Foundation

```
┌─────────────────────────────────────────────────────────────────────────┐
│                   TEMPLATE-DRIVEN ARCHITECTURE                           │
│                   [template-driven-architecture.md]                      │
└─────────────────────────────────────────────────────────────────────────┘

Class Template (*_template.json)
    ↓
    Contains property definitions with types:
    - ReferenceProperty → generates foreign key parameters
    - OSThreatReference → generates reference list parameters
    - StringProperty, IntegerProperty, etc. → standard properties
    ↓
Python Function Signature Auto-Generation
    ↓
    Example: Incident_template.json contains:
    "event_refs": {"property": "OSThreatReference", ...}
    "sequence_start_refs": {"property": "OSThreatReference", ...}
    ↓
    Automatically generates:
    def make_incident(incident_form, event_refs=None, sequence_start_refs=None, ...)
    ↓
Data Template (*.json)
    ↓
    Provides actual values matching class template structure
    Example: phishing_incident.json
    ↓
Python Block Execution
    ↓
    make_*.py processes data_form with template-driven parameters
    Returns: STIX Object (JSON)
```

**Key Documents:**
- [template-driven-architecture.md](template-driven-architecture.md) - Complete template system specification
- [block-architecture.md](block-architecture.md) - Python block patterns and execution

---

### Phase 2: Data Form Generation

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    DATA FORM GENERATION PIPELINE                         │
│              [reconstitution-and-notebook-generation.md]                 │
└─────────────────────────────────────────────────────────────────────────┘

STIX Objects (from Block Execution)
    ↓
Orchestration/Utilities/convert_object_list_to_data_forms.py
    ↓
    Key Functions:
    - create_data_forms_from_stix_objects()
      * Analyzes object structure using ParseContent
      * Extracts properties and references
      * Creates data form structure
      * Generates reconstitution metadata
    ↓
Outputs:
    1. Data Forms (*_data_form.json)
       - Structured JSON with all object properties
       - References preserved separately
    
    2. Reconstitution Data (reconstitution_data.json)
       - Reference restoration metadata
       - ID mapping for object relationships
       - Embedded object information
    
    3. Creation Sequence (creation_sequence.json)
       - Dependency-ordered object list
       - Required for proper reconstitution
       - Ensures references resolve correctly
    ↓
Storage Location:
    - Mode 1: Block_Families/StixORM/<GROUP>/<TYPE>_form/
    - Mode 2: Custom directory (e.g., tests/generated/)
```

**Key Utilities:**
- `convert_object_list_to_data_forms.py` - Main data form generator (99.3% success rate)
- `parse.py` - ParseContent metadata extraction
- `reconstitute_object_list.py` - Reference restoration engine

**Key Documents:**
- [reconstitution-and-notebook-generation.md](reconstitution-and-notebook-generation.md) - Complete data form architecture

---

### Phase 3: Reconstitution Engine

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    STIX RECONSTITUTION ENGINE                            │
│              [reconstitution-and-notebook-generation.md]                 │
└─────────────────────────────────────────────────────────────────────────┘

STIXReconstitutionEngine (from reconstitute_object_list.py)
    ↓
Input Files:
    - Data Forms (*_data_form.json)
    - Reconstitution Data (reconstitution_data.json)
    - Creation Sequence (creation_sequence.json)
    ↓
Processing Steps:
    ↓
    1. Load Reconstitution Data
       - Parse creation_sequence for dependency order
       - Load ID mapping for reference restoration
       - Identify embedded objects
    ↓
    2. Restore References (for each data form)
       - Replace reference IDs with full objects
       - Handle embedded object dependencies
       - Maintain STIX 2.1 compliance
    ↓
    3. Execute Blocks in Dependency Order
       - Process creation_sequence index by index
       - Load data form
       - Call corresponding make_*.py block
       - Collect reconstituted object
    ↓
Output:
    - Reconstituted STIX Objects (in creation_sequence order)
    - 99.3% success rate (151/152 objects in production testing)
    - 100% success rate (53/53 objects in focused testing)
```

**Key Functions:**
- `STIXReconstitutionEngine.__init__(data_forms_directory)`
- `load_reconstitution_data()` - Load metadata
- `restore_references_to_data_form()` - Reference restoration
- `reconstitute_stix_objects()` - Main execution

**Key Documents:**
- [reconstitution-and-notebook-generation.md](reconstitution-and-notebook-generation.md) - Engine architecture
- [stixorm-testing-system-design.md](stixorm-testing-system-design.md) - Testing validation

---

### Phase 4: Testing & Validation

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    STIXORM TESTING SYSTEM                                │
│                  [stixorm-testing-system-design.md]                      │
└─────────────────────────────────────────────────────────────────────────┘

5-Phase Testing Pipeline:

Phase 1: DISCOVERY
    ↓
    tests/utils/discovery.py
    - Load all STIX objects from Block_Families/examples/
    - Use ParseContent to identify object type and location
    - Filter for objects with corresponding make_*.py blocks
    - Result: 53 testable objects across 15 STIX types
    ↓
Phase 2: DATA FORM GENERATION
    ↓
    tests/utils/data_form_generator.py
    - Calls convert_object_list_to_data_forms.py
    - Generates data forms for all testable objects
    - Saves to tests/generated/
    - Result: 53 data forms (100% success)
    ↓
Phase 3: BLOCK EXECUTION
    ↓
    conftest.py: execution_results fixture
    - Uses STIXReconstitutionEngine (production-proven)
    - Loads reconstitution_data.json
    - Executes blocks in creation_sequence order
    - Maps using deterministic index-based approach
    - Result: 53 reconstituted objects (100% success)
    ↓
Phase 4: VERIFICATION
    ↓
    tests/utils/comparator.py
    - Manual UUID normalization (portable approach)
    - DeepDiff comparison with ignore_order=True
    - Structural comparison independent of UUIDs
    - Result: 53/53 objects match (100% pass rate)
    ↓
Phase 5: REPORTING
    ↓
    tests/utils/reporter.py
    - Generate test_results.json (detailed per-object results)
    - Generate test_summary.json (summary statistics)
    - Generate test_summary.md (human-readable report)
    - Result: Comprehensive test reports

Final Metrics:
    ✅ 100% pass rate (53/53 objects)
    ✅ 100% execution success
    ✅ All 18 test cases passing
    ✅ Zero structural differences
    ✅ <1 second execution time
```

**Key Components:**
- `tests/utils/discovery.py` - Object discovery
- `tests/utils/data_form_generator.py` - Data form wrapper
- `tests/utils/comparator.py` - DeepDiff comparison
- `tests/utils/reporter.py` - Report generation
- `tests/conftest.py` - STIXReconstitutionEngine integration

**Key Documents:**
- [stixorm-testing-system-design.md](stixorm-testing-system-design.md) - Complete testing architecture

---

### Phase 5: Context Memory & Orchestration

```
┌─────────────────────────────────────────────────────────────────────────┐
│                  CONTEXT MEMORY & ORCHESTRATION                          │
│     [context-memory-architecture.md, orchestration-architecture.md]     │
└─────────────────────────────────────────────────────────────────────────┘

STIX Objects (from Blocks or Reconstitution)
    ↓
save_incident_context.py (Automatic STIX Object Routing)
    ↓
    Intelligent routing based on object.type:
    - SDO types → 'sdo' context
    - SCO types → 'sco' context
    - SRO types → 'sro' context
    - Custom types → specified context_type
    ↓
Context Memory Storage
    ↓
    Structure:
    Orchestration/context_mem/<context_id>/
        ├── sdo.json           # SDO objects array
        ├── sco.json           # SCO objects array
        ├── sro.json           # SRO objects array
        ├── sequences.json     # Sequence definitions
        └── tasks.json         # Task objects
    ↓
Workflow Orchestration (Jupyter Notebooks)
    ↓
    - Step_0: Initialize company context and identities
    - Step_1: Create incident with alert
    - Step_2: Get anecdote and analyze
    - Step_3: Create context and additional data
    ↓
    Mathematical Equivalence Validated:
    - NEW workflow (4 notebooks) ≡ OLD workflow (3 notebooks)
    - Same final STIX objects
    - Same reference relationships
    - Improved code clarity
```

**Key Functions:**
- `save_incident_context.py` - Automatic object routing
- `get_incident_context.py` - Context retrieval
- Notebook utilities in `Orchestration/Utilities/`

**Key Documents:**
- [context-memory-architecture.md](context-memory-architecture.md) - Storage architecture
- [orchestration-architecture.md](orchestration-architecture.md) - Workflow composition

---

## Component Interactions

### Template System ↔ Block Execution

```
Class Template                    Python Block
    ↓                                ↑
Property Definitions          Function Signature
    ↓                                ↑
ReferenceProperty      →      Foreign Key Parameter
OSThreatReference      →      Reference List Parameter
StringProperty         →      Standard Parameter
    ↓                                ↑
Data Template                  Function Call
    ↓                                ↑
Actual Values          →      Parameter Values
```

**Interaction Flow:**
1. Class template defines property types
2. System scans template and generates function signature
3. Data template provides values for properties
4. Block execution receives template-driven parameters
5. Block returns STIX-compliant object

**Documents:** [template-driven-architecture.md](template-driven-architecture.md), [block-architecture.md](block-architecture.md)

---

### Data Form Generation ↔ Reconstitution Engine

```
Data Form Generator                Reconstitution Engine
    ↓                                     ↑
STIX Objects Input                  Data Forms Input
    ↓                                     ↑
Extract Properties         ←→       Restore Properties
Extract References         ←→       Restore References
Generate Metadata          ←→       Load Metadata
Create Sequence            ←→       Process Sequence
    ↓                                     ↑
Data Forms Output                   STIX Objects Output
```

**Interaction Flow:**
1. Generator analyzes STIX objects and extracts structure
2. Generator creates data forms with separated references
3. Generator produces reconstitution metadata and sequence
4. Engine loads metadata and dependency order
5. Engine restores references using ID mapping
6. Engine executes blocks in sequence order
7. Engine returns reconstituted STIX objects

**Documents:** [reconstitution-and-notebook-generation.md](reconstitution-and-notebook-generation.md)

---

### Reconstitution Engine ↔ Testing System

```
Reconstitution Engine              Testing System
    ↓                                     ↑
Production-Proven Logic           Test Integration
    ↓                                     ↑
99.3% Success Rate         →       Validate Accuracy
Automatic References       →       Verify Restoration
Dependency Ordering        →       Check Sequence
    ↓                                     ↑
Reconstituted Objects              Comparison Results
    ↓                                     ↑
Index-Based Output         ←→      Index-Based Mapping
    ↓                                     ↑
                           100% Pass Rate Achieved
```

**Interaction Flow:**
1. Testing system uses STIXReconstitutionEngine directly
2. Engine processes data forms in dependency order
3. Testing maps original → reconstituted using creation_sequence index
4. Testing performs DeepDiff comparison with UUID normalization
5. Testing validates 100% structural equivalence

**Critical Decision:** Use production engine instead of custom executor
- Improves pass rate from 9.4% → 100%
- Eliminates reference restoration bugs
- Ensures production parity

**Documents:** [stixorm-testing-system-design.md](stixorm-testing-system-design.md), [reconstitution-and-notebook-generation.md](reconstitution-and-notebook-generation.md)

---

### Testing System ↔ Template System

```
Template System                    Testing System
    ↓                                     ↑
Class Templates              →     Discovery Phase
make_*.py Blocks            →     Filter Testable Objects
    ↓                                     ↑
53 Object Types             ←→     53 Testable Objects
    ↓                                     ↑
Template Structure          →     Data Form Generation
Function Signatures         →     Block Execution
    ↓                                     ↑
                           Validates Template Correctness
```

**Interaction Flow:**
1. Discovery scans for objects with make_*.py blocks
2. ParseContent identifies template structure
3. Data form generation uses template metadata
4. Block execution validates function signatures
5. Comparison verifies template-driven output

**Validation:** Testing proves template-driven architecture works correctly
- All 53 objects with blocks execute successfully
- All function signatures match templates
- All references restore correctly

**Documents:** [stixorm-testing-system-design.md](stixorm-testing-system-design.md), [template-driven-architecture.md](template-driven-architecture.md)

---

## Utility Functions

### Core Utilities (`Orchestration/Utilities/`)

#### Data Form Generation
```python
convert_object_list_to_data_forms.py
    ↓
create_data_forms_from_stix_objects(objects, stixorm_path, output_dir)
    Input:  List of STIX objects
    Output: (data_forms_dict, reconstitution_data, creation_sequence)
    Success: 99.3% (151/152 objects)
```

#### Reconstitution Engine
```python
reconstitute_object_list.py
    ↓
class STIXReconstitutionEngine:
    __init__(data_forms_directory)
    load_reconstitution_data() → reconstitution_data
    restore_references_to_data_form(data_form, ref_info, id_mapping) → restored_form
    reconstitute_stix_objects(reconstitution_data) → List[STIX objects]
```

#### ParseContent Metadata
```python
Block_Families/General/_library/parse.py
    ↓
get_parse_content_for_object(stix_obj)
    Input:  STIX object dict
    Output: ParseContent(typeql, python_class, group, ...)
    Success: 100% on 133 tested objects
```

#### Context Memory
```python
save_incident_context.py
    ↓
save_context(context_id, objects, context_type=None)
    - Automatic STIX type routing
    - No context_type needed for standard STIX
    - Returns: saved file paths
```

### Testing Utilities (`tests/utils/`)

```python
discovery.py
    ↓
ObjectDiscovery.discover_testable_objects()
    - Loads examples from Block_Families/examples/
    - Filters objects with make_*.py blocks
    - Uses ParseContent for metadata

data_form_generator.py
    ↓
DataFormGenerator.generate_data_forms(objects)
    - Wraps convert_object_list_to_data_forms.py
    - Organizes outputs into test directory

comparator.py
    ↓
ObjectComparator.compare_objects(original, reconstituted)
    - Manual UUID normalization
    - DeepDiff with ignore_order=True
    - Returns (is_identical, differences)

reporter.py
    ↓
TestReporter.generate_summary()
    - Aggregates test results
    - Produces JSON and Markdown reports
```

---

## Testing Integration

### How Testing Validates the Entire System

```
Template System
    ↓ validated by ↓
Discovery finds objects with make_*.py blocks
    ↓
Data Form Generation
    ↓ validated by ↓
100% success creating data forms
    ↓
Reconstitution Engine
    ↓ validated by ↓
100% success executing blocks
    ↓
Template Compliance
    ↓ validated by ↓
100% pass rate on structural comparison
```

**Key Achievements:**
1. **Template Validation:** All 53 objects with templates successfully processed
2. **Data Form Validation:** 100% conversion success (53/53)
3. **Reconstitution Validation:** 100% execution success (53/53)
4. **Structural Validation:** 100% comparison success (53/53)
5. **Performance Validation:** <1 second total execution time

**Evolution:**
- Phase 1 (Custom Executor): 9.4% pass rate
- Phase 2 (Engine + Type Matching): 49.1% pass rate
- Phase 3 (Engine + Index Mapping): 100% pass rate

**Critical Insights:**
1. STIXReconstitutionEngine is production-ready (99.3% → 100%)
2. Index-based mapping is critical (eliminates type+name ambiguity)
3. Manual UUID normalization is portable (works across DeepDiff versions)
4. Template-driven architecture ensures consistency

---

## Cross-Document Reference Guide

### For Understanding Template-Driven Architecture
**Start:** [template-driven-architecture.md](template-driven-architecture.md)
- Three-file pattern specification
- Property type → parameter generation
- Foreign key parameter rules

**Then:** [block-architecture.md](block-architecture.md)
- Python block patterns
- Function signature examples
- Execution patterns

**Then:** [stix-object-architecture.md](stix-object-architecture.md)
- STIX 2.1 compliance
- Object type specifications
- Extension handling

---

### For Understanding Data Flow
**Start:** [reconstitution-and-notebook-generation.md](reconstitution-and-notebook-generation.md)
- Complete STIX → Data Forms → Reconstitution flow
- Utility function details
- Success metrics

**Then:** [stixorm-testing-system-design.md](stixorm-testing-system-design.md)
- Testing pipeline phases
- Validation approach
- Performance metrics

**Then:** [system-overview.md](system-overview.md)
- High-level architecture
- Component relationships
- Deployment models

---

### For Understanding Testing & Validation
**Start:** [stixorm-testing-system-design.md](stixorm-testing-system-design.md)
- 5-phase testing pipeline
- 100% pass rate achievement
- Implementation decisions

**Then:** [reconstitution-and-notebook-generation.md](reconstitution-and-notebook-generation.md)
- STIXReconstitutionEngine details
- Reference restoration logic
- Dependency ordering

**Then:** [template-driven-architecture.md](template-driven-architecture.md)
- How templates drive the system
- What testing validates
- Why it works

---

### For Understanding Context & Orchestration
**Start:** [context-memory-architecture.md](context-memory-architecture.md)
- Automatic STIX routing
- Storage structure
- Context isolation

**Then:** [orchestration-architecture.md](orchestration-architecture.md)
- Workflow composition
- Notebook patterns
- Mathematical equivalence

**Then:** [api-integration-architecture.md](api-integration-architecture.md)
- Production deployment
- External integrations
- Enterprise features

---

### For Understanding Complete System
**Start:** [system-overview.md](system-overview.md)
- High-level architecture
- Dual-environment design
- Core concepts

**Then:** This document (system-interaction-map.md)
- Component interactions
- Data flow
- Cross-references

**Then:** Any specific document based on your focus area

---

## Component Dependency Graph

```
                    ┌──────────────────────────┐
                    │  Template System (Core)  │
                    │  - Class Templates       │
                    │  - Data Templates        │
                    │  - Python Blocks         │
                    └──────────┬───────────────┘
                               │
                 ┌─────────────┴─────────────┐
                 │                           │
                 ↓                           ↓
    ┌────────────────────────┐    ┌─────────────────────┐
    │  Block Execution       │    │  ParseContent       │
    │  - make_*.py files     │    │  - Metadata         │
    │  - STIX generation     │    │  - Type info        │
    └──────────┬─────────────┘    └──────────┬──────────┘
               │                              │
               └──────────┬───────────────────┘
                          │
                          ↓
              ┌───────────────────────────┐
              │  Data Form Generation     │
              │  - convert_object_list... │
              │  - reconstitution_data    │
              │  - creation_sequence      │
              └───────────┬───────────────┘
                          │
                 ┌────────┴────────┐
                 │                 │
                 ↓                 ↓
    ┌────────────────────┐  ┌──────────────────────┐
    │  Reconstitution    │  │  Testing System      │
    │  - Engine          │  │  - Discovery         │
    │  - Reference       │  │  - Execution         │
    │    restoration     │  │  - Verification      │
    └─────────┬──────────┘  └──────────┬───────────┘
              │                        │
              └────────┬───────────────┘
                       │
                       ↓
            ┌──────────────────────────┐
            │  Context Memory          │
            │  - Storage               │
            │  - Automatic routing     │
            │  - Multi-tenant          │
            └──────────┬───────────────┘
                       │
                       ↓
            ┌──────────────────────────┐
            │  Orchestration           │
            │  - Workflows             │
            │  - Notebooks             │
            │  - Integration           │
            └──────────────────────────┘
```

**Key Dependencies:**
1. Everything depends on template system (foundation)
2. Data forms depend on block execution and ParseContent
3. Reconstitution and testing both use data forms
4. Context memory uses reconstituted/generated objects
5. Orchestration composes all components

---

## Summary

The Brett Blocks system is a sophisticated, fully-integrated architecture where:

1. **Templates drive everything** - Class templates define structure and generate function interfaces
2. **Data forms enable round-trip conversion** - STIX → Forms → STIX with 99.3%+ accuracy
3. **Reconstitution engine handles complexity** - Automatic reference restoration and dependency ordering
4. **Testing validates the entire pipeline** - 100% pass rate proves system correctness
5. **Context memory provides persistence** - Automatic routing and multi-tenant storage
6. **Orchestration enables workflows** - Compose components into complex threat analysis

**All components are proven through testing:**
- 53 objects across 15 STIX types
- 100% execution success
- 100% structural validation
- <1 second execution time
- Production-ready accuracy

This interaction map serves as your guide to understanding how all pieces work together to create a complete, validated cybersecurity intelligence platform.
