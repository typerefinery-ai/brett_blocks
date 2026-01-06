# User Setup Story - Step_0_User_Setup.ipynb

## Story Overview

**Notebook**: `Orchestration/Step_0_User_Setup.ipynb`  
**Purpose**: Initialize the cybersecurity analyst's personal identity and team context  
**Graph Patterns**: Pattern 3.2 (Identity Sub-Pattern with Extensions)  
**Dependency Level**: Levels 0-2 (Foundation objects)

### The Story

Before investigating cyber incidents, the analyst must first establish their identity in the system. This is the foundational step where you register yourself and your immediate team as cybersecurity intelligence agents who will perform investigations, create tasks, analyze evidence, and manage incidents.

Think of this as "joining the cybersecurity team" - you're creating your digital credentials that will track all your future activities. Every task you assign, every event you document, every impact you assess will be linked back to your identity object created in this notebook.

## Characters in This Story

### Primary Character
- **You (TR_user)**: The cybersecurity analyst/investigator
  - Role: Primary investigator and incident responder
  - Identity: Created with full contact details (email, account)
  - Context: Stored in `/usr/cache_me.json` (personal workspace)

### Supporting Characters (Team Members)
- **Team Member 1 (nick1)**: First team member identity
- **Team Member 2 (hilda2)**: Second team member identity  
- **Team Member 3 (trusty3)**: Third team member identity
  - Roles: Collaboration, task assignment, incident response support
  - Context: Stored in `/usr/cache_team.json` (team workspace)

## Graph Patterns Applied

### Pattern 3.2: Identity Sub-Pattern with Extensions

This notebook demonstrates the complete Level 0-2 dependency chain from stix-graph-patterns.md:

```
Level 0: user-account (SCO)
         └── No dependencies except created_by_ref (bootstrapped)
         
Level 1: email-addr (SCO)
         └── belongs_to_ref → user-account (Level 0)
         
Level 2: identity (SDO)
         └── IdentityContact extension
             └── EmailContact sub-object
                 └── email_address_ref → email-addr (Level 1)
```

**Key Insight**: This pattern MUST be followed in this exact order:
1. Create user-account first (Level 0)
2. Create email-addr linking to user-account (Level 1)
3. Create identity linking to email-addr (Level 2)

Violating this order causes reference errors because objects cannot reference objects that don't exist yet.

## Notebook Cell-by-Cell Story

### Act 1: Environment Preparation (Cells 1-7)

**Scene 1 - Import Libraries (Cells 1-3)**
- **Markdown**: Introduce notebook purpose and goals
- **Code**: Import STIX 2.1 libraries and OS Threat extensions
- **Story Moment**: "You open your cybersecurity analyst workstation and load the tools needed to register your identity"
- **Technical**: Imports Identity, EmailAddress, UserAccount classes plus IdentityContact extension

**Scene 2 - Configure Paths (Cells 4-5)**
- **Markdown**: Explain path configuration needs
- **Code**: Set up Python paths for Brett Blocks utilities
- **Story Moment**: "You configure your system to access the identity registration utilities"
- **Technical**: Adds `../` to sys.path for relative imports

**Scene 3 - Load Data (Cells 6-7)**
- **Markdown**: Describe utility imports and data configuration
- **Code**: Import utility functions and load identities_data configuration
- **Story Moment**: "You load the identity blueprints for yourself and 3 team members"
- **Technical**: Imports `invoke_make_*` utilities and loads JSON configuration for 4 identities

### Act 2: Create Your Personal Identity (Cells 8-15)

**Scene 1 - Select Your Data (Cells 8-10)**
- **Markdown**: Explain data selection for personal identity
- **Code**: Extract "me" configuration from identities_data
- **Story Moment**: "You select your personal identity data: TR_user with email and account details"
- **Technical**: Finds `ident["who"] == "me"` and extracts file paths

**Scene 2 - Create User Account (Cells 11-12)**
- **Markdown**: Describe user account creation (Level 0)
- **Code**: `TR_user_acct = invoke_make_user_account_block(acct_path, results_path)`
- **Story Moment**: "You create your system account object with user ID and login credentials"
- **Technical Details**:
  - **Input**: `Block_Families/StixORM/SCO/User_Account/usr_account_TR_user.json`
  - **Output**: `Results/step0/me__usr_acct.json`
  - **Object Type**: `user-account` (SCO, Level 0)
  - **Fields**: user_id, account_login, display_name
  - **Dependencies**: None (Level 0)
- **Graph Pattern**: This is the foundation object with no embedded references (except created_by_ref which is bootstrapped)

**Scene 3 - Create Email Address (Cells 13-14)**
- **Markdown**: Describe email creation and account linking (Level 1)
- **Code**: `TR_email_addr = invoke_make_email_addr_block(email_path, results_path, TR_user_acct)`
- **Story Moment**: "You create your email address and link it to your user account"
- **Technical Details**:
  - **Input**: `Block_Families/StixORM/SCO/Email_Addr/email_addr_TR_user.json`
  - **Output**: `Results/step0/me__email.json`
  - **Object Type**: `email-addr` (SCO, Level 1)
  - **Fields**: value (email address), display_name, belongs_to_ref
  - **Dependencies**: `belongs_to_ref` → `TR_user_acct.id` (Level 0)
