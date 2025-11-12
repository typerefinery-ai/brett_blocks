# Incident Extension Storyboard - Expanding the Phishing Investigation

## Document Purpose

This storyboard describes the story for extending the existing phishing incident created in Step_2 and Step_3 notebooks. It demonstrates how to build out a more complete incident investigation by adding additional observed data, tasks, events, impacts, and sequences. This follows the patterns established in stix-graph-patterns.md and expands on the foundation laid in notebook-storyboards.md.

---

## Story Overview: The Investigation Deepens

**Starting Point:**  
You have a confirmed phishing incident with:
- Initial SIEM alert (sighting-alert)
- Employee testimony (sighting-anecdote)
- Basic phishing email evidence (url, email-message, email-addr SCOs)
- One indicator (phishing pattern)
- Initial event (phishing email received)
- Investigation task (analyze email)
- Preliminary impact assessment (availability or confidentiality)

**Story Arc:**  
The investigation continues and you discover:
1. **More Evidence:** Additional compromised accounts, follow-on malicious activities
2. **Deeper Analysis:** Threat intelligence enrichment, hunt findings, framework attribution
3. **Expanded Timeline:** Multiple events showing attack progression
4. **Complex Tasks:** Remediation workflows, containment actions, recovery procedures
5. **Cascading Impacts:** Additional systems and users affected
6. **Workflow Orchestration:** Sequence objects coordinating response activities

---

## Extension 1: Additional Observed Data with Hunt Findings

### Story: The Hunt Team Discovers More Victims

**Narrative:**  
Your initial phishing incident targeted one user. The security hunt team proactively searches across the enterprise and discovers the same phishing campaign hit 15 additional employees. Some clicked the link; others forwarded the email internally.

### Graph Pattern Used

**Pattern 6.2:** Evidence Collection (Sighting-Based) with sighting-hunt extension

### Implementation Details

**1. Discover Additional SCOs:**
```
For each additional victim:
  - Create user-account SCO (if not already in Step 1)
  - Create email-addr SCO (if not already in Step 1)
  - Create email-message SCO (each instance of the phishing email)
  - Link: email-message.from_ref → attacker email-addr
  - Link: email-message.to_refs → victim email-addr
  - Link: email-message.body_multipart[].body_raw_ref → url (phishing link)
```

**2. Create Observed Data Bundles:**
```
Create observed-data SDO for each hunt finding:
  - object_refs → [user-account, email-addr, email-message, url]
  - first_observed = when email received
  - last_observed = when hunt team discovered it
  - number_observed = 1 per instance
  - created_by_ref → your identity
```

**3. Create Sighting with Hunt Extension:**
```
Create sighting SRO for hunt findings:
  - sighting_of_ref → indicator (same phishing indicator)
  - observed_data_refs → [all new observed-data objects]
  - where_sighted_refs → [company network segments, email servers]
  - Extension: sighting-hunt
    * name = "Proactive Hunt for Phishing Campaign"
    * hunt_type = "hypothesis-driven" or "baseline-anomaly"
    * start_time = when hunt began
    * end_time = when hunt completed
    * completed = true
    * hypothesis = "Same phishing pattern may have targeted multiple users"
  - count = 15 (number of additional victims found)
  - created_by_ref → your identity
```

**4. Update Incident:**
```
Retrieve incident from Step 2/3:
  - Add to other_object_refs → [new sightings, observed-data, SCOs]
  - Update determination = "confirmed-true-positive" (multiple victims = confirmed campaign)
  - Update sophistication = adjust if multiple targets indicate targeted campaign
  - Update modified timestamp
```

**Objects Created:**
- 15 x email-message SCOs (one per victim)
- 0-15 x user-account SCOs (if not already in Step 1)
- 0-15 x email-addr SCOs (if not already in Step 1)
- 15 x observed-data SDOs
- 1 x sighting SRO (with sighting-hunt extension aggregating all findings)
- Total: ~30-60 new objects

