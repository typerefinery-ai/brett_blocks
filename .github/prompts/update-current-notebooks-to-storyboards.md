# Prompt: Update Current Notebooks to Storyboards

## Purpose
This prompt guides AI assistants in updating the existing four notebooks (Step_0 through Step_3) to emphasize storytelling over code execution.

## Context
You are updating existing Jupyter notebooks that create STIX incident graphs. These notebooks currently work but focus too much on code mechanics. They need more narrative emphasis to serve as teaching tools.

## Reference Documents
Before starting, review:
- `.github/architecture/stix-graph-patterns.md` - Complete STIX graph pattern reference
- `.github/architecture/notebook-storyboards.md` - Comprehensive notebook development guide
- `.github/architecture/new_user.md` - Story for Step_0
- `.github/architecture/new_company.md` - Story for Step_1  
- `.github/architecture/phishing-incident.md` - Story for Step_2+3

## Target Notebooks
1. `Orchestration/Step_0_User_Setup.ipynb` (19 cells)
2. `Orchestration/Step_1_Company_Setup.ipynb` (18 cells)
3. `Orchestration/Step_2_Create_Incident_with_an_Alert.ipynb` (47 cells)
4. `Orchestration/Step_3_Get the Anecdote.ipynb` (24 cells)

## Update Principles

### 1. Add Story Context
**Before** (current):
```markdown
# Create User Account
```
```python
user_account = invoke_make_user_account_block(...)
```

**After** (updated):
```markdown
## Creating Your Identity: The Bootstrap Problem

Before we can investigate incidents, we need to exist in the system. But there's a circular dependency: identities need email addresses, and email addresses need user accounts. This is the **bootstrap problem**.

We solve it by building from the ground up (Level 0 → Level 2):
- **Level 0**: user-account (no embedded refs)
- **Level 1**: email-addr (no embedded refs)  
- **Level 2**: identity (refs both user-account and email-addr)

Let's create your analyst identity.
```
```python
# Create the foundation: user-account
user_account = invoke_make_user_account_block(
    user_id="your_username",
    account_login="you@company.com",
    display_name="Your Name"
)

print(f"✅ Created {user_account.type}: {user_account.id}")
print(f"   Level 0 foundation complete")
```

### 2. Explain Pattern Usage
After creating each object, explain which pattern it demonstrates:

```markdown
**Pattern Used**: Pattern 3.2 (Identity Sub-Pattern)

This pattern creates the Level 0-2 dependency chain that all identities need. We just built:
1. user-account (Level 0) - no dependencies
2. email-addr (Level 0) - no dependencies
3. identity (Level 2) - depends on both

This is reusable: every analyst, every employee, every system identity follows this pattern.
```

### 3. Show Before/After State
When objects reference others, show the dependency:

```markdown
## Creating the Incident Container

We've built all the evidence (Levels 0-5). Now we package it into an incident (Level 6).

**Current state:**
- ✅ 18 objects created across 6 levels
- ❌ No incident container yet
- ❌ Objects not linked together

**After this step:**
- ✅ Incident created with IncidentCoreExt
- ✅ All objects linked via `_refs` lists
- ✅ Complete graph ready for analysis
```

### 4. Use Visual Metaphors
Help readers visualize relationships:

```markdown
Think of the incident like a case file:
- **Cover page**: Incident object (name, type, dates)
- **Evidence section**: Sightings, observed-data, indicators
- **Timeline**: Events showing what happened when
- **Damage report**: Impacts showing what was affected
- **Action items**: Tasks showing response steps
- **Workflows**: Sequences organizing the work

The IncidentCoreExt `_refs` lists are the table of contents pointing to each section.
```

### 5. Add "Why This Matters" Sections
After major steps, explain significance:

```markdown
### Why This Matters: Incident Reconstitution

Later, you can query the graph:
- "Show me all phishing incidents from last month"
- "What tasks were created for incident X?"
- "Who reported this incident?"
- "What evidence led to this determination?"

The graph preserves the complete story. Every object, every relationship, every decision is preserved for reconstruction.
```

## Update Workflow

### For Each Notebook:

**Step 1: Add Enhanced Introduction**
Replace brief intro with:
- Story overview (what we're building)
- Characters (who's involved)
- Learning objectives (what patterns you'll see)
- Prerequisites (what must exist first)

**Step 2: Group Cells into Acts**
Add markdown headers creating narrative structure:
- Act 1: Environment Setup
- Act 2: Foundation Objects (Levels 0-1)
- Act 3: Container Objects (Level 2-3)
- Act 4: Response Objects (Level 4-5)
- Act 5: Incident Creation (Level 6)

**Step 3: Enhance Code Cells**
For each code cell:
- Add markdown BEFORE explaining what's about to happen
- Keep code clean (no changes unless fixing bugs)
- Add markdown AFTER explaining what was created
- Show object IDs and types in print statements
- Reference patterns from stix-graph-patterns.md

**Step 4: Add Verification Cells**
After major milestones, add verification:
```python
# Verify our incident structure
print("Incident Container Check:")
print(f"  Sightings: {len(incident.extensions['IncidentCoreExt']['sighting_refs'])}")
print(f"  Events: {len(incident.extensions['IncidentCoreExt']['event_refs'])}")
print(f"  Impacts: {len(incident.extensions['IncidentCoreExt']['impact_refs'])}")
print(f"  Tasks: {len(incident.extensions['IncidentCoreExt']['task_refs'])}")
print(f"  Sequences: {len(incident.extensions['IncidentCoreExt']['sequence_refs'])}")
print("\n✅ Incident graph complete!")
```

**Step 5: Add Summary Section**
End each notebook with:
- What we built (object count by type)
- What patterns we used
- Where objects are saved (context memory)
- What comes next (link to next notebook)
- Reflection questions for learners

## Specific Notebook Updates

### Step_0_User_Setup.ipynb

**Current focus**: Creating identities
**Story emphasis**: The bootstrap problem

**Key additions**:
- Explain why we need identities before incidents
- Show the circular dependency problem
- Demonstrate Pattern 3.2 four times (you + 3 team members)
- Explain /usr/ context memory location
- End with "Now we can create organizational context"

**New cells to add**:
- Cell after imports: "Understanding the Bootstrap Problem"
- Cell after your identity: "Pattern 3.2 in Action"
- Cell after team: "Why Four Identities?"
- Final cell: "What We Learned"

### Step_1_Company_Setup.ipynb

**Current focus**: Creating company/employee identities
**Story emphasis**: Organizational context for incidents

**Key additions**:
- Explain why incidents need organizational context
- Show Pattern 3.2 reuse (same pattern, different identities)
- Demonstrate IdentityContact extension usage
- Explain identity_class differences
- Show how these identities will appear in incidents

**New cells to add**:
- "Why Organizational Context Matters"
- "Pattern 3.2: Now With Extensions"
- "Identity Classes Explained"
- "Preview: These Identities in Incidents"

### Step_2_Create_Incident_with_an_Alert.ipynb

**Current focus**: Creating complete phishing incident
**Story emphasis**: From evidence to response

**Key additions**:
- Open with the story: "It's 3:47 AM. An alert fires..."
- Show dependency hierarchy as you build (Levels 0→6)
- Explain each pattern as it's used (Patterns 3.1, 3.3-3.8)
- Show task dependencies visually
- Demonstrate sequence workflows
- End with incident reconstitution preview

**New cells to add**:
- "The Story So Far" (after intro)
- "Understanding Sighting Extensions" (at sighting-alert)
- "Why Events Matter" (at event creation)
- "Task Dependencies Explained" (at task creation)
- "Packaging Everything: The Incident Container"

### Step_3_Get the Anecdote.ipynb

**Current focus**: Adding user report to incident
**Story emphasis**: Evidence accumulation

**Key additions**:
- Open with timeline: "Five hours later..."
- Explain anecdote vs alert (different evidence sources)
- Show Pattern 3.9 (Anecdote Provenance)
- Demonstrate impact supersession (Pattern 3.10)
- Show incident update process (append to _refs)
- Compare before/after incident structure

**New cells to add**:
- "New Evidence Arrives" (intro)
- "Pattern 3.9: Anecdote Provenance"
- "Comparing Alert vs Anecdote Sightings"
- "Impact Supersession: Lowering Severity"
- "How the Incident Grew" (before/after comparison)

## Quality Checklist

After updating each notebook, verify:

### Story Quality
- [ ] Narrative is engaging (not just procedural)
- [ ] Each section has clear purpose
- [ ] Progression feels natural (not mechanical)
- [ ] Patterns are explained, not just referenced
- [ ] Visual metaphors aid understanding

### Educational Quality
- [ ] Explains WHY, not just WHAT
- [ ] Shows design decisions
- [ ] Highlights pattern reuse
- [ ] Includes common mistakes to avoid
- [ ] References stix-graph-patterns.md

### Technical Quality
- [ ] Code still works (no breaking changes)
- [ ] Print statements show progress
- [ ] Verification cells confirm correctness
- [ ] Context memory structure explained
- [ ] Dependencies clearly shown

### Notebook Flow
- [ ] Clear acts/chapters with markdown headers
- [ ] Markdown before code explains next step
- [ ] Code executes the plan
- [ ] Markdown after code explains result
- [ ] Summary ties everything together

## Example Transform

**Before** (terse):
```markdown
# Create Sighting
```
```python
sighting = invoke_make_sighting_block(
    sighting_of_ref=indicator.id,
    observed_data_refs=[observed_data.id],
    extensions={"sighting-alert": {"alert_type": "siem"}}
)
```

**After** (storytelling):
```markdown
## The SIEM Alert: How We Detected This

At 3:47 AM, your SIEM fired an alert: "Phishing pattern detected." This automated detection is our first piece of evidence.

**Pattern 3.3**: Observed-Data/Sighting/Evidence
- We have observed-data (the email + URL)
- We have an indicator (the phishing pattern)
- The sighting connects them: "This indicator was seen in this observed-data"

The `sighting-alert` extension adds context:
- **alert_type**: "siem" (vs "edr", "ids", etc.)
- **severity**: "high"
- **source_system**: Which SIEM fired this alert

This is evidence with provenance. Later, we can ask: "What alerted us to this incident?"
```
```python
# Create the SIEM alert sighting
sighting = invoke_make_sighting_block(
    sighting_of_ref=indicator.id,  # What we detected (the phishing pattern)
    observed_data_refs=[observed_data.id],  # Where we saw it (the email)
    extensions={
        "sighting-alert": {
            "alert_type": "siem",
            "severity": "high",
            "source_system": "splunk-prod-01",
            "alert_id": "ALERT-2024-0147"
        }
    }
)

print(f"✅ Created {sighting.type}: {sighting.id}")
print(f"   Evidence type: sighting-alert")
print(f"   References: indicator + observed-data")
print(f"   This is Level 3 in our dependency hierarchy")
```
```markdown
**What we just built:**
- A sighting object linking indicator to observed-data
- Evidence that an automated system detected this
- Provenance: which system, what type, when

**Why it matters:**
- Different evidence sources (alert vs anecdote vs hunt) provide different confidence levels
- Automated alerts can be false positives (need human verification)
- The graph preserves: was this detected by machine or reported by human?

**Next**: We'll derive an event from this sighting to add it to the incident timeline.
```

## Common Pitfalls to Avoid

### 1. Over-explaining Code
❌ Don't explain Python syntax
✅ Do explain STIX concepts and patterns

### 2. Under-explaining Patterns
❌ Don't just say "using Pattern 3.3"
✅ Do explain what Pattern 3.3 is and why it applies here

### 3. Breaking Working Code
❌ Don't refactor code that works
✅ Do add markdown around working code

### 4. Losing Technical Accuracy
❌ Don't oversimplify to the point of incorrectness
✅ Do use metaphors that maintain technical accuracy

### 5. Forgetting the Audience
❌ Don't assume expert knowledge
✅ Do write for analysts learning STIX

## Output Format

For each updated notebook, provide:

1. **Summary of Changes**
   - Number of cells added
   - Number of cells modified (markdown only)
   - Key story improvements

2. **Pattern Coverage**
   - Which patterns are now explicitly explained
   - Where pattern references were added

3. **Educational Enhancements**
   - New sections added
   - Visual metaphors used
   - Verification cells added

4. **Testing Notes**
   - Confirm all cells still execute
   - Verify context memory structure unchanged
   - Check output matches expectations

## References

- `notebook-storyboards.md` - Complete development guide
- `stix-graph-patterns.md` - Pattern reference
- Story files (new_user.md, new_company.md, phishing-incident.md) - Narrative examples

## Success Criteria

Updated notebooks should:
1. Teach STIX concepts through stories
2. Make patterns visible and understandable
3. Maintain technical correctness
4. Execute without errors
5. Engage readers with narrative flow

**Remember**: Code executes; stories teach. Both are essential.
