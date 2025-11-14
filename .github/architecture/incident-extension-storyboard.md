# Incident Extension Storyboard

## Purpose
This storyboard provides detailed instructions for extending the phishing incident from Step_2/Step_3 with additional evidence types. It demonstrates how incidents evolve as new information arrives from different sources.

**Target Audience**: Developers creating notebooks that extend existing incidents with new evidence.

## The Extension Principle

Incidents are living documents. They grow as evidence accumulates:
- **Hour 0**: SIEM alert fires (Step_2)
- **Hour 5**: User reports (Step_3) 
- **Hour 12**: Threat intel arrives (context)
- **Hour 24**: Forensics completes (enrichment)
- **Day 3**: Proactive hunt finds related activity (hunt)
- **Week 1**: External vendor provides analysis (external)

Each evidence type uses a different sighting extension. Each sighting creates events, impacts, potentially tasks.

## Available Sighting Extensions

### Already Demonstrated
- ✅ **sighting-alert**: Automated detection (SIEM, EDR, IDS) - Step_2
- ✅ **sighting-anecdote**: Human reports (users, analysts) - Step_3

### Available for Extension
- **sighting-context**: External threat intelligence
- **sighting-exclusion**: False positive identification
- **sighting-enrichment**: Reputation/classification data
- **sighting-hunt**: Proactive investigation findings
- **sighting-framework**: MITRE ATT&CK or other framework mapping
- **sighting-external**: Third-party analysis

## Extension Pattern Template

For each new evidence type, follow this pattern:

### Step 1: Create Evidence SCO(s)
Determine what observable was sighted:
- Context: Create artifact with external report
- Enrichment: Add properties to existing SCOs or create new ones
- Hunt: Create new SCOs for discovered indicators
- Framework: Reference external framework entries

### Step 2: Create observed-data
Wrap the new SCO(s) in observed-data:
```python
observed_data = invoke_make_observed_data_block(
    object_refs=[new_sco.id],
    first_observed="2024-01-15T12:00:00Z",
    last_observed="2024-01-15T12:00:00Z"
)
```

### Step 3: Create Sighting with Extension
Use appropriate sighting extension:
```python
sighting = invoke_make_sighting_block(
    sighting_of_ref=indicator.id,  # Same indicator from Step_2
    observed_data_refs=[observed_data.id],
    extensions={
        "sighting-[type]": {
            # Extension-specific properties
        }
    }
)
```

### Step 4: Create Event
Derive event from sighting:
```python
event = invoke_make_event_block(
    event_types=["[appropriate-type]"],
    sighting_refs=[sighting.id],
    changed_objects=[observed_data.id]
)
```

### Step 5: Assess Impact (if needed)
Create new impact or supersede existing:
```python
impact = invoke_make_impact_block(
    impact_category="[category]",
    criticality=50,
    description="...",
    supersedes_refs=[previous_impact.id]  # If superseding
)
```

### Step 6: Update Incident
Add new objects to incident references:
```python
incident.extensions["IncidentCoreExt"]["sighting_refs"].append(sighting.id)
incident.extensions["IncidentCoreExt"]["event_refs"].append(event.id)
incident.extensions["IncidentCoreExt"]["other_object_refs"].append(observed_data.id)
# Save updated incident
save_to_context(incident)
```

## Extension Example 1: Threat Intelligence (sighting-context)

### Story
12 hours after the phishing alert, your threat intel feed reports that `evil.com` is a known phishing infrastructure operated by APT28.

### Notebook: `Step_4_Add_Threat_Intel.ipynb`

**Cell 1-2**: Story introduction
```markdown
# Adding Threat Intelligence Context

Our threat intelligence feed has identified the malicious domain `evil.com` 
as infrastructure associated with APT28 (Fancy Bear). This provides attribution 
context for our incident.
```

**Cell 3-7**: Environment setup, load existing incident

**Cell 8-10**: Create threat intel artifact
```python
# Story: "External threat intelligence arrives"
threat_report = invoke_make_artifact_block(
    payload_bin="<base64-encoded-threat-report>",
    mime_type="application/json"
)
```

**Cell 11-13**: Create observed-data
```python
observed_data_intel = invoke_make_observed_data_block(
    object_refs=[threat_report.id],
    first_observed="2024-01-15T12:00:00Z"
)
```

