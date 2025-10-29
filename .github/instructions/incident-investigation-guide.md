# Incident Investigation Instructions - **Template-Driven Implementation**

## 🎯 Purpose

This guide provides **template-driven implementation patterns** for creating comprehensive cybersecurity incident investigations using the Brett Blocks system. **Template-driven architecture** enables creation of complete incident contexts with evidence documentation, threat indicators, and forensic-quality investigation capabilities through automatic code generation.

## 🚨 Critical Template-Driven Implementation Discoveries

### 0. **Template-Driven Context Operations** - **Critical Definition**

**IMPORTANT**: Context memory uses template-driven storage patterns:

✅ **CORRECT**: Template-driven context memory maintains directory structure:
```powershell
# Clear template-generated context data, preserve directory structure  
Remove-Item -Path "context_mem\*" -Recurse -Force
# Result: Empty context_mem/ directory remains (template system functional)
```

❌ **WRONG**: Never delete the context_mem directory itself:
```powershell
# This breaks template-driven context system - DON'T DO THIS
Remove-Item -Path "context_mem" -Recurse -Force  
# Result: No context_mem/ directory (breaks template-driven context operations)
```

**Rationale**: The context memory directory is part of the template-driven architecture. Templates and auto-generated functions expect this directory structure for context storage operations.

### 1. **Template-Driven Parameter Generation** - **Critical Auto-Generation**

**Discovery**: Templates automatically generate function parameters based on property types:

**Template Property Type Auto-Generation**:

```python
# ✅ TEMPLATE-DRIVEN PARAMETER GENERATION - Real examples

# Incident_template.json property types → make_incident.py function parameters:
# "sequence_start_refs": {"type": "OSThreatReference"} → sequence_start_refs=None
# "event_refs": {"type": "OSThreatReference"} → event_refs=None  
# "impact_refs": {"type": "OSThreatReference"} → impact_refs=None

# Email_template.json property types → make_email_addr.py function parameters:
# "belongs_to_ref": {"type": "ReferenceProperty"} → usr_account=None

# Identity_template.json property types → make_identity.py function parameters:
# "contact_information": {"type": "EmbeddedObjectProperty"} → contact_information=None

# ✅ CORRECT - Use template-driven auto-generated parameters
incident_obj = invoke_make_incident_block(
    "SDO/Incident/incident_phishing.json",    # ✅ Data template path
    "step2/phishing_incident",                # Results path
    sequence_start_refs, sequence_refs, task_refs, event_refs, impact_refs, other_object_refs
    # All parameters auto-generated from Incident_template.json property types
)

# ❌ WRONG - Manual parameter definition ignoring template structure
# Never manually define parameters - always use template-driven auto-generation
```

### 2. **Three-Tier Context Architecture** - **Enhanced Understanding**

**User Context** (`/usr/`) - No setup required:
- Direct storage for personal identity objects
- Automatic directory creation on first write
- Array-based storage format

**Company Context** (`/identity--{uuid}/`) - Setup required:
- Must call `invoke_create_company_context()` first
- Category-based storage (users.json, systems.json, assets.json)
- Enterprise scope for organizational infrastructure

**Incident Context** (`/incident--{uuid}/`) - **NEW VALIDATED PATTERN**:
- Must call `invoke_create_incident_context()` first  
- Evidence categorization (observables.json, indicators.json, relationships.json)
- Investigation scope for forensic evidence tracking

### 3. **Context Type Categories** - **Validated Storage Patterns**

```python
# Incident context storage categories (validated through execution)
incident_context_types = {
    "incident": "incident.json",           # Primary incident object
    "observables": "observables.json",     # Evidence objects (email, URL, file)
    "indicators": "indicators.json",       # Threat detection patterns
    "relationships": "relationships.json", # Evidence-to-incident linkages
    "evidence": "evidence.json",           # General investigation evidence
    "analysis": "analysis.json"            # Investigation findings and reports
}

# Usage pattern for categorized storage
context_type = {"context_type": "observables"}  # Specify storage category
result = invoke_save_incident_context_block(obj_path, context_path, context_type)
```

