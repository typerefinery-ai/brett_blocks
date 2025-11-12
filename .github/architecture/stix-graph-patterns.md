# STIX Graph Patterns - Complete Object Linkage Map

## Document Purpose

This document provides an exhaustive map of all embedded reference connections and SRO relationship patterns for the current StixORM objects. Every object class, field name, and valid type is explicitly defined to enable complete hierarchy reconstitution.

---

## 1. EMBEDDED REFERENCE GRAPH (ReferenceProperty & OSThreatReference)

### 1.1 SDO (STIX Domain Objects)

#### identity
**Class:** Identity  
**Type:** identity

**Embedded Reference Fields:**
- `created_by_ref` : ReferenceProperty → [identity]
- `object_marking_refs` : ListProperty<ReferenceProperty> → [marking-definition]
- **Extension: extension-definition--66e2492a-bbd3-4be6-88f5-cc91a017a498**
  - **Sub-object: EmailContact**
    - `email_address_ref` : ReferenceProperty → [email-addr] (required)
  - **Sub-object: SocialMediaContact**
    - `user_account_ref` : ReferenceProperty → [email-addr] (required) *Note: template shows email-addr but logically should be user-account*

---

#### indicator
**Class:** Indicator  
**Type:** indicator

**Embedded Reference Fields:**
- `created_by_ref` : ReferenceProperty → [identity]
- `object_marking_refs` : ListProperty<ReferenceProperty> → [marking-definition]

---

#### impact
**Class:** Impact  
**Type:** impact

**Embedded Reference Fields:**
- `created_by_ref` : ReferenceProperty → [identity]
- `object_marking_refs` : ListProperty<ReferenceProperty> → [marking-definition]
- `impacted_refs` : ListProperty<OSThreatReference> → [_any]
- `superseded_by_ref` : OSThreatReference → [impact]

**Extensions:** 7 impact type extensions (availability, confidentiality, external, integrity, monetary, physical, traceability) - no additional reference fields

---

#### incident
**Class:** Incident  
**Type:** incident

**Embedded Reference Fields:**
- `created_by_ref` : ReferenceProperty → [identity]
- `object_marking_refs` : ListProperty<ReferenceProperty> → [marking-definition]
- **Extension: extension-definition--ef765651-680c-498d-9894-99799f2fa126 (Incident Core)**
  - `sequence_start_refs` : ListProperty<OSThreatReference> → [sequence]
  - `sequence_refs` : ListProperty<OSThreatReference> → [sequence]
  - `task_refs` : ListProperty<OSThreatReference> → [task]
  - `event_refs` : ListProperty<OSThreatReference> → [event]
  - `impact_refs` : ListProperty<OSThreatReference> → [impact]
  - `other_object_refs` : ListProperty<OSThreatReference> → [_any]

---

#### event
**Class:** Event  
**Type:** event

**Embedded Reference Fields:**
- `created_by_ref` : ReferenceProperty → [identity]
- `object_marking_refs` : ListProperty<ReferenceProperty> → [marking-definition]
- `sighting_refs` : ListProperty<OSThreatReference> → [_any]
- **Sub-object: StateChangeObject** (in `changed_objects`)
  - `initial_ref` : OSThreatReference → [_any]
  - `result_ref` : OSThreatReference → [_any]

---

#### observed-data
**Class:** ObservedData  
**Type:** observed-data

**Embedded Reference Fields:**
- `created_by_ref` : ReferenceProperty → [identity]
- `object_marking_refs` : ListProperty<ReferenceProperty> → [marking-definition]
- `object_refs` : ListProperty<ReferenceProperty> → [_any]

---

#### sequence
**Class:** Sequence  
**Type:** sequence

**Embedded Reference Fields:**
- `created_by_ref` : ReferenceProperty → [identity]
- `object_marking_refs` : ListProperty<ReferenceProperty> → [marking-definition]
- `sequenced_object` : OSThreatReference → [event, task]
- `on_completion` : OSThreatReference → [sequence]
- `on_success` : OSThreatReference → [sequence]
- `on_failure` : OSThreatReference → [sequence]
- `next_steps` : ListProperty<OSThreatReference> → [sequence]

---

#### task
**Class:** Task  
**Type:** task

**Embedded Reference Fields:**
- `created_by_ref` : ReferenceProperty → [identity]
- `object_marking_refs` : ListProperty<ReferenceProperty> → [marking-definition]
- `owner` : ReferenceProperty → [identity]
- **Sub-object: StateChangeObject** (in `changed_objects`)
  - `initial_ref` : ReferenceProperty → [_any]
  - `result_ref` : ReferenceProperty → [_any]

---

### 1.2 SCO (STIX Cyber Observable Objects)

#### anecdote
**Class:** Anecdote  
**Type:** anecdote

**Embedded Reference Fields:**
- `object_marking_refs` : ListProperty<ReferenceProperty> → [marking-definition]
- `provided_by_ref` : ReferenceProperty → [identity]

---

#### email-addr
**Class:** EmailAddress  
**Type:** email-addr

**Embedded Reference Fields:**
- `object_marking_refs` : ListProperty<ReferenceProperty> → [marking-definition]
- `belongs_to_ref` : ReferenceProperty → [user-account]

---

#### user-account
**Class:** UserAccount  
**Type:** user-account

**Embedded Reference Fields:**
- `object_marking_refs` : ListProperty<ReferenceProperty> → [marking-definition]

---

#### url
**Class:** URL  
**Type:** url

**Embedded Reference Fields:**
- `object_marking_refs` : ListProperty<ReferenceProperty> → [marking-definition]

---

#### email-message
**Class:** EmailMessage  
**Type:** email-message

**Embedded Reference Fields:**
- `object_marking_refs` : ListProperty<ReferenceProperty> → [marking-definition]
- `from_ref` : ReferenceProperty → [email-addr]
- `sender_ref` : StringProperty (template shows StringProperty but parameters indicate email-addr - likely error)
- `to_refs` : ListProperty<ReferenceProperty> → [email-addr]
- `cc_refs` : ListProperty<ReferenceProperty> → [email-addr]
- `bcc_refs` : ListProperty<ReferenceProperty> → [email-addr]
- `raw_email_ref` : ReferenceProperty → [artifact]
- **Sub-object: EmailMIMEComponent** (in `body_multipart`)
  - `body_raw_ref` : ReferenceProperty → [artifact, file]

---

### 1.3 SRO (STIX Relationship Objects)

#### relationship
**Class:** Relationship  
**Type:** relationship

**Embedded Reference Fields:**
- `created_by_ref` : ReferenceProperty → [identity]
- `object_marking_refs` : ListProperty<ReferenceProperty> → [marking-definition]
- `source_ref` : ReferenceProperty → [_any] (required) - excludes: bundle, language-content, marking-definition, relationship, sighting
- `target_ref` : ReferenceProperty → [_any] (required) - excludes: bundle, language-content, marking-definition, relationship, sighting

**Note:** The `relationship_type` field constrains valid source/target combinations (see Section 2 below)

---

#### sighting
**Class:** Sighting  
**Type:** sighting

**Embedded Reference Fields:**
- `created_by_ref` : ReferenceProperty → [identity]
- `object_marking_refs` : ListProperty<ReferenceProperty> → [marking-definition]
- `sighting_of_ref` : ReferenceProperty → [_sdo] (required)
- `observed_data_refs` : ListProperty<ReferenceProperty> → [observed-data] (required)
- `where_sighted_refs` : ListProperty<ReferenceProperty> → [identity, location] (required)

**Extensions:** 7 sighting evidence types (sighting-alert, sighting-anecdote, sighting-context, sighting-exclusion, sighting-enrichment, sighting-hunt, sighting-framework, sighting-external) - no additional reference fields

---

## 2. SRO RELATIONSHIP TYPE GRAPH

These relationship_type values constrain which source/target object type combinations are valid.

### 2.1 Event Relationship Types

| source_ref | relationship_type | target_ref |
|------------|------------------|------------|
| event | impacts | infrastructure |
| event | led-to | event |
| event | located-at | location |
| event | observed | _sco |
| indicator | based-on | event |
| malware | performed | event |

