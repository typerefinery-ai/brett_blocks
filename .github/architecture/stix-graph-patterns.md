# STIX Graph Patterns for OS-Triage Incident Management

## Executive Summary

This document provides a comprehensive map of STIX object graph linkage patterns in the OS-Triage system, enabling complete incident reconstitution from the IncidentCoreExt extension structure. It documents:

- **15 STIX Object Types**: 9 SDO, 5 SCO, 2 SRO (8 SDO + 1 SDO templates available, 5 SCO templates, 2 SRO templates)
- **7-Level Dependency Hierarchy**: From Level 0 (no dependencies) to Level 6 (incident - top container)
- **50+ Embedded Reference Fields**: ReferenceProperty and OSThreatReference fields creating object dependencies
- **26 SRO Relationship Types**: Source/target constrained relationship patterns
- **13 Graph Patterns**: 7 from seed documentation + 6 newly discovered from template analysis

**Key Insight**: STIX incidents use TWO interconnected graph networks:
1. **Embedded Reference Graph**: Creates strict dependency hierarchy (must build bottom-up)
2. **SRO Relationship Graph**: Creates flexible semantic connections (can be added anytime)

## 1. Dual Graph Network Architecture

### 1.1 Embedded Reference Network

Objects contain fields (`ReferenceProperty` or `OSThreatReference`) that directly reference other object IDs. This creates:
- **Strict Dependencies**: Referenced objects MUST exist before referencing object
- **Build Order Constraints**: Objects must be created in dependency order (Level 0 → Level 6)
- **Hierarchy Enforcement**: Lower-level objects are more foundational than higher-level objects
- **Incident Completeness**: All objects reachable via embedded refs from IncidentCoreExt

**Property Types**:
- `ReferenceProperty`: Standard STIX 2.1 reference field
- `OSThreatReference`: US DoD extension reference field (supports `_any` for flexible typing)

### 1.2 SRO Relationship Network

Relationship and Sighting objects connect two objects via `source_ref` and `target_ref` (or specialized fields). This creates:
- **Flexible Connections**: Can be added independent of dependency hierarchy
- **Semantic Richness**: 26 distinct `relationship_type` values with specific source/target constraints
- **Graph Traversal**: Enables queries like "show all tasks that block this event"
- **Bi-directional Links**: Relationships can be traversed in both directions

**Critical Rule**: All SRO objects in an incident MUST be registered in IncidentCoreExt's `other_object_refs` field for incident completeness.

## 2. Complete Dependency Hierarchy (7 Levels)

Objects organized by embedded reference dependencies. Each level can only reference objects at the same or lower levels.

### Level 0: Foundation Objects (No Dependencies)

**No embedded references except `created_by_ref` (external identity)**

| Object Type | STIX Type | Description |
|------------|-----------|-------------|
| UserAccount | `user-account` | SCO - User credential and account details |
| URL | `url` | SCO - Web address/link |
| Indicator | `indicator` | SDO - Pattern representing malicious activity |

**Build Order**: Create these first (any order within level)

### Level 1: Simple Reference Objects

**References only Level 0 objects**

| Object Type | STIX Type | Embedded References | Dependency |
|------------|-----------|---------------------|------------|
| EmailAddress | `email-addr` | `belongs_to_ref` | → user-account (Level 0) |
| Anecdote | `anecdote` | `provided_by_ref` | → identity (external) |

**Build Order**: Create after Level 0

### Level 2: Extended Reference Objects

**References Level 0-1 objects**

| Object Type | STIX Type | Embedded References | Dependencies |
|------------|-----------|---------------------|--------------|
| Identity | `identity` | `EmailContact.email_address_ref`<br>`SocialMediaContact.user_account_ref` | → email-addr (Level 1)<br>→ user-account (Level 0) |
| EmailMessage | `email-message` | `from_ref`, `to_refs`, `cc_refs`, `bcc_refs`<br>`raw_email_ref` (future) | → email-addr (Level 1)<br>→ artifact (not implemented) |

**Build Order**: Create after Level 1

**Special Note**: Identity with IdentityContact extension (`extension-definition--66e2492a-bbd3-4be6-88f5-cc91a017a498`) contains:
- `contact_numbers`: List of ContactNumber sub-objects (no references)
- `email_addresses`: List of EmailContact sub-objects (`email_address_ref` → email-addr)
- `social_media_accounts`: List of SocialMediaContact sub-objects (`user_account_ref` → user-account)

### Level 3: Container & Assessment Objects

**References Level 0-2 objects**

| Object Type | STIX Type | Embedded References | Dependencies |
|------------|-----------|---------------------|--------------|
| ObservedData | `observed-data` | `object_refs` | → _any SCO (Level 0-2) |
| Impact | `impact` | `impacted_refs`<br>`superseded_by_ref` | → _any (flexible)<br>→ impact (self-reference) |
| Task | `task` | `owner`<br>`changed_objects.initial_ref`<br>`changed_objects.result_ref` | → identity (Level 2)<br>→ _any<br>→ _any |

**Build Order**: Create after Level 2

**Impact Extensions** (7 types via US DoD extensions):
1. `availability` - Availability impact assessment
2. `confidentiality` - Data confidentiality breach assessment
3. `external` - External/reputational impact
4. `integrity` - Data integrity compromise assessment
5. `monetary` - Financial/monetary impact
6. `physical` - Physical damage assessment
7. `traceability` - Evidence traceability impact

### Level 4: Evidence & Analysis Objects

**References Level 0-3 objects**

| Object Type | STIX Type | Embedded References | Dependencies |
|------------|-----------|---------------------|--------------|
| Sighting | `sighting` (SRO) | `sighting_of_ref`<br>`observed_data_refs`<br>`where_sighted_refs` | → _sdo (what was sighted)<br>→ observed-data (Level 3)<br>→ identity/location (Level 2) |
| Event | `event` | `sighting_refs`<br>`changed_objects.initial_ref`<br>`changed_objects.result_ref` | → sighting (Level 4)<br>→ _any<br>→ _any |

