# 🚀 Brett Blocks AI Assistant Guide - Complete Reference with Smart Indexing

**Last Updated:** 2025-11-08  
**Status:** ✅ Production-Ready with Validated Patterns

---

## 📖 TABLE OF CONTENTS - SMART INDEX

### 🎯 Quick Start (5 min)
- [Critical Rules](#critical-rules) - Must-know patterns
- [Common Mistakes](#common-mistakes) - What to avoid
- [File Structure](#file-structure-quick-reference) - Where everything lives

### 🏗️ Architecture (15 min)
- [Template-Driven System](#template-driven-architecture) - Core concept
- [STIX Object Patterns](#stix-object-implementation) - All 88 objects
- [Context Memory](#context-memory-system) - State management
- [Data Forms & Reconstitution](#data-forms-and-reconstitution) - NEW Nov 2025

### 💻 Development (30 min)
- [Notebook Patterns](#notebook-development-patterns) - How to create workflows
- [Utility Functions](#utility-function-reference) - Complete API
- [Testing](#testing-and-validation) - Validation approaches

### 📚 Deep Dive (60 min)
- [Complete STIX Analysis](#complete-stix-object-analysis) - All implementations
- [Round-Trip Workflows](#round-trip-workflows) - Data form conversion
- [Advanced Patterns](#advanced-patterns) - Complex scenarios

---

## 🎯 CRITICAL RULES

### Rule 1: Never Add .json Extension
```python
# ✅ CORRECT
results_path = "step3/observation_anecdote"
save_path = results_base + results_path

# ❌ WRONG - Causes PermissionError
save_path = results_base + results_path + ".json"
```

### Rule 2: Use Utility Functions, Never Direct Blocks
```python
# ✅ CORRECT  
from Utilities.local_make_general import invoke_make_object_from_data_form_block
obj = invoke_make_object_from_data_form_block(data_form_path, results_path)

# ❌ WRONG
from Block_Families.SDO.Campaign.script import main
obj = main(input, output)  # Never call blocks directly
```

### Rule 3: Small Notebook Cells with Descriptive Text
```python
# ✅ CORRECT - One object per cell
### Campaign #1
Create object from data form: `campaign_data_form.json`

# Load data form and create object
data_form_path = 'SDO/Campaign_form/campaign_data_form.json'
results_path = 'generated/campaign_1.json'
obj = invoke_make_object_from_data_form_block(data_form_path, results_path)

# ❌ WRONG - Large cells without description
# Creating 50 objects in one cell with no markdown
```

### Rule 4: Follow Creation Sequence for Dependencies
```python
# ✅ CORRECT - Process in dependency order
creation_sequence = load_reconstitution_data()['creation_sequence']
for obj_info in creation_sequence:  # Ordered by dependencies
    create_object(obj_info)

# ❌ WRONG - Random order breaks references
for obj in random_order:
    create_object(obj)
```

### Rule 5: Data Forms Go Alongside Templates
```python
# ✅ CORRECT location
Block_Families/StixORM/SDO/Campaign_form/
├── campaign_template.json          ← Template
└── campaign_*_data_form.json       ← Data form

# ❌ WRONG - Separate directory
separate_data_forms/campaign_form.json
```

---

## 🚫 COMMON MISTAKES

### Mistake 1: Calling Blocks Directly
**Problem:** Bypasses utility layer, breaks path handling
**Solution:** Always use `invoke_*_block()` functions from Utilities/

### Mistake 2: Incorrect Import Statements in Notebooks
**Problem:** Using complex import paths
**Solution:** Follow existing notebook patterns:
```python
from Utilities.local_make_general import invoke_save_unattached_context_block
from Utilities.local_make_sdo import *
```

### Mistake 3: Large Notebook Cells
**Problem:** Hard to debug, doesn't match existing notebooks
**Solution:** One object per cell, maximum 30 lines

### Mistake 4: Missing Progress Indicators
**Problem:** No visibility into execution
**Solution:** Print statements with emojis:
```python
print(f'📝 Creating campaign from data form...')
print(f'✅ campaign #1 created successfully')
```

### Mistake 5: Ignoring Creation Sequence
**Problem:** Objects created before their dependencies exist
**Solution:** Always use `creation_sequence` from reconstitution_data.json

---

## 📁 FILE STRUCTURE - QUICK REFERENCE

```
brett_blocks/
├── .github/
│   └── instructions/
│       └── README.md                      ← You are here
│
├── architecture/
│   ├── reconstitution-and-notebook-generation.md  ← NEW: Data forms guide
│   ├── template-driven-architecture.md    ← Core architecture
│   └── stix-object-generation-patterns.md ← All 88 STIX objects
│
├── Block_Families/
│   ├── StixORM/                           ← Templates AND data forms
│   │   ├── SDO/
│   │   │   ├── Campaign_form/
│   │   │   │   ├── campaign_template.json
│   │   │   │   └── *_data_form.json      ← Generated here
│   │   │   └── .../
│   │   ├── SCO/
│   │   └── SRO/
│   │
│   ├── OS_Triage/
│   │   ├── Save_Context/                  ← Context save blocks
│   │   ├── Get_Context/                   ← Context retrieval
│   │   └── Create_Context/                ← Context creation
│   │
│   └── General/
│       └── _library/                      ← Shared utilities
│
├── Orchestration/
│   ├── Utilities/
│   │   ├── reconstitute_and_generate_notebooks.py  ← NEW: Dual-mode system
│   │   ├── reconstitute_object_list.py    ← Reconstitution engine
│   │   ├── convert_object_list_to_data_forms.py   ← Data form creation
│   │   ├── local_make_general.py          ← General utilities
│   │   ├── local_make_sdo.py              ← SDO creation
│   │   ├── local_make_sco.py              ← SCO creation
│   │   └── local_make_sro.py              ← SRO creation
│   │
│   ├── Results/                           ← All generated objects
│   │   └── generated/
│   │       └── context/                   ← Context memory
│   │
│   ├── Step_0_User_Setup.ipynb            ← User context workflow
│   ├── Step_1_Company_Setup.ipynb         ← Company context workflow
│   ├── Step_2_Create_Incident_with_an_Alert.ipynb  ← Incident workflow
│   └── Step_3_Get the Anecdote.ipynb      ← Evidence collection
│
└── test*.py                               ← Test scripts
```

---

## 🏗️ TEMPLATE-DRIVEN ARCHITECTURE

### Three-File Pattern

Every STIX object uses three files:

1. **Class Template** (`*_template.json`)
   - Defines object structure
   - Specifies property types
   - Generates function parameters automatically

2. **Data Template** (`*.json` or `*_data_form.json`)
   - Provides actual values
   - Populated by user or system
   - Used for object creation

3. **Python Block** (`script.py`)
   - Processes templates
   - Creates STIX objects
   - Saves to TypeDB or files

### Automatic Parameter Generation

```json
// In class template
{
  "event_refs": {
    "property": "OSThreatReference",
    "parameters": {
      "valid_types": ["event"]
    }
  }
}
```

```python
// Automatically becomes function parameter
def make_incident(
    incident_form,
    event_refs=None,    ← Generated automatically
    sequence_refs=None, ← Generated automatically
    task_refs=None      ← Generated automatically
):
```

**Benefit:** 30-40% fewer manual parameters required

---

## 🎯 STIX OBJECT IMPLEMENTATION

### Current Status (15 of 88 objects)

**SDO (System Domain Objects) - 8 implemented:**
- Attack Pattern, Campaign, Event, Identity, Incident, Indicator, Note, Observed Data

**SCO (Cyber Observable Objects) - 5 implemented:**
- Domain Name, Email Address, Email Message, URL, User Account  

**SRO (STIX Relationship Objects) - 2 implemented:**
- Relationship, Sighting

### Complexity Distribution (All 88 Objects)

| Complexity | Param Count | Objects | Percentage | Automation Feasibility |
|------------|-------------|---------|------------|----------------------|
| MINIMAL    | 0-1        | 41      | 47%        | ✅ High - Auto-generate |
| LOW        | 2          | 16      | 18%        | ✅ Medium - Template-driven |
| MODERATE   | 3-4        | 15      | 17%        | ⚠️ Medium - Manual testing |
| HIGH       | 5          | 5       | 6%         | ⚠️ Low - Complex integration |
| VERY HIGH  | 6          | 6       | 7%         | ❌ Low - Manual integration |
| EXTREME    | 7+         | 5       | 6%         | ❌ Very Low - Expert needed |

**Key Insight:** 65% of all STIX objects (MINIMAL + LOW) are highly automatable

See `architecture/stix-object-generation-patterns.md` for complete analysis.

---

## 💾 CONTEXT MEMORY SYSTEM

### Four Context Types

1. **Unattached** (`/incident_1/unattached_objs`)
   - Temporary storage
   - Objects not yet associated
   - Cleared when moved to other contexts

2. **Incident** (`/incident--{uuid}/`)
   - Investigation-specific objects
   - Evidence, events, tasks
   - Full workflow state

3. **Company** (`/identity--{uuid}/`)
   - Organizational data
   - Employees, infrastructure
   - Persistent across incidents

4. **User** (`/usr/`)
   - Analyst preferences
   - Personal settings
   - Cross-company persistence

### Context Save Functions

```python
# Unattached context
from Utilities.local_make_general import invoke_save_unattached_context_block
result = invoke_save_unattached_context_block(obj_path, context_path, context_type)

# Incident context  
from Utilities.local_make_general import invoke_save_incident_context_block
result = invoke_save_incident_context_block(obj_path, context_path, context_type)

# Company context
from Utilities.local_make_general import invoke_save_company_context_block
result = invoke_save_company_context_block(obj_path, context_path, context_type)

# User context
from Utilities.local_make_general import invoke_save_user_context_block
result = invoke_save_user_context_block(obj_path, context_path)
```

---

## 🔄 DATA FORMS AND RECONSTITUTION

### Overview (NEW - November 2025)

**Data forms** enable round-trip conversion with 99.3%+ accuracy:
1. STIX Objects → Data Forms (conversion)
2. Data Forms → Reconstituted STIX Objects (reconstitution)
3. Data Forms → Executable Notebooks (generation)

### Creating Data Forms

```python
from Orchestration.Utilities.convert_object_list_to_data_forms import (
    create_data_forms_from_stix_objects
)

result = create_data_forms_from_stix_objects(
    stix_objects=my_objects,
    test_directory='Block_Families/StixORM'
)

# Creates:
# - *_data_form.json files (one per object)
# - reconstitution_data.json (metadata + sequence)
# - creation_sequence.json (dependency order)
```

### Reconstituting Objects

```python
from Orchestration.Utilities.reconstitute_and_generate_notebooks import (
    reconstitute_and_generate
)

# Mode 1: Test reconstitution
result = reconstitute_and_generate(
    mode='test',
    data_forms_dir='Block_Families/StixORM',
    reconstitution_data_file='Block_Families/StixORM/reconstitution_data.json',
    output_dir='test_output'
)

print(f"Reconstituted: {result['objects_created']} objects")
print(f"Success rate: {result['success_rate']}")
```

### Generating Notebooks

```python
# Mode 2: Generate executable notebook
result = reconstitute_and_generate(
    mode='notebook',
    stix_objects=my_objects,
    output_dir='Orchestration',
    notebook_name='My_Workflow.ipynb',
    context_type='unattached'  # or 'incident', 'company', 'user'
)

print(f"Generated: {result['notebook_path']}")
print(f"Cells: {result['cell_count']}")
```

### Data Form Structure

```json
{
  "campaign_form": {
    "type": "campaign",
    "spec_version": "2.1",
    "id": "campaign--0e79d112-...",
    "name": "Green Group Attacks",
    "description": "...",
    "created": "2016-04-06T20:03:00.000Z",
    "modified": "2016-04-06T20:03:00.000Z"
  }
}
```

### Reconstitution Metadata

Stored in `reconstitution_data.json`:

```json
{
  "creation_sequence": [
    {
      "form_name": "location_form",
      "filename": "location_fbd9947e_data_form.json",
      "object_id": "location--fbd9947e-...",
      "type": "location"
    },
    ...
  ],
  "reference_info": {
    "campaign--0e79d112-...": {
      "refs": {},
      "embedded": {}
    }
  }
}
```

**Key Points:**
- **creation_sequence** defines dependency order
- **reference_info** tracks all object relationships
- **Statistics** validate conversion accuracy

---

## 📓 NOTEBOOK DEVELOPMENT PATTERNS

### Pattern 1: Environment Setup

**Every notebook must start with:**

```python
# Cell 1: Install STIX libraries
import sys
!{sys.executable} -m pip install stixorm

# Import core STIX 2.1 objects
from stixorm.module.authorise import import_type_factory
from stixorm.module.definitions.stix21 import *

# Initialize import factory
import_type = import_type_factory.get_all_imports()

print('✅ STIX libraries initialized')
```

### Pattern 2: Path Configuration

```python
# Cell 2: Configure paths
import sys
sys.path.append('../')
import os

cwd = os.getcwd()
print(f'✅ Working directory: {cwd}')
print('✅ Python path configured')
```

### Pattern 3: Utility Imports

```python
# Cell 3: Import utilities (context-aware)
import json
import os

# Import Brett Blocks utility functions
from Utilities.local_make_general import (
    invoke_save_unattached_context_block,
    invoke_make_object_from_data_form_block
)
from Utilities.util import emulate_ports, unwind_ports, conv

# Import STIX object creation utilities
from Utilities.local_make_sdo import *
from Utilities.local_make_sco import *
from Utilities.local_make_sro import *

# Configure base paths
path_base = '../Block_Families/StixORM/'
results_base = '../Orchestration/Results/'

# Ensure directories exist
os.makedirs(results_base + 'generated/context', exist_ok=True)

print('✅ Brett Blocks utilities imported')
print('✅ Context type: unattached')
```

### Pattern 4: Object Creation Cell (Small & Focused)

```markdown
### Campaign #1

Create object from data form: `campaign_Green_Group_data_form.json`
```

```python
# Load data form and create object
data_form_path = 'SDO/Campaign_form/campaign_Green_Group_data_form.json'
results_path = 'generated/campaign_1.json'

print(f'📝 Creating campaign from data form...')

# Create object from data form using utility block
obj_1 = invoke_make_object_from_data_form_block(data_form_path, results_path)

# Configure context type
context_type = {'context_type': 'unattached'}

# Define storage paths
obj_path = results_base + results_path
context_path = results_base + 'generated/context/campaign_1_context.json'

# Save to unattached context
result = invoke_save_unattached_context_block(obj_path, context_path, context_type)

print(f'✅ campaign #1 created successfully')
print(f'   Object: {obj_path}')
print(f'   Context saved: {result}')
```

### Pattern 5: Summary Cell

```markdown
## Summary

✅ Successfully created 8 STIX objects
✅ All objects saved to unattached context

All objects are now available in context memory for use in investigations and analysis.
```

### Cell Size Guidelines

- **Maximum 30 lines per code cell**
- **One object per cell** (preferred)
- **Markdown before every code cell**
- **Progress indicators** (📝, ✅, ❌)
- **Path confirmations** in output

---

## 🛠️ UTILITY FUNCTION REFERENCE

### Object Creation from Data Forms

```python
invoke_make_object_from_data_form_block(data_form_path, results_path) -> Dict
```

**Args:**
- `data_form_path`: Relative path from `path_base` to data form JSON
- `results_path`: Relative path from `results_base` for output

**Returns:** Created STIX object dictionary

**Example:**
```python
obj = invoke_make_object_from_data_form_block(
    'SDO/Campaign_form/campaign_data_form.json',
    'generated/campaign_1.json'
)
```

### Context Save Functions

#### Unattached Context
```python
invoke_save_unattached_context_block(obj_path, context_path, context_type) -> Dict
```

#### Incident Context
```python
invoke_save_incident_context_block(obj_path, context_path, context_type) -> Dict
```

#### Company Context
```python
invoke_save_company_context_block(obj_path, context_path, context_type) -> Dict
```

#### User Context
```python
invoke_save_user_context_block(obj_path, context_path) -> Dict
```

**Common Args:**
- `obj_path`: Full path to STIX object JSON file
- `context_path`: Full path for context save result
- `context_type`: Dict with `{'context_type': 'unattached'}` (or 'observables', 'event', etc.)

### SDO Creation Functions

All in `Utilities/local_make_sdo.py`:

```python
invoke_make_campaign_block(template_path, results_path)
invoke_make_indicator_block(template_path, results_path, pattern=None)
invoke_make_identity_block(template_path, results_path, email_results=None, acct_results=None)
invoke_make_incident_block(template_path, results_path, event_refs=None, ...)
invoke_make_event_block(template_path, results_path)
invoke_make_observed_data_block(template_path, results_path, observation=None)
```

### SCO Creation Functions

All in `Utilities/local_make_sco.py`:

```python
invoke_make_email_addr_block(template_path, results_path)
invoke_make_url_block(template_path, results_path)
invoke_make_domain_name_block(template_path, results_path)
invoke_make_user_account_block(template_path, results_path)
invoke_make_e_msg_block(template_path, results_path, from_ref, to_ref, cc_ref, bcc_ref)
```

### SRO Creation Functions

All in `Utilities/local_make_sro.py`:

```python
invoke_make_relationship_block(template_path, results_path, source, target)
invoke_sighting_block(template_path, results_path, observed, sighted, where)
```

---

## ✅ TESTING AND VALIDATION

### Test Scripts

**1. Notebook Generation Test**
```bash
poetry run python test_notebook_generation.py
```

Validates:
- Data form creation
- Notebook structure
- Cell organization
- File generation

**2. Round-Trip Test**
```bash
poetry run python test_roundtrip.py
```

Validates:
- STIX → Data Forms conversion
- Data Forms → STIX reconstitution
- Accuracy percentage

### Validation Criteria

✅ **Notebook Structure**
- 29 cells minimum (18 markdown, 11 code)
- Small cells (< 30 lines)
- Descriptive markdown before code

✅ **Data Form Accuracy**
- 99.3%+ reconstitution success
- All references preserved
- Dependency order maintained

✅ **Context Memory**
- Objects saved correctly
- Context types accurate
- File paths correct

---

## 🔍 COMPLETE STIX OBJECT ANALYSIS

### Implementation Priority Matrix

**Tier 1: High-Value, Low-Complexity (Immediate Implementation)**
- Artifact (0 params) - File attachments
- Directory (0 params) - File system paths
- File (1 param) - File objects
- MAC Address (0 params) - Network identifiers
- Mutex (0 params) - Synchronization primitives

**Tier 2: Medium-Value, Low-Complexity (Next Quarter)**
- IPv4/IPv6 Address (0 params each)
- Network Traffic (2 params)
- Process (1 param)
- Software (0 params)
- Windows Registry Key (0 params)

**Tier 3: High-Value, Medium-Complexity (Future)**
- Malware, Tool, Vulnerability (2 params each)
- Infrastructure, Threat Actor, Intrusion Set (3-4 params)

**Tier 4: Specialized/Complex (As Needed)**
- Course of Action, Grouping, Location (3-5 params)
- Opinion, Language Content (6-7 params)

### Full Object Catalog

See `architecture/stix-object-generation-patterns.md` for:
- Complete function signature matrix
- Complexity analysis
- Implementation recommendations
- Automation feasibility scores

---

## 🚀 ROUND-TRIP WORKFLOWS

### Workflow 1: STIX Objects → Data Forms → Notebook

```python
# Step 1: Create data forms
from Orchestration.Utilities.convert_object_list_to_data_forms import (
    create_data_forms_from_stix_objects
)

result = create_data_forms_from_stix_objects(
    stix_objects=my_objects,
    test_directory='Block_Families/StixORM'
)

# Step 2: Generate notebook
from Orchestration.Utilities.reconstitute_and_generate_notebooks import (
    reconstitute_and_generate
)

notebook_result = reconstitute_and_generate(
    mode='notebook',
    stix_objects=my_objects,
    output_dir='Orchestration',
    notebook_name='My_Workflow.ipynb',
    context_type='incident'
)

# Step 3: Execute notebook (manual or automated)
# Open and run: Orchestration/My_Workflow.ipynb
```

### Workflow 2: Data Forms → Reconstituted STIX Objects

```python
# Reconstitute from existing data forms
result = reconstitute_and_generate(
    mode='test',
    data_forms_dir='Block_Families/StixORM',
    reconstitution_data_file='Block_Families/StixORM/reconstitution_data.json',
    output_dir='validation_output'
)

# Validate
print(f"Original: {len(original_objects)}")
print(f"Reconstituted: {result['objects_created']}")
print(f"Success rate: {result['success_rate']}")
```

### Workflow 3: Full Round-Trip Validation

```python
# 1. Start with STIX objects
original_objects = [campaign, indicator, location, ...]

# 2. Convert to data forms
create_data_forms_from_stix_objects(original_objects, 'Block_Families/StixORM')

# 3. Reconstitute from data forms
recon_result = reconstitute_and_generate(mode='test', ...)

# 4. Compare
reconstituted_objects = recon_result['objects']
compare_objects(original_objects, reconstituted_objects)

# Expected: 99.3%+ match
```

---

## 🎓 ADVANCED PATTERNS

### Custom Context Types

```python
# Define custom context type for specialized storage
context_type = {
    'context_type': 'threat_intel'  # Custom category
}

result = invoke_save_incident_context_block(
    obj_path,
    context_path,
    context_type
)
```

### Batch Object Creation

```python
# Process multiple objects efficiently
for i, obj_info in enumerate(creation_sequence, 1):
    data_form_path = f"{obj_info['type']}_form/{obj_info['filename']}"
    results_path = f"generated/{obj_info['type']}_{i}.json"
    
    obj = invoke_make_object_from_data_form_block(data_form_path, results_path)
    # Save to context...
```

### Dynamic Notebook Generation

```python
# Generate notebooks programmatically for different contexts
for context in ['unattached', 'incident', 'company', 'user']:
    reconstitute_and_generate(
        mode='notebook',
        stix_objects=my_objects,
        notebook_name=f'Test_{context.title()}_Context.ipynb',
        context_type=context
    )
```

---

## 📚 ADDITIONAL RESOURCES

### Architecture Documentation
- `architecture/reconstitution-and-notebook-generation.md` - Complete reconstitution guide
- `architecture/template-driven-architecture.md` - Core architecture principles
- `architecture/stix-object-generation-patterns.md` - All 88 STIX objects analyzed
- `architecture/context-memory-architecture.md` - Context memory system

### Example Notebooks
- `Orchestration/Step_0_User_Setup.ipynb` - User context setup
- `Orchestration/Step_1_Company_Setup.ipynb` - Company context setup
- `Orchestration/Step_2_Create_Incident_with_an_Alert.ipynb` - Incident creation
- `Orchestration/Step_3_Get the Anecdote.ipynb` - Evidence collection

### Test Scripts
- `test_notebook_generation.py` - Notebook generation validation
- `test_roundtrip.py` - Round-trip conversion testing
- `example_reconstitute_generate.py` - Usage examples

---

## 🎯 QUICK DECISION TREE

**Creating a new workflow?**
→ Generate notebook using `reconstitute_and_generate(mode='notebook', ...)`

**Have STIX objects to process?**
→ Convert to data forms using `create_data_forms_from_stix_objects()`

**Need to validate conversion?**
→ Run `reconstitute_and_generate(mode='test', ...)`

**Adding objects to context?**
→ Use `invoke_save_*_context_block()` functions

**Working with templates?**
→ Use `invoke_make_object_from_data_form_block()`

**Debugging notebook cells?**
→ Check: imports, paths, cell size, descriptive text

---

## ✨ KEY TAKEAWAYS

1. **Always use utility functions** - Never call blocks directly
2. **Never add .json extensions** - Functions handle this
3. **Follow creation sequence** - Dependencies matter
4. **Small, focused cells** - One object per cell
5. **Descriptive markdown** - Text before every code cell
6. **Progress indicators** - Emoji + print statements
7. **Store alongside templates** - Data forms go in StixORM/
8. **99.3%+ accuracy** - Round-trip conversion works
9. **Four context types** - Unattached, incident, company, user
10. **65% automatable** - Most STIX objects are simple

---

**Last Updated:** 2025-11-08  
**Maintainer:** Brett Blocks Development Team  
**Status:** ✅ Production-Ready