**Story Impact:**  
The incident scope expands dramatically. What looked like a single targeted attack is now a widespread campaign. This triggers escalation, broader remediation, and executive notification.

---

## Extension 2: Threat Intelligence Enrichment

### Story: Attribution Through External Intelligence

**Narrative:**  
You submit the phishing URL and email indicators to threat intelligence platforms (VirusTotal, MISP, commercial feeds). The enrichment reveals this campaign is part of a known APT operation tracked as "SeaShell Phishing" by multiple vendors.

### Graph Pattern Used

**Pattern 6.2:** Evidence Collection (Sighting-Based) with sighting-enrichment extension

### Implementation Details

**1. Create External References:**
```
Create external-reference objects (STIX common property):
  - source_name = "VirusTotal"
  - description = "Malicious URL analysis"
  - url = "https://virustotal.com/analysis/abc123"
  - hashes = {"SHA-256": "..."}
  
  - source_name = "MISP Event 12345"
  - description = "SeaShell Phishing Campaign"
  - url = "https://misp.example.com/events/12345"
```

**2. Create Enrichment Sighting:**
```
Create sighting SRO:
  - sighting_of_ref → indicator (phishing indicator)
  - observed_data_refs → [existing observed-data from Step 2]
  - Extension: sighting-enrichment
    * name = "Threat Intelligence Enrichment"
    * enrichment_type = "external-lookup"
    * source = "VirusTotal, MISP, ThreatStream"
    * confidence_score = 95 (high confidence attribution)
    * enrichment_date = timestamp
  - external_references → [VirusTotal, MISP references]
  - created_by_ref → your identity
```

**3. Create Threat Actor/Campaign Objects (Optional):**
```
If attribution warrants:
  - Create threat-actor SDO:
    * name = "SeaShell APT"
    * threat_actor_types = ["nation-state"]
    * sophistication = "advanced"
    * resource_level = "government"
    * primary_motivation = "organizational-gain"
    
  - Create campaign SDO:
    * name = "SeaShell Phishing Campaign 2024-Q1"
    * campaign_types = ["phishing"]
    * first_seen = earliest known sighting
    * last_seen = most recent sighting
    
  - Create SRO relationships:
    * threat-actor → attributed-to → campaign
    * incident → attributed-to → threat-actor
    * indicator → indicates → campaign
```

**4. Update Incident:**
```
Retrieve incident:
  - Add to other_object_refs → [sighting-enrichment, threat-actor, campaign]
  - Update determination = "confirmed-true-positive"
  - Update confidence = 95 (based on enrichment)
  - Update external_references → [VirusTotal, MISP]
  - Add to labels → ["APT", "nation-state", "SeaShell"]
```

**Objects Created:**
- 1 x sighting SRO (with sighting-enrichment)
- 0-1 x threat-actor SDO
- 0-1 x campaign SDO
- 0-2 x relationship SROs
- Total: ~2-5 new objects

**Story Impact:**  
The incident gains geopolitical context. Executive leadership needs to know this is a nation-state actor. This changes response priorities, legal considerations, and notification requirements.

---

## Extension 3: Multiple Events Showing Attack Progression

### Story: The Attack Timeline Unfolds

**Narrative:**  
Analysis reveals the phishing attack progressed through multiple stages:
1. **Event 1 (T+0 hours):** Phishing emails sent
2. **Event 2 (T+2 hours):** User clicked malicious link
3. **Event 3 (T+2.5 hours):** Credential harvesting page displayed
4. **Event 4 (T+3 hours):** User entered credentials
5. **Event 5 (T+4 hours):** Attacker logged in with stolen credentials
6. **Event 6 (T+5 hours):** Lateral movement to file server
7. **Event 7 (T+6 hours):** Data exfiltration detected

### Graph Pattern Used

**Pattern 6.3:** Event Creation from Evidence  
**Pattern 6.5:** Workflow Sequencing (Sequence object)

### Implementation Details

