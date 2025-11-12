# Notebook Storyboards - OS-Triage STIX Incident Management

## Document Purpose

This document describes the stories being told in each of the current OS-Triage notebooks, identifying the specific graph patterns used from stix-graph-patterns.md and explaining how each notebook fits into the overall incident management workflow.

---

## Notebook 1: Step_0_User_Setup.ipynb

### Story: Establishing Your Personal Digital Identity

**Narrative:**  
You are an incident responder joining the OS-Triage system for the first time. Before you can investigate incidents or manage security events, the system needs to know who you are and who your team members are. This notebook tells the story of creating your digital identity footprint in the STIX ecosystem.

### Graph Patterns Used

**Primary Pattern:** Pattern 6.1 - User Identity Setup

**Detailed Object Creation Flow:**
1. **Level 0 - Foundation:** Create user-account SCO (no dependencies)
2. **Level 1 - Email Connection:** Create email-addr SCO with `belongs_to_ref`→user-account
3. **Level 2 - Full Identity:** Create identity SDO with extension-definition--66e2492a-bbd3-4be6-88f5-cc91a017a498 (IdentityContact)
   - Add EmailContact sub-object with `email_address_ref`→email-addr
   - Add SocialMediaContact sub-object with `user_account_ref`→user-account
   - Add ContactNumber sub-objects for phone numbers
   - Set `created_by_ref`→identity (self-reference)

**Objects Created Per Person:**
- 1 x user-account (foundation)
- 1+ x email-addr (one per email address)
- 1 x identity (complete person profile)

**Total Objects Created:**
- Personal identity (you): ~3 objects
- Team members: ~3 objects per team member
- Approximate total: 10-20 objects depending on team size

### Story Elements

**Beginning (Cells 1-3):** Environment setup - importing STIX libraries and OS Threat extensions  
**Middle (Cells 4-17):** Creating your personal identity objects step by step  
**End (Cells 18-19):** Saving to `/usr/` context memory for future use

### Why This Story Matters

Every STIX SDO requires a `created_by_ref` field pointing to an identity object. By establishing your identity first, you create the foundation for all future work. Your identity will be referenced in:
- Every incident you create (`created_by_ref`)
- Every task you own (`owner` field)
- Every event you document (`created_by_ref`)
- All sightings and observations you record (`created_by_ref`)

### Context Storage

**Location:** `context_mem/usr/`  
**Files:**
- `cache_me.json` - Your personal identity objects
- `cache_team.json` - Team member identity objects  
- `edges.json` - User-level relationships

**Graph Pattern Application:**  
All objects stored in incident.other_object_refs when used in incidents.

---

## Notebook 2: Step_1_Company_Setup.ipynb

### Story: Mapping the Digital Footprint of Your Organization

**Narrative:**  
Now that you exist in the system, you need to define the organization you're protecting. This notebook tells the story of creating a fictional company with its IT infrastructure, systems, and assets. You're building the "playing field" where security incidents will occur.

### Graph Patterns Used

**Primary Pattern:** Pattern 6.1 - User Identity Setup (adapted for organizations/systems)

**Detailed Object Creation Flow:**
1. **Company Identity:** Create identity SDO for the organization
   - `identity_class` = "organization"
   - `sectors` = industry sectors
   - Add IdentityContact extension for company contact information
   - `created_by_ref`→your personal identity from Step 0

2. **IT System Identities:** Create identity SDOs for each IT system/resource
   - Email servers, web servers, databases, etc.
   - `identity_class` = "system"
   - `created_by_ref`→your personal identity

3. **User Accounts for Company:** Create user-account SCOs for company employees
   - Link to company identity via context
   - `created_by_ref`→your personal identity

4. **Email Infrastructure:** Create email-addr SCOs for company email addresses
   - `belongs_to_ref`→user-account of employee
   - Link to company domain

**Objects Created:**
- 1 x company identity
- Multiple x IT system identities (servers, databases, etc.)
- Multiple x user-account (company employees)
- Multiple x email-addr (company email addresses)
- Approximate total: 15-30 objects

### Story Elements

**Beginning (Cells 1-3):** Environment setup and load personal identity from Step 0  
**Middle (Cells 4-16):** Creating company organizational structure and IT assets  
**End (Cells 17-18):** Saving to company context memory

### Why This Story Matters

Incidents don't happen in a vacuum - they happen to real organizations with real assets. By defining the company's digital footprint, you create:
- **Targets for incidents:** The systems and users that get compromised
- **Impact recipients:** The identities affected when incidents occur (via incident.impacts→identity)
- **Location context:** Where sightings occur (via sighting.where_sighted_refs)
- **Asset inventory:** What needs to be protected