## 🔍 Validated Incident Investigation Workflow

### Step 1: Initialize Incident Context

```python
# Create primary incident object
incident_template_path = "SDO/Incident/incident_phishing.json"  # ✅ Relative path
incident_results_path = "step2/phishing_incident"

incident_obj = invoke_make_incident_block(
    incident_template_path,
    incident_results_path,
    sequence_start_refs=[],  # Initialize empty lists
    sequence_refs=[],
    task_refs=[],
    event_refs=[], 
    impact_refs=[],
    other_object_refs=[]
)

# Create incident context directory structure
incident_results_obj_path = results_base + incident_results_path + "__incident.json"
incident_results_context_path = results_base + "step2/context/phishing_incident_context.json"

# Initialize incident context storage
result = invoke_create_incident_context(incident_results_obj_path, incident_results_context_path)
```

### Step 2: Document Evidence Objects

```python
# Create email evidence
attacker_email_template = "SCO/Email_Addr/email_addr_malicious.json"  # ✅ Relative path
attacker_email_results = "step2/attacker_email"

attacker_email_obj = invoke_make_email_addr_block(
    attacker_email_template,
    attacker_email_results
)

# Store in observables context
context_type = {"context_type": "observables"}  # ✅ Evidence categorization
attacker_email_obj_path = results_base + attacker_email_results + "__email.json" 
attacker_email_context_path = results_base + "step2/context/attacker_email_context.json"

result = invoke_save_incident_context_block(
    attacker_email_obj_path,
    attacker_email_context_path,
    context_type
)

# Create URL evidence
malicious_url_template = "SCO/URL/url_malicious.json"  # ✅ Relative path  
malicious_url_results = "step2/malicious_url"

malicious_url_obj = invoke_make_url_block(
    malicious_url_template,
    malicious_url_results
)

# Store in same observables context
malicious_url_obj_path = results_base + malicious_url_results + "__url.json"
malicious_url_context_path = results_base + "step2/context/malicious_url_context.json"

result = invoke_save_incident_context_block(
    malicious_url_obj_path,
    malicious_url_context_path,
    context_type  # Same observables category
)

# Create file evidence  
malicious_file_template = "SCO/File/file_suspicious.json"  # ✅ Relative path
malicious_file_results = "step2/malicious_attachment"

malicious_file_obj = invoke_make_file_block(
    malicious_file_template,
    malicious_file_results
)

# Store in observables context
malicious_file_obj_path = results_base + malicious_file_results + "__file.json"
malicious_file_context_path = results_base + "step2/context/malicious_file_context.json"

result = invoke_save_incident_context_block(
    malicious_file_obj_path,
    malicious_file_context_path,
    context_type
)
```

### Step 3: Create Threat Indicators

```python
# Create email domain indicator for future detection
email_indicator_template = "SDO/Indicator/indicator_email_domain.json"  # ✅ Relative path
email_indicator_results = "step2/email_domain_indicator"

email_indicator_obj = invoke_make_indicator_block(
    email_indicator_template,
    email_indicator_results
)

# Store in indicators context
context_type = {"context_type": "indicators"}  # ✅ Threat pattern categorization
email_indicator_obj_path = results_base + email_indicator_results + "__indicator.json"
email_indicator_context_path = results_base + "step2/context/email_indicator_context.json"

result = invoke_save_incident_context_block(
    email_indicator_obj_path,
    email_indicator_context_path,
    context_type
)

# Create URL pattern indicator
url_indicator_template = "SDO/Indicator/indicator_url_pattern.json"  # ✅ Relative path
url_indicator_results = "step2/url_pattern_indicator"

url_indicator_obj = invoke_make_indicator_block(
    url_indicator_template,
    url_indicator_results
)

# Store in same indicators context
url_indicator_obj_path = results_base + url_indicator_results + "__indicator.json"
url_indicator_context_path = results_base + "step2/context/url_indicator_context.json"

result = invoke_save_incident_context_block(
    url_indicator_obj_path,
    url_indicator_context_path,
    context_type  # Same indicators category
)
```

