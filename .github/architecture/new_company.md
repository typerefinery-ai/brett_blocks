# Company Setup Story - Step_1_Company_Setup.ipynb

## Story Overview

**Notebook**: `Orchestration/Step_1_Company_Setup.ipynb`  
**Purpose**: Establish company organizational context with employees, systems, and assets  
**Graph Patterns**: Pattern 3.2 (Identity Sub-Pattern)  
**Dependency Level**: Levels 0-2 (reusing user pattern for company entities)

### The Story

After establishing your personal identity as a cybersecurity analyst (Step 0), you now need to create the organization you'll be investigating incidents for. This notebook creates a complete company profile with:

- **The Company**: Main organizational identity
- **Employees**: Company personnel who might be victims or witnesses
- **IT Systems**: Servers, workstations, databases that can be attack targets
- **Hardware Assets**: Physical and virtual infrastructure

This establishes the "stage" where incidents will occur. Every future incident investigation happens within this company context.

## Characters Created

### Primary Character
- **Company Identity**: The organization (e.g., "Acme Corporation")
  - Role: `identity_class` = "organization"
  - Contains: All employees, systems, and assets
  - Context: `/identity--{company-uuid}/company.json`

### Supporting Characters - Employees
- **Multiple Employee Identities**: Users who work at the company
  - Same pattern as Step 0: user-account → email-addr → identity
  - These are potential phishing victims, incident witnesses
  - Context: `/identity--{company-uuid}/users.json`

### Supporting Characters - IT Infrastructure
- **System Identities**: Servers, workstations, network devices
  - Role: `identity_class` = "system"
  - These are potential attack targets
  - Context: `/identity--{company-uuid}/systems.json`

- **Asset Identities**: Databases, applications, storage
  - Role: `identity_class` = "class"
  - These can be impacted by incidents
  - Context: `/identity--{company-uuid}/assets.json`

## Graph Patterns Applied

### Pattern 3.2 (Reused): Identity Sub-Pattern

Same pattern as Step 0, but applied to company entities:

**For Employees** (with contact extensions):
```
user-account (Level 0) → email-addr (Level 1) → identity (Level 2)
```

**For Company/Systems/Assets** (without contact extensions):
```
identity (Level 2 - simple form, no embedded references)
```

**Key Difference**: Company organizational identity and IT system identities don't need user accounts or emails, so they're created as simple identity objects (Level 2) without the IdentityContact extension.

## Notebook Structure

### Act 1: Environment & Configuration (Cells 1-7)

- **Import STIX Libraries**: Same as Step 0
- **Configure Paths**: Set up company context paths
- **Load Company Data**: Configuration for company, employees, systems, assets
- **Create Company Context**: Initialize `/identity--{company-uuid}/` directory

### Act 2: Create Company Identity (Cells 8-9)

**Story Moment**: "You create the primary identity for Acme Corporation"

- **Object Type**: `identity` (SDO, Level 2)
- **Fields**: 
  - `name`: "Acme Corporation"
  - `identity_class`: "organization"
  - `sectors`: ["technology", "healthcare", etc.]
  - `description`: Company description
- **No Embedded References**: Company identity has no user-account or email-addr
- **Context Storage**: `/identity--{company-uuid}/company.json`
- **Graph Pattern**: Simple identity object (no extension)

### Act 3: Create Employee Identities (Cells 10-13)

**Story Moment**: "You create identities for company employees who might be phishing victims"

**For Each Employee** (e.g., John Doe, Jane Smith, etc.):

1. Create `user-account` (Level 0):
   - `user_id`: "jdoe"
   - `account_login`: "jdoe@acme.com"
   
2. Create `email-addr` (Level 1):
   - `value`: "jdoe@acme.com"
   - `belongs_to_ref` → user-account ID

3. Create `identity` (Level 2):
   - `name`: "John Doe"
   - `identity_class`: "individual"
   - `roles`: ["employee"]
   - IdentityContact extension:
     - `email_addresses[]` → EmailContact with `email_address_ref` → email-addr

**Context Storage**: All employees in `/identity--{company-uuid}/users.json`

**Pattern**: Exact same Level 0-2 chain as Step 0, demonstrating pattern reusability

### Act 4: Create IT System Identities (Cells 14-15)

**Story Moment**: "You create identities for IT infrastructure: mail server, file server, database server"