**Cell 14-16**: Create sighting with sighting-context
```python
sighting_intel = invoke_make_sighting_block(
    sighting_of_ref=indicator.id,  # Original phishing indicator
    observed_data_refs=[observed_data_intel.id],
    extensions={
        "sighting-context": {
            "context_type": "threat-intelligence",
            "source": "ThreatFeed-Pro",
            "confidence": 85,
            "description": "Domain associated with APT28 phishing campaigns"
        }
    }
)
```

**Cell 17-19**: Create event
```python
event_intel = invoke_make_event_block(
    event_types=["threat-intel-received"],
    sighting_refs=[sighting_intel.id],
    changed_objects=[observed_data_intel.id],
    description="External threat intelligence confirms APT28 attribution"
)
```

**Cell 20-22**: Update incident
```python
incident.extensions["IncidentCoreExt"]["sighting_refs"].append(sighting_intel.id)
incident.extensions["IncidentCoreExt"]["event_refs"].append(event_intel.id)
incident.extensions["IncidentCoreExt"]["other_object_refs"].append(observed_data_intel.id)
save_to_context(incident)
```

**Cell 23**: Summary showing incident growth

### Pattern Demonstrated
- Pattern 3.3 (Observed-Data/Sighting/Evidence) with context extension
- Pattern 3.4 (Event Derivation)
- Incident accumulation pattern

## Extension Example 2: Enrichment (sighting-enrichment)

### Story
URL reputation service returns verdict: `evil.com` has reputation score 5/100 (malicious).

### Notebook: `Step_5_Add_Enrichment.ipynb`

**Cell 8-10**: Create enrichment data (no new SCO needed - enriches existing URL)
```python
# Story: "URL reputation check completes"
# Use existing URL SCO, create observed-data referencing it
observed_data_enrichment = invoke_make_observed_data_block(
    object_refs=[url_obj.id],  # Existing URL from Step_2
    first_observed="2024-01-15T14:00:00Z"
)
```

**Cell 11-13**: Create sighting with sighting-enrichment
```python
sighting_enrichment = invoke_make_sighting_block(
    sighting_of_ref=indicator.id,
    observed_data_refs=[observed_data_enrichment.id],
    extensions={
        "sighting-enrichment": {
            "enrichment_type": "reputation",
            "source_system": "VirusTotal",
            "reputation_score": 5,
            "classification": "malicious",
            "categories": ["phishing", "c2-infrastructure"]
        }
    }
)
```

**Cell 14-16**: Create event
```python
event_enrichment = invoke_make_event_block(
    event_types=["enrichment-completed"],
    sighting_refs=[sighting_enrichment.id],
    changed_objects=[url_obj.id],
    description="URL reputation confirms malicious classification"
)
```

**Cell 17-19**: Update incident (same pattern as Example 1)

### Pattern Demonstrated
- Enrichment doesn't create new SCOs - adds metadata to existing
- Pattern 3.3 with enrichment extension
- Reuse of existing URL object

## Extension Example 3: Proactive Hunt (sighting-hunt)

### Story
Your hunt team searches for other emails from `attacker@evil.com` and finds 15 additional phishing attempts.

### Notebook: `Step_6_Add_Hunt_Findings.ipynb`

**Cell 8-10**: Create new email-message SCOs (discovered emails)
```python
# Story: "Hunt team finds related emails"
hunt_emails = []
for i in range(15):
    email = invoke_make_email_message_block(
        from_ref=attacker_email.id,  # Same attacker
        to_refs=[employee_emails[i].id],  # Different victims
        subject=f"Phishing variant {i}",
        # ... other properties
    )
    hunt_emails.append(email)
```

**Cell 11-13**: Create observed-data for hunt findings
```python
observed_data_hunt = invoke_make_observed_data_block(
    object_refs=[e.id for e in hunt_emails]
)
```

**Cell 14-16**: Create sighting with sighting-hunt
```python
sighting_hunt = invoke_make_sighting_block(
    sighting_of_ref=indicator.id,
    observed_data_refs=[observed_data_hunt.id],
    extensions={
        "sighting-hunt": {
            "hunt_type": "email-search",
            "query": "from:attacker@evil.com",
            "results_count": 15,
            "description": "Proactive hunt found 15 related phishing emails"
        }
    }
)
```

**Cell 17-19**: Create impact (escalation)
```python
impact_hunt = invoke_make_impact_block(
    impact_category="availability",
    criticality=90,  # Escalated from 30
    description="15 employees targeted - campaign wider than initially thought",
    supersedes_refs=[impact_updated.id]  # From Step_3
)
```

**Cell 20-22**: Create event
```python
event_hunt = invoke_make_event_block(
    event_types=["hunt-completed"],
    sighting_refs=[sighting_hunt.id],
    changed_objects=[o.id for o in hunt_emails],
    description="Proactive hunt identified campaign scope"
)
```