### 2.2 Task Relationship Types

| source_ref | relationship_type | target_ref |
|------------|------------------|------------|
| task | uses | course-of-action |
| task | blocks | event |
| task | causes | event |
| task | detects | event |
| task | creates | indicator |
| task | impacts | infrastructure, _sco |
| task | located-at | location |
| task | errored-to | task |
| task | followed-by | task |
| identity | assigned | task |
| identity | contact-for | task, incident |
| identity | participated-in | task |
| identity | performed | task |
| tool | performed | event, task |

### 2.3 Incident Relationship Types

| source_ref | relationship_type | target_ref |
|------------|------------------|------------|
| incident | attributed-to | intrusion-set |
| incident | impacts | identity |
| incident | led-to | incident |
| incident | located-at | location |
| incident | targets | identity |
| campaign | associated-with | incident |
| indicator | detected | incident |

---

## 3. DEPENDENCY HIERARCHY (Bottom-Up Creation Order)

### Level 0: Foundation Objects (No External References)
- **user-account** - only marking-definition refs
- **url** - only marking-definition refs

### Level 1: Single Reference Dependencies
- **email-addr** → requires: user-account
- **anecdote** → requires: identity (via provided_by_ref)

### Level 2: Identity Layer
- **identity** → requires: identity (self for created_by_ref), email-addr, user-account (via extension)

### Level 3: Observable Data & Impacts
- **observed-data** → requires: identity, any SCOs
- **impact** → requires: identity, optional any objects (impacted_refs), optional impact (superseded_by_ref)
- **indicator** → requires: identity
- **email-message** → requires: email-addr, artifact, file

### Level 4: Evidence & Workflows
- **sighting** → requires: identity, any SDO (sighting_of_ref), observed-data, identity/location (where_sighted_refs)
- **event** → requires: identity, any objects (sighting_refs, StateChangeObject refs)
- **task** → requires: identity (created_by_ref, owner), any objects (StateChangeObject refs)
- **sequence** → requires: identity, event/task (sequenced_object), sequence (workflow chain refs)

### Level 5: Top-Level Orchestration
- **incident** → requires: identity, sequence, task, event, impact, any objects (other_object_refs)
- **relationship** → requires: identity, any two valid objects (source_ref, target_ref)

---

## 4. COMPLETE OBJECT REFERENCE MATRIX

This matrix shows every object and what it CAN reference:

| Object Type | Can Reference (Field Name → Object Types) |
|-------------|-------------------------------------------|
| identity | created_by_ref→identity, object_marking_refs→marking-definition, EmailContact.email_address_ref→email-addr, SocialMediaContact.user_account_ref→email-addr |
| indicator | created_by_ref→identity, object_marking_refs→marking-definition |
| impact | created_by_ref→identity, object_marking_refs→marking-definition, impacted_refs→_any, superseded_by_ref→impact |
| incident | created_by_ref→identity, object_marking_refs→marking-definition, sequence_start_refs→sequence, sequence_refs→sequence, task_refs→task, event_refs→event, impact_refs→impact, other_object_refs→_any |
| event | created_by_ref→identity, object_marking_refs→marking-definition, sighting_refs→_any, StateChangeObject.initial_ref→_any, StateChangeObject.result_ref→_any |
| observed-data | created_by_ref→identity, object_marking_refs→marking-definition, object_refs→_any |
| sequence | created_by_ref→identity, object_marking_refs→marking-definition, sequenced_object→event/task, on_completion→sequence, on_success→sequence, on_failure→sequence, next_steps→sequence |
| task | created_by_ref→identity, object_marking_refs→marking-definition, owner→identity, StateChangeObject.initial_ref→_any, StateChangeObject.result_ref→_any |
| anecdote | object_marking_refs→marking-definition, provided_by_ref→identity |
| email-addr | object_marking_refs→marking-definition, belongs_to_ref→user-account |
| user-account | object_marking_refs→marking-definition |
| url | object_marking_refs→marking-definition |
| email-message | object_marking_refs→marking-definition, from_ref→email-addr, to_refs→email-addr, cc_refs→email-addr, bcc_refs→email-addr, raw_email_ref→artifact, EmailMIMEComponent.body_raw_ref→artifact/file |
| relationship | created_by_ref→identity, object_marking_refs→marking-definition, source_ref→_any, target_ref→_any |
| sighting | created_by_ref→identity, object_marking_refs→marking-definition, sighting_of_ref→_sdo, observed_data_refs→observed-data, where_sighted_refs→identity/location |

---

## 5. COMPLETE REVERSE REFERENCE MATRIX

This matrix shows what objects CAN BE referenced by others:

| Object Type | Referenced By (Object Type.Field Name) |
|-------------|----------------------------------------|
| identity | identity.created_by_ref, indicator.created_by_ref, impact.created_by_ref, incident.created_by_ref, event.created_by_ref, observed-data.created_by_ref, sequence.created_by_ref, task.created_by_ref, task.owner, anecdote.provided_by_ref, relationship.created_by_ref, sighting.created_by_ref, sighting.where_sighted_refs |
| email-addr | identity.EmailContact.email_address_ref, email-message.from_ref, email-message.to_refs, email-message.cc_refs, email-message.bcc_refs |
| user-account | email-addr.belongs_to_ref, identity.SocialMediaContact.user_account_ref |
| marking-definition | ALL_OBJECTS.object_marking_refs |
| sequence | incident.sequence_start_refs, incident.sequence_refs, sequence.on_completion, sequence.on_success, sequence.on_failure, sequence.next_steps |
| task | incident.task_refs, sequence.sequenced_object |
| event | incident.event_refs, sequence.sequenced_object |
| impact | incident.impact_refs, impact.superseded_by_ref |
| observed-data | sighting.observed_data_refs |
| _any (any SDO) | sighting.sighting_of_ref |
| _any (any object) | impact.impacted_refs, incident.other_object_refs, event.sighting_refs, event.StateChangeObject.initial_ref, event.StateChangeObject.result_ref, observed-data.object_refs, task.StateChangeObject.initial_ref, task.StateChangeObject.result_ref, relationship.source_ref, relationship.target_ref |
| artifact | email-message.raw_email_ref, email-message.EmailMIMEComponent.body_raw_ref |
| file | email-message.EmailMIMEComponent.body_raw_ref |
| location | sighting.where_sighted_refs |

---

## 6. SUB-GRAPH PATTERNS

### Pattern 6.1: User Identity Setup
**Order:** user-account → email-addr → identity

1. Create **user-account** (no dependencies except marking-definition)
2. Create **email-addr** with `belongs_to_ref`→user-account
3. Create **identity** with extension-definition--66e2492a-bbd3-4be6-88f5-cc91a017a498
   - Add EmailContact sub-object with `email_address_ref`→email-addr
   - Add SocialMediaContact sub-object with `user_account_ref`→user-account

**Storage:** All stored in incident.other_object_refs

---

### Pattern 6.2: Evidence Collection (Sighting-Based)
**Order:** SCOs → observed-data → sighting

1. Create **SCO objects** (email-addr, url, user-account, email-message, anecdote, etc.)
2. Create **observed-data** with `object_refs`→list of SCO IDs
3. Create **sighting** with:
   - `sighting_of_ref`→SDO (what was sighted, e.g., indicator, event)
   - `observed_data_refs`→list of observed-data IDs
   - `where_sighted_refs`→list of identity/location IDs
   - Add sighting extension (sighting-alert, sighting-anecdote, sighting-context, etc.)

**Storage:** sighting and observed-data in incident.other_object_refs

---

### Pattern 6.3: Event Creation from Evidence
**Order:** sightings → event

1. Create **sighting(s)** following Pattern 6.2
2. Create **event** with:
   - `sighting_refs`→list of sighting IDs
   - `changed_objects`→StateChangeObject sub-objects if state changed
   - `created_by_ref`→identity

**Storage:** event in incident.event_refs, sightings in incident.other_object_refs

**SRO Relationships:** event can connect via relationships to infrastructure, other events, locations, SCOs

---

### Pattern 6.4: Task Creation with Ownership
**Order:** identity → task