**1. Create Event Chain:**
```
For each stage of attack:

Event 2: User Clicked Link
  - sighting_refs → [sighting with web proxy logs]
  - event_types = ["user-activity", "phishing"]
  - status = "occurred"
  - start_time = click timestamp
  - changed_objects → [StateChangeObject for web browser state]
  - created_by_ref → your identity

Event 3: Credential Harvesting Page Displayed
  - sighting_refs → [sighting with web content analysis]
  - event_types = ["malicious-activity", "credential-theft"]
  - status = "occurred"
  - changed_objects → [StateChangeObject for fake login page]
  
Event 4: Credentials Entered
  - sighting_refs → [sighting with keylogger or form submission]
  - event_types = ["credential-theft", "user-activity"]
  - status = "occurred"
  - changed_objects → [StateChangeObject capturing credential compromise]

Event 5: Unauthorized Access
  - sighting_refs → [sighting with authentication logs]
  - event_types = ["unauthorized-access", "authentication-failure"]
  - status = "occurred"
  - changed_objects → [StateChangeObject for user session]

Event 6: Lateral Movement
  - sighting_refs → [sighting with network traffic analysis]
  - event_types = ["lateral-movement", "unauthorized-access"]
  - status = "occurred"
  - changed_objects → [StateChangeObject for file server access]

Event 7: Data Exfiltration
  - sighting_refs → [sighting with DLP alerts]
  - event_types = ["data-exfiltration", "unauthorized-access"]
  - status = "occurred"
  - changed_objects → [StateChangeObject for data transfer]
```

**2. Create SRO Relationships for Event Causality:**
```
Create relationship SROs:
  - event1 → led-to → event2
  - event2 → led-to → event3
  - event3 → led-to → event4
  - event4 → led-to → event5
  - event5 → led-to → event6
  - event6 → led-to → event7
  
  relationship_type = "led-to"
  source_ref → earlier event
  target_ref → subsequent event
```

**3. Create Sequence Object (Pattern 6.5):**
```
Create sequence SDO to orchestrate the event chain:
  - name = "Phishing Attack Kill Chain"
  - sequenced_object = "event"
  - sequence_type = "attack-chain"
  - step_type = "serial" (events must occur in order)
  - step_refs → [event1, event2, event3, event4, event5, event6, event7] (ordered)
  - created_by_ref → your identity
```

**4. Update Incident:**
```
Retrieve incident:
  - Update event_refs → [all 7 events]
  - Add to other_object_refs → [sequence, relationship SROs]
  - Update determination = "confirmed-true-positive"
  - Update investigation_status = "completed" or "in-progress"
```

**Objects Created:**
- 6 x event SDOs (Event 1 already exists from Step 2)
- 6 x relationship SROs (led-to chain)
- 1 x sequence SDO
- Multiple x sighting SROs (one per evidence source: proxy, DLP, auth logs, etc.)
- Multiple x observed-data SDOs (backing the sightings)
- Total: ~20-30 new objects

**Story Impact:**  
The incident transforms from a single phishing email to a complete attack timeline. This enables:
- **Root cause analysis:** Understand how the attack succeeded
- **Kill chain mapping:** Identify where defenses failed
- **Lessons learned:** Determine prevention opportunities at each stage
- **Executive briefing:** Present clear attack narrative

---

## Extension 4: Comprehensive Task Workflow

### Story: Coordinated Incident Response

**Narrative:**  
Your initial investigation task spawns a complete incident response workflow. Multiple teams (SOC, IR, IT, Legal, Comms) each have specific tasks that must be coordinated and tracked.

### Graph Pattern Used

**Pattern 6.4:** Task Creation with Ownership  
**Pattern 6.5:** Workflow Sequencing (Sequence object)

### Implementation Details

