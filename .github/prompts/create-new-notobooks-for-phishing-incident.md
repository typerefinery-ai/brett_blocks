# Prompt: Create New Notebooks for Phishing Incident Extension

## Purpose
This prompt guides AI assistants in creating new notebooks (Step_4 through Step_9) that extend the phishing incident with additional evidence types.

## Context
You are creating new Jupyter notebooks that extend the existing phishing incident from Step_2/Step_3. Each notebook adds a different type of evidence using a different sighting extension, demonstrating how incidents evolve as information accumulates.

## Reference Documents
Before starting, review:
- `.github/architecture/stix-graph-patterns.md` - Complete STIX graph pattern reference
- `.github/architecture/incident-extension-storyboard.md` - Detailed instructions for each extension type
- `.github/architecture/phishing-incident.md` - The base incident story (Step_2+3)
- `.github/architecture/notebook-storyboards.md` - Notebook development principles

## Target Notebooks to Create

### Extension Sequence
1. **Step_4_Add_Threat_Intel.ipynb** - Threat intelligence context (sighting-context)
2. **Step_5_Add_Enrichment.ipynb** - URL reputation data (sighting-enrichment)
3. **Step_6_Add_Hunt_Findings.ipynb** - Proactive hunt results (sighting-hunt)
4. **Step_7_Add_Framework_Mapping.ipynb** - MITRE ATT&CK mapping (sighting-framework)
5. **Step_8_Add_External_Analysis.ipynb** - Vendor forensics (sighting-external)
6. **Step_9_Mark_False_Positive.ipynb** - Exclusion of false positive (sighting-exclusion)

## Universal Notebook Structure

Each extension notebook follows this pattern:

### Cells 1-7: Setup
**Cell 1**: Story introduction (markdown)
```markdown
# Step_X: [Extension Type]

## The Story So Far

[Recap previous steps]

## New Evidence Arrives

[Timeline: when this evidence arrives]
[Source: who/what provides this evidence]
[Impact: how this changes our understanding]
```

**Cells 2-7**: Environment setup
```python
# Standard imports and utilities
import sys
sys.path.append('../')
from Block_Families.General.Import_Bundle.import_bundle import *
# ... other imports
```

### Cells 8-9: Load Existing Incident
**Cell 8**: Explanation (markdown)
```markdown
## Retrieving the Existing Incident

We're extending an incident created in Step_2, updated in Step_3 [and potentially Step_4-X].
The incident is stored in context memory. We'll load it, add new evidence, and save it back.
```

**Cell 9**: Load code
```python
# Load incident from context
incident_id = "incident--[uuid]"  # From previous steps
incident = load_from_context(incident_id)

# Verify current state
print(f"Loaded: {incident.name}")
print(f"Current sightings: {len(incident.extensions['IncidentCoreExt']['sighting_refs'])}")
print(f"Current events: {len(incident.extensions['IncidentCoreExt']['event_refs'])}")
```

### Cells 10-13: Create Evidence
**Cell 10**: Evidence explanation (markdown)
```markdown
## [Evidence Type]

[Explain what this evidence is]
[Show what SCO(s) represent it]
[Explain why this evidence type is valuable]
```

**Cells 11-13**: Create SCO(s) and observed-data
```python
# Create evidence SCO (if needed)
evidence_obj = invoke_make_[type]_block(...)

# Create observed-data wrapping evidence
observed_data = invoke_make_observed_data_block(
    object_refs=[evidence_obj.id]
)
```

### Cells 14-16: Create Sighting
**Cell 14**: Sighting explanation (markdown)
```markdown
## Creating the Sighting: [Extension Type]

**Pattern 3.3**: Observed-Data/Sighting/Evidence

The sighting links our new evidence to the original indicator:
- **sighting_of_ref**: The phishing indicator from Step_2
- **observed_data_refs**: Our new evidence
- **Extension**: sighting-[type] with specific properties
```

**Cells 15-16**: Create sighting
```python
sighting = invoke_make_sighting_block(
    sighting_of_ref=indicator.id,  # Original indicator
    observed_data_refs=[observed_data.id],
    extensions={
        "sighting-[type]": {
            # Extension-specific properties
        }
    }
)
```

### Cells 17-19: Create Event
**Cell 17**: Event explanation (markdown)
```markdown
## Timeline Update: [Event Type]

**Pattern 3.4**: Event Derivation from Sightings

This sighting creates a new event in our incident timeline.
```

**Cells 18-19**: Create event
```python
event = invoke_make_event_block(
    event_types=["[appropriate-type]"],
    sighting_refs=[sighting.id],
    changed_objects=[observed_data.id],
    description="[What happened]"
)
```

