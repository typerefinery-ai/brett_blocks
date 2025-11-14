# Prompt: Create New Notebooks as Storyboards

## Purpose
This prompt guides AI assistants in creating entirely new incident notebooks for different incident types (malware, data breach, insider threat, DDoS, etc.) using the phishing incident as a template.

## Context
You are creating new Jupyter notebooks for incident types beyond phishing. These notebooks demonstrate that STIX graph patterns are reusable across different threat scenarios. Each incident type uses the same patterns but with different SCOs, indicators, tasks, and narratives.

## Reference Documents
Before starting, review:
- `.github/architecture/stix-graph-patterns.md` - Complete STIX graph pattern reference
- `.github/architecture/new-incident-storyboard.md` - Templates for multiple incident types
- `.github/architecture/phishing-incident.md` - Example of complete incident (use as template)
- `.github/architecture/notebook-storyboards.md` - Notebook development principles

## Pattern Reusability Principle

**Every incident uses the same core patterns:**
- Pattern 3.1: Incident Container (Level 6)
- Pattern 3.3: Observed-Data/Sighting/Evidence (Level 2-3)
- Pattern 3.4: Event Derivation from Sightings (Level 4)
- Pattern 3.5: Task Integration (Level 4)
- Pattern 3.6: Impact Assessment (Level 3)
- Pattern 3.7: Sequence Workflow Orchestration (Level 5)

**What changes per incident type:**
- SCO types (file vs email vs network-traffic)
- Indicator patterns (file hash vs SQL injection vs behavior)
- Task details (forensics vs containment vs compliance)
- Impact types (confidentiality vs availability vs integrity)
- Story narrative (phishing vs malware vs breach)

## Pre-Planning Checklist

Before creating a new incident notebook, complete this analysis:

### 1. Define the Story
- [ ] **One-sentence summary**: What happened?
- [ ] **Attack vector**: How did it start?
- [ ] **Detection method**: How was it discovered?
- [ ] **Primary impact**: Confidentiality, integrity, or availability?
- [ ] **Response type**: Investigation, containment, recovery, or notification?

### 2. Identify Characters (Identities)
- [ ] **Victims**: Which users/systems affected? (from Step_1)
- [ ] **Witnesses**: Who reported it? (from Step_0)
- [ ] **Attackers**: Known threat actor? (create if needed)
- [ ] **Responders**: Who handles this? (from Step_0)

### 3. Map Observables to SCOs
List all evidence and map to STIX SCO types:
- Email-based: email-message, email-addr, url
- File-based: file, directory, process
- Network-based: network-traffic, ipv4-addr, domain-name
- User-based: user-account, identity
- Data-based: artifact (logs, reports, dumps)

### 4. Design Event Timeline
Create chronological event list:
1. Initial compromise (T+0)
2. Attacker actions (T+minutes/hours)
3. Detection (T+X)
4. Analysis (T+X+Y)
5. Response (T+X+Y+Z)

### 5. Plan Response Tasks
List investigation/response tasks with dependencies:
- Immediate: What must happen first?
- Investigation: What needs analysis?
- Containment: How to stop it?
- Recovery: How to restore?
- Prevention: How to prevent recurrence?

### 6. Assess Impact
Determine impact characteristics:
- **Category**: confidentiality, integrity, availability, physical (from 7 impact extensions)
- **Criticality**: 0-100 score
- **Affected entities**: Systems, users, data
- **Potential supersession**: Will impact change as evidence arrives?

## Universal Notebook Template

All incident notebooks follow this structure (adapt cell counts as needed):

### Act 1: Setup and Introduction (Cells 1-9)

**Cell 1**: Story introduction
```markdown
# Incident: [Type] - [Name]

## Story Overview

[Engaging narrative describing what happened]

**Incident Type**: [malware|data-breach|insider-threat|denial-of-service|etc.]
**Primary Impact**: [confidentiality|integrity|availability]
**Detection Method**: [alert|user-report|hunt|audit|etc.]

## Learning Objectives

By the end of this notebook, you'll understand:
1. How to model [incident type] using STIX
2. Which SCOs represent [specific observables]
3. How to create [specific indicators]
4. Response tasks specific to [incident type]
5. Pattern reusability across incident types

## Prerequisites

- Step_0: User identities created
- Step_1: Company/employee identities created
- Understanding of Patterns 3.1-3.7 from stix-graph-patterns.md
```