### Context Storage

**Location:** `context_mem/{company_name}/`  
**Files:**
- `cache_company.json` - Company identity and IT system objects
- `cache_users.json` - Company user account and email objects
- `edges.json` - Company-level relationships

**Graph Pattern Application:**  
All objects stored in incident.other_object_refs when used in incidents. Company identity may be referenced via incident→impacts→identity or incident→targets→identity relationships.

---

## Notebook 3: Step_2_Create_Incident_with_an_Alert.ipynb

### Story: The First Warning - When the SIEM Sounds the Alarm

**Narrative:**  
A phishing email has slipped past the filters and landed in an employee's inbox. The SIEM system detects suspicious URL patterns and raises an alert. This notebook tells the story of how that first piece of evidence - an automated alert - becomes a formal security incident that requires investigation and response.

### Graph Patterns Used

**Multiple Integrated Patterns:**

#### Pattern 6.2: Evidence Collection (Sighting-Based)  
Creating the alert evidence:

1. **SCO Creation (Level 0-3):**
   - Create url SCO (suspicious link in phishing email)
   - Create email-message SCO with references to email-addr objects
   - Create email-addr SCOs (sender, recipients)
   - `created_by_ref`→your identity

2. **Observed Data (Level 3):**
   - Create observed-data SDO
   - `object_refs`→[url, email-message, email-addr objects]
   - `first_observed`, `last_observed` timestamps
   - `created_by_ref`→your identity

3. **Indicator Creation (Level 3):**
   - Create indicator SDO for phishing pattern
   - `pattern` = STIX pattern matching the URL/email characteristics
   - `pattern_type` = "stix"
   - `indicator_types` = ["malicious-activity", "phishing"]
   - `created_by_ref`→your identity

4. **Sighting with Alert Extension (Level 4):**
   - Create sighting SRO
   - `sighting_of_ref`→indicator
   - `observed_data_refs`→[observed-data]
   - `where_sighted_refs`→[company identity or location]
   - Extension: sighting-alert
     - `name` = "Phishing URL Detected"
     - `product` = "SIEM System"
     - `source` = "Email Gateway"
     - `log` = alert log reference
   - `created_by_ref`→your identity

#### Pattern 6.3: Event Creation from Evidence  
Converting the alert into an event:

1. **Event Creation (Level 4):**
   - Create event SDO
   - `sighting_refs`→[sighting with alert]
   - `event_types` = ["phishing"]
   - `status` = "new" or "in-progress"
   - `start_time`, `end_time` timestamps
   - Optional: `changed_objects` with StateChangeObject sub-objects
   - `created_by_ref`→your identity

2. **SRO Relationships (if applicable):**
   - event→led-to→event (if this event triggers others)
   - event→impacts→infrastructure (if systems affected)
   - event→located-at→location (if location known)

#### Pattern 6.4: Task Creation with Ownership  
Creating response tasks:

1. **Task Creation (Level 4):**
   - Create task SDO for investigation
   - `name` = "Investigate Phishing Alert"
   - `task_types` = ["investigate"]
   - `owner`→identity (analyst assigned)
   - `priority` = high
   - `status` = "pending" or "in-progress"
   - `created_by_ref`→your identity

2. **SRO Relationships:**
   - task→detects→event (this task investigates the event)
   - identity→assigned→task (analyst assigned to task)

#### Pattern 6.6: Impact Tracking  
Recording the incident's impact:

1. **Impact Creation (Level 3):**
   - Create impact SDO
   - `impact_category` = "availability" or "confidentiality"
   - `impacted_refs`→[email system identity, affected user identities]
   - Extension: availability, confidentiality, or other impact type
   - `start_time`, potential `end_time`
   - `recoverability` = "regular" or "supplemented"
   - `created_by_ref`→your identity

#### Pattern 6.7: Complete Incident Assembly  
Bringing it all together:

1. **Incident Creation (Level 5):**
   - Create incident SDO
   - Extension: extension-definition--ef765651-680c-498d-9894-99799f2fa126 (Incident Core)
   - Populate extension fields:
     - `event_refs`→[event]
     - `task_refs`→[investigation task]
     - `impact_refs`→[impact]
     - `other_object_refs`→[sighting, observed-data, indicator, identities, SCOs]
   - Set incident properties:
     - `name` = "Phishing Incident - Suspicious Email Campaign"
     - `incident_types` = ["phishing"]
     - `determination` = "suspected" or "confirmed"
     - `investigation_status` = "new"
   - `created_by_ref`→your identity

2. **SRO Relationships:**
   - incident→impacts→identity (company or user identity)
   - incident→targets→identity (targeted users)
   - incident→located-at→location (if applicable)

