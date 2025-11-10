# STIX Object Creation Prompts

## Overview

**STIX Analysis Reference**: For comprehensive understanding of all 88 available STIX objects, their complexity distribution, and implementation patterns, see:
- `architecture/stix-object-generation-patterns.md` - Complete complexity analysis
- `architecture/complete-stix-pattern-matrix.md` - Function signature matrix for all implemented objects
- `a_seed/2_initial_set_of_blocks.md` - Complete inventory of implemented and available objects

**Current Implementation**: 15 objects implemented (8 SDO, 5 SCO, 2 SRO) with 73 additional objects available for expansion.

## Create Team Member Objects

**Context:** When adding new team members to the system
**Input:** Team member details (name, role, contact info)
**Expected Output:** Coordinated set of identity, email-addr, and user-account objects

### Prompt Text:
```
Create a new team member object set following the existing pattern in the project. 

Requirements:
1. Create identity object in Block_Families/StixORM/SDO/Identity/ following the pattern of identity_team1.json and identity_team2.json
2. Create email-addr object in Block_Families/StixORM/SCO/EmailAddress/ following email_addr_team1.json pattern
3. Create user-account object in Block_Families/StixORM/SCO/UserAccount/ following usr_account_team1.json pattern

For team member: [NAME] with role [ROLE]

Ensure:
- Consistent naming across all three objects
- Proper STIX 2.1 compliance
- Sequential numbering (team3, team4, etc.)
- Appropriate prefixes (Mr, Ms, Dr) for variety
- Incremental phone numbers and user IDs following existing pattern
- Same team affiliation ("os-threat")
- Consistent account_type ("soc,")
```

### Example Usage:
Create team member objects for "Strategic Analyst" role, which would generate team3 files with coordinated data.

## Analyze STIX Object Relationships

**Context:** When investigating object connections and data flow
**Input:** STIX object IDs or file paths
**Expected Output:** Relationship analysis and visualization data

### Prompt Text:
```
Analyze the relationships between STIX objects in the current incident context.

Please:
1. Load the context from Orchestration/generated/os-triage/context_mem/
2. Identify all relationships between the specified objects
3. Map both embedded relationships and formal STIX relationship objects
4. Show the relationship hierarchy and flow
5. Identify any unattached or orphaned objects
6. Generate a summary of object types and their connections

Focus on objects: [OBJECT_IDS_OR_TYPES]

Output format:
- Visual relationship map
- Object inventory with types and IDs
- Relationship summary by type
- Any issues or missing connections
```

## Create Object Form Templates

**Context:** When creating new STIX object types or templates
**Input:** Object type specification
**Expected Output:** Properly structured object form template

### Prompt Text:
```
Create a new STIX object form template for [OBJECT_TYPE].

Requirements:
1. Follow STIX 2.1 specification for the object type
2. Use the project's standard form structure with base_required, base_optional, object, extensions, and sub sections
3. Include all required STIX properties for this object type
4. Add common optional properties that are typically used
5. Include appropriate extension placeholders
6. Add sub-object relationships that are commonly associated with this type
7. Follow the naming conventions used in existing object forms
8. Include descriptive comments where helpful

Reference existing forms in Block_Families/StixORM/ for structure patterns.
```