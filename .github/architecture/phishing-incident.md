# The Phishing Incident Story

## Overview
This story combines **Step_2_Create_Incident_with_an_Alert.ipynb** and **Step_3_Get the Anecdote.ipynb** to show a complete phishing incident lifecycle: from initial SIEM alert detection through user report submission. It demonstrates how evidence accumulates through different sighting extensions (alert, anecdote) and how the incident graph evolves.

**Key Concept**: An incident isn't created all at once. It grows as evidence accumulates. Step_2 creates the initial incident from a SIEM alert. Step_3 extends it with a user report (anecdote).

## Story Arc

### Act 1: The Alert (Step_2)
At 3:47 AM, your SIEM detects a suspicious email. An automated alert fires: "Phishing pattern detected - malicious URL in email to executive."

### Act 2: The Evidence Extension (Step_3)
Hours later, the targeted executive submits a report through your incident response portal: "I received a suspicious email pretending to be from IT. I didn't click the link."

Both pieces of evidence point to the same incident. The graph connects them.

## Characters

### The Malicious Email (Step_2)
- **Sender**: attacker@evil.com
- **Recipient**: ceo@victim-company.com
- **Subject**: "Urgent: Verify your account"
- **Body**: Contains phishing text with malicious URL
- **URL**: https://evil.com/phish

### The User Report (Step_3)
- **Reporter**: CEO (identity from Step_1)
- **Report Time**: 8:15 AM (5 hours after alert)
- **Content**: Textual description of the phishing attempt
- **Context**: User didn't click, reported immediately

### The Evidence Trail
1. **SIEM Alert** (automated detection)
2. **User Anecdote** (human verification)

Both confirm the same incident from different perspectives.

## Graph Patterns Applied

### Pattern 3.8: Email Message Communication Graph (Step_2)
The phishing email creates a communication graph:
```
email-message
├── from_ref → email-addr (attacker@evil.com)
├── to_refs → [email-addr (ceo@victim-company.com)]
└── body_multipart[0].body_raw_ref → artifact (email body text)
   └── Contains URL reference
```

### Pattern 3.3: Observed-Data/Sighting/Evidence (Both Steps)
**Step_2**: Observed-data wraps URL + email-message, sighting uses `sighting-alert` extension
**Step_3**: Observed-data wraps anecdote SCO, sighting uses `sighting-anecdote` extension

Both sightings link to the same incident through their `sighting_of_ref` (the indicator).

### Pattern 3.9: Anecdote Provenance (Step_3)
The anecdote SCO records:
```json
{
  "type": "anecdote",
  "statement": "I received a suspicious email...",
  "made_by_ref": "identity--{ceo}",
  "context_refs": ["observed-data--{original-email}"]
}
```

This creates provenance: who said what, when, and in what context.

### Pattern 3.4: Event Derivation from Sightings (Both Steps)
**Step_2**: Event derived from sighting-alert
- `event_types`: ["alert-created"]
- `changed_objects`: The observed-data containing email + URL
- `description`: "Automated SIEM alert fired"

**Step_3**: Event derived from sighting-anecdote
- `event_types`: ["user-reported"]
- `changed_objects`: The observed-data containing anecdote
- `description`: "User submitted incident report"

Two events, same incident, different evidence sources.

### Pattern 3.6: Impact Assessment (Both Steps)
**Step_2**: Initial impact assessment
```json
{
  "type": "impact",
  "impact_category": "availability",
  "criticality": 70,
  "description": "Potential account compromise if link clicked",
  "impacted_entity_counts": {
    "systems-affected": 0,
    "users-affected": 1
  }
}
```

**Step_3**: Updated impact after user report
```json
{
  "type": "impact",
  "impact_category": "integrity",
  "criticality": 30,
  "description": "User did not click link - no compromise occurred",
  "supersedes_refs": ["impact--{initial-assessment}"]
}
```

Pattern 3.10 (Impact Supersession Chain) in action: new evidence lowers criticality.

### Pattern 3.5: Task Integration (Step_2)
Five investigation tasks created:
1. **Analyze Email Headers** (created_by_ref → analyst identity)
2. **Check URL Reputation** (owned_by_ref → security team)
3. **Scan User Mailbox** (depends_on_refs → [task-1])
4. **Block Sender Domain** (depends_on_refs → [task-2])
5. **Notify Affected Users** (depends_on_refs → [task-3, task-4])

