# STIX Object Reconstitution and Notebook Generation System

## Overview

This system provides **two operational modes** for working with STIX objects and data forms:

1. **Test Mode**: Reconstitute STIX objects from data forms for validation testing
2. **Notebook Mode**: Generate executable Jupyter notebooks that create objects and save to context memory

## Purpose

### Mode 1: Test Mode (Validation)
- Validate round-trip conversion (STIX → data form → STIX)
- Verify structural integrity of reconstituted objects
- Test reference restoration and UUID mapping
- Quality assurance for data form templates

### Mode 2: Notebook Mode (Production)
- Generate executable notebooks for creating STIX objects
- Store data forms alongside templates in `Block_Families/StixORM/`
- Create notebooks that invoke blocks to create objects in sequence
- Save objects to context memory (unattached, incident, company, or user)

## Architecture

```
Mode 1 (Test):
STIX Objects → Data Forms → Reconstituted Objects
                 ↓
            Validation & Comparison

Mode 2 (Notebook):
STIX Objects → Data Forms → Jupyter Notebook
                 ↓               ↓
        Block_Families/      Orchestration/
         StixORM/           (executable notebook)
                                 ↓
                          Context Memory
                    (unattached/incident/company/user)
```

## Usage

### Mode 1: Test Mode

```python
from Orchestration.Utilities.reconstitute_and_generate_notebooks import reconstitute_and_generate

# Reconstitute objects for validation
results = reconstitute_and_generate(
    mode='test',
    data_forms_dir=Path('generated/data_forms'),
    reconstitution_data_file=Path('generated/data_forms/reconstitution_data.json'),
    output_dir=Path('generated/reconstituted')
)

if results['success']:
    print(f"✅ Reconstituted {len(results['generated_files'])} objects")
else:
    print(f"❌ Errors: {results['errors']}")
```

### Mode 2: Notebook Mode

```python
from Orchestration.Utilities.reconstitute_and_generate_notebooks import reconstitute_and_generate

# Load STIX objects
stix_objects = [...]  # Your STIX objects list

# Generate notebook for user context
results = reconstitute_and_generate(
    mode='notebook',
    stix_objects=stix_objects,
    notebook_name='User_Setup',
    context_type='user',  # unattached, incident, company, or user
    notebook_title='User Context Setup',
    notebook_description='Create user identity and save to user context'
)

if results['success']:
    print(f"✅ Notebook created: {results['notebook_path']}")
    print(f"✅ Data forms: {results['data_forms_created']}")
```

## Context Types

The system supports four context memory locations:

| Context Type | Use Case | Save Function |
|-------------|----------|---------------|
| `unattached` | Objects not linked to specific incident/company | `save_unattached_context.py` |
| `incident` | Incident-specific evidence and investigation data | `save_incident_context.py` |
| `company` | Company infrastructure and organizational data | `save_company_context.py` |
| `user` | User-specific identity and account information | `save_user_context.py` |

## Generated Notebook Structure

Notebooks generated in Mode 2 follow this structure:

```python
# 1. Title and description
# 2. Environment setup (STIX libraries, imports)
# 3. Path configuration
# 4. Utility imports (context-specific)
# 5. Object creation sections (grouped by type)
#    - Load data form
#    - Invoke block to create object
#    - Save to context memory
# 6. Summary and results
```

### Example Generated Notebook Cell

```python
# Load data form
data_form_path = 'SDO/Identity/identity_5e2f7cea_data_form.json'
results_path = 'generated/identity_1'

# Create object using block
obj_1 = invoke_make_identity_block(data_form_path, results_path)

# Configure context type
context_type_config = {'context_type': 'user'}

# Save to user context
obj_path = results_base + results_path + '.json'
context_path = results_base + 'generated/context/identity_1_context.json'
result = invoke_save_user_context_block(obj_path, context_path)

print(f'✅ identity #1 created and saved')
```

## Data Form Storage

In **Notebook Mode**, data forms are stored alongside their templates:

```
Block_Families/StixORM/
├── SDO/
│   ├── Identity/
│   │   ├── identity_template.json           (template)
│   │   └── identity_5e2f7cea_data_form.json (generated)
│   ├── Incident/
│   │   ├── phishing_incident.json           (template)
│   │   └── incident_b03035d2_data_form.json (generated)
├── SCO/
│   ├── Email_Addr/
│   │   ├── email_addr_template.json         (template)
│   │   └── email_addr_6bc3398c_data_form.json (generated)
├── SRO/
    └── Relationship/
        ├── relationship_template.json       (template)
        └── relationship_232b130a_data_form.json (generated)
```

## Example Workflows

### Workflow 1: User Setup (similar to Step_0_User_Setup.ipynb)

```python
# 1. Load user identity objects
user_objects = load_user_stix_objects()  # identity, user-account, email-addr

# 2. Generate notebook
results = reconstitute_and_generate(
    mode='notebook',
    stix_objects=user_objects,
    notebook_name='Step_0_User_Setup',
    context_type='user',
    notebook_title='User Context Setup',
    notebook_description='Create user identity, account, and email'
)

# 3. Execute generated notebook
# The notebook will:
#   - Create data forms in Block_Families/StixORM/
#   - Invoke blocks to create objects
#   - Save to user context memory
```

### Workflow 2: Incident Investigation (similar to Step_2_Create_Incident_with_an_Alert.ipynb)