**Cell 23-25**: Create new tasks (notify 15 employees)
```python
task_notify_all = invoke_make_task_block(
    name="Notify all affected employees",
    task_types=["communication"],
    # ... other properties
)
```

**Cell 26-28**: Update incident
```python
# Add all new objects
incident.extensions["IncidentCoreExt"]["sighting_refs"].append(sighting_hunt.id)
incident.extensions["IncidentCoreExt"]["event_refs"].append(event_hunt.id)
incident.extensions["IncidentCoreExt"]["impact_refs"].append(impact_hunt.id)
incident.extensions["IncidentCoreExt"]["task_refs"].append(task_notify_all.id)
incident.extensions["IncidentCoreExt"]["other_object_refs"].extend([o.id for o in hunt_emails])
save_to_context(incident)
```

### Pattern Demonstrated
- Hunt can discover multiple new objects
- Pattern 3.10 (Impact Supersession) - escalation instead of de-escalation
- Pattern 3.5 (Task Integration) - new tasks from new findings

## Extension Example 4: Framework Mapping (sighting-framework)

### Story
You map the phishing technique to MITRE ATT&CK: T1566.002 (Phishing: Spearphishing Link).

### Notebook: `Step_7_Add_Framework_Mapping.ipynb`

**Cell 8-10**: No new SCO needed - framework mapping is metadata

**Cell 11-13**: Create observed-data (references original email + URL)
```python
observed_data_framework = invoke_make_observed_data_block(
    object_refs=[email_obj.id, url_obj.id]
)
```

**Cell 14-16**: Create sighting with sighting-framework
```python
sighting_framework = invoke_make_sighting_block(
    sighting_of_ref=indicator.id,
    observed_data_refs=[observed_data_framework.id],
    extensions={
        "sighting-framework": {
            "framework_name": "MITRE ATT&CK",
            "framework_version": "14.1",
            "technique_id": "T1566.002",
            "technique_name": "Phishing: Spearphishing Link",
            "tactic": "Initial Access"
        }
    }
)
```

**Cell 17-19**: Create event
```python
event_framework = invoke_make_event_block(
    event_types=["framework-mapped"],
    sighting_refs=[sighting_framework.id],
    description="Incident mapped to MITRE ATT&CK framework"
)
```

**Cell 20-22**: Update incident

### Pattern Demonstrated
- Framework mapping adds analytical context
- Enables cross-incident analysis (find all T1566.002 incidents)
- Pattern 3.3 with framework extension

## Extension Example 5: External Analysis (sighting-external)

### Story
You send email headers to a third-party vendor for analysis. They return detailed forensic report.

### Notebook: `Step_8_Add_External_Analysis.ipynb`

**Cell 8-10**: Create artifact with vendor report
```python
vendor_report = invoke_make_artifact_block(
    payload_bin="<base64-vendor-report-pdf>",
    mime_type="application/pdf"
)
```

**Cell 11-13**: Create observed-data
```python
observed_data_external = invoke_make_observed_data_block(
    object_refs=[vendor_report.id]
)
```

**Cell 14-16**: Create sighting with sighting-external
```python
sighting_external = invoke_make_sighting_block(
    sighting_of_ref=indicator.id,
    observed_data_refs=[observed_data_external.id],
    extensions={
        "sighting-external": {
            "source_organization": "CyberForensics LLC",
            "analysis_type": "email-header-analysis",
            "confidence": 95,
            "findings": "Headers confirm spoofed sender, originated from known phishing infrastructure"
        }
    }
)
```

**Cell 17-19**: Create event, update incident (standard pattern)

### Pattern Demonstrated
- External analysis provides independent verification
- Pattern 3.3 with external extension

## Extension Example 6: Exclusion (sighting-exclusion)

### Story
One of the 15 hunt findings is determined to be a false positive - legitimate email with similar pattern.

### Notebook: `Step_9_Mark_False_Positive.ipynb`

**Cell 8-10**: Identify the false positive email (from hunt findings)
```python
false_positive_email = hunt_emails[7]  # Example
```

**Cell 11-13**: Create observed-data for exclusion
```python
observed_data_exclusion = invoke_make_observed_data_block(
    object_refs=[false_positive_email.id]
)
```

