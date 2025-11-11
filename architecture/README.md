# Brett Blocks System Architecture Documentation

## 📋 Documentation Overview

This directory contains comprehensive architecture documentation for the Brett Blocks cybersecurity intelligence system. These documents provide detailed technical specifications for system designers, developers, and architects working with the platform.

**Key Update**: All documents have been updated with the corrected understanding of the **template-driven architecture** where class templates define both STIX object structure and Python function interfaces through automatic foreign key parameter generation.

## � How the System Pieces Interact

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    BRETT BLOCKS SYSTEM ARCHITECTURE                      │
└─────────────────────────────────────────────────────────────────────────┘

1. TEMPLATE-DRIVEN FOUNDATION
   Class Templates (*_template.json)
          ↓
   Define Structure & Generate Function Signatures
          ↓
   Python Blocks (make_*.py) + Data Templates (*.json)
          ↓
   [See: template-driven-architecture.md]

2. BLOCK EXECUTION & DATA FORMS
   Python Blocks execute with template-driven parameters
          ↓
   Generate STIX Objects (JSON)
          ↓
   Convert to Data Forms via Utilities
          ↓
   [See: block-architecture.md, reconstitution-and-notebook-generation.md]

3. RECONSTITUTION ENGINE
   Data Forms + Reconstitution Metadata
          ↓
   Restore References in Dependency Order
          ↓
   Reconstituted STIX Objects (99.3% accuracy)
          ↓
   [See: reconstitution-and-notebook-generation.md]

4. TESTING & VALIDATION
   Discovery: Find testable objects (53 objects across 15 types)
          ↓
   Generation: Create data forms (100% success)
          ↓
   Execution: STIXReconstitutionEngine (100% success)
          ↓
   Verification: DeepDiff comparison (100% pass rate)
          ↓
   Reporting: JSON & Markdown reports
          ↓
   [See: stixorm-testing-system-design.md]

5. CONTEXT MEMORY & ORCHESTRATION
   STIX Objects stored in context memory
          ↓
   Automatic object routing by STIX type
          ↓
   Workflow composition via Jupyter notebooks
          ↓
   [See: context-memory-architecture.md, orchestration-architecture.md]