**1. Create Task Hierarchy:**
```
Task 1: Containment (Already exists from Step 2)
  - name = "Contain phishing incident"
  - task_types = ["contain"]
  - owner → SOC analyst identity
  - priority = 90
  - status = "completed"
  - outcome = "Blocked malicious URLs, disabled compromised accounts"

Task 2: Eradication
  - name = "Remove malicious artifacts"
  - task_types = ["eradicate", "remediation"]
  - owner → IR team lead identity
  - priority = 80
  - status = "in-progress"
  - start_time = containment completion time
  - impacted_entity_refs → [compromised email server, user accounts]
  
Task 3: Recovery
  - name = "Restore compromised accounts"
  - task_types = ["recover", "remediation"]
  - owner → IT admin identity
  - priority = 70
  - status = "pending"
  - dependencies → [Task 2 must complete first]
  
Task 4: Evidence Collection
  - name = "Preserve forensic evidence"
  - task_types = ["investigate", "forensics"]
  - owner → forensics analyst identity
  - priority = 85
  - status = "completed"
  
Task 5: Legal Review
  - name = "Assess breach notification requirements"
  - task_types = ["legal", "compliance"]
  - owner → legal counsel identity
  - priority = 75
  - status = "in-progress"
  
Task 6: User Communication
  - name = "Notify affected users"
  - task_types = ["communication"]
  - owner → security awareness team identity
  - priority = 60
  - status = "pending"
  - dependencies → [Task 5 legal review must complete]

Task 7: Executive Briefing
  - name = "Brief CISO on incident"
  - task_types = ["communication", "reporting"]
  - owner → SOC manager identity
  - priority = 95
  - status = "completed"
```

**2. Create Task Relationships:**
```
Create relationship SROs showing task dependencies:
  - task1 → blocks → task3 (can't recover until contained)
  - task2 → blocks → task3 (can't recover until eradicated)
  - task5 → blocks → task6 (can't notify until legal approves)
  
  - task1 → detects → event (containment responds to initial event)
  - task2 → mitigates → incident (eradication mitigates the incident)
  - task4 → investigates → incident (forensics investigates incident)
```

**3. Create Sequence Object for Task Workflow:**
```
Create sequence SDO:
  - name = "Phishing Incident Response Workflow"
  - sequenced_object = "task"
  - sequence_type = "playbook"
  - step_type = "parallel-then-serial"
  - step_refs → [
      [task1, task4, task7],  # Parallel: Containment, forensics, briefing
      [task2],                  # Serial: Eradication after containment
      [task5],                  # Serial: Legal review after eradication
      [task3, task6]            # Parallel: Recovery and notification after legal
    ]
  - created_by_ref → your identity
```

**4. Update Incident:**
```
Retrieve incident:
  - Update task_refs → [all 7 tasks]
  - Add to other_object_refs → [sequence, task relationship SROs]
  - Update investigation_status based on task completion:
    * All completed → "closed"
    * Some in-progress → "active-investigation"
    * Some pending → "pending-response"
```

**Objects Created:**
- 6 x task SDOs (Task 1 already exists)
- 5-8 x relationship SROs (task dependencies)
- 1 x sequence SDO
- 0-3 x identity SDOs (if new team members need to be created)
- Total: ~12-18 new objects

**Story Impact:**  
Incident response becomes visible and trackable:
- **Accountability:** Each task has an owner
- **Status visibility:** Leadership knows what's done, in-progress, pending
- **Dependency awareness:** Teams know what's blocking them
- **Workflow automation:** Sequence object enables SOAR integration
- **Audit trail:** Forensic record of response actions

---

## Extension 5: Cascading Impact Assessment

### Story: Understanding the Full Damage

**Narrative:**  
Initial impact was "confidentiality" (credentials stolen). Deeper analysis reveals cascading impacts: availability (accounts disabled), integrity (data modified), financial (incident response costs), and regulatory (potential GDPR breach).

### Graph Pattern Used

**Pattern 6.6:** Impact Tracking

### Implementation Details