1. Create **identity** for owner/assignee
2. Create **task** with:
   - `owner`→identity ID
   - `created_by_ref`→identity ID
   - `changed_objects`→StateChangeObject sub-objects if applicable

**Storage:** task in incident.task_refs, identity in incident.other_object_refs

**SRO Relationships:** task can connect via relationships to events, indicators, course-of-action, infrastructure, locations, other tasks

---

### Pattern 6.5: Workflow Sequencing
**Order:** events/tasks → sequences (chained)

1. Create **event** or **task** objects
2. Create **sequence** objects with:
   - `sequenced_object`→event or task ID
   - `sequence_type`→(event|task)
   - `step_type`→(start_step|intermediate_step|end_step)
   - Chain using: `on_completion`, `on_success`, `on_failure`, `next_steps`
3. Add starting sequences to incident via `sequence_start_refs`

**Storage:** sequences in incident.sequence_refs and incident.sequence_start_refs

---

### Pattern 6.6: Impact Tracking
**Order:** impacted objects → impact

1. Create objects that are impacted (infrastructure, identities, SCOs, etc.)
2. Create **impact** with:
   - `impacted_refs`→list of impacted object IDs
   - `superseded_by_ref`→newer impact ID (if applicable)
   - Add impact extension (availability, confidentiality, integrity, monetary, physical, traceability, external)

**Storage:** impact in incident.impact_refs, impacted objects elsewhere or in incident.other_object_refs

**SRO Relationships:** incidents and events can connect to impacts via "impacts" relationship

---

### Pattern 6.7: Complete Incident Assembly
**Order:** ALL subordinate objects → incident

1. Create all objects following Patterns 6.1-6.6
2. Create **incident** with extension-definition--ef765651-680c-498d-9894-99799f2fa126
3. Populate:
   - `event_refs`→all event IDs
   - `task_refs`→all task IDs
   - `impact_refs`→all impact IDs
   - `sequence_refs`→all sequence IDs
   - `sequence_start_refs`→starting sequence IDs
   - `other_object_refs`→sightings, observed-data, identities, relationships, indicators, etc.

**SRO Relationships:** incident can connect to intrusion-sets, identities, locations, other incidents via relationships

---

## 7. HIERARCHY RECONSTITUTION INSTRUCTIONS

To reconstitute any complete hierarchy:

1. **Identify target object** - Determine what you want to create (e.g., incident, event, task)

2. **Check Embedded References** - Look up object in Section 1, note ALL fields with ReferenceProperty/OSThreatReference

3. **Check Dependency Level** - Look up object in Section 3, identify all prerequisite objects

4. **Create in Bottom-Up Order:**
   - Start at Level 0 (user-account, url)
   - Progress through each level, creating all dependencies first
   - End at Level 5 (incident, relationship)

5. **Populate Reference Fields:**
   - Use Section 4 to see what each object can reference
   - Use Section 5 to see what can reference each object
   - Ensure all referenced objects exist before creating referencing object

6. **Add SRO Relationships (Optional):**
   - Use Section 2 to determine valid relationship_type values
   - Create relationship objects with proper source_ref, target_ref, relationship_type

7. **Register in Incident:**
   - Events → incident.event_refs
   - Tasks → incident.task_refs
   - Impacts → incident.impact_refs
   - Sequences → incident.sequence_refs
   - Sequence starts → incident.sequence_start_refs
   - Everything else → incident.other_object_refs

**Key Principles:**
- All SDOs have `created_by_ref`→identity
- All objects have `object_marking_refs`→marking-definition
- incident.other_object_refs is the catch-all for objects not in other specific _refs fields
- `_any` means any STIX object type
- `_sdo` means any STIX Domain Object
- `_sco` means any STIX Cyber Observable Object
- Sequences chain to other sequences for workflows of task and event objects
- Sightings bridge SDOs with observed-data (which contains SCOs)

---

## 8. SUMMARY STATISTICS

**Current Objects:** 17
- **SDOs:** 9 (identity, indicator, impact, incident, event, observed-data, sequence, task)
- **SCOs:** 5 (anecdote, email-addr, user-account, url, email-message)
- **SROs:** 2 (relationship, sighting)
- **Referenced but not in current_objects:** 1 (marking-definition)

**Total Embedded Reference Fields:** 48 (across all objects)

**SRO Relationship Types:** 26 unique relationship_type values

**Extension Definitions:**
- 1 Identity Contact Extension (extension-definition--66e2492a-bbd3-4be6-88f5-cc91a017a498)
- 1 Incident Core Extension (extension-definition--ef765651-680c-498d-9894-99799f2fa126)
- 1 Event New SDO Extension (extension-definition--4ca6de00-5b0d-45ef-a1dc-ea7279ea910e)
- 1 Task New SDO Extension (extension-definition--2074a052-8be4-4932-849e-f5e7798e0030)
- 1 Sequence New SDO Extension (extension-definition--be0c7c79-1961-43db-afde-637066a87a64)
- 1 Impact New SDO Extension (extension-definition--7cc33dd6-f6a1-489b-98ea-522d351d71b9)
- 1 Anecdote New SCO Extension (extension-definition--23676abf-481e-4fee-ac8c-e3d0947287a4)
- 1 Sighting Evidence Extension (extension-definition--0d76d6d9-16ca-43fd-bd41-4f800ba8fc43)
- 7 Impact Type Extensions (availability, confidentiality, external, integrity, monetary, physical, traceability)
- 7 Sighting Evidence Type Extensions (sighting-alert, sighting-anecdote, sighting-context, sighting-exclusion, sighting-enrichment, sighting-hunt, sighting-framework, sighting-external)

**Dependency Levels:** 6 (0-5)

---

## 9. ASCII DIAGRAM VISUALIZATIONS

### 9.1 Complete Embedded Reference Network

This ASCII diagram shows all embedded reference connections between the 17 STIX objects.