**Build Order**: Create after Level 3

**Sighting Extensions** (8 evidence types via US DoD `extension-definition--0d76d6d9-16ca-43fd-bd41-4f800ba8fc43`):

1. **`sighting-alert`** (class `SightingAlert`): Alert issued by system or user
   - Fields: name, log, system_id, source, product, format
   - Use: Initial detection, automated alerting systems

2. **`sighting-anecdote`** (class `SightingAnecdote`): User-reported observation
   - Fields: person_name, person_context, report_submission
   - Use: User reports, phishing emails forwarded, eyewitness accounts

3. **`sighting-context`** (class `SightingContext`): Internal system query results
   - Fields: name, description, value
   - Use: Exchange queries, SAP data, historical logs (100% confidence)

4. **`sighting-exclusion`** (class `SightingExclusion`): Exclusion/blocklist check results
   - Fields: source, channel
   - Use: Threat feed lookups, reputation checks

5. **`sighting-enrichment`** (class `SightingEnrichment`): OSINT/paid intel enrichment
   - Fields: name, url, paid, value
   - Use: VirusTotal, Shodan, passive DNS lookups

6. **`sighting-hunt`** (class `SightingHunt`): Threat hunting investigation results
   - Fields: name, playbook_id, rule
   - Use: Kestrel hunts, EDR queries, proactive threat hunting

7. **`sighting-framework`** (class `SightingFramework`): Framework mapping (ATT&CK, etc.)
   - Fields: framework, version, domain, comparison, comparison_approach
   - Use: MITRE ATT&CK mapping, DISARM, kill chain

8. **`sighting-external`** (class `SightingExternal`): External threat intel reports
   - Fields: source, version, last_update, pattern, pattern_type, payload, valid_from, valid_until
   - Use: MISP feeds, vendor threat reports, IOC sharing

### Level 5: Workflow & Semantic Objects

**References Level 0-4 objects**

| Object Type | STIX Type | Embedded References | Dependencies |
|------------|-----------|---------------------|--------------|
| Sequence | `sequence` | `sequenced_object`<br>`on_completion`<br>`on_success`<br>`on_failure`<br>`next_steps` | → event OR task (Level 3-4)<br>→ sequence (self-ref)<br>→ sequence (self-ref)<br>→ sequence (self-ref)<br>→ sequence list (self-ref) |
| Relationship | `relationship` (SRO) | `source_ref`<br>`target_ref` | → _any (constrained by relationship_type)<br>→ _any (constrained by relationship_type) |

**Build Order**: Create after Level 4

**Sequence Workflow Patterns**:
- **Linear Sequence**: Use `on_completion` to chain steps
- **Conditional Branching**: Use `on_success`/`on_failure` for decision points
- **Parallel Execution**: Use `next_steps` list for concurrent actions
- **Start Steps**: Set `step_type` = "start_step" and register in incident's `sequence_start_refs`

### Level 6: Incident Container (Top Level)

**References all lower levels**

| Object Type | STIX Type | Embedded References (IncidentCoreExt) | Dependencies |
|------------|-----------|--------------------------------------|--------------|
| Incident | `incident` | `event_refs`<br>`impact_refs`<br>`task_refs`<br>`sequence_refs`<br>`sequence_start_refs`<br>`other_object_refs` | → event list (Level 4)<br>→ impact list (Level 3)<br>→ task list (Level 3)<br>→ sequence list (Level 5)<br>→ sequence list (Level 5)<br>→ _any (all objects not in above lists) |

**Build Order**: Create LAST after all constituent objects

**IncidentCoreExt Extension** (`extension-definition--ef765651-680c-498d-9894-99799f2fa126`):
- **Purpose**: Extends base incident stub with operational fields and comprehensive object references
- **Critical Fields**: 6 `_refs` fields create complete object graph
- **Incident Completeness**: All objects in incident MUST be reachable via these 6 fields
- **Object Registry**:
  - `event_refs`: All event objects
  - `impact_refs`: All impact objects
  - `task_refs`: All task objects
  - `sequence_refs`: All sequence objects (including non-start steps)
  - `sequence_start_refs`: Subset of sequences marking workflow entry points (`step_type`="start_step")
  - `other_object_refs`: All other objects (identities, SCOs, sightings, relationships, observed-data, indicators, etc.)

## 3. Graph Pattern Catalog

### Pattern 3.1: Incident Container Pattern *(from seed 1.1)*

**Description**: IncidentCoreExt extension provides orthogonal reference lists for complete incident object registration.

**Structure**:
```
Incident (SDO)
├── extensions.IncidentCoreExt
│   ├── event_refs[] → Event objects (Level 4)
│   ├── impact_refs[] → Impact objects (Level 3)
│   ├── task_refs[] → Task objects (Level 3)
│   ├── sequence_refs[] → Sequence objects (Level 5)
│   ├── sequence_start_refs[] → Sequence objects with step_type="start_step" (Level 5)
│   └── other_object_refs[] → All other objects (Levels 0-5)
│       ├── Identity, ObservedData, Indicator (SDOs)
│       ├── UserAccount, EmailAddress, URL, EmailMessage, Anecdote (SCOs)
│       └── Sighting, Relationship (SROs)
```

**Usage**: Build all constituent objects first (Levels 0-5), then create incident and populate all 6 `_refs` fields.

**Key Rules**:
- Every object in the incident MUST appear in one of the 6 `_refs` fields
- Use appropriate field for each object type (e.g., events in `event_refs`, not `other_object_refs`)
- `sequence_start_refs` is subset of `sequence_refs` (start sequences appear in both)
- `created_by_ref` identities typically go in `other_object_refs`

### Pattern 3.2: Identity Sub-Pattern with Extensions *(from seed 1.2)*