- **Graph Pattern**: Demonstrates Level 0 → Level 1 dependency via belongs_to_ref

**Scene 4 - Create Personal Identity (Cells 15-16)**
- **Markdown**: Describe identity creation linking all objects (Level 2)
- **Code**: `TR_ident = invoke_make_identity_block(ident_path, results_path, email_results=TR_email_addr, acct_results=TR_user_acct)`
- **Story Moment**: "You create your primary cybersecurity analyst identity that ties everything together"
- **Technical Details**:
  - **Input**: `Block_Families/StixORM/SDO/Identity/identity_TR_user.json`
  - **Output**: `Results/step0/me__ident.json`
  - **Object Type**: `identity` (SDO, Level 2)
  - **Fields**: name, description, roles, identity_class
  - **Extension**: IdentityContact (`extension-definition--66e2492a-bbd3-4be6-88f5-cc91a017a498`)
    - `email_addresses[]` → EmailContact sub-objects
      - `email_address_ref` → `TR_email_addr.id` (Level 1)
    - `social_media_accounts[]` → SocialMediaContact sub-objects (if any)
      - `user_account_ref` → `TR_user_acct.id` (Level 0)
  - **Dependencies**: 
    - EmailContact.email_address_ref → email-addr (Level 1)
    - SocialMediaContact.user_account_ref → user-account (Level 0)
- **Graph Pattern**: Demonstrates Level 1-2 dependency via IdentityContact extension

### Act 3: Create Team Members (Cells 17-18)

**Scene 1 - Iterate Team Members (Cell 18)**
- **Markdown**: Describe team member creation process
- **Code**: Loop through `identities_data` for team members (who[:3] == "tea")
- **Story Moment**: "You create identity objects for your 3 team members: nick1, hilda2, trusty3"
- **Technical Details**:
  - **Processing**: Same 3-step pattern (account → email → identity) for each team member
  - **Team Members**:
    1. **nick1**: `SCO/User_Account/usr_account_team1.json` → `email_addr_team1.json` → `identity_team1.json`
    2. **hilda2**: `SCO/User_Account/usr_account_team2.json` → `email_addr_team2.json` → `identity_team2.json`
    3. **trusty3**: `SCO/User_Account/usr_account_team3.json` → `email_addr_team3.json` → `identity_team3.json`
  - **Context Storage**: All team objects saved to `/usr/cache_team.json` (separate from personal)
  - **Pattern Reuse**: Demonstrates pattern universality - same Level 0-2 dependency chain

### Act 4: Completion (Cell 19)

**Scene 1 - Summary (Cell 19)**
- **Markdown**: Completion message and next steps
- **Story Moment**: "You've successfully registered your identity and team. You're now ready to investigate incidents and manage cybersecurity intelligence."

## Context Memory Created

### Storage Structure

```
context_mem/
└── usr/                           # User workspace (no company required)
    ├── cache_me.json              # Your personal identity objects
    │   ├── user-account--{id}     # Your account (Level 0)
    │   ├── email-addr--{id}       # Your email (Level 1)
    │   └── identity--{id}         # Your identity (Level 2)
    ├── cache_team.json            # Team member identity objects
    │   ├── user-account--{id1}    # Team member 1 account
    │   ├── email-addr--{id1}      # Team member 1 email
    │   ├── identity--{id1}        # Team member 1 identity
    │   ├── user-account--{id2}    # Team member 2 account
    │   ├── email-addr--{id2}      # Team member 2 email
    │   ├── identity--{id2}        # Team member 2 identity
    │   ├── user-account--{id3}    # Team member 3 account
    │   ├── email-addr--{id3}      # Team member 3 email
    │   └── identity--{id3}        # Team member 3 identity
    └── edges.json                 # User-level relationships (if any)
```

### Object Counts

- **Total Objects Created**: 12 (4 identities × 3 objects each)
- **SCOs**: 8 (4 user-accounts + 4 email-addrs)
- **SDOs**: 4 (4 identities)
- **SROs**: 0 (no relationships in this notebook)

### Dependency Chain Summary

```
Personal Identity Chain:
user-account--TR_user (Level 0)
  ↓ belongs_to_ref
email-addr--TR_user (Level 1)
  ↓ email_address_ref (IdentityContact extension)
identity--TR_user (Level 2)

Team Member Chains (×3):
user-account--team{1,2,3} (Level 0)
  ↓ belongs_to_ref
email-addr--team{1,2,3} (Level 1)
  ↓ email_address_ref (IdentityContact extension)
identity--team{1,2,3} (Level 2)
```

## Why This Story Matters

### Bootstrapping Problem Solved

