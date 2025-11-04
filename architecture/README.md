# Brett Blocks System Architecture Documentation

## 📋 Documentation Overview

This directory contains comprehensive architecture documentation for the Brett Blocks cybersecurity intelligence system. These documents provide detailed technical specifications for system designers, developers, and architects working with the platform.

**Key Update**: All documents have been updated with the corrected understanding of the **template-driven architecture** where class templates define both STIX object structure and Python function interfaces through automatic foreign key parameter generation.

## 📚 Document Structure

### Core Architecture
- **[system-overview.md](system-overview.md)** - High-level system architecture with template-driven design principles
- **[template-driven-architecture.md](template-driven-architecture.md)** - **NEW** - Detailed explanation of template-driven foreign key parameter generation
- **[block-architecture.md](block-architecture.md)** - Python block design patterns with automatic function signature generation
- **[stix-object-architecture.md](stix-object-architecture.md)** - STIX 2.1 object management with class template specifications

### STIX Object Pattern Analysis (NEW)
- **[stix-object-generation-patterns.md](stix-object-generation-patterns.md)** - **NEW** - Comprehensive analysis of ALL 15 STIX objects with complexity distribution and automation feasibility
- **[complete-stix-pattern-matrix.md](complete-stix-pattern-matrix.md)** - **NEW** - Complete function signature matrix and pattern analysis across all implemented STIX objects

### Component Architecture
- **[context-memory-architecture.md](context-memory-architecture.md)** - Persistent storage and state management **[UPDATED with Three-Tier Edge Relationship System]**
- **[orchestration-architecture.md](orchestration-architecture.md)** - Workflow composition and execution
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
| [template-driven-architecture.md](./template-driven-architecture.md) | ✅ New | 2025-10-27 | **NEW** - Comprehensive template-driven architecture documentation |
| [system-overview.md](./system-overview.md) | ✅ Updated | 2025-10-27 | Added template-driven architecture section with foreign key generation |
| [block-architecture.md](./block-architecture.md) | ✅ Updated | 2025-10-27 | Added foreign key parameter generation patterns and property type specifications |
| [stix-object-architecture.md](./stix-object-architecture.md) | ✅ Updated | 2025-10-27 | Added template structure specifications and property type documentation |
| [context-memory-architecture.md](./context-memory-architecture.md) | ✅ **MAJOR UPDATE** | 2025-10-30 | **CRITICAL DISCOVERIES**: Automatic STIX Object Routing, File Path Patterns, Context Evolution |
| [orchestration-architecture.md](./orchestration-architecture.md) | ✅ **MAJOR UPDATE** | 2025-10-30 | **VALIDATION COMPLETE**: NEW vs OLD Notebook Mathematical Equivalence Proof |
| [api-integration-architecture.md](./api-integration-architecture.md) | ✅ Complete | 2024-10-25 | External system interfaces and deployment strategies |
| [new-knowledge-summary.md](./new-knowledge-summary.md) | ✅ **MAJOR UPDATE** | 2025-10-30 | **BREAKTHROUGH DISCOVERIES**: Automatic STIX Routing, Mathematical Equivalence Proof, Template Optimization |

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