**1. Create Multiple Impact Objects:**
```
Impact 1: Confidentiality Breach (Already exists from Step 2)
  - impact_category = "confidentiality"
  - Extension: extension-definition--7d7c2d3c-23c5-4a67-94e6-8e2e73c3c948 (confidentiality)
    * information_type = "credentials"
    * loss_type = "confirmed-loss"
  - impacted_refs → [user identities whose credentials were stolen]
  - start_time = credential theft time
  - recoverability = "supplemented" (requires password reset)
  - superseded_by_ref → Impact 2 (if severity escalates)

Impact 2: Availability Impact
  - impact_category = "availability"
  - Extension: extension-definition--7d7c2d3c-23c5-4a67-94e6-8e2e73c3c947 (availability)
    * availability_loss_type = "loss"
    * duration = "temporary" or "permanent"
  - impacted_refs → [email system, compromised user accounts]
  - start_time = account lockout time
  - end_time = account restoration time
  - recoverability = "regular" (accounts can be re-enabled)

Impact 3: Integrity Impact
  - impact_category = "integrity"
  - Extension: extension-definition--0c725d12-44e8-4554-8265-05891d016154 (integrity)
    * alteration_type = "modification"
    * integrity_loss_type = "confirmed-loss"
  - impacted_refs → [file server, modified files/directories]
  - start_time = unauthorized modification time
  - recoverability = "supplemented" (requires backup restoration)

Impact 4: Financial Impact
  - impact_category = "monetary"
  - Extension: extension-definition--6b36ed16-cc22-43b4-bdb0-b82df193c59d (monetary)
    * currency = "USD"
    * variety = ["incident-response-costs", "productivity-loss"]
    * max_amount = 50000 (estimated IR costs)
  - impacted_refs → [company identity, IT budget identity]
  - start_time = incident start time
  - recoverability = "not-recoverable" (costs are sunk)

Impact 5: Privacy/Regulatory Impact (GDPR)
  - impact_category = "privacy"
  - Extension: extension-definition--6b36ed16-cc22-43b4-bdb0-b82df193c59e (privacy)
    * privacy_breach_type = "personal-data-exposure"
    * records_affected = 15 (number of users)
    * data_types = ["email-addresses", "credentials", "contact-info"]
  - impacted_refs → [EU-based user identities]
  - start_time = breach time
  - recoverability = "extended" (regulatory investigation, potential fines)

Impact 6: Reputational Impact
  - impact_category = "external"
  - Extension: extension-definition--6b36ed16-cc22-43b4-bdb0-b82df193c59f (external)
    * reputation_loss_type = "brand-damage"
    * stakeholder_type = ["customers", "partners"]
  - impacted_refs → [company identity, executive identities]
  - recoverability = "extended" (long-term trust rebuilding)
```

**2. Create Impact Relationships:**
```
Create relationship SROs showing impact causality:
  - impact1 → led-to → impact2 (credential theft led to account lockout)
  - impact1 → led-to → impact3 (stolen creds enabled file modification)
  - incident → impacts → identity (for each affected user/system)
  - event6 → caused → impact3 (lateral movement event caused integrity impact)
```

**3. Update Incident:**
```
Retrieve incident:
  - Update impact_refs → [all 6 impacts]
  - Add to other_object_refs → [impact relationship SROs]
  - Update impact_criticality = "high" (based on cumulative impact)
  - Update recoverability = "extended" (worst-case from all impacts)
```

**Objects Created:**
- 5 x impact SDOs (Impact 1 already exists)
- 4-8 x relationship SROs (impact causality)
- Total: ~9-13 new objects

**Story Impact:**  
Incident severity becomes clear:
- **Executive visibility:** Understand full business impact
- **Budget justification:** Financial impact supports resource requests
- **Regulatory compliance:** Privacy impact triggers breach notification
- **Risk assessment:** Inform future risk management decisions
- **Insurance claims:** Document losses for cyber insurance

---

## Extension 6: Framework Mapping (MITRE ATT&CK)

### Story: Mapping to Industry Standards