### Objects Created

**Total Object Count:** ~25-40 objects

**Breakdown:**
- 3-5 SCOs (url, email-message, email-addr objects)
- 1 observed-data
- 1 indicator
- 1 sighting (with sighting-alert extension)
- 1 event
- 1-2 tasks
- 1 impact
- 1 incident (container for all)
- Multiple identities (reused from previous notebooks)
- 0-3 relationship SROs

### Story Elements

**Beginning (Cells 1-3):** Load environment and retrieve saved context  
**Rising Action (Cells 4-25):** SIEM detects phishing URL, create SCOs and observed-data  
**Climax (Cells 26-35):** Create sighting with alert evidence, make indicator  
**Falling Action (Cells 36-42):** Create event and investigation tasks  
**Resolution (Cells 43-47):** Assemble complete incident with all components

### Why This Story Matters

This notebook demonstrates the complete lifecycle of incident creation from automated detection:

1. **Evidence First:** Start with concrete observations (SCOs in observed-data)
2. **Context Added:** Wrap observations in sighting with provenance (SIEM alert)
3. **Analysis Applied:** Create indicator to formalize the threat pattern
4. **Event Declared:** Acknowledge something significant happened
5. **Response Initiated:** Create tasks for human investigation
6. **Impact Assessed:** Document consequences
7. **Incident Formalized:** Package everything into a formal incident case

This pattern is foundational for all automated detection systems (SIEM, IDS/IPS, EDR, email gateways, etc.).

### Context Storage

**Updated Location:** `context_mem/{company_name}/`  
**Updated Files:**
- `cache_incident.json` - Incident object  
- `cache_events.json` - Event objects
- `cache_tasks.json` - Task objects
- `cache_impacts.json` - Impact objects
- `cache_sightings.json` - Sighting objects with alert extension
- `cache_observations.json` - Observed-data and SCO objects
- `cache_indicators.json` - Indicator objects
- `edges.json` - All SRO relationships

---

## Notebook 4: Step_3_Get the Anecdote.ipynb

### Story: The Human Witness - When an Employee Reports the Attack

**Narrative:**  
After the automated alert in Step 2, an employee (the actual target of the phishing email) reports directly to IT that they received a suspicious email. This human testimony - an anecdote - provides additional context and confirmation that the automated alert was correct. This notebook tells the story of capturing human-reported evidence and adding it to the existing incident.

### Graph Patterns Used

**Primary Pattern:** Pattern 6.2 - Evidence Collection (Sighting-Based) with sighting-anecdote extension

**Detailed Object Creation Flow:**

1. **Anecdote SCO Creation (Level 1):**
   - Create anecdote SCO
   - `value` = "I received a suspicious email claiming to be from IT asking me to reset my password"
   - `provided_by_ref`→identity (the employee who reported it)
   - `report_date` = timestamp of report
   - Extension: extension-definition--23676abf-481e-4fee-ac8c-e3d0947287a4 (Anecdote New SCO)

2. **Observed Data Update (Level 3):**
   - Create new observed-data SDO OR update existing
   - `object_refs`→[anecdote, possibly other SCOs like email-addr, user-account of reporter]
   - `first_observed`, `last_observed` = when employee noticed/reported
   - `created_by_ref`→your identity

3. **Sighting with Anecdote Extension (Level 4):**
   - Create sighting SRO
   - `sighting_of_ref`→indicator (same indicator from Step 2, or event)
   - `observed_data_refs`→[observed-data containing anecdote]
   - `where_sighted_refs`→[employee identity, company identity]
   - Extension: sighting-anecdote
     - `person_name` = employee name
     - `person_context` = employee's role/position
     - `report_submission` = how they reported (email, phone, portal)
   - `created_by_ref`→your identity

4. **Update Existing Event (Level 4):**
   - Retrieve event from Step 2
   - Update `sighting_refs` to include new sighting
   - Update `modified` timestamp

5. **Create Additional Task (Level 4):**
   - Create task SDO
   - `name` = "Interview employee about phishing attempt"
   - `task_types` = ["investigate", "interview"]
   - `owner`→identity (analyst)
   - `created_by_ref`→your identity
   - SRO: task→detects→event

6. **Update Incident (Level 5):**
   - Retrieve incident from Step 2
   - Update `other_object_refs` to include new sighting, observed-data, anecdote
   - Update `task_refs` to include interview task
   - Update `determination` = "confirmed" (human confirmation adds credibility)
   - Update `modified` timestamp

### Objects Created

**New Objects:** ~5-8 objects

**Breakdown:**
- 1 anecdote SCO
- 1 observed-data (new or updated)
- 1 sighting (with sighting-anecdote extension)
- 1 task (interview/follow-up)
- Possibly 1-2 relationship SROs
- Updates to existing event and incident