- **Object Type**: `identity` (SDO, Level 2 - simple)
- **Examples**:
  - Email Server: `identity_class` = "system", `name` = "Exchange Server"
  - File Server: `identity_class` = "system", `name` = "File Server 01"
  - Database: `identity_class` = "system", `name` = "Customer DB"
- **No Extensions**: Systems don't have user accounts or emails
- **Context Storage**: `/identity--{company-uuid}/systems.json`

### Act 5: Create Hardware Asset Identities (Cells 16-17)

**Story Moment**: "You create identities for physical/virtual assets that can be impacted"

- **Object Type**: `identity` (SDO, Level 2 - simple)
- **Examples**:
  - Workstation: `identity_class` = "class", `name` = "Workstation-12345"
  - Storage Array: `identity_class` = "class", `name` = "SAN-Storage-01"
- **Context Storage**: `/identity--{company-uuid}/assets.json`

### Act 6: Summary (Cell 18)

**Completion**: Company context established and ready for incident investigations

## Context Memory Created

```
context_mem/
├── context_map.json                    # Routes to company contexts
└── identity--{company-uuid}/           # Company-specific context
    ├── company.json                    # Company identity (1 object)
    ├── users.json                      # Employee identities (~5-10 objects)
    │   └── Each: user-account + email-addr + identity (3 objects per employee)
    ├── systems.json                    # IT system identities (~3-5 objects)
    │   └── Each: Simple identity (1 object per system)
    └── assets.json                     # Asset identities (~2-4 objects)
        └── Each: Simple identity (1 object per asset)
```

**Typical Object Count**:
- Company: 1 identity
- Employees: 5 employees × 3 objects = 15 objects (user-account, email-addr, identity)
- Systems: 4 identities (mail server, file server, database, domain controller)
- Assets: 3 identities (workstations, storage, backup)
- **Total**: ~23 objects

## Why This Story Matters

### Establishes Incident Context

Every incident needs:
- **Victim Identity**: Who was attacked? (employee from users.json)
- **Affected Systems**: What was impacted? (systems from systems.json)
- **Organizational Context**: Which company? (company identity)

Without this context, you can't investigate incidents because you don't have:
- Potential phishing victims (employees)
- Potential attack targets (systems)
- Organizational scope (company)

### Enables Multi-Company Support

The context structure `/identity--{company-uuid}/` enables:
- Multiple company contexts (e.g., clients you investigate for)
- Company isolation (each company's objects are separate)
- Company-specific incident investigations

### Demonstrates Pattern Reusability

The same Level 0-2 dependency pattern from Step 0 is reused for employees:
- ✅ Pattern works for personal identities (Step 0)
- ✅ Pattern works for employee identities (Step 1)
- ✅ Pattern will work for any identity needing contact info

## Comparison to Step 0 (User Setup)

| Aspect | Step 0 (User) | Step 1 (Company) |
|--------|---------------|------------------|
| **Context Location** | `/usr/cache_me.json` | `/identity--{uuid}/company.json` |
| **Identity Types** | Personal analyst + team | Company + employees + systems |
| **Pattern Applied** | 3.2 with extensions | 3.2 with/without extensions |
| **Contact Extensions** | All identities have extensions | Only employees have extensions |
| **Purpose** | Who investigates | What is being investigated |
| **Dependency** | Bootstrapped | References analyst identity |

## Next Steps

After completing this notebook, you have:

✅ **Company Context**: Established organizational structure  
✅ **Potential Victims**: Employees who can receive phishing emails  
✅ **Attack Targets**: Systems that can be compromised  
✅ **Investigation Scope**: Company boundaries defined

Now ready for:

**Step_2_Create_Incident_with_an_Alert.ipynb**:
- Create incident object (Level 6 - top of hierarchy)
- Use employee identities as phishing victims
- Reference systems as attack targets
- Demonstrate Levels 3-6 object creation
- Apply Patterns 3.3 (Sighting), 3.4 (Event), 3.6 (Impact), 3.7 (Sequence)

---

**Objects Created**: ~23 total (1 company, 15 employees, 4 systems, 3 assets)  
**Dependency Levels**: 0-2 (reused pattern)  
**Graph Patterns**: Pattern 3.2 (applied twice - with/without extensions)  
**Context Memory**: `/identity--{company-uuid}/` directory structure  
**Next Notebook**: Step_2_Create_Incident_with_an_Alert.ipynb