**Description**: Identity objects can include contact details via IdentityContact extension, creating dependency on user-account and email-addr SCOs.

**Dependency Chain**:
```
Level 0: user-account (SCO) - No dependencies
         ↓ belongs_to_ref
Level 1: email-addr (SCO) - Depends on user-account
         ↓ email_address_ref (via EmailContact)
         ↓ user_account_ref (via SocialMediaContact)
Level 2: identity (SDO) - Depends on email-addr and user-account
```

**Structure**:
```
identity (SDO)
├── extensions.IdentityContact
│   ├── contact_numbers[] (ContactNumber sub-objects)
│   │   └── No references
│   ├── email_addresses[] (EmailContact sub-objects)
│   │   └── email_address_ref → email-addr (Level 1)
│   └── social_media_accounts[] (SocialMediaContact sub-objects)
│       └── user_account_ref → user-account (Level 0)
```

**Usage**:
1. Create user-account SCO (e.g., `user_id`: "jdoe", `account_login`: "jdoe@company.com")
2. Create email-addr SCO with `belongs_to_ref` pointing to user-account
3. Create identity SDO with IdentityContact extension
4. Add EmailContact sub-object with `email_address_ref` pointing to email-addr
5. Add SocialMediaContact sub-object with `user_account_ref` pointing to user-account

**Use Cases**:
- **Personal Identities**: Security analysts, incident responders (full contact details)
- **User Identities**: Company employees, victims, witnesses
- **Organizational Identities**: Companies, departments (may not have extension)
- **System Identities**: Servers, workstations, network devices (may use simple identity)
- **Adversary Identities**: Threat actors (typically simple identity without extension)

### Pattern 3.3: Observed-Data, Sighting & Evidence Extensions *(from seed 1.3)*

**Description**: Three-layer pattern for evidence collection: SCOs → ObservedData → Sighting with provenance extensions.

**Dependency Chain**:
```
Level 0-2: SCOs (url, user-account, email-addr, email-message, anecdote)
           ↓ object_refs
Level 3: observed-data (SDO) - Contains SCO references
           ↓ observed_data_refs
Level 4: sighting (SRO) - Links observations to "what" and "where"
         ├── sighting_of_ref → Indicator/Identity/etc. ("what was sighted")
         ├── observed_data_refs → observed-data ("the observations")
         ├── where_sighted_refs → Identity/Location ("where it was sighted")
         └── extensions → Evidence provenance (1 of 8 types)
```

**Structure**:
```
Sighting (SRO)
├── sighting_of_ref → SDO (what: Indicator, Identity, Infrastructure, etc.)
├── observed_data_refs[] → observed-data (the evidence)
│   └── observed-data.object_refs[] → SCOs (email-message, url, email-addr, etc.)
├── where_sighted_refs[] → Identity/Location (where: company, system, location)
└── extensions (ONE of 8 evidence types)
    ├── sighting-alert (automated detection)
    ├── sighting-anecdote (user report)
    ├── sighting-context (internal query, 100% confidence)
    ├── sighting-exclusion (blocklist check)
    ├── sighting-enrichment (OSINT/paid intel)
    ├── sighting-hunt (threat hunting results)
    ├── sighting-framework (ATT&CK mapping)
    └── sighting-external (external threat intel)
```

**Usage**:
1. Create SCOs (url, email-message, email-addr, user-account, etc.)
2. Create observed-data with `object_refs` containing SCO IDs
3. Create SDO representing "what" (Indicator, Identity, etc.)
4. Create sighting with:
   - `sighting_of_ref` → what was sighted (SDO)
   - `observed_data_refs` → [observed-data ID]
   - `where_sighted_refs` → [company identity, system identity, etc.]
   - Extension matching evidence source (alert, anecdote, context, etc.)

**Evidence Type Selection**:
- **Alert**: Automated SIEM/EDR/IDS detection → `sighting-alert`
- **User Report**: Phishing report, suspicious activity → `sighting-anecdote`
- **Internal Query**: Exchange logs, SAP data, AD query → `sighting-context`
- **Threat Feed**: IOC lookup, reputation check → `sighting-exclusion`
- **Intel Enrichment**: VirusTotal, passive DNS → `sighting-enrichment`
- **Threat Hunt**: Kestrel query, EDR hunt → `sighting-hunt`
- **Framework Map**: ATT&CK technique, kill chain → `sighting-framework`
- **External Report**: MISP feed, vendor report → `sighting-external`

### Pattern 3.4: Event Derivation from Sightings *(from seed 1.4)*

**Description**: Events aggregate one or more sightings to represent confirmed malicious activity, then connect via SRO relationships.

**Dependency Chain**:
```
Level 4: sighting(s) (SRO) - Evidence collection
         ↓ sighting_refs
Level 4: event (SDO) - Derived malicious activity
         ↓ SRO relationships
         ├→ event (led-to) → cascade to next event
         ├→ infrastructure/SCO (impacts) → impact on systems
         └→ location (located-at) → geographic attribution
```

**Structure**:
```
Event (SDO)
├── sighting_refs[] → Sighting IDs (evidence supporting this event)
├── event_types[] → Categorization (phishing, malware execution, data exfiltration)
├── start_time/end_time → Temporal bounds
└── SRO Relationship connections:
    ├── event -[led-to]→ event (cascade/chain of events)
    ├── event -[impacts]→ infrastructure/SCO (affected systems)
    ├── event -[located-at]→ location (geographic context)
    ├── indicator -[based-on]→ event (IOC derived from event)
    └── malware -[performed]→ event (malware attribution)
```

**Event Types** (via `event_types` field - open vocab):
- phishing-attempt
- malware-execution
- data-exfiltration
- credential-theft
- lateral-movement
- privilege-escalation
- persistence-establishment
- defense-evasion

**Usage**:
1. Create sighting(s) capturing raw observations
2. Create event with `sighting_refs` containing sighting IDs
3. Set `event_types` to categorize activity
4. Create SRO relationships:
   - `led-to` relationships to show event progression
   - `impacts` relationships to show affected systems
   - `located-at` relationships for geographic attribution
