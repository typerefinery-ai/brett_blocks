# Notebook Storyboards: Complete Guide

## Purpose
This document synthesizes all four setup notebooks (Step_0 through Step_3) into comprehensive storyboards that guide notebook development. Each notebook tells a story using STIX graph patterns. The story comes first; the code implements the story.

**Key Principle**: Notebooks are narratives, not scripts. They teach through stories, not procedures.

## The Complete Story Arc

### The Four Acts
1. **Step_0**: "Who Am I?" - Personal identity bootstrap
2. **Step_1**: "Who Are We?" - Organizational context
3. **Step_2**: "What Happened?" - Incident detection
4. **Step_3**: "What Else?" - Evidence accumulation

Each builds on the previous, creating a complete incident response system.

## Storyboard 1: User Setup (Step_0)

**File**: `Step_0_User_Setup.ipynb` (19 cells)

**Story Summary**: You're a new analyst. Before investigating incidents, you need an identity in the system. This notebook bootstraps your personal identity and creates a small team.

**Narrative Arc**:
- **Setup**: "I need to exist in the system"
- **Challenge**: Bootstrap problem - can't create identity without email, can't create email without identity
- **Solution**: Pattern 3.2 (Level 0→1→2 dependency chain)
- **Outcome**: Four analyst identities ready for incident work

**Graph Patterns**: Pattern 3.2 (Identity Sub-Pattern)

**Objects Created**: 12 total
- 4× user-account (Level 0)
- 4× email-addr (Level 0)
- 4× identity (Level 2)

**Context Memory**:
```
/usr/
├── cache_me.json         # Your identity
└── cache_team.json       # Team identities
```

**Cell Structure** (3 Acts):

**Act 1: Environment** (Cells 1-7)
- Cell 1: Story introduction (markdown)
- Cells 2-7: Imports, utilities, path setup

**Act 2: Personal Identity** (Cells 8-13)
- Cell 8: Story: "Creating my identity"
- Cell 9: Create your user-account
- Cell 10: Create your email-addr
- Cell 11: Create your identity (links to user-account, email-addr)
- Cell 12: Save to /usr/cache_me.json
- Cell 13: Verify structure

**Act 3: Team Identities** (Cells 14-19)
- Cell 14: Story: "Creating team identities"
- Cell 15: Create 3 team members (loop)
- Cell 16: Save to /usr/cache_team.json
- Cell 17: Verify team structure
- Cell 18: Summary: "We now have 4 analysts"
- Cell 19: Next steps teaser (points to Step_1)

**Story Emphasis**:
- Emphasize the bootstrap problem
- Show why order matters (Level 0→1→2)
- Highlight that identities are reusable across incidents
- Personal connection: "This is YOUR identity"

**Development Notes**:
- Keep code simple - focus on story
- Add markdown cells between each major step
- Use print statements to show objects created
- Verify each step before proceeding
- End with clear "what we built" summary

## Storyboard 2: Company Setup (Step_1)

**File**: `Step_1_Company_Setup.ipynb` (18 cells)

**Story Summary**: Incidents happen in organizational context. This notebook creates the company, employees, systems, and assets that will appear in incident investigations.

**Narrative Arc**:
- **Setup**: "Incidents need context"
- **Challenge**: How to represent complex organizations in STIX
- **Solution**: Reuse Pattern 3.2 with IdentityContact extensions
- **Outcome**: Complete organizational graph ready for incident attachment

**Graph Patterns**: Pattern 3.2 (with/without IdentityContact extension)

**Objects Created**: ~23 total
- 1× company identity (with IdentityContact)
- 15× employee identities (with IdentityContact)
- 4× system identities (infrastructure)
- 3× asset identities (data, applications)

**Context Memory**:
```
/identity--{company-uuid}/
├── identity--{company}.json
├── identity--{employee-1}.json
├── identity--{employee-2}.json
├── ...
├── identity--{system-1}.json
└── ...
```