This notebook solves the "who creates the first identity?" problem:
- All STIX objects have `created_by_ref` → identity
- But the first identity has no creator
- Solution: **Bootstrap** the first identity with self-reference (`created_by_ref` → self)
- All subsequent objects can reference this bootstrapped identity

### Foundation for All Future Work

Every future notebook relies on these identities:
- **Incidents**: `created_by_ref` → your identity
- **Tasks**: `created_by_ref` → your identity, `owner` → team member identity
- **Events**: `created_by_ref` → your identity
- **Impacts**: `created_by_ref` → your identity
- **Sightings**: `created_by_ref` → your identity
- **Relationships**: `created_by_ref` → your identity

Without this notebook, you cannot create ANY other objects because they all require a `created_by_ref` identity.

### Team Collaboration Enabled

By creating team member identities:
- You can assign tasks to team members (`identity -[assigned]→ task`)
- Team members can be task owners (`task.owner` → team member identity)
- You can track who performed which tasks (`identity -[performed]→ task`)
- Incident response coordination is possible

## Technical Implementation Notes

### Utility Function Pattern

All object creation follows this pattern:
```python
# Pattern: invoke_make_{object_type}_block(input_path, results_path, dependencies)
TR_user_acct = invoke_make_user_account_block(acct_path, results_path)
TR_email_addr = invoke_make_email_addr_block(email_path, results_path, TR_user_acct)
TR_ident = invoke_make_identity_block(ident_path, results_path, email_results=TR_email_addr, acct_results=TR_user_acct)
```

**Key Points**:
- Input files are JSON templates from `Block_Families/StixORM/`
- Results files saved to `Results/step0/`
- Dependencies passed as arguments (email needs account, identity needs both)
- Utility handles all StixORM object creation and validation

### Context Storage Pattern

Two storage mechanisms:
1. **Object Storage**: Full STIX JSON in `Results/step0/{who}__{type}.json`
2. **Context Storage**: Dual-layer format in context memory
   - STIX data layer: Valid STIX 2.1 bundle
   - UI metadata layer: UI-specific data for visualization

### Data Flow

```
JSON Template → invoke_make_*_block() → STIX Object → invoke_save_*_context_block() → Context Memory

Example:
usr_account_TR_user.json → invoke_make_user_account_block() → TR_user_acct → invoke_save_user_context_block() → /usr/cache_me.json
```

## Comparison to Graph Patterns Document

### Patterns Applied from stix-graph-patterns.md

✅ **Pattern 3.2**: Identity Sub-Pattern with Extensions
- Demonstrates complete Level 0-2 dependency chain
- Shows IdentityContact extension usage
- EmailContact.email_address_ref linking
- SocialMediaContact.user_account_ref linking (optional)

### Dependency Hierarchy Demonstration

✅ **Level 0 Objects**: user-account (4 created)
✅ **Level 1 Objects**: email-addr (4 created)  
✅ **Level 2 Objects**: identity (4 created)

### Missing Patterns (Expected)

❌ **Pattern 3.3**: Observed-Data/Sighting (requires company/incident context)
❌ **Pattern 3.4**: Event Derivation (requires incidents)
❌ **Pattern 3.5**: Task Integration (requires incidents)
❌ **Pattern 3.6**: Impact Assessment (requires incidents)
❌ **Pattern 3.7**: Sequence Workflows (requires tasks/events)

These patterns appear in subsequent notebooks after company and incident contexts are created.

## Next Steps

After completing this notebook, you proceed to:

1. **Step_1_Company_Setup.ipynb**:
   - Create company identity (organization role)
   - Create company employee identities
   - Create company IT system identities
   - Establish company context memory

2. **Step_2_Create_Incident_with_an_Alert.ipynb**:
   - Create first incident (phishing attack)
   - Use your identity as `created_by_ref` for all objects
   - Demonstrate Levels 3-6 object creation

3. **Step_3_Get the Anecdote.ipynb**:
   - Add additional evidence to incident
   - Create anecdote SCO with `provided_by_ref` → employee identity
   - Demonstrate evidence extension patterns

## Story Summary

This notebook tells the foundational story of establishing the investigator's identity. It's the "origin story" where you become a cybersecurity analyst by creating your digital credentials in the STIX intelligence system. Without this identity, you cannot perform any investigations, create incidents, or manage cyber threat intelligence.

The story demonstrates the critical importance of dependency order - you must build from the foundation (Level 0) upward (Level 2). Any attempt to reverse this order fails because objects cannot reference objects that don't exist yet.

This is Pattern 3.2 in action: The Identity Sub-Pattern with Extensions, creating the foundation for all future cybersecurity intelligence activities.

---

**Objects Created**: 12 total (4 user-accounts, 4 email-addrs, 4 identities)  
**Dependency Levels**: 0-2  
**Graph Patterns**: Pattern 3.2  
**Context Memory**: `/usr/cache_me.json`, `/usr/cache_team.json`  
**Next Notebook**: Step_1_Company_Setup.ipynb