```python
# 1. Load phishing incident objects
incident_objects = [
    incident_obj,
    attacker_email,
    malicious_url,
    suspicious_file,
    observed_data,
    relationships
]

# 2. Generate notebook
results = reconstitute_and_generate(
    mode='notebook',
    stix_objects=incident_objects,
    notebook_name='Step_2_Phishing_Investigation',
    context_type='incident',
    notebook_title='Phishing Email Investigation',
    notebook_description='Document phishing evidence and investigation'
)

# 3. Execute generated notebook
# The notebook will:
#   - Create incident context
#   - Generate evidence objects
#   - Link evidence to incident
#   - Save all to incident context
```

### Workflow 3: Company Infrastructure (similar to Step_1_Company_Setup.ipynb)

```python
# 1. Load company infrastructure objects
company_objects = [
    company_identity,
    office_locations,
    network_infrastructure,
    employee_identities
]

# 2. Generate notebook
results = reconstitute_and_generate(
    mode='notebook',
    stix_objects=company_objects,
    notebook_name='Step_1_Company_Setup',
    context_type='company',
    notebook_title='Company Infrastructure Setup',
    notebook_description='Initialize company context with infrastructure data'
)
```

## Integration with Existing Notebooks

The generated notebooks follow the same pattern as existing manual notebooks:

- **Step_0_User_Setup.ipynb** → Generated with `context_type='user'`
- **Step_1_Company_Setup.ipynb** → Generated with `context_type='company'`
- **Step_2_Create_Incident_with_an_Alert.ipynb** → Generated with `context_type='incident'`
- **Step_3_Get the Anecdote.ipynb** → Custom logic, can use `context_type='unattached'`

## API Reference

### reconstitute_and_generate()

```python
def reconstitute_and_generate(
    mode: Literal['test', 'notebook'],
    stix_objects: List[Dict[str, Any]] = None,
    data_forms_dir: Path = None,
    reconstitution_data_file: Path = None,
    output_dir: Path = None,
    notebook_name: str = None,
    context_type: Literal['unattached', 'incident', 'company', 'user'] = 'unattached',
    notebook_title: str = None,
    notebook_description: str = None
) -> Dict[str, Any]
```

**Parameters:**

**Mode 1 (test) - Required:**
- `mode='test'`
- `data_forms_dir`: Path to directory containing data form JSON files
- `reconstitution_data_file`: Path to reconstitution_data.json metadata
- `output_dir`: Path for reconstituted object output

**Mode 2 (notebook) - Required:**
- `mode='notebook'`
- `stix_objects`: List of STIX objects to process
- `notebook_name`: Name of generated notebook (without .ipynb)
- `context_type`: Target context ('unattached', 'incident', 'company', 'user')

**Mode 2 (notebook) - Optional:**
- `notebook_title`: Display title in notebook (default: formatted notebook_name)
- `notebook_description`: Description text in notebook header

**Returns:**
```python
{
    'mode': str,                    # 'test' or 'notebook'
    'success': bool,                # Overall success status
    'generated_files': List[Path],  # List of generated files
    'errors': List[str],            # Error messages if any
    
    # Notebook mode only:
    'data_forms_created': int,      # Number of data forms created
    'notebook_path': str            # Path to generated notebook
}
```

## File Locations

### Input Files (Mode 1: Test)
```
temporary_reconstitution_testing/
└── generated/
    ├── data_forms/
    │   ├── identity_5e2f7cea_data_form.json
    │   ├── email_addr_6bc3398c_data_form.json
    │   └── reconstitution_data.json
    └── reconstituted/
        ├── identity_5e2f7cea_reconstituted.json
        └── email_addr_6bc3398c_reconstituted.json
```

### Output Files (Mode 2: Notebook)
```
Block_Families/StixORM/
├── SDO/Identity/identity_5e2f7cea_data_form.json
└── SCO/Email_Addr/email_addr_6bc3398c_data_form.json

Orchestration/
└── Generated_User_Setup.ipynb  (executable notebook)
```

## Examples

See `Orchestration/Utilities/example_reconstitute_generate.py` for complete examples:

```bash
# Run all examples
python Orchestration/Utilities/example_reconstitute_generate.py all

# Run specific mode
python Orchestration/Utilities/example_reconstitute_generate.py test
python Orchestration/Utilities/example_reconstitute_generate.py user
python Orchestration/Utilities/example_reconstitute_generate.py incident
python Orchestration/Utilities/example_reconstitute_generate.py company
```

## Benefits

### Mode 1 (Test)
✅ Validate data form quality
✅ Verify template completeness
✅ Test reference restoration
✅ Quality assurance automation

### Mode 2 (Notebook)
✅ Automated notebook generation
✅ Consistent structure across notebooks
✅ Reproducible object creation
✅ Context-aware object storage
✅ Integration with existing workflows

## Version History

- **v2.0** - Added dual-mode operation (test + notebook generation)
- **v1.5** - Original reconstitution-only mode (99.3% success rate)

## See Also

- `reconstitute_object_list.py` - Core reconstitution engine
- `convert_object_list_to_data_forms.py` - Data form generation
- `Step_0_User_Setup.ipynb` - Manual user context notebook example
- `Step_1_Company_Setup.ipynb` - Manual company context notebook example
- `Step_2_Create_Incident_with_an_Alert.ipynb` - Manual incident context notebook example