5. Register event in incident's `event_refs` field
6. Register SRO relationships in incident's `other_object_refs` field

### Pattern 3.5: Task Integration via SRO Relationships *(from seed 1.5)*

**Description**: Tasks coordinate incident response activities, connecting to events, indicators, identities, and other tasks via 15 distinct SRO relationship types.

**Task Embedded References**:
```
Task (SDO - Level 3)
├── owner → identity (who owns this task)
└── changed_objects[] → StateChangeObject
    ├── initial_ref → _any (before state)
    └── result_ref → _any (after state)
```

**Task SRO Relationships**:
```
Task → Relationships
├── task -[uses]→ course-of-action (remediation approach)
├── task -[blocks]→ event (prevents/stops event)
├── task -[causes]→ event (task triggers event)
├── task -[detects]→ event (task discovers event)
├── task -[creates]→ indicator (task produces IOC)
├── task -[impacts]→ infrastructure/SCO (task affects systems)
├── task -[located-at]→ location (task geographic location)
├── task -[errored-to]→ task (task failed, escalated to new task)
├── task -[followed-by]→ task (task sequence in workflow)
├── identity -[assigned]→ task (person assigned to task)
├── identity -[contact-for]→ task (person to contact about task)
├── identity -[participated-in]→ task (person helped with task)
├── identity -[performed]→ task (person executed task)
└── tool -[performed]→ task (tool executed task)
```

**Usage**:
1. Create task SDO with `owner` field (who owns it)
2. Optionally add StateChangeObject entries showing before/after states
3. Create SRO relationships based on task purpose:
   - **Investigation tasks**: `detects` event, `creates` indicator
   - **Remediation tasks**: `blocks` event, `uses` course-of-action
   - **Workflow tasks**: `followed-by` next task, `errored-to` escalation task
4. Create identity assignments: `assigned`, `performed`, `participated-in`
5. Register task in incident's `task_refs` field
6. Register SRO relationships in incident's `other_object_refs` field

**Task Types** (via `task_types` field):
- investigation
- remediation
- containment
- eradication
- recovery
- analysis
- reporting

### Pattern 3.6: Impact Assessment with 7 Extensions *(from seed 1.6)*

**Description**: Impact objects quantify incident damage across 7 dimensions using US DoD impact extensions.

**Structure**:
```
Impact (SDO - Level 3)
├── impacted_refs[] → _any (systems, data, identities affected)
├── superseded_by_ref → impact (updated impact assessment)
├── impact_category → Classification string
├── criticality → Integer severity
├── start_time/end_time → Temporal bounds
├── recoverability → Enum (regular, supplemented, extended, not-recoverable)
└── extensions (ONE or MORE of 7 types):
    ├── availability → availability_impact (integer)
    ├── confidentiality → information_type, loss_type, record_count, record_size
    ├── external → impact_type (reputational, regulatory, etc.)
    ├── integrity → alteration (modification, deletion, etc.), info_type, record_count
    ├── monetary → variety, currency, min/max_amount, conversion_rate
    ├── physical → impact_type, asset_type
    └── traceability → traceability_impact (degraded, lost, etc.)
```

**Extension Selection**:
- **Availability**: System downtime, service disruption → `availability` extension
- **Confidentiality**: Data breach, exposure → `confidentiality` extension
- **External**: Reputation damage, regulatory fines → `external` extension
- **Integrity**: Data corruption, unauthorized modification → `integrity` extension
- **Monetary**: Financial loss, ransom, costs → `monetary` extension
- **Physical**: Equipment damage, facility impact → `physical` extension
- **Traceability**: Evidence loss, log deletion → `traceability` extension

**Usage**:
1. Create impact SDO with base fields (`impact_category`, `criticality`)
2. Add `impacted_refs` pointing to affected systems/data/identities
3. Select appropriate extension(s) matching impact type
4. Optionally use `superseded_by_ref` to track impact updates over time
5. Create SRO relationship: `incident -[impacts]→ identity` (affected entities)
6. Register impact in incident's `impact_refs` field

**Impact Progression**:
```
Initial Impact (time T1)
  ↓ superseded_by_ref
Updated Impact (time T2) - Severity increased
  ↓ superseded_by_ref
Final Impact (time T3) - After remediation
```

### Pattern 3.7: Sequence Workflow Orchestration *(from seed 1.7)*

**Description**: Sequence objects create workflows for events and tasks using linear chains, conditional branching, and parallel execution.

**Structure**:
```
Sequence (SDO - Level 5)
├── sequenced_object → event OR task (the object being sequenced)
├── sequence_type → Enum (event | task)
├── step_type → Enum (start_step | intermediate_step | end_step)
└── Progression fields:
    ├── on_completion → sequence (next step after this completes)
    ├── on_success → sequence (next step if successful)
    ├── on_failure → sequence (next step if failed)
    └── next_steps[] → sequence (parallel next steps)
```

**Workflow Patterns**:

**A. Linear Sequence** (use `on_completion`):
```
Sequence 1 (step_type: start_step)
├── sequenced_object → task_1 (initial task)
└── on_completion → Sequence 2

Sequence 2 (step_type: intermediate_step)
├── sequenced_object → task_2
└── on_completion → Sequence 3

Sequence 3 (step_type: end_step)
└── sequenced_object → task_3 (final task)
```

**B. Conditional Branching** (use `on_success`/`on_failure`):
```
Sequence 1 (investigation task)
├── sequenced_object → task_investigate
├── on_success → Sequence 2 (if IOC confirmed)
└── on_failure → Sequence 3 (if false positive)

Sequence 2 (containment)
└── sequenced_object → task_contain

Sequence 3 (close ticket)
└── sequenced_object → task_close
```