**Cell Structure** (6 Acts):

**Act 1: Environment** (Cells 1-3)
- Cell 1: Story introduction
- Cells 2-3: Imports, utilities

**Act 2: Company Identity** (Cells 4-6)
- Cell 4: Story: "Creating the company"
- Cell 5: Create company identity with IdentityContact extension
- Cell 6: Verify company structure

**Act 3: Employee Identities** (Cells 7-9)
- Cell 7: Story: "Adding employees"
- Cell 8: Create 15 employees (loop with IdentityContact)
- Cell 9: Show employee list

**Act 4: System Identities** (Cells 10-12)
- Cell 10: Story: "Adding IT systems"
- Cell 11: Create 4 systems (email server, file server, etc.)
- Cell 12: Show system list

**Act 5: Asset Identities** (Cells 13-15)
- Cell 13: Story: "Adding critical assets"
- Cell 14: Create 3 assets (databases, applications)
- Cell 15: Show asset list

**Act 6: Save Context** (Cells 16-18)
- Cell 16: Save all to incident context directory
- Cell 17: Verify context structure
- Cell 18: Summary and next steps (points to Step_2)

**Story Emphasis**:
- This is "scene setting" for incidents
- Real companies are complex - show that complexity
- Identities are organizational memory
- These identities will appear as victims, witnesses, assets in incidents

**Development Notes**:
- Use loops for multiple similar objects
- Show IdentityContact extension usage
- Emphasize identity_class differences (individual, organization, system)
- Create believable company (use realistic names, roles)
- End with "now we can investigate incidents"

## Storyboard 3: Phishing Incident (Step_2)

**File**: `Step_2_Create_Incident_with_an_Alert.ipynb` (47 cells)

**Story Summary**: A SIEM alert fires at 3:47 AM - phishing email detected targeting the CEO. This notebook creates the complete incident from initial detection through response planning.

**Narrative Arc**:
- **Inciting Incident**: SIEM alert - "Suspicious email detected"
- **Investigation**: What's the evidence? (URL, email-message, observed-data)
- **Analysis**: What does it mean? (Indicator, sighting)
- **Response**: What do we do? (Tasks, sequences, impact)
- **Resolution**: Package everything (Incident container)

**Graph Patterns**: 3.1, 3.3, 3.4, 3.5, 3.6, 3.7, 3.8

**Objects Created**: ~18 total
- 1× URL (malicious link)
- 1× email-message (phishing email)
- 2× email-addr (attacker, victim)
- 1× observed-data (wraps URL + email)
- 1× indicator (phishing pattern)
- 1× sighting (with sighting-alert extension)
- 1× event (alert-created)
- 1× impact (initial assessment)
- 5× task (investigation steps)
- 3× sequence (workflow phases)
- 1× incident (container)

**Context Memory**:
```
/identity--{incident-context}/
├── incident--{phishing}.json
├── url--{malicious}.json
├── email-message--{phishing}.json
├── observed-data--{email-url}.json
├── indicator--{pattern}.json
├── sighting--{alert}.json
├── event--{alert-created}.json
├── impact--{initial}.json
├── task--{1..5}.json
├── sequence--{1..3}.json
└── ...
```

**Cell Structure** (6 Acts):

**Act 1: Setup** (Cells 1-9)
- Cells 1-2: Story introduction - "The alert fires"
- Cells 3-7: Environment setup
- Cells 8-9: Create incident context directory

**Act 2: The Evidence** (Cells 10-16)
- Cell 10: Story: "What did we observe?"
- Cells 11-12: Create URL SCO
- Cell 13: Story: "The phishing email"
- Cell 14: Create email-message SCO
- Cell 15: Story: "Packaging the evidence"
- Cell 16: Create observed-data (Level 2)

**Act 3: The Detection** (Cells 17-21)
- Cell 17: Story: "How did we detect this?"
- Cell 18: Create indicator (STIX pattern)
- Cell 19: Story: "The SIEM alert"
- Cells 20-21: Create sighting with sighting-alert extension