### Cells 20-22: Impact Assessment (if applicable)
**Cell 20**: Impact explanation (markdown)
```markdown
## Reassessing Impact

[Explain how new evidence changes impact]
[Does it escalate or de-escalate?]
[Pattern 3.10: Impact Supersession Chain]
```

**Cells 21-22**: Create impact (if needed)
```python
impact = invoke_make_impact_block(
    impact_category="[category]",
    criticality=[score],
    description="[Updated assessment]",
    supersedes_refs=[previous_impact.id]  # If superseding
)
```

### Cells 23-25: Update Incident
**Cell 23**: Update explanation (markdown)
```markdown
## Updating the Incident

We'll add our new objects to the incident's reference lists.

**Before**: X sightings, Y events, Z impacts
**After**: X+1 sightings, Y+1 events, Z+? impacts
```

**Cells 24-25**: Update and save
```python
# Add new references
incident.extensions["IncidentCoreExt"]["sighting_refs"].append(sighting.id)
incident.extensions["IncidentCoreExt"]["event_refs"].append(event.id)
if impact:
    incident.extensions["IncidentCoreExt"]["impact_refs"].append(impact.id)
incident.extensions["IncidentCoreExt"]["other_object_refs"].append(observed_data.id)

# Save updated incident
save_to_context(incident)

print("✅ Incident updated successfully")
```

### Cell 26: Summary
```markdown
## What We Built

**New Objects Created:**
- 1× [evidence SCO type]
- 1× observed-data
- 1× sighting (sighting-[type])
- 1× event
- [0-1]× impact

**Incident Evolution:**
- Total sightings: X → X+1
- Total events: Y → Y+1
- Evidence sources: [list of sighting types]

**Pattern Demonstrated:**
- Pattern 3.3 (Observed-Data/Sighting/Evidence)
- Pattern 3.4 (Event Derivation)
- [Pattern 3.10 if impact supersession]

**Next Steps:**
[Point to next extension notebook OR final summary]
```

## Specific Notebook Instructions

### Step_4_Add_Threat_Intel.ipynb

**Story**: 12 hours after initial alert, threat intel feed identifies evil.com as APT28 infrastructure.

**SCO to create**: artifact (threat intelligence report)

**Sighting extension**:
```python
"sighting-context": {
    "context_type": "threat-intelligence",
    "source": "ThreatFeed-Pro",
    "confidence": 85,
    "description": "Domain associated with APT28 phishing campaigns"
}
```

**Event type**: "threat-intel-received"

**Impact**: No change (confirms initial assessment)

**Story emphasis**: External context validates our detection

### Step_5_Add_Enrichment.ipynb

**Story**: URL reputation check completes - evil.com scores 5/100 (malicious).

**SCO to create**: None (enriches existing URL from Step_2)

**Sighting extension**:
```python
"sighting-enrichment": {
    "enrichment_type": "reputation",
    "source_system": "VirusTotal",
    "reputation_score": 5,
    "classification": "malicious",
    "categories": ["phishing", "c2-infrastructure"]
}
```

**Event type**: "enrichment-completed"

**Impact**: No change (confirms malicious nature)

**Story emphasis**: Reputation data confirms threat classification

### Step_6_Add_Hunt_Findings.ipynb

**Story**: Proactive hunt finds 15 additional phishing emails from same attacker.

**SCOs to create**: 15× email-message (discovered emails)

**Sighting extension**:
```python
"sighting-hunt": {
    "hunt_type": "email-search",
    "query": "from:attacker@evil.com",
    "results_count": 15,
    "description": "Proactive hunt found 15 related phishing emails"
}
```

**Event type**: "hunt-completed"

**Impact**: ESCALATE (criticality 30 → 90) - more victims than initially thought

**Additional objects**: 
- New tasks (notify all 15 victims)
- Impact supersession showing escalation

**Story emphasis**: Hunt reveals campaign scope

### Step_7_Add_Framework_Mapping.ipynb

**Story**: Analyst maps technique to MITRE ATT&CK T1566.002 (Spearphishing Link).

**SCO to create**: None (mapping is metadata)

**Sighting extension**:
```python
"sighting-framework": {
    "framework_name": "MITRE ATT&CK",
    "framework_version": "14.1",
    "technique_id": "T1566.002",
    "technique_name": "Phishing: Spearphishing Link",
    "tactic": "Initial Access"
}
```

**Event type**: "framework-mapped"

**Impact**: No change (analytical classification)

**Story emphasis**: Framework mapping enables cross-incident analysis

### Step_8_Add_External_Analysis.ipynb

**Story**: Third-party vendor completes email header analysis, provides forensic report.

**SCO to create**: artifact (vendor PDF report)

**Sighting extension**:
```python
"sighting-external": {
    "source_organization": "CyberForensics LLC",
    "analysis_type": "email-header-analysis",
    "confidence": 95,
    "findings": "Headers confirm spoofed sender, originated from known phishing infrastructure"
}
```