**C. Parallel Execution** (use `next_steps[]`):
```
Sequence 1 (initial detection)
├── sequenced_object → event_alert
└── next_steps → [Sequence 2, Sequence 3, Sequence 4]

Sequence 2 → task_notify_security_team
Sequence 3 → task_isolate_system
Sequence 4 → task_collect_forensics
```

**Usage**:
1. Create all event/task objects first (Level 3-4)
2. Create sequence objects wrapping each event/task:
   - Set `sequenced_object` → event/task ID
   - Set `sequence_type` = "event" or "task"
   - Set `step_type` = "start_step" for entry points
3. Connect sequences:
   - Linear: Use `on_completion` for simple chains
   - Conditional: Use `on_success`/`on_failure` for decision points
   - Parallel: Use `next_steps[]` for concurrent execution
4. Register ALL sequences in incident's `sequence_refs` field
5. Register ONLY start sequences in incident's `sequence_start_refs` field

### Pattern 3.8: Email Message Communication Graph *(NEW - from templates)*

**Description**: Email messages connect to multiple email addresses (from, to, cc, bcc) and can reference raw email artifacts.

**Dependency Chain**:
```
Level 0: user-account (SCO)
         ↓ belongs_to_ref
Level 1: email-addr (SCO)
         ↓ from_ref, to_refs, cc_refs, bcc_refs
Level 2: email-message (SCO)
         └→ raw_email_ref → artifact (SCO - not yet implemented)
```

**Structure**:
```
email-message (SCO)
├── is_multipart → boolean
├── from_ref → email-addr (sender)
├── sender_ref → email-addr (if different from from_ref)
├── to_refs[] → email-addr (primary recipients)
├── cc_refs[] → email-addr (carbon copy)
├── bcc_refs[] → email-addr (blind carbon copy)
├── subject → string (email subject line)
├── body → string (plain text body)
├── body_multipart[] → EmailMIMEComponent (attachments, HTML, etc.)
│   └── body_raw_ref → artifact/file (attachment content)
└── raw_email_ref → artifact (complete .eml file)
```

**Usage** (Phishing Email Example):
1. Create victim user-account (e.g., `user_id`: "jdoe")
2. Create victim email-addr with `belongs_to_ref` → user-account
3. Create attacker email-addr (may not have user-account)
4. Create email-message:
   - `from_ref` → attacker email-addr
   - `to_refs` → [victim email-addr]
   - `subject` → "Urgent: Password Reset Required"
   - `body` → Email content with suspicious link
5. Create URL SCO for malicious link
6. Create observed-data containing email-message and URL
7. Create SRO relationship: `email-message -[contains]→ url`
8. Create sighting referencing observed-data with `sighting-alert` extension

### Pattern 3.9: Anecdote Provenance *(NEW - from templates)*

**Description**: Anecdote SCOs capture narrative evidence from specific people, tracking who provided the information.

**Structure**:
```
anecdote (SCO - Level 1)
├── value → string (the narrative/description)
├── report_date → timestamp (when reported)
└── provided_by_ref → identity (who reported it)
```

**Usage**:
1. Create identity for person providing anecdote (if not exists)
2. Create anecdote SCO:
   - `value` → "User reports clicking on link and seeing unusual browser behavior..."
   - `report_date` → timestamp of report
   - `provided_by_ref` → identity of reporting person
3. Create observed-data containing anecdote
4. Create sighting with `sighting-anecdote` extension:
   - `observed_data_refs` → [observed-data with anecdote]
   - `sighting_of_ref` → impact/event being reported
   - Extension fields: `person_name`, `person_context`, `report_submission`

**Use Cases**:
- User reports phishing emails
- Witness accounts of physical security incidents
- User-reported suspicious activity
- Impact statements from affected parties
- Timeline narrative from incident participants

### Pattern 3.10: Impact Supersession Chain *(NEW - from templates)*

**Description**: Impact objects can be updated over time as incident progresses, creating an impact evolution timeline.

**Structure**:
```
Initial Impact (T1)
├── criticality → 50 (moderate)
├── impacted_refs → [server-1]
├── extensions.confidentiality
│   └── record_count → 100
└── superseded_by_ref → Updated Impact (T2)

Updated Impact (T2)
├── criticality → 80 (high)
├── impacted_refs → [server-1, server-2, database-1]
├── extensions.confidentiality
│   └── record_count → 10000 (scope increased)
└── superseded_by_ref → Final Impact (T3)

Final Impact (T3)
├── criticality → 30 (low - after remediation)
├── impacted_refs → [database-1] (servers recovered)
├── extensions.confidentiality
│   └── record_count → 5000 (refined estimate)
└── superseded_by_ref → null (current assessment)
```

**Usage**:
1. Create initial impact when first detected
2. As incident progresses and scope changes:
   - Create new impact with updated fields
   - Set previous impact's `superseded_by_ref` → new impact ID
3. Final impact after remediation shows residual damage
4. All impacts in chain registered in incident's `impact_refs` field

**Traversal**: Follow `superseded_by_ref` chain from initial → final for complete impact timeline.

### Pattern 3.11: Task Ownership vs Creation *(NEW - from templates)*

**Description**: Tasks distinguish between who created the task (`created_by_ref`) and who owns/executes it (`owner`).

**Structure**:
```
task (SDO)
├── created_by_ref → identity (incident commander who created task)
├── owner → identity (analyst who owns/executes task)
├── SRO relationships:
│   ├── identity -[assigned]→ task (formal assignment)
│   ├── identity -[performed]→ task (who did the work)
│   └── identity -[participated-in]→ task (helpers/contributors)
```

**Usage**:
1. Incident commander creates task:
   - `created_by_ref` → commander identity
   - `owner` → assigned analyst identity
2. Create SRO: `commander -[assigned]→ task`
3. After task completion, create SRO: `analyst -[performed]→ task`
4. If others helped, create SRO: `helper -[participated-in]→ task`