**Act 4: The Timeline** (Cells 22-27)
- Cell 22: Story: "What happened?"
- Cells 23-24: Create event from sighting
- Cell 25: Story: "What's the impact?"
- Cells 26-27: Create initial impact assessment

**Act 5: The Response** (Cells 28-40)
- Cell 28: Story: "What should we do?"
- Cells 29-33: Create 5 investigation tasks (with dependencies)
- Cell 34: Story: "Organizing the work"
- Cells 35-40: Create 3 sequence workflows

**Act 6: The Incident** (Cells 41-47)
- Cell 41: Story: "Packaging everything together"
- Cell 42: Create incident with IncidentCoreExt (all _refs)
- Cells 43-45: Save to context, verify structure
- Cell 46: Summary: "What we built"
- Cell 47: Next steps (points to Step_3)

**Story Emphasis**:
- This is a REAL phishing incident (make it believable)
- Show evidence → analysis → response flow
- Emphasize dependency hierarchy (build bottom-up)
- Tasks show "what an analyst would actually do"
- Incident is a container - it references everything else

**Development Notes**:
- Create realistic email content (actual phishing language)
- Show task dependencies clearly
- Use markdown to separate story beats
- Print objects as they're created (show progress)
- Verify each level before building next
- End with incident reconstitution preview

## Storyboard 4: Evidence Extension (Step_3)

**File**: `Step_3_Get the Anecdote.ipynb` (24 cells)

**Story Summary**: Five hours after the alert, the CEO submits an incident report: "I got a suspicious email, didn't click the link." This notebook extends the incident with new evidence.

**Narrative Arc**:
- **Setup**: "We have an existing incident"
- **New Evidence**: User report arrives
- **Integration**: How to add it to existing incident?
- **Solution**: Create new sighting, update incident
- **Outcome**: Incident grows, impact assessment updated

**Graph Patterns**: 3.3, 3.4, 3.6, 3.9, 3.10

**Objects Created**: 5 total
- 1× anecdote (user report)
- 1× observed-data (wraps anecdote)
- 1× sighting (with sighting-anecdote extension)
- 1× event (user-reported)
- 1× impact (supersedes initial)

**Context Memory** (extends Step_2):
```
/identity--{incident-context}/
├── incident--{phishing}.json           # UPDATED
├── anecdote--{user-report}.json        # NEW
├── observed-data--{anecdote}.json      # NEW
├── sighting--{anecdote}.json           # NEW
├── event--{user-reported}.json         # NEW
└── impact--{updated}.json              # NEW
```

**Cell Structure** (6 Acts):

**Act 1: Setup** (Cells 1-7)
- Cells 1-2: Story introduction - "New evidence arrives"
- Cells 3-7: Environment setup

**Act 2: Load Existing** (Cells 8-9)
- Cell 8: Story: "Retrieving the incident"
- Cell 9: Load incident from context (from Step_2)

**Act 3: User Report** (Cells 10-13)
- Cell 10: Story: "The CEO reports"
- Cell 11: Create anecdote SCO (with made_by_ref, context_refs)
- Cell 12: Story: "Packaging the report"
- Cell 13: Create observed-data wrapping anecdote

**Act 4: Evidence Extension** (Cells 14-15)
- Cell 14: Story: "Adding to evidence trail"
- Cell 15: Create sighting with sighting-anecdote extension

**Act 5: Impact Update** (Cells 16-19)
- Cell 16: Story: "Reassessing impact"
- Cell 17: Create new impact (supersedes_refs previous)
- Cell 18: Story: "New event from report"
- Cell 19: Create event (user-reported)

**Act 6: Incident Update** (Cells 20-24)
- Cell 20: Story: "Updating the incident"
- Cells 21-23: Update incident._refs lists, save
- Cell 24: Summary: "How the incident grew"