Dependencies create execution order. Pattern 3.11 (Task Ownership vs Creation) shown.

### Pattern 3.7: Sequence Workflow Orchestration (Step_2)
Three sequences created:
1. **Initial Triage**: [task-1, task-2]
2. **Remediation**: [task-3, task-4]
3. **Communication**: [task-5]

Sequences group tasks into logical phases. Conditional logic (Pattern 3.13) can gate sequence execution.

### Pattern 3.1: Incident Container (Both Steps)
**Step_2**: Initial incident creation
```json
{
  "type": "incident",
  "name": "Phishing Email - Executive Targeted",
  "incident_types": ["phishing"],
  "extensions": {
    "extension-definition--{IncidentCoreExt}": {
      "extension_type": "property-extension",
      "determination": "suspected",
      "impact_refs": ["impact--{initial}"],
      "task_refs": ["task--1", "task--2", "task--3", "task--4", "task--5"],
      "sequence_refs": ["sequence--1", "sequence--2", "sequence--3"],
      "event_refs": ["event--{alert}"],
      "sighting_refs": ["sighting--{alert}"],
      "other_object_refs": ["indicator--{phishing-url}", "observed-data--{email}"]
    }
  }
}
```

**Step_3**: Updated incident (accumulates evidence)
```json
{
  "extensions": {
    "extension-definition--{IncidentCoreExt}": {
      "impact_refs": ["impact--{initial}", "impact--{updated}"],
      "event_refs": ["event--{alert}", "event--{user-report}"],
      "sighting_refs": ["sighting--{alert}", "sighting--{anecdote}"],
      "other_object_refs": [
        "indicator--{phishing-url}",
        "observed-data--{email}",
        "observed-data--{anecdote}"
      ]
    }
  }
}
```

The incident grows as evidence accumulates. Each `_refs` list expands.

## Notebook Structure

### Step_2: Create Incident with Alert (47 cells)

**Act 1: Setup** (Cells 1-9)
1. Introduction markdown
2-7. Environment setup (imports, utilities)
8-9. Create incident context directory

**Act 2: Observed Evidence** (Cells 10-16)
10-12. Create URL SCO (malicious link)
```python
url_obj = invoke_make_url_block(value="https://evil.com/phish")
```

13-14. Create email-message SCO (phishing email)
```python
email_obj = invoke_make_email_message_block(
    from_ref=attacker_email.id,
    to_refs=[ceo_email.id],
    subject="Urgent: Verify your account",
    body_multipart=[...],
    additional_header_fields={...}
)
```

15-16. Create observed-data wrapping URL + email-message
```python
observed_data = invoke_make_observed_data_block(
    object_refs=[url_obj.id, email_obj.id]
)
```

**Act 3: Detection** (Cells 17-21)
17-18. Create indicator (pattern: URL in email)
```python
indicator = invoke_make_indicator_block(
    pattern="[email-message:body_multipart[*].body_raw_ref.payload_bin MATCHES 'evil.com']",
    indicator_types=["malicious-activity"]
)
```

19-21. Create sighting with `sighting-alert` extension
```python
sighting = invoke_make_sighting_block(
    sighting_of_ref=indicator.id,
    observed_data_refs=[observed_data.id],
    extensions={
        "sighting-alert": {
            "alert_type": "siem",
            "severity": "high",
            "source_system": "splunk-prod-01"
        }
    }
)
```

**Act 4: Event Derivation** (Cells 22-24)
22-24. Create event from sighting
```python
event = invoke_make_event_block(
    event_types=["alert-created"],
    sighting_refs=[sighting.id],
    changed_objects=[observed_data.id]
)
```

**Act 5: Impact & Response** (Cells 25-40)
25-27. Create initial impact assessment
28-33. Create 5 investigation tasks with dependencies
34-40. Create 3 sequence workflows grouping tasks