**Distinction**:
- `created_by_ref`: **Who initiated** the task (ticket creator)
- `owner`: **Who is responsible** for task (current assignee)
- `assigned` relationship: **Formal assignment** (may be reassigned)
- `performed` relationship: **Who actually executed** the task

### Pattern 3.12: State Change Tracking *(NEW - from templates)*

**Description**: Event and Task objects can track object state changes using StateChangeObject sub-objects.

**Structure**:
```
event/task (SDO)
└── changed_objects[] → StateChangeObject
    ├── state_change_type → string (description of change)
    ├── initial_ref → _any (object before change)
    └── result_ref → _any (object after change)
```

**Usage Examples**:

**A. Event State Change** (Malware Modified File):
```
Event (malware-execution)
└── changed_objects[0]
    ├── state_change_type → "file_encrypted"
    ├── initial_ref → file--original-id (clean file)
    └── result_ref → file--encrypted-id (encrypted file)
```

**B. Task State Change** (Password Reset):
```
Task (reset-compromised-password)
└── changed_objects[0]
    ├── state_change_type → "credential_rotated"
    ├── initial_ref → user-account--old-id (old password)
    └── result_ref → user-account--new-id (new password)
```

**C. Impact State Change** (System Restored):
```
Task (system-restoration)
└── changed_objects[0]
    ├── state_change_type → "availability_restored"
    ├── initial_ref → impact--degraded-id (system down)
    └── result_ref → impact--restored-id (system operational)
```

### Pattern 3.13: Sequence Conditional Workflows *(NEW - from templates)*

**Description**: Sequence objects support conditional branching beyond simple `on_completion`, enabling decision trees and error handling.

**Structure**:
```
sequence (SDO)
├── on_completion → sequence (always execute next)
├── on_success → sequence (execute if sequenced_object succeeds)
├── on_failure → sequence (execute if sequenced_object fails)
└── next_steps[] → sequence (parallel execution)
```

**Decision Tree Example**:
```
S1: Analyze Alert
├── on_success → S2 (true positive path)
└── on_failure → S3 (false positive path)

S2: True Positive Branch
├── sequenced_object → task_contain_threat
└── on_completion → S4

S3: False Positive Branch
├── sequenced_object → task_tune_detection
└── on_completion → S5

S4: Escalate to Incident
└── sequenced_object → task_create_incident

S5: Close Alert
└── sequenced_object → task_close_ticket
```

**Error Handling Example**:
```
S1: Automated Remediation
├── sequenced_object → task_auto_block_ip
├── on_success → S2 (automation succeeded)
└── on_failure → S3 (automation failed)

S2: Verify Remediation
└── sequenced_object → task_verify_block

S3: Manual Escalation
└── sequenced_object → task_manual_intervention
```

**Parallel with Convergence**:
```
S1: Initial Investigation
├── next_steps → [S2, S3, S4] (parallel execution)

S2: Check Endpoint → on_completion → S5
S3: Check Network → on_completion → S5
S4: Check Email Gateway → on_completion → S5

S5: Consolidate Findings
└── sequenced_object → task_final_analysis
```

## 4. Complete Embedded Reference Catalog

All ReferenceProperty and OSThreatReference fields across 15 object types.

### 4.1 SDO Embedded References

| Object Type | Field Name | Reference Type | Valid Types | Level |
|------------|-----------|----------------|-------------|-------|
| identity | created_by_ref | ReferenceProperty | identity | - |
| identity | EmailContact.email_address_ref | ReferenceProperty | email-addr | 2 |
| identity | SocialMediaContact.user_account_ref | ReferenceProperty | user-account | 2 |
| indicator | created_by_ref | ReferenceProperty | identity | 0 |
| impact | created_by_ref | ReferenceProperty | identity | 3 |
| impact | impacted_refs | OSThreatReference | _any | 3 |
| impact | superseded_by_ref | OSThreatReference | impact | 3 |
| incident | created_by_ref | ReferenceProperty | identity | 6 |
| incident | sequence_start_refs | OSThreatReference | sequence | 6 |
| incident | sequence_refs | OSThreatReference | sequence | 6 |
| incident | task_refs | OSThreatReference | task | 6 |
| incident | event_refs | OSThreatReference | event | 6 |
| incident | impact_refs | OSThreatReference | impact | 6 |
| incident | other_object_refs | OSThreatReference | _any | 6 |
| event | created_by_ref | ReferenceProperty | identity | 4 |
| event | sighting_refs | OSThreatReference | _any | 4 |
| event | StateChangeObject.initial_ref | OSThreatReference | _any | 4 |
| event | StateChangeObject.result_ref | OSThreatReference | _any | 4 |
| observed-data | created_by_ref | ReferenceProperty | identity | 3 |
| observed-data | object_refs | ReferenceProperty | _any | 3 |
| sequence | created_by_ref | ReferenceProperty | identity | 5 |
| sequence | sequenced_object | OSThreatReference | event, task | 5 |
| sequence | on_completion | OSThreatReference | sequence | 5 |
| sequence | on_success | OSThreatReference | sequence | 5 |
| sequence | on_failure | OSThreatReference | sequence | 5 |
| sequence | next_steps | OSThreatReference | sequence | 5 |
| task | created_by_ref | ReferenceProperty | identity | 3 |
| task | owner | ReferenceProperty | identity | 3 |
| task | StateChangeObject.initial_ref | ReferenceProperty | _any | 3 |
| task | StateChangeObject.result_ref | ReferenceProperty | _any | 3 |

**Total SDO Embedded References**: 30 fields across 9 object types

### 4.2 SCO Embedded References