```
┌─────────────────────────────────────────────────────────────────────────────────────┐
│                      STIX OBJECT EMBEDDED REFERENCE NETWORK                         │
│                    (Solid lines = ReferenceProperty/OSThreatReference)              │
└─────────────────────────────────────────────────────────────────────────────────────┘

LEVEL 0: Foundation (No Dependencies)
┌──────────────┐                    ┌──────────────┐
│ user-account │                    │     url      │
│    (SCO)     │                    │    (SCO)     │
└──────┬───────┘                    └──────────────┘
       │
       │ ┌─────────────────────────────────────────────────────────────────┐
       │ │ LEVEL 1: Basic References                                       │
       │ │                                                                  │
       └─┼──belongs_to_ref──────────────────────┐                          │
         │                                       ▼                          │
         │                              ┌────────────────┐                  │
         │                              │  email-addr    │                  │
         │                              │     (SCO)      │                  │
         │                              └────────┬───────┘                  │
         │                                       │                          │
         │      ┌────────────────────────────────┤                          │
         │      │                                │                          │
         │      │                ┌───────────────┴──────────────┐           │
         │      │                │                              │           │
         │      │                ▼                              ▼           │
         │   ┌──┴─────────────────────────────┐      ┌──────────────────┐  │
         │   │       identity (SDO)           │      │  email-message   │  │
         │   │  ┌──────────────────────────┐  │      │      (SCO)       │  │
         │   │  │ IdentityContact Extension│  │      │   Level 2        │  │
         │   │  │ ┌─────────────────────┐  │  │      └──────────────────┘  │
         │   │  │ │ EmailContact        │  │  │                            │
         │   │  │ │ .email_address_ref──┼──┼──┼───────────────────────┘    │
         │   │  │ └─────────────────────┘  │  │                            │
         │   │  │ ┌─────────────────────┐  │  │                            │
         │   │  │ │ SocialMediaContact  │  │  │                            │
         │   │  │ │ .user_account_ref───┼──┼──┼────────────────────────┐   │
         │   │  │ └─────────────────────┘  │  │                        │   │
         │   │  └──────────────────────────┘  │                        │   │
         │   │         │                      │                        │   │
         │   │         │ created_by_ref (self)│                        │   │
         │   │         └──────────────────────┘                        │   │
         │   └────────────────────────────────┘                        │   │
         │                   │                                         │   │
         │                   │                                         │   │
         │   ┌───────────────┴──────────┐      ┌──────────────────┐   │   │
         │   │     indicator (SDO)      │      │   anecdote (SCO) │   │   │
         │   │   created_by_ref─────────┼──────┤ provided_by_ref──┼───┘   │
         │   └──────────────────────────┘      └──────────────────┘       │
         └──────────────────────────────────────────────────────────────────┘

┌────────────────────────────────────────────────────────────────────────────────────┐
│ LEVEL 3: Evidence & Impact                                                         │
│                                                                                     │
│  ┌─────────────────────────────────────────────────────────────────────┐          │
│  │                      observed-data (SDO)                             │          │
│  │  ┌──────────────────────────────────────────────────────────┐       │          │
│  │  │ object_refs (list) can point to ANY SCO:                 │       │          │
│  │  │  • user-account                                           │       │          │
│  │  │  • url                                                    │       │          │
│  │  │  • email-addr                                             │       │          │
│  │  │  • email-message                                          │       │          │
│  │  │  • anecdote                                               │       │          │
│  │  │  • file, process, network-traffic, ipv4-addr, etc.       │       │          │
│  │  └──────────────────────────────────────────────────────────┘       │          │
│  │  created_by_ref ──────────────────────────────────► identity        │          │
│  └─────────────────────────────────────────────────────────────────────┘          │
│                                                                                     │
│  ┌─────────────────────────────────────────────────────────────────────┐          │
│  │                         impact (SDO)                                 │          │
│  │  impacted_refs (list) ──────────────────────► [ANY object]          │          │
│  │  superseded_by_ref ──────────────────────────► impact (optional)    │          │
│  │  created_by_ref ──────────────────────────────► identity            │          │
│  │                                                                      │          │
│  │  Extensions (7 types):                                              │          │
│  │    • availability    • confidentiality   • external                 │          │
│  │    • integrity       • monetary          • physical                 │          │
│  │    • traceability                                                   │          │
│  └─────────────────────────────────────────────────────────────────────┘          │
└────────────────────────────────────────────────────────────────────────────────────┘

┌────────────────────────────────────────────────────────────────────────────────────┐
│ LEVEL 4: Analysis & Response                                                       │
│                                                                                     │
│  ┌─────────────────────────────────────────────────────────────────────┐          │
│  │                        sighting (SRO)                                │          │
│  │  sighting_of_ref ─────────────────────► indicator OR event          │          │
│  │  observed_data_refs (list) ────────────► observed-data              │          │
│  │  where_sighted_refs (list) ─────────────► identity OR location      │          │
│  │  created_by_ref ────────────────────────► identity                  │          │
│  │                                                                      │          │
│  │  Evidence Extensions (7 types):                                     │          │
│  │    • sighting-alert      • sighting-anecdote   • sighting-context   │          │
│  │    • sighting-exclusion  • sighting-enrichment • sighting-hunt      │          │
│  │    • sighting-framework                                             │          │
│  └─────────────────────────────────────────────────────────────────────┘          │
│                                      │                                             │
│                                      │                                             │
│  ┌───────────────────────────────────▼──────────────────────────────┐             │
│  │                         event (SDO)                               │             │
│  │  sighting_refs (list) ───────────► sighting                      │             │
│  │  changed_objects[].object_ref ────► [ANY object]                 │             │
│  │  created_by_ref ──────────────────► identity                     │             │
│  └───────────────────────────────────────────────────────────────────┘             │
│                                                                                     │
│  ┌─────────────────────────────────────────────────────────────────────┐          │
│  │                          task (SDO)                                  │          │
│  │  owner ─────────────────────────────────────► identity              │          │
│  │  impacted_entity_refs (list) ────────────────► [ANY object]         │          │
│  │  changed_objects[].object_ref ────────────────► [ANY object]        │          │
│  │  created_by_ref ──────────────────────────────► identity            │          │
│  └─────────────────────────────────────────────────────────────────────┘          │
│                                                                                     │
│  ┌─────────────────────────────────────────────────────────────────────┐          │
│  │                        sequence (SDO)                                │          │
│  │  step_refs (ordered list) ────────────────────► [ANY object]        │          │
│  │    (commonly: event, task, or playbook steps)                       │          │
│  │  created_by_ref ──────────────────────────────► identity            │          │
│  └─────────────────────────────────────────────────────────────────────┘          │
└────────────────────────────────────────────────────────────────────────────────────┘

┌────────────────────────────────────────────────────────────────────────────────────┐
│ LEVEL 5: Orchestration (Top of Hierarchy)                                         │
│                                                                                     │
│  ┌─────────────────────────────────────────────────────────────────────────────┐  │
│  │                      incident (SDO) - IncidentCore Extension                │  │
│  │  ┌───────────────────────────────────────────────────────────────────────┐ │  │
│  │  │ Extension Fields (IncidentCore):                                      │ │  │
│  │  │   event_refs (list) ─────────────────────────────► event             │ │  │
│  │  │   task_refs (list) ──────────────────────────────► task              │ │  │
│  │  │   impact_refs (list) ────────────────────────────► impact            │ │  │
│  │  │   other_object_refs (list) ───────────────────────► [ANY object]     │ │  │
│  │  │     • sighting                                                        │ │  │
│  │  │     • observed-data                                                   │ │  │
│  │  │     • indicator                                                       │ │  │
│  │  │     • sequence                                                        │ │  │
│  │  │     • identity                                                        │ │  │
│  │  │     • SCOs (url, email-addr, user-account, etc.)                     │ │  │
│  │  │     • relationship SROs                                               │ │  │
│  │  │     • attack-pattern, malware, tool, threat-actor, campaign, etc.    │ │  │
│  │  └───────────────────────────────────────────────────────────────────────┘ │  │
│  │  created_by_ref ──────────────────────────────────────► identity          │  │
│  └─────────────────────────────────────────────────────────────────────────────┘  │
│                                                                                     │
│  ┌─────────────────────────────────────────────────────────────────────────────┐  │
│  │                        relationship (SRO)                                   │  │
│  │  source_ref ──────────────────────────────────────────► [ANY object]       │  │
│  │  target_ref ──────────────────────────────────────────► [ANY object]       │  │
│  │  relationship_type (string) - one of 26 valid types                        │  │
│  │  created_by_ref ──────────────────────────────────────► identity           │  │
│  └─────────────────────────────────────────────────────────────────────────────┘  │
└────────────────────────────────────────────────────────────────────────────────────┘

LEGEND:
  ──────►  Embedded reference (ReferenceProperty or OSThreatReference)
  [ANY]    Can reference any STIX object type
  (list)   ListProperty - can contain multiple references
```

### 9.2 SRO Relationship Type Matrix

This diagram shows the 26 valid relationship_type values and their common source/target combinations.