```

## �📚 Document Structure

### Core Architecture (Start Here)
- **[system-overview.md](system-overview.md)** - High-level system architecture with template-driven design principles and dual-environment setup
- **[template-driven-architecture.md](template-driven-architecture.md)** - **CRITICAL** - How class templates generate Python function signatures and drive the entire system
- **[block-architecture.md](block-architecture.md)** - Python block design patterns with automatic function signature generation from templates

### Data Flow & Transformation
- **[reconstitution-and-notebook-generation.md](reconstitution-and-notebook-generation.md)** - **CRITICAL** - Complete data flow: STIX → Data Forms → Reconstitution → Notebooks (99.3% accuracy)
- **[stix-object-architecture.md](stix-object-architecture.md)** - STIX 2.1 object management with class template specifications

### Testing & Validation (NEW - Nov 2025)
- **[stixorm-testing-system-design.md](../architecture/stixorm-testing-system-design.md)** - **NEW** - Complete testing system achieving 100% pass rate, validates entire template → block → reconstitution pipeline

### STIX Object Pattern Analysis
- **[stix-object-generation-patterns.md](stix-object-generation-patterns.md)** - Comprehensive analysis of ALL 15 STIX objects with complexity distribution and automation feasibility
- **[complete-stix-pattern-matrix.md](complete-stix-pattern-matrix.md)** - Complete function signature matrix and pattern analysis across all implemented STIX objects

### Component Architecture
- **[context-memory-architecture.md](context-memory-architecture.md)** - Persistent storage and state management with automatic STIX object routing
- **[orchestration-architecture.md](orchestration-architecture.md)** - Workflow composition and execution with mathematical equivalence validation
- **[api-integration-architecture.md](api-integration-architecture.md)** - External system interfaces and deployment

### Reference Documents
- **[new-knowledge-summary.md](new-knowledge-summary.md)** - Summary of architectural discoveries and corrections

## 🔧 Template-Driven Architecture Highlights

### Critical Understanding
The StixORM system uses a sophisticated **three-file pattern** where:
1. **Class Templates** (`*_template.json`) define object structure AND generate Python function interfaces
2. **Data Templates** (`*.json`) provide actual values for template population
3. **Python Blocks** (`make_*.py`) automatically receive foreign key parameters based on template property types

### Foreign Key Parameter Generation
Properties with `ReferenceProperty` or `OSThreatReference` types automatically become function parameters:

```json
// In class template
"event_refs": {"property": "OSThreatReference", "parameters": {"valid_types": ["event"]}}
```

```python
// Automatically generates function signature
def make_incident(incident_form, event_refs=None, ...):
```

## 🚀 MAJOR ARCHITECTURAL DISCOVERIES (October 2025)

### Automatic STIX Object Routing
**CRITICAL DISCOVERY**: The `save_incident_context.py` function implements intelligent object routing based on STIX type, eliminating the need for manual `context_type` parameters in most cases.

### Brett Blocks File Path Patterns
**VALIDATED PATTERN**: Creation functions produce files WITHOUT `.json` extensions. Save operations must use exact paths: `results_path` (not `results_path + ".json"`).

### NEW vs OLD Notebook Mathematical Equivalence
**VALIDATION COMPLETE**: The optimized NEW notebook sequence (4 notebooks) produces mathematically identical results to the legacy OLD sequence (3 notebooks) while providing improved code clarity and maintainability.

### Context Memory Evolution Tracking
**METHODOLOGY ESTABLISHED**: Complete validation protocol for testing notebook sequences with file-level monitoring and mathematical equivalence verification.

## 📋 Document Status

| Document | Status | Last Updated | Key Updates |
|----------|--------|--------------|-------------|
| [system-overview.md](./system-overview.md) | ✅ Updated | 2025-11-10 | Complete system architecture with testing integration |
| [template-driven-architecture.md](./template-driven-architecture.md) | ✅ Complete | 2025-10-27 | Template-driven architecture with automatic parameter generation |
| [reconstitution-and-notebook-generation.md](./reconstitution-and-notebook-generation.md) | ✅ Updated | 2025-11-10 | Data forms, reconstitution engine (99.3%), testing validation (100%) |
| [stixorm-testing-system-design.md](../architecture/stixorm-testing-system-design.md) | ✅ **NEW** | 2025-11-10 | **Production testing system achieving 100% pass rate** |
| [block-architecture.md](./block-architecture.md) | ✅ Updated | 2025-10-27 | Foreign key parameter generation patterns and property types |
| [stix-object-architecture.md](./stix-object-architecture.md) | ✅ Updated | 2025-10-27 | Template structure specifications and property type documentation |
| [context-memory-architecture.md](./context-memory-architecture.md) | ✅ Updated | 2025-10-30 | Automatic STIX routing, file path patterns, context evolution |
| [orchestration-architecture.md](./orchestration-architecture.md) | ✅ Updated | 2025-10-30 | Notebook mathematical equivalence validation |
| [api-integration-architecture.md](./api-integration-architecture.md) | ✅ Complete | 2024-10-25 | External system interfaces and deployment strategies |
| [stix-object-generation-patterns.md](./stix-object-generation-patterns.md) | ✅ Complete | 2025-10-27 | Comprehensive analysis of 15 STIX object types |
| [complete-stix-pattern-matrix.md](./complete-stix-pattern-matrix.md) | ✅ Complete | 2025-10-27 | Complete function signature matrix across all objects |
| [new-knowledge-summary.md](./new-knowledge-summary.md) | ✅ Updated | 2025-10-30 | Architectural discoveries and breakthrough patterns |

## 🎯 Target Audience

**System Architects**: High-level design decisions and integration patterns
**Lead Developers**: Implementation strategies and technical constraints
**Security Engineers**: Security model and compliance requirements
**DevOps Engineers**: Deployment and operational considerations
**AI Assistants**: Comprehensive understanding for development support

## 🎯 Architecture Validation

These architecture documents have been **validated through practical implementation** by executing the Step_0 notebook and observing actual system behavior. Key insights include:

- **Context Memory Dual-Pattern**: User context (no setup) vs Company context (requires initialization)
- **Dual-Layer Object Storage**: STIX data in `original` field + UI metadata for visualization
- **Utility Function Framework**: Block simulation through wrapper functions for development
- **Array-Based Storage**: Objects stored as JSON arrays enabling multiple objects per context
- **Context Routing**: Global `context_map.json` manages multi-tenant architecture

All architectural specifications reflect **actual implementation patterns** observed during notebook execution, ensuring accuracy and practical applicability.

## 🔄 Document Maintenance

These architecture documents are **living specifications** that should be updated as the system evolves:

- **Version Control**: All changes tracked in git with detailed commit messages
- **Review Process**: Major architectural changes require review and approval
- **Consistency**: All documents must align with actual system implementation
- **Validation**: Regular validation against running system to ensure accuracy

## 🚀 Getting Started

**For System Understanding**:
1. Start with [system-overview.md](system-overview.md) for foundational concepts
2. Review [dual-environment-architecture.md](dual-environment-architecture.md) for deployment model
3. Study [block-architecture.md](block-architecture.md) for component design

**For Development Work**:
1. Begin with [development-patterns.md](development-patterns.md) for coding guidance
2. Reference [stix-object-architecture.md](stix-object-architecture.md) for data modeling
3. Use [context-memory-architecture.md](context-memory-architecture.md) for state management

**For Integration Projects**:
1. Review [api-integration-architecture.md](api-integration-architecture.md) for external interfaces
2. Study [orchestration-architecture.md](orchestration-architecture.md) for workflow design
3. Consider [security-architecture.md](security-architecture.md) for compliance requirements

## 📊 Architecture Principles

The Brett Blocks system is built on these foundational principles:

1. **Atomic Functionality**: Each component performs one well-defined function
2. **Stateless Execution**: Components communicate only via JSON files
3. **STIX 2.1 Compliance**: All cybersecurity data follows industry standards
4. **Context Isolation**: Secure execution environments with controlled access
5. **Orchestration Flexibility**: Components compose into complex workflows
6. **Production Ready**: Development patterns translate directly to production

These documents provide the definitive reference for understanding, extending, and maintaining the Brett Blocks cybersecurity intelligence platform.