**Cells 2-7**: Environment setup
```python
# Standard imports
import sys
sys.path.append('../')
from Block_Families.General.Import_Bundle.import_bundle import *
# ... load utilities
# ... load identities from Step_0/Step_1
```

**Cells 8-9**: Create incident context directory
```python
# Create context directory for this incident
context_dir = create_incident_context(company_identity.id)
print(f"Context: {context_dir}")
```

### Act 2: Foundation Evidence (Cells 10-25)
Create Level 0-2 objects (SCOs, observed-data)

**Pattern**: Start with lowest level, build up
- Level 0 SCOs (no embedded refs)
- Level 1 SCOs (refs to Level 0)
- Level 2 observed-data (wraps SCOs)

**For each major evidence piece:**
1. Markdown explaining the evidence
2. Code creating SCO(s)
3. Code creating observed-data
4. Verification print

### Act 3: Analysis Objects (Cells 26-35)
Create Level 3 objects (indicators, sightings, impacts)

**Indicators**:
```markdown
## Creating Threat Indicators

[Explain what patterns indicate malicious activity]
[Show STIX pattern syntax]
```
```python
indicator = invoke_make_indicator_block(
    pattern="[STIX pattern]",
    indicator_types=["malicious-activity"],
    name="[Indicator name]"
)
```

**Sightings**:
```markdown
## Detection: [Sighting Type]

**Pattern 3.3**: Observed-Data/Sighting/Evidence

[Explain detection source]
[Show which sighting extension applies]
```
```python
sighting = invoke_make_sighting_block(
    sighting_of_ref=indicator.id,
    observed_data_refs=[observed_data.id],
    extensions={
        "sighting-[type]": {
            # Type-specific properties
        }
    }
)
```

**Impacts**:
```markdown
## Impact Assessment

**Pattern 3.6**: Impact Assessment

[Explain what was affected]
[Show CIA triad impact]
```
```python
impact = invoke_make_impact_block(
    impact_category="[category]",
    criticality=[0-100],
    description="[What was affected]",
    extensions={
        "impact-[category]": {
            # Category-specific properties
        }
    }
)
```

### Act 4: Timeline Objects (Cells 36-45)
Create Level 4 objects (events, tasks)

**Events**:
```markdown
## Event Timeline

**Pattern 3.4**: Event Derivation from Sightings

[Show chronological event sequence]
```
```python
event_1 = invoke_make_event_block(
    event_types=["[type]"],
    sighting_refs=[sighting.id],
    description="[What happened]",
    start_time="[ISO timestamp]"
)
# ... create all events in timeline
```

**Tasks**:
```markdown
## Response Tasks

**Pattern 3.5**: Task Integration via SRO Relationships

[Explain investigation/response steps]
[Show task dependencies]
```
```python
task_1 = invoke_make_task_block(
    name="[Task name]",
    task_types=["investigation"],
    description="[What to do]",
    created_by_ref=analyst_identity.id
)

task_2 = invoke_make_task_block(
    name="[Dependent task]",
    depends_on_refs=[task_1.id],  # Dependency
    # ...
)
```

### Act 5: Workflow Organization (Cells 46-52)
Create Level 5 objects (sequences)

```markdown
## Workflow Orchestration

**Pattern 3.7**: Sequence Workflow Orchestration

[Explain how tasks are organized]
[Show workflow phases]
```
```python
sequence_1 = invoke_make_sequence_block(
    name="[Phase name]",
    step_refs=[task_1.id, task_2.id],
    description="[Workflow purpose]"
)
```

### Act 6: Incident Container (Cells 53-58)
Create Level 6 object (incident)