```
┌──────────────────────────────────────────────────────────────────────────────────┐
│                    SRO RELATIONSHIP TYPE CONNECTIVITY MATRIX                     │
│                          (26 relationship_type values)                           │
└──────────────────────────────────────────────────────────────────────────────────┘

INCIDENT RELATIONSHIPS (incident as source):
  incident ──[attributed-to]────────────────────────────────► identity
  incident ──[attributed-to]────────────────────────────────► threat-actor
  incident ──[attributed-to]────────────────────────────────► campaign
  incident ──[located-at]───────────────────────────────────► location
  incident ──[impacts]──────────────────────────────────────► identity
  incident ──[impacts]──────────────────────────────────────► infrastructure
  incident ──[targets]──────────────────────────────────────► identity
  incident ──[targets]──────────────────────────────────────► infrastructure
  incident ──[targets]──────────────────────────────────────► location
  incident ──[related-to]───────────────────────────────────► incident

EVENT RELATIONSHIPS (event as source):
  event ──[led-to]──────────────────────────────────────────► event
  event ──[part-of]─────────────────────────────────────────► incident
  event ──[attributed-to]───────────────────────────────────► identity
  event ──[attributed-to]───────────────────────────────────► threat-actor
  event ──[located-at]──────────────────────────────────────► location
  event ──[impacts]─────────────────────────────────────────► infrastructure
  event ──[impacts]─────────────────────────────────────────► identity
  event ──[targets]─────────────────────────────────────────► identity
  event ──[targets]─────────────────────────────────────────► infrastructure

TASK RELATIONSHIPS (task as source):
  task ──[detects]──────────────────────────────────────────► event
  task ──[detects]──────────────────────────────────────────► indicator
  task ──[mitigates]────────────────────────────────────────► incident
  task ──[mitigates]────────────────────────────────────────► vulnerability
  task ──[investigates]─────────────────────────────────────► incident
  task ──[investigates]─────────────────────────────────────► event
  task ──[remediates]───────────────────────────────────────► incident
  task ──[remediates]───────────────────────────────────────► vulnerability
  task ──[blocks]───────────────────────────────────────────► task
  task ──[related-to]───────────────────────────────────────► task

IDENTITY RELATIONSHIPS (identity as source):
  identity ──[assigned]─────────────────────────────────────► task
  identity ──[located-at]───────────────────────────────────► location
  identity ──[part-of]──────────────────────────────────────► identity

INDICATOR RELATIONSHIPS (indicator as source):
  indicator ──[indicates]───────────────────────────────────► malware
  indicator ──[indicates]───────────────────────────────────► threat-actor
  indicator ──[indicates]───────────────────────────────────► campaign
  indicator ──[indicates]───────────────────────────────────► infrastructure
  indicator ──[based-on]────────────────────────────────────► observed-data
  indicator ──[based-on]────────────────────────────────────► event

IMPACT RELATIONSHIPS (impact as source):
  impact ──[led-to]─────────────────────────────────────────► impact
  impact ──[related-to]─────────────────────────────────────► event

OTHER COMMON RELATIONSHIPS:
  sighting ──[related-to]───────────────────────────────────► sighting
  observed-data ──[related-to]──────────────────────────────► observed-data
  malware ──[uses]──────────────────────────────────────────► attack-pattern
  threat-actor ──[uses]─────────────────────────────────────► attack-pattern
  threat-actor ──[uses]─────────────────────────────────────► malware
  threat-actor ──[uses]─────────────────────────────────────► tool
  campaign ──[attributed-to]────────────────────────────────► threat-actor
  campaign ──[uses]─────────────────────────────────────────► attack-pattern

RELATIONSHIP TYPE CATEGORIES:

  Attribution:      attributed-to, part-of
  Causality:        led-to, based-on
  Geospatial:       located-at
  Impact:           impacts, targets
  Response:         detects, mitigates, investigates, remediates
  Dependency:       blocks, uses
  Association:      related-to, assigned
```

### 9.3 Object Creation Dependency Hierarchy (Bottom-Up)

This diagram shows the 6-level dependency hierarchy for building STIX objects.

```
┌──────────────────────────────────────────────────────────────────────────────────┐
│              STIX OBJECT CREATION DEPENDENCY HIERARCHY (6 Levels)                │
│                         (Build from bottom to top)                               │
└──────────────────────────────────────────────────────────────────────────────────┘

LEVEL 5: ORCHESTRATION (Top of Pyramid)
═══════════════════════════════════════════════════════════════════════════════════
                           ┌──────────────────────┐
                           │      incident        │  Requires: events, tasks,
                           │  (IncidentCore Ext)  │  impacts, all evidence
                           └──────────┬───────────┘
                                      │
                           ┌──────────┴───────────┐
                           │     relationship     │  Requires: source + target
                           │        (SRO)         │  objects to exist
                           └──────────────────────┘

                                      ▲
                                      │
════════════════════════════════════════════════════════════════════════════════════
LEVEL 4: ANALYSIS & RESPONSE
────────────────────────────────────────────────────────────────────────────────────
              ┌───────────────┬───────────────┬───────────────┐
              │               │               │               │
        ┌─────┴─────┐   ┌─────┴─────┐   ┌─────┴─────┐   ┌────┴────┐
        │  sighting │   │   event   │   │   task    │   │ sequence│
        │   (SRO)   │   │   (SDO)   │   │   (SDO)   │   │  (SDO)  │
        └─────┬─────┘   └─────┬─────┘   └─────┬─────┘   └────┬────┘
              │               │               │               │
              │  Requires:    │  Requires:    │  Requires:    │  Requires:
              │  • indicator  │  • sighting   │  • identity   │  • identity
              │  • obs-data   │  • identity   │  • targets    │  • steps
              │  • identity   │               │               │
              │               │               │               │
              ▲               ▲               ▲               ▲
              │               │               │               │
════════════════════════════════════════════════════════════════════════════════════
LEVEL 3: EVIDENCE & IMPACT
────────────────────────────────────────────────────────────────────────────────────
                      ┌────────────────┬────────────────┐
                      │                │                │
              ┌───────┴───────┐  ┌─────┴─────┐         │
              │ observed-data │  │  impact   │         │
              │     (SDO)     │  │   (SDO)   │         │
              └───────┬───────┘  └─────┬─────┘         │
                      │                │               │
                      │  Requires:     │  Requires:    │
                      │  • SCOs        │  • identity   │
                      │  • identity    │  • targets    │
                      │                │               │
                      ▲                ▲               │
                      │                │               │
════════════════════════════════════════════════════════════════════════════════════
LEVEL 2: COMPOUND OBJECTS
────────────────────────────────────────────────────────────────────────────────────
                                                       │
                                              ┌────────┴────────┐
                                              │  email-message  │
                                              │      (SCO)      │
                                              └────────┬────────┘
                                                       │
                                                       │  Requires:
                                                       │  • email-addr
                                                       │
                                                       ▲
                                                       │
════════════════════════════════════════════════════════════════════════════════════
LEVEL 1: BASIC REFERENCES
────────────────────────────────────────────────────────────────────────────────────
           ┌──────────┬──────────┬──────────┬──────────┐
           │          │          │          │          │
      ┌────┴────┐ ┌───┴────┐ ┌──┴──────┐ ┌─┴────────┐ │
      │email-addr│ │identity│ │indicator│ │ anecdote │ │
      │  (SCO)  │ │ (SDO)  │ │  (SDO)  │ │  (SCO)   │ │
      └────┬────┘ └───┬────┘ └──┬──────┘ └─┬────────┘ │
           │          │          │          │          │
           │  Req:    │  Req:    │  Req:    │  Req:    │
           │  • u-acc │  • ident │  • ident │  • ident │
           │          │  (self)  │          │          │
           ▲          ▲          ▲          ▲          │
           │          │          │          │          │
════════════════════════════════════════════════════════════════════════════════════
LEVEL 0: FOUNDATION (No Dependencies - Start Here)
────────────────────────────────────────────────────────────────────────────────────
                              ┌──────────┬──────────┐
                              │          │          │
                         ┌────┴─────┐ ┌──┴────┐    │
                         │user-account│ │ url  │    │
                         │   (SCO)    │ │(SCO) │    │
                         └────────────┘ └───────┘   │
                                                     │
                         No dependencies - Create these first!
                                                     │
═══════════════════════════════════════════════════════════════════════════════════

BUILD ORDER RULES:
  1. Start at Level 0 (user-account, url)
  2. Move up one level at a time
  3. Cannot create object until ALL its dependencies exist
  4. identity can self-reference (created_by_ref → itself)
  5. incident goes last (Level 5) - requires everything else

ABBREVIATIONS:
  u-acc = user-account      obs-data = observed-data      ident = identity
  SCO = STIX Cyber Observable               SDO = STIX Domain Object
  SRO = STIX Relationship Object            Ext = Extension
```

### 9.4 Sub-Graph Pattern: User Identity Setup (Pattern 6.1)