**Cell 14-16**: Create sighting with sighting-exclusion
```python
sighting_exclusion = invoke_make_sighting_block(
    sighting_of_ref=indicator.id,
    observed_data_refs=[observed_data_exclusion.id],
    extensions={
        "sighting-exclusion": {
            "exclusion_reason": "false-positive",
            "explanation": "Legitimate IT department email with similar URL pattern",
            "excluded_by_ref": analyst_identity.id,
            "exclusion_timestamp": "2024-01-16T10:00:00Z"
        }
    }
)
```

**Cell 17-19**: Create event
```python
event_exclusion = invoke_make_event_block(
    event_types=["false-positive-identified"],
    sighting_refs=[sighting_exclusion.id],
    description="Email 8 of 15 determined to be false positive"
)
```

**Cell 20-22**: Update impact (reduce scope)
```python
impact_corrected = invoke_make_impact_block(
    impact_category="availability",
    criticality=85,  # Down from 90
    description="14 confirmed phishing emails (1 false positive excluded)",
    supersedes_refs=[impact_hunt.id]
)
```

**Cell 23-25**: Update incident

### Pattern Demonstrated
- Exclusions reduce incident scope
- Pattern 3.10 (Impact Supersession) - correction
- Provenance: who excluded it and why

## Multi-Extension Orchestration

As you add extensions, the incident accumulates:

```python
# After all extensions
incident.extensions["IncidentCoreExt"] = {
    "determination": "confirmed",  # Evolved from "suspected"
    "sighting_refs": [
        sighting_alert.id,      # Step_2: SIEM
        sighting_anecdote.id,   # Step_3: User report
        sighting_intel.id,      # Step_4: Threat intel
        sighting_enrichment.id, # Step_5: Reputation
        sighting_hunt.id,       # Step_6: Hunt findings
        sighting_framework.id,  # Step_7: ATT&CK
        sighting_external.id,   # Step_8: Vendor analysis
        sighting_exclusion.id   # Step_9: False positive
    ],
    "event_refs": [
        # 8 events corresponding to 8 sightings
    ],
    "impact_refs": [
        impact_initial.id,      # Step_2: High severity
        impact_updated.id,      # Step_3: Reduced (user didn't click)
        impact_hunt.id,         # Step_6: Escalated (15 targets)
        impact_corrected.id     # Step_9: Reduced (1 false positive)
    ],
    # ... other refs
}
```

## Development Checklist

For each extension notebook:

### Story
- [ ] Clear narrative: what new evidence arrived?
- [ ] Timing: when did this happen in incident timeline?
- [ ] Source: who/what provided the evidence?
- [ ] Impact: how does this change our understanding?

### Technical
- [ ] Load existing incident from context
- [ ] Create appropriate SCOs (if needed)
- [ ] Create observed-data wrapping evidence
- [ ] Create sighting with correct extension
- [ ] Create event from sighting
- [ ] Assess impact change (supersede if needed)
- [ ] Update incident._refs lists
- [ ] Save updated incident to context

### Educational
- [ ] Explain why this extension type is appropriate
- [ ] Show before/after incident state
- [ ] Demonstrate pattern reuse
- [ ] Point to other possible extensions

## Pattern Summary

| Extension | Creates New SCOs? | Typical Event Type | Impact Change | Common Use |
|-----------|-------------------|-------------------|---------------|------------|
| sighting-alert | Often | alert-created | Initial assessment | SIEM, EDR, IDS |
| sighting-anecdote | Yes (anecdote) | user-reported | Often reduces | User reports |
| sighting-context | Yes (artifact) | threat-intel-received | Varies | External intel |
| sighting-enrichment | No | enrichment-completed | Rarely | Reputation |
| sighting-hunt | Often many | hunt-completed | Often escalates | Proactive search |
| sighting-framework | No | framework-mapped | No | ATT&CK mapping |
| sighting-external | Yes (artifact) | external-analysis-received | Varies | Vendor analysis |
| sighting-exclusion | No | false-positive-identified | Reduces | FP removal |

## References

- See `stix-graph-patterns.md` for Pattern 3.3 (Sighting) details
- See `phishing-incident.md` for alert + anecdote examples
- See `notebook-storyboards.md` for notebook development principles

## Summary

Incident extension follows a consistent pattern:
1. New evidence arrives (SCO or metadata)
2. Wrap in observed-data
3. Create sighting with appropriate extension
4. Derive event from sighting
5. Reassess impact if needed
6. Update incident

Each extension adds depth to the incident narrative. The graph preserves provenance: what evidence arrived, when, from what source, and how it changed our understanding.

**Remember**: Evidence accumulation is organic. Don't force all extensions into one notebook. Let the story drive the structure.