| Object Type | Field Name | Reference Type | Valid Types | Level |
|------------|-----------|----------------|-------------|-------|
| anecdote | provided_by_ref | ReferenceProperty | identity | 1 |
| email-addr | belongs_to_ref | ReferenceProperty | user-account | 1 |
| user-account | (none) | - | - | 0 |
| url | (none) | - | - | 0 |
| email-message | from_ref | ReferenceProperty | email-addr | 2 |
| email-message | sender_ref | ReferenceProperty | email-addr | 2 |
| email-message | to_refs | ReferenceProperty | email-addr | 2 |
| email-message | cc_refs | ReferenceProperty | email-addr | 2 |
| email-message | bcc_refs | ReferenceProperty | email-addr | 2 |
| email-message | raw_email_ref | ReferenceProperty | artifact | 2 |
| email-message | EmailMIMEComponent.body_raw_ref | ReferenceProperty | artifact, file | 2 |

**Total SCO Embedded References**: 11 fields across 5 object types (2 objects have no references)

### 4.3 SRO Embedded References

| Object Type | Field Name | Reference Type | Valid Types | Level |
|------------|-----------|----------------|-------------|-------|
| relationship | created_by_ref | ReferenceProperty | identity | 5 |
| relationship | source_ref | ReferenceProperty | _any | 5 |
| relationship | target_ref | ReferenceProperty | _any | 5 |
| sighting | created_by_ref | ReferenceProperty | identity | 4 |
| sighting | sighting_of_ref | ReferenceProperty | _sdo | 4 |
| sighting | observed_data_refs | ReferenceProperty | observed-data | 4 |
| sighting | where_sighted_refs | ReferenceProperty | identity, location | 4 |

**Total SRO Embedded References**: 7 fields across 2 object types

**GRAND TOTAL**: 48 embedded reference fields across 15 object types (excludes `object_marking_refs` and `granular_markings` present in all objects)

## 5. Complete SRO Relationship Type Catalog

26 relationship_type values with source/target constraints (from seed 1.1 table).

### 5.1 Event Relationships (4 types)

| Source | relationship_type | Target | Description |
|--------|------------------|--------|-------------|
| event | led-to | event | Event caused or triggered another event (cascade) |
| event | impacts | infrastructure, _sco | Event affected infrastructure or cyber objects |
| event | located-at | location | Event occurred at this geographic location |
| malware | performed | event | Malware executed this event |

### 5.2 Task Relationships (10 types)

| Source | relationship_type | Target | Description |
|--------|------------------|--------|-------------|
| task | blocks | event | Task prevents or stops event from occurring |
| task | causes | event | Task triggers or creates event |
| task | detects | event | Task discovers or identifies event |
| task | creates | indicator | Task produces indicator (IOC) |
| task | impacts | infrastructure, _sco | Task affects infrastructure or cyber objects |
| task | located-at | location | Task performed at this geographic location |
| task | uses | course-of-action | Task employs this remediation/mitigation approach |
| task | errored-to | task | Task failed and escalated to new task |
| task | followed-by | task | Task followed in sequence by next task |
| tool | performed | task, event | Tool executed this task or event |

### 5.3 Identity Relationships (4 types)

| Source | relationship_type | Target | Description |
|--------|------------------|--------|-------------|
| identity | assigned | task | Person formally assigned to task |
| identity | contact-for | task, incident | Person is point of contact for task/incident |
| identity | participated-in | task | Person contributed to task execution |
| identity | performed | task | Person executed/completed task |

### 5.4 Incident Relationships (5 types)

| Source | relationship_type | Target | Description |
|--------|------------------|--------|-------------|
| incident | attributed-to | intrusion-set | Incident attributed to threat actor group |
| incident | impacts | identity | Incident affected this person/organization |
| incident | led-to | incident | Incident caused or triggered another incident |
| incident | located-at | location | Incident occurred at this geographic location |
| incident | targets | identity | Incident targeted this person/organization |

### 5.5 Indicator Relationships (2 types)

| Source | relationship_type | Target | Description |
|--------|------------------|--------|-------------|
| indicator | based-on | event | Indicator derived from analysis of event |
| indicator | detected | incident | Indicator matched and detected this incident |

### 5.6 Campaign Relationship (1 type)

| Source | relationship_type | Target | Description |
|--------|------------------|--------|-------------|
| campaign | associated-with | incident | Campaign is related to incident |

**Total**: 26 relationship_type values with specific source/target constraints

## 6. Context Memory Architecture

All incidents stored in hierarchical directory structure for efficient retrieval and incident reconstitution.

### 6.1 Directory Structure

```
context_memory/
├── users/
│   └── {analyst_identity_id}/
│       └── profile.json (analyst identity object)
├── companies/
│   └── {company_identity_id}/
│       ├── profile.json (company identity object)
│       ├── users/ (company employee identities)
│       ├── systems/ (IT infrastructure identities)
│       └── incidents/
│           └── {incident_id}/
│               ├── incident.json (incident SDO)
│               ├── events/ (event SDOs)
│               ├── tasks/ (task SDOs)
│               ├── impacts/ (impact SDOs)
│               ├── sequences/ (sequence SDOs)
│               ├── sightings/ (sighting SROs)
│               ├── relationships/ (relationship SROs)
│               ├── observed_data/ (observed-data SDOs)
│               ├── indicators/ (indicator SDOs)
│               └── scos/ (SCOs: email-addr, user-account, url, email-message, anecdote)
```

### 6.2 Incident Reconstitution Process

**Given**: Incident ID (e.g., `incident--d1cdb31f-8e54-4bdd-b3f9-ce9d0c94acc8`)

**Steps**:
1. Load `incident.json` from `context_memory/companies/{company_id}/incidents/{incident_id}/`
2. Parse IncidentCoreExt extension to get 6 `_refs` fields:
   - `event_refs[]` → Load from `events/` directory
   - `task_refs[]` → Load from `tasks/` directory
   - `impact_refs[]` → Load from `impacts/` directory
   - `sequence_refs[]` → Load from `sequences/` directory
   - `sequence_start_refs[]` → Subset of `sequence_refs` (entry points)
   - `other_object_refs[]` → Load from appropriate directories (sightings/, relationships/, observed_data/, indicators/, scos/)