**Narrative:**  
Your CISO wants to understand the attack in terms of MITRE ATT&CK framework. You map the incident to specific tactics, techniques, and procedures (TTPs).

### Graph Pattern Used

**Pattern 6.2:** Evidence Collection (Sighting-Based) with sighting-framework extension

### Implementation Details

**1. Create MITRE ATT&CK Mapping:**
```
Create sighting SRO with framework extension:
  - sighting_of_ref → indicator (phishing indicator)
  - observed_data_refs → [relevant observed-data]
  - Extension: sighting-framework
    * name = "MITRE ATT&CK Mapping"
    * framework = "ATT&CK"
    * version = "v14.1"
    * framework_id = "T1566.002" (Phishing: Spearphishing Link)
    * tactic = ["initial-access"]
    * technique = ["phishing"]
    * url = "https://attack.mitre.org/techniques/T1566/002/"
  - external_references → [MITRE ATT&CK reference]
  - created_by_ref → your identity

Create additional framework sightings for each technique:
  - T1078: Valid Accounts (credential use after theft)
  - T1021: Remote Services (lateral movement)
  - T1048: Exfiltration Over Alternative Protocol
  - T1110: Brute Force (if password spraying detected)
```

**2. Create Attack Pattern Objects (Optional):**
```
If detailed TTP documentation needed:
  - Create attack-pattern SDO for each MITRE technique:
    * name = "Spearphishing Link"
    * external_references → [MITRE ATT&CK T1566.002]
    * kill_chain_phases = [
        {
          "kill_chain_name": "mitre-attack",
          "phase_name": "initial-access"
        }
      ]
  
  - Create relationship SROs:
    * indicator → indicates → attack-pattern
    * incident → uses → attack-pattern
    * threat-actor → uses → attack-pattern
```

**3. Update Incident:**
```
Retrieve incident:
  - Add to other_object_refs → [framework sightings, attack-patterns]
  - Update external_references → [MITRE ATT&CK]
  - Add to labels → ["T1566.002", "initial-access", "credential-access"]
```

**Objects Created:**
- 3-6 x sighting SROs (with sighting-framework, one per technique)
- 0-6 x attack-pattern SDOs
- 0-6 x relationship SROs
- Total: ~6-18 new objects

**Story Impact:**  
Industry-standard analysis:
- **Benchmarking:** Compare to industry baseline for phishing TTPs
- **Control mapping:** Map ATT&CK techniques to existing controls
- **Gap analysis:** Identify missing detections/preventions
- **Threat modeling:** Understand adversary methodology
- **Board reporting:** Executives understand standardized framework

---

## Extension 7: Adding Context Evidence

### Story: Environmental Context and Situational Awareness

**Narrative:**  
The incident occurred during a major company acquisition announcement, which may explain why employees were more susceptible to phishing (high stress, many legitimate urgent emails). You document this contextual information.

### Graph Pattern Used

**Pattern 6.2:** Evidence Collection (Sighting-Based) with sighting-context extension

### Implementation Details

**1. Create Context Sighting:**
```
Create sighting SRO:
  - sighting_of_ref → event (phishing email event)
  - Extension: sighting-context
    * name = "Incident Context - Acquisition Announcement"
    * context_type = "situational"
    * description = "Company announced major acquisition 2 days before phishing campaign. Employees received many urgent legitimate emails from leadership, reducing suspicion of phishing."
    * relevance = "high"
    * temporal_context = "coincident"
  - created_by_ref → your identity
```

**2. Link Context to Other Objects:**
```
Create relationship SROs:
  - context-sighting → explains → incident (context explains why incident succeeded)
  - context-sighting → relates-to → company-identity (organizational context)
```

**3. Update Incident:**
```
Retrieve incident:
  - Add to other_object_refs → [context sighting]
  - Update description to include contextual information
  - Possibly update sophistication (attackers timed campaign strategically)
```

**Objects Created:**
- 1 x sighting SRO (with sighting-context)
- 1-2 x relationship SROs
- Total: ~2-3 new objects