```markdown
## The Incident Container

**Pattern 3.1**: Incident Container with IncidentCoreExt

We've built everything the incident references. Now we package it all together.

**Objects created:**
- Level 0-1: [X] SCOs
- Level 2: [Y] observed-data
- Level 3: [Z] indicators, sightings, impacts
- Level 4: [A] events, tasks
- Level 5: [B] sequences

All of these will be referenced by the incident's IncidentCoreExt.
```
```python
incident = invoke_make_incident_block(
    name="[Incident name]",
    incident_types=["[type]"],
    description="[Incident description]",
    extensions={
        "IncidentCoreExt": {
            "determination": "suspected",  # or confirmed
            "impact_refs": [impact.id for impact in impacts],
            "task_refs": [task.id for task in tasks],
            "sequence_refs": [seq.id for seq in sequences],
            "event_refs": [event.id for event in events],
            "sighting_refs": [sighting.id for sighting in sightings],
            "other_object_refs": [
                # indicators, observed-data, etc.
            ]
        }
    }
)
```

### Act 7: Save and Verify (Cells 59-62)
```markdown
## Saving to Context Memory

All objects saved to: `/identity--{company}/incident--{uuid}.json`
```
```python
# Save all objects to context
save_to_context(incident)
save_to_context(all_objects)

# Verify
print(f"✅ Incident created: {incident.id}")
print(f"   Total objects: {total_count}")
print(f"   Context: {context_dir}")
```

## Incident Type Specific Guidance

### Malware Infection Incident

**SCO focus**: file, process, network-traffic
**Indicators**: File hashes, process behavior, C2 patterns
**Events**: email-received → file-downloaded → macro-executed → malware-downloaded → process-created → files-encrypted
**Tasks**: Isolate host, analyze malware, check backups, reimage, restore
**Impact**: availability (file encryption), integrity (data loss)
**Sightings**: alert (EDR), anecdote (user report), enrichment (hash reputation), hunt (other infections)

**Key difference from phishing**: Process execution chain, file-based evidence

### Data Breach Incident

**SCO focus**: network-traffic, user-account, artifact
**Indicators**: SQL injection pattern, data exfiltration volume, attacker IP
**Events**: vulnerability-exploited → access-gained → data-queried → data-exfiltrated → breach-discovered
**Tasks**: Isolate database, audit logs, identify victims, patch, notify, regulatory reporting
**Impact**: confidentiality (PII exposed) - often no supersession (irreversible)
**Sightings**: alert (audit log), hunt (other accounts), external (law enforcement), enrichment (IP reputation)

**Key difference from phishing**: Network-traffic based, compliance tasks, confidentiality impact

### Insider Threat Incident

**SCO focus**: file, user-account, directory, process
**Indicators**: Behavior patterns (unusual access, off-hours, volume)
**Events**: access-increased → files-accessed → files-copied → alert-created → manager-reported
**Tasks**: Disable account, retrieve device, audit access, interview, review policies
**Impact**: confidentiality (potential data loss), often superseded after recovery
**Sightings**: alert (DLP), anecdote (manager report), hunt (other access), exclusion (legitimate activity)

**Key difference from phishing**: User is both victim and attacker, HR/legal involvement, behavior patterns vs events

### DDoS Attack Incident

**SCO focus**: network-traffic, ipv4-addr, domain-name, artifact (pcaps)
**Indicators**: Traffic volume, botnet signatures, request patterns
**Events**: traffic-increased → alert-created → service-degraded → service-unavailable → mitigation-started → service-restored
**Tasks**: Enable protection, analyze pattern, block IPs, scale infrastructure, contact ISP
**Impact**: availability (service down), rapid fluctuation (multiple supersessions)
**Sightings**: alert (monitoring), enrichment (IP reputation - botnet), external (ISP analysis)

**Key difference from phishing**: Many SCOs (hundreds of IPs), rapid state changes, network-focused

## Pattern Mapping Reference

Use this to ensure all required patterns are demonstrated:

| Pattern | All Incidents | Notes |
|---------|---------------|-------|
| 3.1 (Incident) | ✅ Required | Always Level 6, always has IncidentCoreExt |
| 3.2 (Identity) | ✅ Required | Reuse from Step_0/Step_1 |
| 3.3 (Sighting) | ✅ Required | At least one sighting (usually multiple) |
| 3.4 (Event) | ✅ Required | Timeline shows progression |
| 3.5 (Task) | ✅ Required | Response/investigation steps |
| 3.6 (Impact) | ✅ Required | CIA triad assessment |
| 3.7 (Sequence) | ✅ Required | Organize tasks into workflows |
| 3.8 (Email) | Optional | Only for email-based incidents |
| 3.9 (Anecdote) | Optional | If human reports exist |
| 3.10 (Supersession) | Recommended | Show impact evolution |
| 3.11 (Ownership) | Recommended | created_by_ref vs owned_by_ref |
| 3.12 (State) | Recommended | State changes via events |
| 3.13 (Conditional) | Optional | If/else workflows |

## Development Workflow

### Phase 1: Planning (Before Coding)
1. Complete pre-planning checklist
2. Review new-incident-storyboard.md for type-specific guidance
3. Sketch object dependency graph (Level 0→6)
4. Write story narrative first (markdown only)

### Phase 2: Implementation (Coding)
1. Start with Act 1 (setup)
2. Build bottom-up (Level 0→6)
3. Verify each level before proceeding
4. Add story markdown between code cells
5. Print objects as created

### Phase 3: Enhancement (Storytelling)
1. Add pattern explanations
2. Add visual metaphors
3. Add "why this matters" sections
4. Add comparison to phishing incident
5. Add verification cells

### Phase 4: Testing (Validation)
1. Execute all cells sequentially
2. Verify context memory structure
3. Check incident references complete
4. Validate against stix-graph-patterns.md
5. Review for story coherence

## Quality Checklist

### Story Quality
- [ ] Engaging narrative (not just procedures)
- [ ] Characters well-defined (identities from Step_0/Step_1)
- [ ] Timeline logical and realistic
- [ ] Response appropriate to threat type
- [ ] Comparison to phishing shows differences

### Technical Quality
- [ ] All objects in dependency order
- [ ] All embedded references valid
- [ ] Incident references all created objects
- [ ] Context memory structure correct
- [ ] No hard-coded UUIDs

### Educational Quality
- [ ] All 7 core patterns demonstrated
- [ ] Pattern usage explained clearly
- [ ] Design decisions shown
- [ ] References stix-graph-patterns.md
- [ ] Includes "what we learned" summary

### Code Quality
- [ ] Clean, readable code
- [ ] Consistent naming conventions
- [ ] Adequate comments
- [ ] Print statements show progress
- [ ] Error handling present

## Common Mistakes to Avoid

### 1. Wrong Dependency Order
❌ Creating incident before evidence
✅ Build Level 0→6 sequentially

### 2. Incorrect SCO Selection
❌ Using email-message for network scan
✅ Use network-traffic for network evidence

### 3. Missing Pattern Explanations
❌ Just using patterns without explaining
✅ Show which pattern, why it applies

### 4. Unrealistic Timeline
❌ All events at same timestamp
✅ Logical time progression (minutes/hours/days)

### 5. Generic Tasks
❌ "Investigate incident" (vague)
✅ "Analyze malware binary in sandbox" (specific)

## Extension Ideas

After creating base incident, consider:

### Additional Evidence (Step_N notebooks)
- Add threat intelligence (sighting-context)
- Add enrichment data (sighting-enrichment)
- Add hunt findings (sighting-hunt)
- Add framework mapping (sighting-framework)

### Related Incidents
- Model multi-stage attacks (phishing → malware → breach)
- Use relationships to link incidents
- Show campaign evolution

### Advanced Patterns
- Conditional workflows (Pattern 3.13)
- Complex task dependency graphs
- Impact supersession chains
- Cross-incident analysis

## References

- `new-incident-storyboard.md` - Type-specific templates
- `stix-graph-patterns.md` - Pattern reference
- `phishing-incident.md` - Complete example
- `notebook-storyboards.md` - Development principles

## Success Criteria

New incident notebooks should:
1. Tell coherent, engaging stories
2. Demonstrate all core patterns (3.1-3.7)
3. Use appropriate SCOs for evidence type
4. Create realistic response tasks
5. Execute without errors
6. Serve as teaching tools

**Remember**: Different incidents, same patterns. The STIX graph structure is consistent; only the story and SCOs change. This is the power of pattern reusability.