3. For each loaded object, recursively resolve embedded references:
   - Sighting → `observed_data_refs` → observed-data → `object_refs` → SCOs
   - Event → `sighting_refs` → Sighting objects
   - Sequence → `sequenced_object`, `on_completion`, etc. → Other sequences, events, tasks
   - Identity → EmailContact.`email_address_ref` → email-addr → `belongs_to_ref` → user-account
4. Load all SRO relationships from `relationships/` and `sightings/` directories
5. Build complete graph: All objects + all embedded refs + all SRO relationships

**Result**: Complete incident graph with all objects, dependencies, and semantic relationships.

## 7. Summary: Seed vs Enhanced Documentation

### 7.1 Original Seed Coverage

**From `a_seed/5_graph_pattern_nature_of_stix.md`**:

✅ **Covered Patterns** (7):
1. US DoD Incident Extension Definition Pattern (IncidentCoreExt) - Section 1.1
2. User Account, Email Address and Identity Sub Pattern - Section 1.2
3. Observed-Data, Sighting and Sighting Extension Sub Pattern - Section 1.3
4. Event Derivation from Sightings - Section 1.4
5. Task Integration via SRO Relationships - Section 1.5
6. Impact Object with 7 Extensions - Section 1.6
7. Summary of Graph Nature - Section 1.8

⚠️ **Incomplete**:
- Email Message pattern - Section 1.7 (title only, no content)

✅ **Included Data**:
- Dual graph network concept (embedded refs + SRO relationships)
- 26 SRO relationship_type values with source/target table
- 8 sighting evidence extension types
- 7 impact extension types
- Basic dependency hierarchy concept
- IncidentCoreExt 6 `_refs` fields

### 7.2 Enhanced Documentation Additions

**NEW Patterns** (6):
1. ✨ **Pattern 3.8**: Email Message Communication Graph (completed section 1.7)
2. ✨ **Pattern 3.9**: Anecdote Provenance
3. ✨ **Pattern 3.10**: Impact Supersession Chain
4. ✨ **Pattern 3.11**: Task Ownership vs Creation
5. ✨ **Pattern 3.12**: State Change Tracking (Event/Task StateChangeObject)
6. ✨ **Pattern 3.13**: Sequence Conditional Workflows (on_success/on_failure)

**NEW Documentation**:
- ✨ Complete 7-level dependency hierarchy (Level 0-6) with build order
- ✨ All 48 embedded reference fields cataloged
- ✨ Embedded reference types explained (ReferenceProperty vs OSThreatReference)
- ✨ Template-based field discovery (all 15 template files analyzed)
- ✨ Context memory directory structure
- ✨ Incident reconstitution process
- ✨ Sub-object reference patterns (EmailContact, SocialMediaContact, EmailMIMEComponent, StateChangeObject)
- ✨ Detailed usage examples for each pattern
- ✨ Extension selection guides (sighting evidence types, impact types)

**Enhanced Existing Patterns**:
- ✅ Pattern 3.1 (Incident): Added complete field-by-field breakdown of IncidentCoreExt
- ✅ Pattern 3.2 (Identity): Added IdentityContact extension details with 3 sub-object types
- ✅ Pattern 3.3 (Sighting): Added all 8 evidence extension field details
- ✅ Pattern 3.4 (Event): Added StateChangeObject sub-object pattern
- ✅ Pattern 3.5 (Task): Added owner field, StateChangeObject, and all 15 relationship types
- ✅ Pattern 3.6 (Impact): Added all 7 impact extension field details and supersession
- ✅ Pattern 3.7 (Sequence): Added conditional branching fields (on_success/on_failure)

### 7.3 Coverage Metrics

| Aspect | Seed | Enhanced | Improvement |
|--------|------|----------|-------------|
| **Graph Patterns Documented** | 7 (1 incomplete) | 13 (all complete) | +6 patterns |
| **Dependency Levels Defined** | Concept only | 7 levels (0-6) explicit | Full hierarchy |
| **Embedded References Cataloged** | ~10 mentioned | 48 complete | +38 references |
| **Object Types Analyzed** | 9 (partial) | 15 (complete) | +6 objects |
| **Template Files Reviewed** | 0 | 15 | +15 templates |
| **SRO Relationships** | 26 (table) | 26 (table + patterns) | Enhanced context |
| **Evidence Types** | 8 (names) | 8 (full field details) | Field-level docs |
| **Impact Types** | 7 (names) | 7 (full field details) | Field-level docs |
| **Sequence Workflow Patterns** | Linear only | Linear + Conditional + Parallel | +2 patterns |
| **Usage Examples** | Minimal | Comprehensive | Complete guides |

### 7.4 Document Purpose & Usage

**For AI/Human Readers**:
- ✅ Complete STIX graph reference - no need to consult multiple sources
- ✅ Dependency hierarchy enables correct build order
- ✅ Pattern catalog provides templates for common scenarios
- ✅ Embedded reference catalog enables object relationship validation
- ✅ SRO catalog enables semantic relationship construction
- ✅ Context memory architecture enables incident storage/retrieval

**For Notebook Development** (Tasks 2-3):
- ✅ Pattern examples guide notebook cell structure
- ✅ Dependency hierarchy determines notebook sequencing
- ✅ Usage examples become notebook markdown narratives
- ✅ Build order ensures objects created before referenced
- ✅ Extension catalogs guide data collection requirements

**For Incident Reconstitution**:
- ✅ IncidentCoreExt 6 `_refs` fields provide entry points
- ✅ Embedded reference chains enable recursive object loading
- ✅ SRO relationships enable semantic graph traversal
- ✅ Context memory structure enables efficient file retrieval

---

**End of Document** | Total Length: ~1,200 lines | Created: Task 1 (Sequential Thinking Analysis) | Source: a_seed/5_graph_pattern_nature_of_stix.md + 15 Template Files Analysis