**Story Emphasis**:
- Incidents evolve over time (not created complete)
- Multiple evidence sources (SIEM alert + user report)
- Impact can change with new information
- Anecdote provides provenance (who said what, when)
- Same indicator, different sightings

**Development Notes**:
- Load incident first (show it's from Step_2)
- Create realistic user report text
- Show before/after incident structure
- Emphasize supersedes_refs for impact
- Compare alert vs anecdote sightings
- End with "more evidence could arrive" teaser

## Development Principles

### Story-First Approach
1. **Start with narrative**: What's happening?
2. **Identify characters**: Who's involved?
3. **Map to patterns**: Which patterns apply?
4. **Create objects**: Implement the story
5. **Verify structure**: Does it make sense?

### Markdown as Storytelling
- Use markdown cells as chapter breaks
- Each code cell should have narrative context
- Explain WHY, not just WHAT
- Use personal pronouns ("We're creating...", "This represents...")

### Progressive Reveal
- Don't show everything at once
- Build complexity gradually
- Verify each step before proceeding
- Show objects as they're created (print statements)

### Educational Focus
- Teach patterns through examples
- Show common mistakes and how to avoid them
- Explain design decisions
- Connect code to real-world scenarios

### Reusability
- Create utility functions for repeated patterns
- Save objects to context for reuse
- Show how to load existing objects
- Demonstrate pattern reuse across notebooks

## Pattern Coverage Map

| Pattern | Step_0 | Step_1 | Step_2 | Step_3 |
|---------|--------|--------|--------|--------|
| 3.1 (Incident Container) | - | - | ✅ | ✅ (update) |
| 3.2 (Identity Sub-Pattern) | ✅ | ✅ | Uses | Uses |
| 3.3 (Observed-Data/Sighting) | - | - | ✅ | ✅ |
| 3.4 (Event Derivation) | - | - | ✅ | ✅ |
| 3.5 (Task Integration) | - | - | ✅ | - |
| 3.6 (Impact Assessment) | - | - | ✅ | ✅ |
| 3.7 (Sequence Workflows) | - | - | ✅ | - |
| 3.8 (Email Communication) | - | - | ✅ | - |
| 3.9 (Anecdote Provenance) | - | - | - | ✅ |
| 3.10 (Impact Supersession) | - | - | - | ✅ |
| 3.11 (Task Ownership) | - | - | ✅ | - |
| 3.12 (State Change) | - | - | ✅ | ✅ |
| 3.13 (Conditional Sequences) | - | - | Mentioned | - |

**Coverage Strategy**:
- Step_0/1: Foundation (identities)
- Step_2: Breadth (most patterns)
- Step_3: Depth (evidence accumulation)

## Build Order Requirements

### Level Dependencies
Objects must be created in dependency order:

**Level 0** (no embedded refs):
- user-account, email-addr, url

**Level 1** (refs to Level 0):
- email-message (refs email-addr)

**Level 2** (refs to Level 0-1):
- identity (refs user-account, email-addr)
- observed-data (refs SCOs)

**Level 3** (refs to Level 2):
- indicator (refs observed-data pattern)
- sighting (refs observed-data, indicator)
- impact (standalone)

**Level 4** (refs to Level 3):
- event (refs sighting)
- task (refs other tasks via depends_on_refs)

**Level 5** (refs to Level 4):
- sequence (refs tasks, events)

**Level 6** (refs to everything):
- incident (refs via IncidentCoreExt._refs)

### Cross-Notebook Dependencies

**Step_0 → Step_1**:
- Step_1 can reference analyst identities from Step_0
- Creates organizational identities independently

**Step_1 → Step_2**:
- Step_2 uses CEO identity from Step_1 (victim)
- Uses company identity for context directory

**Step_2 → Step_3**:
- Step_3 REQUIRES incident from Step_2
- Loads incident, extends it
- Must run Step_2 first

### Context Memory Flow
```
Step_0: Creates /usr/cache_me.json, /usr/cache_team.json
↓
Step_1: Creates /identity--{company}/identity--*.json
↓
Step_2: Creates /identity--{company}/incident--*.json + evidence
↓
Step_3: Updates /identity--{company}/incident--*.json, adds evidence
```

## Common Patterns

### Pattern: Create SCO
```python
# Story: "Creating a [object type]"
obj = invoke_make_[type]_block(
    # Required properties
    property=value,
    # Optional embedded refs
    ref_property=other_obj.id
)
# Verify
print(f"Created {obj.type}: {obj.id}")
```

### Pattern: Create SDO with Extension
```python
# Story: "Creating [object] with [extension]"
obj = invoke_make_[type]_block(
    # Standard properties
    name="...",
    # Extension
    extensions={
        "extension-name": {
            "property": value,
            "refs": [other_obj.id]
        }
    }
)
```

### Pattern: Create SRO
```python
# Story: "Connecting [source] to [target]"
rel = invoke_make_relationship_block(
    source_ref=source.id,
    target_ref=target.id,
    relationship_type="related-to"
)
```

### Pattern: Update Incident
```python
# Story: "Adding new evidence"
incident.extensions["IncidentCoreExt"]["sighting_refs"].append(new_sighting.id)
incident.extensions["IncidentCoreExt"]["event_refs"].append(new_event.id)
# Save updated incident
save_to_context(incident)
```

### Pattern: Load from Context
```python
# Story: "Retrieving existing [object]"
obj = load_from_context(obj_id)
print(f"Loaded {obj.type}: {obj.name}")
```

## Verification Checklist

After creating each notebook, verify:

### Structure
- [ ] Markdown introduction explains the story
- [ ] Each code cell has narrative context (markdown before it)
- [ ] Objects created in dependency order
- [ ] Each object verified after creation (print statements)
- [ ] Context memory saved and verified
- [ ] Summary cell at end explains what was built

### Content
- [ ] Story is coherent and engaging
- [ ] Objects have realistic data (names, descriptions, etc.)
- [ ] Patterns are correctly applied
- [ ] Extensions used appropriately
- [ ] References (embedded and SRO) are valid

### Educational Value
- [ ] Explains WHY, not just WHAT
- [ ] Shows design decisions
- [ ] Highlights pattern reuse
- [ ] Points to next notebook (continuity)
- [ ] Includes "what we learned" section

### Technical Correctness
- [ ] All imports present
- [ ] Utility functions available
- [ ] File paths correct
- [ ] No circular dependencies
- [ ] Objects validate against STIX schema

## Extension Ideas

### Additional Evidence Types
Create notebooks showing:
- `sighting-context`: External threat intel
- `sighting-enrichment`: Reputation data
- `sighting-hunt`: Proactive investigation
- `sighting-framework`: MITRE ATT&CK mapping

### Additional Incident Types
Create notebooks for:
- Malware infection
- Ransomware attack
- Data breach
- Insider threat
- DDoS attack

### Advanced Patterns
Show:
- Pattern 3.13: Conditional sequence workflows
- Multiple impact supersession chains
- Complex task dependency graphs
- Cross-incident relationships

## References

- See `stix-graph-patterns.md` for detailed pattern explanations
- See `new_user.md` for Step_0 story breakdown
- See `new_company.md` for Step_1 story breakdown
- See `phishing-incident.md` for Step_2+3 combined story

## Summary

Notebooks are stories told through STIX graphs. The four notebooks create a complete narrative:
1. **Who am I?** (Personal identity)
2. **Who are we?** (Organizational identity)
3. **What happened?** (Incident detection)
4. **What else?** (Evidence accumulation)

Each notebook teaches patterns through realistic scenarios. Code implements stories; stories teach patterns; patterns enable incident reconstitution.

**Remember**: The story always comes first. The STIX graph preserves the story for later reconstruction.