**Act 6: Incident Creation** (Cells 41-47)
41-42. Create incident object with IncidentCoreExt
```python
incident = invoke_make_incident_block(
    name="Phishing Email - Executive Targeted",
    incident_types=["phishing"],
    extensions={
        "IncidentCoreExt": {
            "determination": "suspected",
            "impact_refs": [impact.id],
            "task_refs": [t1.id, t2.id, t3.id, t4.id, t5.id],
            "sequence_refs": [s1.id, s2.id, s3.id],
            "event_refs": [event.id],
            "sighting_refs": [sighting.id],
            "other_object_refs": [indicator.id, observed_data.id]
        }
    }
)
```

43-47. Save incident to context memory, verify structure

### Step_3: Get the Anecdote (24 cells)

**Act 1: Setup** (Cells 1-9)
1-2. Introduction markdown
3-7. Environment setup (same utilities)
8-9. **Retrieve existing incident** from context memory
```python
incident = load_from_context(incident_id)
```

**Act 2: User Report** (Cells 10-13)
10-11. Create anecdote SCO
```python
anecdote = invoke_make_anecdote_block(
    statement="I received a suspicious email claiming to be from IT...",
    made_by_ref=ceo_identity.id,  # From Step_1
    context_refs=[observed_data_email.id]  # References original email
)
```

12-13. Create observed-data wrapping anecdote
```python
observed_data_anecdote = invoke_make_observed_data_block(
    object_refs=[anecdote.id]
)
```

**Act 3: Evidence Extension** (Cells 14-15)
14-15. Create sighting with `sighting-anecdote` extension
```python
sighting_anecdote = invoke_make_sighting_block(
    sighting_of_ref=indicator.id,  # Same indicator from Step_2
    observed_data_refs=[observed_data_anecdote.id],
    extensions={
        "sighting-anecdote": {
            "report_type": "user-submitted",
            "verification_status": "verified"
        }
    }
)
```

**Act 4: Impact Update** (Cells 16-17)
16-17. Create new impact superseding initial assessment
```python
impact_updated = invoke_make_impact_block(
    impact_category="integrity",
    criticality=30,  # Down from 70
    description="User did not click link - no compromise",
    supersedes_refs=[impact_initial.id]  # Pattern 3.10
)
```

**Act 5: Event Creation** (Cells 18-19)
18-19. Create event from anecdote sighting
```python
event_report = invoke_make_event_block(
    event_types=["user-reported"],
    sighting_refs=[sighting_anecdote.id],
    changed_objects=[observed_data_anecdote.id]
)
```

**Act 6: Incident Update** (Cells 20-24)
20-23. Update incident with new evidence
```python
incident.extensions["IncidentCoreExt"]["impact_refs"].append(impact_updated.id)
incident.extensions["IncidentCoreExt"]["event_refs"].append(event_report.id)
incident.extensions["IncidentCoreExt"]["sighting_refs"].append(sighting_anecdote.id)
incident.extensions["IncidentCoreExt"]["other_object_refs"].append(observed_data_anecdote.id)
```

24. Summary markdown

## Context Memory Created

### Step_2 Creates:
```
/identity--{incident-context-id}/
├── incident--{phishing-incident}.json
├── url--{malicious-link}.json
├── email-message--{phishing-email}.json
├── email-addr--{attacker}.json
├── email-addr--{ceo}.json
├── observed-data--{email-and-url}.json
├── indicator--{phishing-pattern}.json
├── sighting--{alert}.json
├── event--{alert-created}.json
├── impact--{initial-assessment}.json
├── task--{analyze-headers}.json
├── task--{check-url}.json
├── task--{scan-mailbox}.json
├── task--{block-sender}.json
├── task--{notify-users}.json
├── sequence--{triage}.json
├── sequence--{remediation}.json
└── sequence--{communication}.json
```

### Step_3 Adds:
```
/identity--{incident-context-id}/
├── anecdote--{user-report}.json          # NEW
├── observed-data--{anecdote}.json        # NEW
├── sighting--{anecdote}.json             # NEW
├── event--{user-reported}.json           # NEW
├── impact--{updated-assessment}.json     # NEW
└── incident--{phishing-incident}.json    # UPDATED
```

The incident file is updated in-place with new `_refs` pointing to the additional evidence.

## Why This Story Matters