```
┌──────────────────────────────────────────────────────────────────────────────┐
│                   PATTERN 6.1: USER IDENTITY SETUP                           │
│              (Foundation pattern for all incident responders)                │
└──────────────────────────────────────────────────────────────────────────────┘

STEP 1: Create Foundation SCO
──────────────────────────────────────────────────────────────────────────────
    ┌────────────────────────────────────────────┐
    │         user-account (SCO)                 │
    │  ─────────────────────────────────────     │
    │  • type: "user-account"                    │
    │  • user_id: "jwalsh"                       │
    │  • account_type: "windows-local"           │
    │  • display_name: "Jennifer Walsh"          │
    └────────────────────────────────────────────┘
                        │
                        │ Level 0 → Level 1
                        ▼
STEP 2: Create Email SCO with belongs_to_ref
──────────────────────────────────────────────────────────────────────────────
    ┌────────────────────────────────────────────┐
    │         email-addr (SCO)                   │
    │  ─────────────────────────────────────     │
    │  • type: "email-addr"                      │
    │  • value: "jwalsh@hospital.com"            │
    │  • belongs_to_ref ───────────┐             │
    └──────────────────────────────┼─────────────┘
                                   │
                                   │ References user-account
                                   ▼
                        ┌──────────────────────┐
                        │    user-account      │
                        │   (from Step 1)      │
                        └──────────────────────┘

STEP 3: Create Identity SDO with IdentityContact Extension
──────────────────────────────────────────────────────────────────────────────
    ┌──────────────────────────────────────────────────────────────────────┐
    │                  identity (SDO)                                      │
    │  ──────────────────────────────────────────────────────────────      │
    │  • type: "identity"                                                  │
    │  • name: "Jennifer Walsh"                                            │
    │  • identity_class: "individual"                                      │
    │  • created_by_ref ─────────────┐ (self-reference)                   │
    │                                 └─────────────────────┐              │
    │  ┌────────────────────────────────────────────────┐  │              │
    │  │ Extension: IdentityContact                     │  │              │
    │  │  extension-definition--66e2492a...             │  │              │
    │  │                                                 │  │              │
    │  │  ┌──────────────────────────────────────────┐ │  │              │
    │  │  │ EmailContact (sub-object)                │ │  │              │
    │  │  │   • digital_contact_type: "email"        │ │  │              │
    │  │  │   • email_address_ref ───────────┐       │ │  │              │
    │  │  └──────────────────────────────────┼───────┘ │  │              │
    │  │                                     │         │  │              │
    │  │  ┌──────────────────────────────────▼───────┐ │  │              │
    │  │  │ References: email-addr from Step 2       │ │  │              │
    │  │  └──────────────────────────────────────────┘ │  │              │
    │  │                                                │  │              │
    │  │  ┌──────────────────────────────────────────┐ │  │              │
    │  │  │ SocialMediaContact (sub-object)          │ │  │              │
    │  │  │   • digital_contact_type: "social"       │ │  │              │
    │  │  │   • user_account_ref ─────────────┐      │ │  │              │
    │  │  └────────────────────────────────────┼──────┘ │  │              │
    │  │                                       │        │  │              │
    │  │  ┌────────────────────────────────────▼──────┐ │  │              │
    │  │  │ References: user-account from Step 1      │ │  │              │
    │  │  └───────────────────────────────────────────┘ │  │              │
    │  └────────────────────────────────────────────────┘  │              │
    └───────────────────────────────────────────────────────┼──────────────┘
                                                            │
                                                            ▼
                                               ┌────────────────────┐
                                               │  identity (self)   │
                                               └────────────────────┘

RESULT: Complete User Profile
──────────────────────────────────────────────────────────────────────────────
    user-account ────► Foundation account object
         │
         └──belongs_to_ref──► email-addr ────► Contact information
                                   │
                                   └──email_address_ref──► identity
                                                              │
                                   ┌──────────────────────────┘
                                   │
                        user_account_ref from identity extension

    3 objects created, all interconnected via embedded references
    Ready to use identity.id as created_by_ref for all future objects
```

### 9.5 Sub-Graph Pattern: Evidence Collection (Pattern 6.2)

```
┌──────────────────────────────────────────────────────────────────────────────┐
│              PATTERN 6.2: EVIDENCE COLLECTION WITH SIGHTING                  │
│         (Foundation pattern for all incident evidence documentation)         │
└──────────────────────────────────────────────────────────────────────────────┘

PHASE 1: Collect Observable Artifacts (SCOs)
═══════════════════════════════════════════════════════════════════════════════
    ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
    │  url (SCO)      │    │ email-addr      │    │ email-message   │
    │  Level 0        │    │  Level 1        │    │  Level 2        │
    │                 │    │                 │    │                 │
    │ • value: "http  │    │ • value: "bad@" │    │ • from_ref ───┐ │
    │   ://phish.com" │    │ • belongs_to... │    │ • to_refs ────┼─┼───┐
    └─────────────────┘    └─────────────────┘    │ • subject: ..  │ │   │
                                                   └────────────────┘ │   │
                                                                      │   │
                                                   References ────────┘   │
                                                   email-addr objects ────┘

PHASE 2: Group SCOs in observed-data (Level 3)
═══════════════════════════════════════════════════════════════════════════════
    ┌────────────────────────────────────────────────────────────────────────┐
    │                      observed-data (SDO)                               │
    │  ────────────────────────────────────────────────────────────────      │
    │  • first_observed: "2024-01-15T08:00:00Z"                              │
    │  • last_observed: "2024-01-15T08:00:00Z"                               │
    │  • number_observed: 1                                                  │
    │                                                                         │
    │  • object_refs (list): ┌────────────────────────────────────┐          │
    │                        │ • url (from Phase 1)               │          │
    │                        │ • email-addr sender (from Phase 1) │          │
    │                        │ • email-addr recipient (Phase 1)   │          │
    │                        │ • email-message (from Phase 1)     │          │
    │                        └────────────────────────────────────┘          │
    │                                                                         │
    │  • created_by_ref ──────────────────────► identity (responder)         │
    └────────────────────────────────────────────────────────────────────────┘

PHASE 3: Create Indicator Pattern (Level 1)
═══════════════════════════════════════════════════════════════════════════════
    ┌────────────────────────────────────────────────────────────────────────┐
    │                        indicator (SDO)                                 │
    │  ────────────────────────────────────────────────────────────────      │
    │  • name: "Phishing URL Pattern"                                        │
    │  • indicator_types: ["malicious-activity", "phishing"]                 │
    │  • pattern: "[url:value = 'http://phish.com']"                         │
    │  • pattern_type: "stix"                                                │
    │  • valid_from: "2024-01-15T08:00:00Z"                                  │
    │  • created_by_ref ──────────────────────► identity (responder)         │
    └────────────────────────────────────────────────────────────────────────┘

PHASE 4: Create Sighting with Evidence Extension (Level 4)
═══════════════════════════════════════════════════════════════════════════════
    ┌────────────────────────────────────────────────────────────────────────┐
    │                         sighting (SRO)                                 │
    │  ────────────────────────────────────────────────────────────────      │
    │  • sighting_of_ref ──────────────────► indicator (from Phase 3)        │
    │  • observed_data_refs (list) ─────────► [observed-data (Phase 2)]      │
    │  • where_sighted_refs (list) ─────────► [company-identity]             │
    │  • first_seen: "2024-01-15T08:00:00Z"                                  │
    │  • count: 1                                                            │
    │                                                                         │
    │  ┌──────────────────────────────────────────────────────────────────┐  │
    │  │ Extension: Choose ONE evidence type:                             │  │
    │  │                                                                   │  │
    │  │ Option A: sighting-alert (automated detection)                   │  │
    │  │  • name: "SIEM Alert - Phishing URL"                             │  │
    │  │  • product: "Splunk Enterprise Security"                         │  │
    │  │  • severity: "high"                                              │  │
    │  │  • source: "Email Gateway"                                       │  │
    │  │                                                                   │  │
    │  │ Option B: sighting-anecdote (human report)                       │  │
    │  │  • person_name: "Bob Smith"                                      │  │
    │  │  • person_context: "Finance Manager"                             │  │
    │  │  • report_submission: "email to IT helpdesk"                     │  │
    │  │                                                                   │  │
    │  │ Option C: sighting-hunt (proactive search)                       │  │
    │  │  • name: "Proactive Phishing Hunt"                               │  │
    │  │  • hunt_type: "hypothesis-driven"                                │  │
    │  │  • completed: true                                               │  │
    │  │                                                                   │  │
    │  │ Option D: sighting-enrichment (external intel)                   │  │
    │  │  • enrichment_type: "external-lookup"                            │  │
    │  │  • source: "VirusTotal, MISP"                                    │  │
    │  │  • confidence_score: 95                                          │  │
    │  │                                                                   │  │
    │  │ (Other options: context, exclusion, framework, external)         │  │
    │  └──────────────────────────────────────────────────────────────────┘  │
    │                                                                         │
    │  • created_by_ref ──────────────────────► identity (responder)         │
    └────────────────────────────────────────────────────────────────────────┘

FINAL RESULT: Evidence Chain
═══════════════════════════════════════════════════════════════════════════════

    WHAT was observed?     ───► SCOs (url, email-message, email-addr)
            │
            ▼
    WHEN was it observed?  ───► observed-data (timestamps, grouping)
            │
            ▼
    WHY is it significant? ───► indicator (pattern definition)
            │
            ▼
    WHO observed it?       ───► sighting.where_sighted_refs (identity/location)
    HOW was it found?      ───► sighting extension type
    WHERE was it seen?     ───► sighting.where_sighted_refs
            │
            ▼
    Complete evidence package ready for event creation (Pattern 6.3)
```