### Story Elements

**Beginning (Cells 1-3):** Load environment and retrieve incident from Step 2  
**Middle (Cells 4-15):** Employee reports phishing email, create anecdote and sighting  
**End (Cells 16-23):** Update incident with new evidence, create follow-up tasks

### Why This Story Matters

This notebook demonstrates critical incident management concepts:

**1. Evidence Layering:**  
Incidents rarely have just one source of evidence. This shows how to combine:
- Automated detection (SIEM alert from Step 2)
- Human reporting (anecdote)
- Future additions (could add hunt, enrichment, framework, external evidence)

**2. Evidence Provenance:**  
Different sighting extensions capture different evidence sources:
- `sighting-alert` = automated system detected it
- `sighting-anecdote` = human reported it
- Each has unique metadata fields appropriate to source

**3. Incident Evolution:**  
Incidents grow over time as new evidence arrives. This shows:
- How to update existing incidents without recreating from scratch
- Adding new sightings to events via `sighting_refs`
- Adding new objects to incident via `other_object_refs`
- Changing determination from "suspected" to "confirmed"

**4. Human Element:**  
Cybersecurity isn't just automated tools - humans are critical:
- They report observations machines miss
- They provide context and interpretation
- They need to be tracked via identity objects
- Their testimony has evidentiary value

### Context Storage

**Updated Location:** `context_mem/{company_name}/`  
**Updated Files:**
- `cache_incident.json` - Updated incident object
- `cache_events.json` - Updated event objects
- `cache_tasks.json` - Added interview task
- `cache_sightings.json` - Added anecdote sighting
- `cache_observations.json` - Added observed-data with anecdote
- `cache_scos.json` - Added anecdote SCO
- `edges.json` - Updated relationships

---

## Story Arc Across All Notebooks

### The Complete Phishing Incident Narrative

**Act 1 (Step 0):** Establishing Identity  
You join the security team. The system learns who you are and who your teammates are. Foundation is laid.

**Act 2 (Step 1):** Defining the Territory  
You map out the organization you're protecting - its systems, users, and digital assets. The "playing field" is established.

**Act 3 (Step 2):** The Attack Begins  
A phishing email arrives. The SIEM detects it. You create a formal incident with all the technical evidence, analysis, response tasks, and impact assessment. The investigation starts.

**Act 4 (Step 3):** Human Confirmation  
The targeted employee reports the attack. You add their testimony to the incident. The case strengthens. Multiple evidence sources corroborate the threat.

**Act 5 (Future):** Continued Development  
More evidence could be added:
- Hunt findings (sighting-hunt)
- Threat intelligence enrichment (sighting-enrichment)
- Framework mapping (sighting-framework)
- External feeds (sighting-external)
- Additional context (sighting-context)
- Exclusion lists (sighting-exclusion)

### Graph Pattern Progression

1. **Foundation** (Steps 0-1): Pattern 6.1 (User Identity Setup)
2. **Evidence** (Steps 2-3): Pattern 6.2 (Evidence Collection)
3. **Analysis** (Step 2): Pattern 6.3 (Event Creation)
4. **Response** (Step 2): Pattern 6.4 (Task Creation)
5. **Consequences** (Step 2): Pattern 6.6 (Impact Tracking)
6. **Orchestration** (Step 2): Pattern 6.7 (Incident Assembly)
7. **Evolution** (Step 3): Pattern 6.2 repeated with different evidence type

### Key STIX Principles Demonstrated

1. **Hierarchy Matters:** Create objects bottom-up (SCOs → observed-data → sighting → event → incident)
2. **Provenance is Critical:** Every object tracks who created it (`created_by_ref`)
3. **Evidence Has Context:** Sightings connect observations (what) with locations (where) and indicators (why)
4. **Incidents Evolve:** Use `other_object_refs` to add new evidence over time
5. **Relationships Enrich:** SRO relationships add semantic meaning beyond embedded references
6. **Extensions Enable Specialization:** Standard STIX + US DoD extensions = powerful incident management

---

## How to Use These Storyboards

**For Notebook Authors:**
- Reference these stories when writing new cells
- Ensure each cell advances the narrative
- Include markdown explanations of "why" not just "how"
- Connect code to graph patterns explicitly

**For Notebook Users:**
- Read the story first to understand the purpose
- Follow the graph pattern flow to see dependencies
- Understand which pattern to use for your scenario
- Recognize where to customize for your organization

**For System Developers:**
- Use these patterns as templates for new scenarios
- Maintain consistency across incident types
- Document deviations from patterns with rationale
- Extend patterns for new evidence types or workflows