**Event type**: "external-analysis-received"

**Impact**: No change (independent verification)

**Story emphasis**: External validation increases confidence

### Step_9_Mark_False_Positive.ipynb

**Story**: One of the 15 hunt findings determined to be false positive - legitimate IT email.

**SCO to create**: None (marks existing email-message from Step_6)

**Sighting extension**:
```python
"sighting-exclusion": {
    "exclusion_reason": "false-positive",
    "explanation": "Legitimate IT department email with similar URL pattern",
    "excluded_by_ref": analyst_identity.id,
    "exclusion_timestamp": "2024-01-16T10:00:00Z"
}
```

**Event type**: "false-positive-identified"

**Impact**: DE-ESCALATE (criticality 90 → 85) - 14 confirmed victims, not 15

**Story emphasis**: Exclusions refine accuracy

## Story Continuity

Maintain narrative thread across notebooks:

**Step_2**: "3:47 AM - Alert fires"
**Step_3**: "8:15 AM - CEO reports (5 hours later)"
**Step_4**: "3:00 PM - Threat intel arrives (12 hours later)"
**Step_5**: "5:00 PM - Reputation check completes (14 hours later)"
**Step_6**: "Next day 9:00 AM - Hunt findings (24 hours later)"
**Step_7**: "Same day 11:00 AM - Framework mapping (26 hours later)"
**Step_8**: "Day 3 - Vendor report arrives (3 days later)"
**Step_9**: "Day 3 - False positive identified (3 days later)"

Each notebook's intro should reference timeline position.

## Code Reusability

### Extract Common Patterns

Create utility function for incident update:
```python
def update_incident_with_evidence(incident, sighting, event, impact=None, observed_data=None):
    """Add new evidence to incident."""
    incident.extensions["IncidentCoreExt"]["sighting_refs"].append(sighting.id)
    incident.extensions["IncidentCoreExt"]["event_refs"].append(event.id)
    if impact:
        incident.extensions["IncidentCoreExt"]["impact_refs"].append(impact.id)
    if observed_data:
        incident.extensions["IncidentCoreExt"]["other_object_refs"].append(observed_data.id)
    return incident
```

### Load Previous Objects

For continuity, load objects from previous steps:
```python
# From Step_2
indicator = load_from_context("indicator--[uuid]")
url_obj = load_from_context("url--[uuid]")

# From Step_3
impact_updated = load_from_context("impact--[uuid]")  # For supersession

# From Step_6 (for Step_9)
hunt_emails = [load_from_context(email_id) for email_id in hunt_email_ids]
```

## Quality Checklist

For each new notebook:

### Story Quality
- [ ] Clear timeline placement ("X hours/days after initial alert")
- [ ] Explains what new evidence arrived and from what source
- [ ] Shows how evidence changes understanding
- [ ] Maintains continuity with previous notebooks

### Technical Quality
- [ ] Loads existing incident correctly
- [ ] Creates appropriate SCO(s) for evidence type
- [ ] Uses correct sighting extension
- [ ] Creates event with appropriate type
- [ ] Updates incident correctly
- [ ] Saves to context memory

### Educational Quality
- [ ] Explains the sighting extension type
- [ ] Shows pattern usage (Patterns 3.3, 3.4, 3.10)
- [ ] Demonstrates evidence accumulation
- [ ] Highlights before/after incident state

### Code Quality
- [ ] No hard-coded UUIDs (load from context)
- [ ] Print statements show progress
- [ ] Verification cells confirm correctness
- [ ] Error handling for missing objects

## Testing

After creating all 6 notebooks, test the sequence:

1. Run Step_2 (create incident)
2. Run Step_3 (add anecdote)
3. Run Step_4 (add threat intel)
4. Run Step_5 (add enrichment)
5. Run Step_6 (add hunt findings)
6. Run Step_7 (add framework mapping)
7. Run Step_8 (add external analysis)
8. Run Step_9 (mark false positive)

**Final incident should have**:
- 8 sightings (alert, anecdote, context, enrichment, hunt, framework, external, exclusion)
- 8 events (one per sighting)
- 4 impacts (initial, reduced, escalated, corrected)
- Original tasks + new hunt tasks
- All evidence preserved

## References

- `incident-extension-storyboard.md` - Detailed instructions for each extension
- `stix-graph-patterns.md` - Pattern reference
- `phishing-incident.md` - Base incident story

## Success Criteria

Extension notebooks should:
1. Follow consistent structure
2. Tell coherent story with timeline
3. Demonstrate specific sighting extension
4. Show incident evolution clearly
5. Maintain technical correctness
6. Reference base incident consistently

**Remember**: Each notebook adds one piece to the puzzle. Together they show how incidents evolve from initial detection to comprehensive understanding.