### 9.6 Sub-Graph Pattern: Complete Incident Assembly (Pattern 6.7)

```
┌──────────────────────────────────────────────────────────────────────────────┐
│           PATTERN 6.7: COMPLETE INCIDENT ASSEMBLY (Level 5)                  │
│              (Orchestrates all evidence, analysis, and response)             │
└──────────────────────────────────────────────────────────────────────────────┘

                              ┌────────────────┐
                              │   incident     │
                              │  (Level 5 SDO) │
                              └────────┬───────┘
                                       │
                   ┌───────────────────┼───────────────────┐
                   │                   │                   │
                   │  IncidentCore Extension:             │
                   │                                       │
                   ▼                   ▼                   ▼

┌──────────────────────┐  ┌──────────────────────┐  ┌──────────────────────┐
│   event_refs (list)  │  │   task_refs (list)   │  │  impact_refs (list)  │
└──────────┬───────────┘  └──────────┬───────────┘  └──────────┬───────────┘
           │                         │                         │
           ▼                         ▼                         ▼
┌──────────────────────┐  ┌──────────────────────┐  ┌──────────────────────┐
│  event (Level 4)     │  │   task (Level 4)     │  │  impact (Level 3)    │
│  ──────────────────  │  │  ──────────────────  │  │  ──────────────────  │
│  • event_types: [..] │  │  • name: "Contain.." │  │  • impact_category:  │
│  • status: occurred  │  │  • task_types: [..] │  │    "confidentiality" │
│  • start_time        │  │  • owner ────►ident. │  │  • impacted_refs:    │
│  • sighting_refs ──┐ │  │  • priority: 90      │  │    [identities]      │
│                    │ │  │  • status: completed │  │  • recoverability    │
│  • changed_objects │ │  └──────────────────────┘  └──────────────────────┘
│    [StateChange..] │ │
└────────────────────┼─┘            │
                    │                │
                    │                │  All feed into...
                    │                │
                    ▼                ▼
           ┌────────────────────────────────────────────────────────────┐
           │         other_object_refs (list) - The Evidence Vault      │
           │  ────────────────────────────────────────────────────────  │
           │                                                             │
           │  CATEGORY 1: Sightings (Evidence with Provenance)          │
           │  ┌────────────────────────────────────────────────────┐    │
           │  │ • sighting (sighting-alert extension)              │    │
           │  │ • sighting (sighting-anecdote extension)           │    │
           │  │ • sighting (sighting-hunt extension)               │    │
           │  │ • sighting (sighting-enrichment extension)         │    │
           │  │ • sighting (sighting-framework extension)          │    │
           │  └────────────────────────────────────────────────────┘    │
           │           │                                                 │
           │           │  Each sighting references...                   │
           │           ▼                                                 │
           │  CATEGORY 2: Observed Data (Grouped SCO Observations)      │
           │  ┌────────────────────────────────────────────────────┐    │
           │  │ • observed-data (phishing email evidence)          │    │
           │  │ • observed-data (network traffic logs)             │    │
           │  │ • observed-data (file system artifacts)            │    │
           │  └────────────────────────────────────────────────────┘    │
           │           │                                                 │
           │           │  Each observed-data contains...                │
           │           ▼                                                 │
           │  CATEGORY 3: SCOs (Raw Observable Artifacts)               │
           │  ┌────────────────────────────────────────────────────┐    │
           │  │ • url (malicious link)                             │    │
           │  │ • email-addr (sender, recipients)                  │    │
           │  │ • email-message (phishing email)                   │    │
           │  │ • user-account (compromised accounts)              │    │
           │  │ • anecdote (user testimony)                        │    │
           │  │ • file, process, network-traffic, ipv4-addr, etc.  │    │
           │  └────────────────────────────────────────────────────┘    │
           │                                                             │
           │  CATEGORY 4: Indicators (Threat Patterns)                  │
           │  ┌────────────────────────────────────────────────────┐    │
           │  │ • indicator (phishing URL pattern)                 │    │
           │  │ • indicator (malicious file hash)                  │    │
           │  │ • indicator (C2 domain pattern)                    │    │
           │  └────────────────────────────────────────────────────┘    │
           │                                                             │
           │  CATEGORY 5: Identities (People, Orgs, Systems)            │
           │  ┌────────────────────────────────────────────────────┐    │
           │  │ • identity (victims)                               │    │
           │  │ • identity (responders)                            │    │
           │  │ • identity (company/organization)                  │    │
           │  │ • identity (IT systems)                            │    │
           │  └────────────────────────────────────────────────────┘    │
           │                                                             │
           │  CATEGORY 6: Sequences (Workflow Orchestration)            │
           │  ┌────────────────────────────────────────────────────┐    │
           │  │ • sequence (attack timeline: event chain)          │    │
           │  │ • sequence (response playbook: task workflow)      │    │
           │  └────────────────────────────────────────────────────┘    │
           │                                                             │
           │  CATEGORY 7: Relationships (Semantic Connections)          │
           │  ┌────────────────────────────────────────────────────┐    │
           │  │ • relationship (incident→attributed-to→identity)   │    │
           │  │ • relationship (event→led-to→event)                │    │
           │  │ • relationship (task→mitigates→incident)           │    │
           │  │ • relationship (impact→led-to→impact)              │    │
           │  └────────────────────────────────────────────────────┘    │
           │                                                             │
           │  CATEGORY 8: Threat Intelligence (Optional)                │
           │  ┌────────────────────────────────────────────────────┐    │
           │  │ • attack-pattern (MITRE ATT&CK techniques)         │    │
           │  │ • malware (identified malware families)            │    │
           │  │ • tool (attacker tools: Mimikatz, etc.)            │    │
           │  │ • threat-actor (attributed adversary)              │    │
           │  │ • campaign (broader threat campaign)               │    │
           │  └────────────────────────────────────────────────────┘    │
           │                                                             │
           └─────────────────────────────────────────────────────────────┘

RESULT: Complete Incident Case File
═══════════════════════════════════════════════════════════════════════════════
  ┌─────────────────────────────────────────────────────────────────────────┐
  │ incident object now contains:                                           │
  │   ✓ What happened (events)                                              │
  │   ✓ What was done (tasks)                                               │
  │   ✓ What was affected (impacts)                                         │
  │   ✓ All evidence (sightings, observed-data, SCOs)                       │
  │   ✓ Why it matters (indicators)                                         │
  │   ✓ Who was involved (identities)                                       │
  │   ✓ How it unfolded (sequences)                                         │
  │   ✓ Deeper connections (relationships)                                  │
  │   ✓ Threat context (attack-patterns, threat-actors, etc.)               │
  │                                                                          │
  │ Total objects: 80-200+ depending on incident complexity                 │
  │ Ready for: Storage, sharing, analysis, reporting, SOAR automation       │
  └─────────────────────────────────────────────────────────────────────────┘
```