### Step 4: Create Investigation Relationships

```python
# Link evidence objects to the incident
evidence_relationship_template = "SRO/Relationship/relationship_evidence.json"  # ✅ Relative path
evidence_relationship_results = "step2/evidence_relationships"

# Create relationships linking evidence to incident
relationship_type = "related-to"  # Evidence is related to incident

email_relationship = invoke_sro_block(
    evidence_relationship_template,
    evidence_relationship_results + "_email",
    attacker_email_obj,   # Source: evidence object
    incident_obj,         # Target: incident object
    relationship_type
)

url_relationship = invoke_sro_block(
    evidence_relationship_template,
    evidence_relationship_results + "_url",
    malicious_url_obj,    # Source: evidence object
    incident_obj,         # Target: incident object
    relationship_type
)

file_relationship = invoke_sro_block(
    evidence_relationship_template,
    evidence_relationship_results + "_file", 
    malicious_file_obj,   # Source: evidence object
    incident_obj,         # Target: incident object
    relationship_type
)

# Store relationships in appropriate context
context_type = {"context_type": "relationships"}  # ✅ Relationship categorization
relationships_obj_path = results_base + evidence_relationship_results + "__relationships.json"
relationships_context_path = results_base + "step2/context/evidence_relationships_context.json"

result = invoke_save_incident_context_block(
    relationships_obj_path,
    relationships_context_path,
    context_type
)
```

## 📁 Resulting Context Memory Structure

```text
context_mem/
├── context_map.json                    # Global context routing (updated)
├── usr/                               # Personal user context
├── identity--{company-uuid}/           # Company context  
└── incident--{incident-uuid}/          # ✅ NEW: Incident investigation context
    ├── incident.json                  # Primary incident STIX object
    ├── observables.json               # Email, URL, file evidence objects
    ├── indicators.json                # Email domain, URL pattern threat indicators
    ├── relationships.json             # Evidence-to-incident linkages
    ├── sequence_start_refs.json       # Attack vector initiation points
    ├── sequence_refs.json             # Attack progression chain
    ├── impact_refs.json               # Business impact assessment
    └── unattached_objs.json           # Evidence pending classification
```

## ✅ Validation Checklist

When implementing incident investigations, ensure:

- **✅ Template Paths**: Use relative paths from StixORM directory only
- **✅ Context Initialization**: Call `invoke_create_incident_context()` before storage
- **✅ Context Types**: Specify appropriate categories for evidence storage
- **✅ Evidence Documentation**: Create observables for all investigation evidence
- **✅ Threat Indicators**: Generate patterns for future detection and prevention
- **✅ Relationship Modeling**: Link evidence objects to primary incident
- **✅ Categorized Storage**: Organize objects by type in appropriate context files

## 🎯 Investigation Capabilities Achieved

This validated implementation provides:

- **Complete Evidence Chain**: Forensic-quality evidence documentation
- **Threat Intelligence**: Actionable indicators for future detection
- **Investigation Context**: Isolated storage for incident-specific data
- **STIX 2.1 Compliance**: Industry-standard cybersecurity object format
- **Relationship Modeling**: Clear connections between evidence and incident
- **Scalable Architecture**: Context memory system supports multiple concurrent investigations

## 🚀 Next Steps for Investigation Enhancement

- **Evidence Analysis**: Examine collected observables for attack patterns
- **Threat Hunting**: Use indicators to search for similar attacks across infrastructure  
- **Impact Assessment**: Document business impact and affected systems
- **Response Actions**: Implement containment and remediation measures
- **Intelligence Sharing**: Export STIX objects for threat intelligence distribution
- **Investigation Reports**: Generate comprehensive analysis documentation

This validated incident investigation framework provides the foundation for sophisticated cybersecurity operations while maintaining industry-standard STIX compliance and enabling advanced investigation capabilities.