### Evidence Accumulation Pattern
Real incidents aren't created complete. Evidence arrives over time:
- **T+0**: Automated alert fires
- **T+5h**: User reports same incident
- **T+1d**: Forensics finds additional indicators
- **T+3d**: Impact fully assessed

The graph accommodates this naturally. The incident object's `_refs` lists grow as evidence arrives.

### Multiple Evidence Sources
This story shows two sighting extensions:
- **sighting-alert**: Automated detection (SIEM, EDR, IDS)
- **sighting-anecdote**: Human reports (users, analysts)

Six more exist: `sighting-context`, `sighting-exclusion`, `sighting-enrichment`, `sighting-hunt`, `sighting-framework`, `sighting-external`. Each represents a different evidence source.

### Incident State Evolution
Pattern 3.12 (State Change Tracking) visible through:
- **Impact supersession**: Initial high-criticality alert downgraded after user confirmation
- **Determination evolution**: "suspected" → "confirmed" → "resolved"
- **Event timeline**: Ordered by timestamps, shows incident progression

### Dependency Hierarchy Demonstrated
Complete Level 0-6 hierarchy:
- **Level 6**: incident (references everything below)
- **Level 5**: sequence (references tasks, events)
- **Level 4**: task, event (reference sightings, impacts)
- **Level 3**: sighting, impact (reference observed-data, indicators)
- **Level 2**: observed-data, indicator (reference SCOs)
- **Level 1**: email-message, anecdote (reference email-addr, identity)
- **Level 0**: email-addr, user-account, identity (no embedded refs)

Build from bottom up. Can't create incident until you have tasks, can't create tasks until you have sightings, etc.

## Comparison to Graph Patterns

| Pattern | Step_2 Usage | Step_3 Usage |
|---------|--------------|--------------|
| 3.1 (Incident Container) | Creates incident with IncidentCoreExt | Updates incident, adds refs |
| 3.2 (Identity Sub-Pattern) | Uses identities from Step_1 | Uses CEO identity from Step_1 |
| 3.3 (Observed-Data/Sighting) | Alert sighting | Anecdote sighting |
| 3.4 (Event Derivation) | Alert-created event | User-reported event |
| 3.5 (Task Integration) | Creates 5 tasks with deps | No new tasks |
| 3.6 (Impact Assessment) | Initial assessment | Superseding assessment |
| 3.7 (Sequence Workflows) | Creates 3 sequences | No new sequences |
| 3.8 (Email Communication) | Email-message graph | References email |
| 3.9 (Anecdote Provenance) | Not used | Creates anecdote with provenance |
| 3.10 (Impact Supersession) | Not used | `supersedes_refs` |
| 3.11 (Task Ownership) | Demonstrates created_by vs owned_by | Not used |
| 3.12 (State Change) | Initial state | State evolution |
| 3.13 (Conditional Sequences) | Mentioned, not implemented | Not used |

**Key Insight**: Step_2 demonstrates breadth (most patterns). Step_3 demonstrates depth (evidence accumulation).

## Next Steps

### For Understanding
1. Review `stix-graph-patterns.md` for detailed pattern explanations
2. Compare this to `new_user.md` and `new_company.md` (simpler Level 0-2 patterns)
3. Note how Patterns 3.1-3.9 interact to create complete incident

### For Development
1. Run Step_2 notebook to create initial incident
2. Verify context memory structure
3. Run Step_3 notebook to extend incident
4. Examine updated incident JSON to see accumulated `_refs`

### For Extension
After completing Step_3, you can:
- Add `sighting-context` (external threat intel)
- Add `sighting-enrichment` (reputation data)
- Add `sighting-hunt` (proactive investigation findings)
- Add additional impacts, events, tasks

Each addition updates the incident's `_refs` lists. The graph grows organically.

## Story Emphasis

This isn't just code execution—it's a narrative:
1. **The Alert**: "Something suspicious happened"
2. **The Report**: "A human confirms it"
3. **The Assessment**: "We understand the impact"
4. **The Response**: "We know what to do"
5. **The Update**: "New information changes our understanding"

The STIX graph preserves this narrative structure. Query the graph later, and you can reconstruct the story: what happened, who saw it, when they saw it, what they thought, what they did.

**This is incident reconstitution.**