### 9.7 Phishing Incident Workflow (ASCII State Diagram)

```
┌──────────────────────────────────────────────────────────────────────────────┐
│          PHISHING INCIDENT WORKFLOW: DETECTION → RESOLUTION                  │
│                   (Complete lifecycle with STIX objects)                     │
└──────────────────────────────────────────────────────────────────────────────┘

    [START]
       │
       ▼
╔════════════════════════════════════════════════════════════════════════╗
║  PHASE 1: AUTOMATED DETECTION                                          ║
╠════════════════════════════════════════════════════════════════════════╣
║  1. SIEM detects suspicious URL in email                               ║
║     └──► Create: url (SCO), email-message (SCO), email-addr (SCO)      ║
║                                                                         ║
║  2. Group artifacts                                                     ║
║     └──► Create: observed-data (object_refs → SCOs)                    ║
║                                                                         ║
║  3. Match against threat intel                                         ║
║     └──► Create: indicator (phishing pattern)                          ║
║                                                                         ║
║  4. Log detection event                                                 ║
║     └──► Create: sighting (sighting-alert extension)                   ║
║              • sighting_of_ref → indicator                             ║
║              • observed_data_refs → observed-data                      ║
║              • Extension fields: product=SIEM, severity=high           ║
╚════════════════════════════════════════════════════════════════════════╝
       │
       │ Alert triggers investigation
       ▼
╔════════════════════════════════════════════════════════════════════════╗
║  PHASE 2: HUMAN REPORTING                                              ║
╠════════════════════════════════════════════════════════════════════════╣
║  1. User reports suspicious email to IT                                ║
║     └──► Create: anecdote (SCO)                                        ║
║              • provided_by_ref → user-identity                         ║
║              • value = user's testimony                                ║
║                                                                         ║
║  2. Document human evidence                                            ║
║     └──► Create: observed-data (object_refs → anecdote)                ║
║                                                                         ║
║  3. Log user report                                                    ║
║     └──► Create: sighting (sighting-anecdote extension)                ║
║              • sighting_of_ref → indicator (or event)                  ║
║              • observed_data_refs → observed-data                      ║
║              • Extension fields: person_name, person_context           ║
╚════════════════════════════════════════════════════════════════════════╝
       │
       │ Evidence confirmed by multiple sources
       ▼
╔════════════════════════════════════════════════════════════════════════╗
║  PHASE 3: INVESTIGATION & HUNTING                                      ║
╠════════════════════════════════════════════════════════════════════════╣
║  1. Declare security event                                             ║
║     └──► Create: event (SDO)                                           ║
║              • sighting_refs → [sighting-alert, sighting-anecdote]     ║
║              • event_types = ["phishing"]                              ║
║              • status = "occurred"                                     ║
║                                                                         ║
║  2. Assign investigation tasks                                         ║
║     └──► Create: task (SDO) - "Analyze phishing email"                 ║
║              • task_types = ["investigate"]                            ║
║              • owner → analyst-identity                                ║
║              • priority = 90                                           ║
║                                                                         ║
║  3. Hunt for additional victims                                        ║
║     └──► Create: observed-data (15 more phishing emails found)         ║
║     └──► Create: sighting (sighting-hunt extension)                    ║
║              • count = 15 (additional victims)                         ║
║              • Extension fields: hunt_type, completed=true             ║
║                                                                         ║
║  4. Query threat intelligence                                          ║
║     └──► Create: sighting (sighting-enrichment extension)              ║
║              • Extension: enrichment_type="external-lookup"            ║
║              • source = "VirusTotal, MISP"                             ║
║              • confidence_score = 95                                   ║
╚════════════════════════════════════════════════════════════════════════╝
       │
       │ Investigation reveals scope
       ▼
╔════════════════════════════════════════════════════════════════════════╗
║  PHASE 4: IMPACT ASSESSMENT                                            ║
╠════════════════════════════════════════════════════════════════════════╣
║  1. Assess confidentiality impact                                      ║
║     └──► Create: impact (confidentiality extension)                    ║
║              • impacted_refs → [user identities]                       ║
║              • Extension: information_type="credentials"               ║
║                                                                         ║
║  2. Assess availability impact                                         ║
║     └──► Create: impact (availability extension)                       ║
║              • impacted_refs → [email system]                          ║
║              • Extension: availability_loss_type="degradation"         ║
║                                                                         ║
║  3. Assess integrity impact (if data modified)                         ║
║     └──► Create: impact (integrity extension)                          ║
╚════════════════════════════════════════════════════════════════════════╝
       │
       │ Impact quantified
       ▼
╔════════════════════════════════════════════════════════════════════════╗
║  PHASE 5: COORDINATED RESPONSE                                         ║
╠════════════════════════════════════════════════════════════════════════╣
║  1. Containment                                                        ║
║     └──► Create: task - "Block malicious URLs"                         ║
║              • status = "completed"                                    ║
║              • outcome = "15 URLs blocked in email gateway"            ║
║                                                                         ║
║  2. Eradication                                                        ║
║     └──► Create: task - "Remove phishing emails from mailboxes"        ║
║              • status = "in-progress"                                  ║
║                                                                         ║
║  3. Recovery                                                           ║
║     └──► Create: task - "Reset compromised credentials"                ║
║              • dependencies → [containment task]                       ║
║              • status = "pending"                                      ║
║                                                                         ║
║  4. Define workflow                                                    ║
║     └──► Create: sequence (response playbook)                          ║
║              • sequenced_object = "task"                               ║
║              • step_refs → [containment, eradication, recovery]        ║
╚════════════════════════════════════════════════════════════════════════╝
       │
       │ Response executed
       ▼
╔════════════════════════════════════════════════════════════════════════╗
║  PHASE 6: INCIDENT CREATION                                            ║
╠════════════════════════════════════════════════════════════════════════╣
║  1. Assemble complete incident                                         ║
║     └──► Create: incident (SDO with IncidentCore extension)            ║
║              • event_refs → [phishing event]                           ║
║              • task_refs → [all response tasks]                        ║
║              • impact_refs → [all impact assessments]                  ║
║              • other_object_refs → [sightings, observed-data,          ║
║                  indicators, SCOs, identities, sequences, etc.]        ║
║              • determination = "confirmed-true-positive"               ║
║              • investigation_status = "active-investigation"           ║
╚════════════════════════════════════════════════════════════════════════╝
       │
       │ Incident documented
       ▼
╔════════════════════════════════════════════════════════════════════════╗
║  PHASE 7: ENRICHMENT & DOCUMENTATION                                   ║
╠════════════════════════════════════════════════════════════════════════╣
║  1. Map to MITRE ATT&CK                                                ║
║     └──► Create: sighting (sighting-framework extension)               ║
║              • framework = "ATT&CK"                                    ║
║              • framework_id = "T1566.002" (Spearphishing Link)         ║
║                                                                         ║
║  2. Create semantic relationships                                      ║
║     └──► Create: relationship (incident → attributed-to → identity)    ║
║     └──► Create: relationship (event → led-to → event)                 ║
║     └──► Create: relationship (task → mitigates → incident)            ║
║                                                                         ║
║  3. Document attack timeline                                           ║
║     └──► Create: sequence (attack kill chain)                          ║
║              • sequenced_object = "event"                              ║
║              • step_refs → [email-sent, clicked, creds-entered, etc.]  ║
╚════════════════════════════════════════════════════════════════════════╝
       │
       ▼
    [COMPLETE INCIDENT CASE FILE]
    
Total Objects Created: 80-150
  • 10-20 SCOs (emails, URLs, accounts)
  • 5-15 observed-data (grouped observations)
  • 5-10 sightings (alert, anecdote, hunt, enrichment, framework)
  • 2-5 indicators (phishing patterns)
  • 1-3 events (phishing email, clicks, compromise)
  • 5-10 tasks (investigate, contain, eradicate, recover)
  • 2-5 impacts (confidentiality, availability, integrity)
  • 2-3 sequences (attack timeline, response workflow)
  • 10-20 identities (victims, responders, company)
  • 5-15 relationships (attributed-to, led-to, mitigates)
  • 1 incident (orchestrating everything)
```

---