**Story Impact:**  
Fuller understanding:
- **Root cause:** Why social engineering succeeded
- **Prevention:** Increase awareness during high-stress periods
- **Detection:** Flag spikes in phishing during corporate events
- **Attribution:** Suggests adversary did reconnaissance

---

## Putting It All Together: The Extended Incident

### Complete Object Inventory

After all extensions, the incident contains:

**SCOs:** ~25-40 objects (emails, URLs, user accounts, addresses, anecdote)  
**Observed-Data:** ~20-30 objects (grouping SCO observations)  
**Sightings:** ~10-15 objects (alert, anecdote, hunt, enrichment, framework, context)  
**Indicators:** ~2-5 objects (phishing patterns, IOCs)  
**Events:** ~7-10 objects (attack timeline)  
**Tasks:** ~7-10 objects (response workflow)  
**Impacts:** ~6-8 objects (all impact categories)  
**Sequences:** ~2-3 objects (event chain, task workflow)  
**Identities:** ~20-30 objects (reused from Steps 0-1)  
**Relationships:** ~15-25 SROs (led-to, blocks, mitigates, etc.)  
**Attack Patterns:** ~3-6 objects (MITRE TTPs)  
**Threat Actor/Campaign:** ~0-2 objects (if attribution)  

**Total Objects:** ~120-200 objects (from initial ~25-40)

**Incident.other_object_refs length:** ~80-150 references

### Story Arc of Extensions

**Phase 1 (Initial):** Single phishing email, one victim, basic investigation  
**Phase 2 (Hunt):** Discovery of 15 additional victims, campaign scope grows  
**Phase 3 (Enrichment):** Attribution to nation-state APT, geopolitical implications  
**Phase 4 (Timeline):** 7-stage attack kill chain documented  
**Phase 5 (Response):** 7-task coordinated response workflow  
**Phase 6 (Impact):** 6 impact categories, full damage assessment  
**Phase 7 (Framework):** MITRE ATT&CK mapping, industry standardization  
**Phase 8 (Context):** Organizational context, root cause understanding  

### Lessons for Incident Development

**1. Start Simple, Build Complexity:**  
Don't try to create the complete incident upfront. Start with core evidence (Step 2), then layer in additional context as investigation progresses.

**2. Evidence Types Have Different Purposes:**
- **sighting-alert:** Automated detection, initial triage
- **sighting-anecdote:** Human reporting, confirmation
- **sighting-hunt:** Proactive discovery, scope expansion
- **sighting-enrichment:** External intelligence, attribution
- **sighting-framework:** Standardization, benchmarking
- **sighting-context:** Situational awareness, root cause

**3. Relationships Tell the Story:**  
SRO relationships (`led-to`, `blocks`, `mitigates`, `investigates`) add semantic meaning that embedded references cannot capture.

**4. Sequences Enable Automation:**  
Sequence objects turn static documentation into executable workflows for SOAR platforms.

**5. Impacts Drive Prioritization:**  
Multiple impact types show business consequences, not just technical details.

**6. Context Prevents Future Incidents:**  
Understanding why an incident succeeded informs prevention strategies.

---

## How to Use This Storyboard

**For Notebook Authors:**
- Create new notebooks following these extension patterns
- Each extension could be its own notebook (Step_4_Hunt.ipynb, Step_5_Enrichment.ipynb, etc.)
- Maintain consistency: load existing incident, add new objects, update incident
- Document the "why" of each extension in markdown cells

**For Incident Responders:**
- Use these patterns as checklists for complete investigations
- Not every incident needs every extension - apply as relevant
- Sequence matters: some extensions depend on others (enrichment after initial evidence, framework after TTPs identified)

**For System Developers:**
- Implement these patterns as reusable functions
- Create libraries for common operations (add_hunt_findings, enrich_with_intel, map_to_framework)
- Build SOAR playbooks based on sequence objects
- Design dashboards showing incident completeness (% of extensions present)

