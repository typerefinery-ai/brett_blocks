# Common Stix object graph patterns in OS Triage Incident Management System

## 1. The Graph Pattern Nature of Stix

Stix has two graph networks within it:

- Embedded References - where an object's field contains a stix id, or list of stix id's, pointing to other objects. This creates a hierarchy in two ways, the number of reference fields in an object, and the types of objects they can reference (i.e. their place in the hieraqrchy)
- Object Relationships - where an SRO relationship object connects two other objects via their id's. Different values of the "relationship_type" field are constrained to have different source and target object type combinations, specific to that relationship type.

Stix Incidents contain both types of graph networks, but all objects in the incident, including SRO's must be registered as an embedded reference in the US DoD extension definition for the incident. This means that the full set of objects in an incident can be found by traversing the embedded references in the incident object extension itself.

Stix objects can be arranged hierarchically based on dependency, so that the object with no dependencies, and no embedded references at the bottom, and the object with the largest number of embedded reference fields, and thus many dependnacies is at the top. However, there is another, more subtle hierarchy based on what type of object the field takes as its value. 

These dependencies can be assessed by reviewing StixORM object class templates (`*_template.json`). Fields that contain either `ReferenceProperty` or `OSThreatReference` types, indicate embedded references to other objects. By reviewing the class templates for each object type, one can build a dependency graph of what types of objects can reference what other types of objects. This creates a hierarchy of object types based on what types of objects they can reference, and the various types of subgraph patterns, as shown below.

### 1.1 The US DoD Incident Extension Definition Pattern

The basic Stix incident is a stub, with no signifcant properties, beyond name and description, and no SRO `relationship_type` values connected to it. 

The US DoD Extension (`extension-definition—​ef765651-680c-498d-9894-99799f2fa126` | class ``IncidentCoreExt`), adds a series of descriptive fields, and most importantly, the series of lists of orthogonal references that sit inside the [incident](Block_Families\StixORM\SDO\Incident\Incident_template.json):
= `event_refs`: A list of references to all the events in the incident
- `impact_refs` : A list of references to all the impacts in the incident
- `sequence_refs`: Every event and task object, has references to its own sequence object that references it through the `sequenced_object_ref` property, where the `sequence_type` = (task | event)
- `sequence_start_refs`: Each sequence of sequence object, has references to its own starting object to the chain, where the `step_type ` = "start_step"
- `task_refs`: A list of references to all the tasks in the incident
- `other_object_refs`: Finally, references to all other objects in the Icnident are store here


This concept and other extensions allow tracking of incidents across their life cycle, and enable better evidentiary judgment processes where each type of [sighting](Block_Families\StixORM\SRO\Sighting\Sighting_template.json) has extensions to capture the provenance, and enable evidentiary value to be assessed. This enables semi-automated judgements and forensic evaluation of decision veracity.

[observed-data](Block_Families\StixORM\SDO\ObservedData\ObservedData_template.json) objects contain SCO observations, and must be reported within a [sighting](Block_Families\StixORM\SRO\Sighting\Sighting_template.json) object alongside the SDO's that describe "what" and "where". This sighting subgraph is connected to the Incident through the `other_object_refs` field of an incident.

Many sighting types create [events](Block_Families\StixORM\SDO\Event\Event_template.json), which are flagged for investigation resulting in [incidents](Block_Families\StixORM\SDO\Incident\Incident_template.json) with [tasks](Block_Families\StixORM\SDO\Task\Task_template.json) being worked to resolve these. [Events](Block_Families\StixORM\SDO\Event\Event_template.json) and [tasks](Block_Families\StixORM\SDO\Task\Task_template.json) can be organised into serial and parallel workflows using [sequence](Block_Families\StixORM\SRO\Sequence\Sequence_template.json) objects, or they can be considered as atomic and discrete if [sequences](Block_Families\StixORM\SRO\Sequence\Sequence_template.json) are not present.

[Identities](Block_Families\StixORM\SDO\Identity\Identity_template.json) can now include more detail, by using the (IdentityContact | 'extension-definition--66e2492a-bbd3-4be6-88f5-cc91a017a498') extension definition, which adds contact details such as phone numbers (ContactNumber | `contact-number`), email addresses (EmailContact | `email-contact`) and social media accounts (SocialMediaContact | `social-media-contact`) as sub-objects. The `social-media-contact` sub-object references user account in `user_account_ref` and `email-contact` sub-object references email-addr SCO's in `email_address_ref` fields, and these objects must be created before the Identity.

Incidents have [impacts](Block_Families\StixORM\SDO\Impact\Impact_template.json) that change over time. [Events](Block_Families\StixORM\SDO\Event\Event_template.json) can cause or influence these [impacts](Block_Families\StixORM\SDO\Impact\Impact_template.json) which are in turn mitigated and potentially resolved by [tasks](Block_Families\StixORM\SDO\Task\Task_template.json) performed as part of the incident response process. Both [events](Block_Families\StixORM\SDO\Event\Event_template.json) and [tasks](Block_Families\StixORM\SDO\Task\Task_template.json) can exist independent of [incidents](Block_Families\StixORM\SDO\Incident\Incident_template.json) and in some workflows may occur prior to an incident being declared as malicious.

Incident objects represent cases composed of [events](Block_Families\StixORM\SDO\Event\Event_template.json) and [tasks](Block_Families\StixORM\SDO\Task\Task_template.json) as well as actual or potential [impacts](Block_Families\StixORM\SDO\Impact\Impact_template.json). [Events](Block_Families\StixORM\SDO\Event\Event_template.json) and [tasks](Block_Families\StixORM\SDO\Task\Task_template.json) can be sequenced by [sequence](Block_Families\StixORM\SRO\Sequence\Sequence_template.json) objects. An Incident SDO can be created prior to a formal determination that the incident has an impact as a way to logically track case work in an attempt to investigate events or lower level alerts.

The Incident object should have sufficient properties to represent the current state of the incident or investigation while serving as an anchor point to record both related activities and the impact to an organization.

The SRO Reltationship objects and their respective `relationship_type` fields are:

| **Source** | **Type** | **Target** |
|------------|----------|------------|
| event | impacts | infrastructure |
| event | led-to | event |
| event | located-at | location |
| task | blocks | event |
| task | causes | event |
| task | creates | indicator |
| task | detects | event |
| task | errored-to | task |
| task | followed-by | task |
| task | impacts | infrastructure |
| task | located-at | location |
| task | uses | course-of-action |
| campaign | associated-with | incident |
| identity | assigned | task |
| identity | contact-for | task, incident |
| identity | participated-in | task |
| identity | performed | task |
| incident | attributed-to | intrusion-set |
| incident | impacts | identity |
| incident | led-to | incident |
| incident | located-at | location |
| incident | targets | identity |
| indicator | based-on | event |
| indicator | detected | incident |
| malware | performed | event |
| tool | performed | event, task |

### 1.2 The User Account, Email Address and Identity Sub Pattern

Apart from the identity that creates them, user accounts are independent of other object dependnencies, and made first. Email address contain the value but also the `belongs_to_ref` field that contains the user account connected with the email address, so it is made second. Conventional Identity objects have no embedded references, apart from `created_by_ref`, but the [Identity Contact](Block_Families\StixORM\SDO\Identity\Identity_template.json) Identity Extension by US DoD (IdentityContact | 'extension-definition--66e2492a-bbd3-4be6-88f5-cc91a017a498') adds additional contact properties and 3 list's of sub-objects:
 - ContactNumber | 'contact-number', class `ContactNumber`, no references only text fields
 - EmailContact | 'email-contact', class `EmailContact`, includes text fields and an `email_address_ref` field pointing to an [email-addr SCO](Block_Families\StixORM\SCO\EmailAddress\EmailAddress_template.json)
 - SocialMediaContact | 'social-media-contact', class `SocialMediaContact`, includes text fields and a `user_account_ref` field pointing to a [user-account SCO](Block_Families\StixORM\SCO\UserAccount\UserAccount_template.json)

In Incident Management, one normally has details of themselves and their team, plus any users in the company they work for, held in this sub-graph format, so it is easy to refrence. However, adverseraries or thers may not be as well defined and only be a simple Identity without Eaxtension. Further, the Identity object is often used for definition of internal resources. In summary, user-account connects to identity through the  `user_account_ref` field in the SocialMediaConteact sub object, whereas the email address object connects through the `email_address_ref` field in the EmailContact sub object.

All of this data is contained in the Incident object's `other_object_refs` field.


### 1.3 The Observed-Data, Sighting and Sighting Extension Sub Pattern

An Incident needs a way to organise and make decision on evidence, observations and sightings and must store them with rigour. In Stix Best Practice, an [observed-data object](Block_Families\StixORM\SDO\ObservedData\ObservedData_template.json) may contain embedded references to SCO's such as file, url, email-addr etc in its `object_refs` field, so this is setup first. But it will not contain embedded references to SDO's such as incident, event, impact etc. Instead one needs to embed the observed-data object in a [sighting object](Block_Families\StixORM\SRO\Sighting\Sighting_template.json) in the `observed_data_refs` field, which links for the SDO's to describe "what was sighted" (e.g. Indicator) in the `sighting_of_ref` and "where" (e,g, Location, OCAGeo, Identity etc.) in the `where_sighted_refs`, apart from `created_by_ref`, as a second step. 

As a third step, [as shown in the class template the OS Threat Sighting Extensions](Block_Families/StixORM/SRO/Sighting/Sighting_template.json), enable one to store additional meta data in the sighting on top of the subgraph, to store the provenance of 8 different sources of evidence as a separate Sighting Extension:

#### Sighting Evidence Extension Types

##### Alert Extension

Automated system detection

name* (string): Alert name in system
log (string): Alert content
system_id (string): Unique origin ID
source (string): Origin system (e.g., "McAfee SIEM v12.0")
product (string): Detection product type (AV, EDR, IPS, SIEM)
format (string): Data format (syslog, json, text, LEEF, CEEF)


##### Anecdote Extension

Human-reported evidence

person_name* (string): Reporter's name
person_context (string): Reporter type (employee, 3rd party, injured, police, anonymous)
report_submission (string): Submission method (mail, interview, transcript, telephone)


##### Context Extension

System-sourced contextual data

name* (string): Source system (Outlook, SAP, etc.)
description (string): Context description
value (string): Value from origin system

##### Exclusion List Extension

Threat feed exclusions

source* (string): Feed source name
channel (string): Source channel

##### Enrichment Extension

Threat intelligence enrichment

name* (string): Enrichment site
url (string): Site URL
paid (boolean): Paid service (true/false)
value (string): Value from origin

##### Hunt Extension

Threat hunting results

name* (string): Hunt system name
playbook_id (string): Playbook identifier
rule (string): Rule definition

##### Framework Extension

Mapping to frameworks (e.g., MITRE ATT&CK)

framework* (string): Framework name
version (string): Framework version
domain (string): Framework domain
comparison (string): Match determination method
comparison_approach (string): Comparison details

##### External Extension

External pattern matching

source* (string): Pattern source
version (string): Report version
last_update (timestamp): Last version update
pattern (string): Pattern content
pattern_type (string): Pattern format (stix, PCRE, sigma, snort, suricata, yara, attckflow)
payload (string): Payload type (simple/external_reference)
valid_from (timestamp): Validity start
valid_until (timestamp): Validity end


All of this data is contained as stix id's in the Incident object's `other_object_refs` field.


### 1.4 The Event is Derived from one or more Sightings

The [Event object](Block_Families\StixORM\SDO\Event\Event_template.json) is made based on one or more sightings, in the `sighting_refs` field, plus the standard embedded references to SDO's such as `created_by_ref`.

The Event is mostly connected in a subgraph through different SRO `relationship_type` values

| `source_ref`    | `relationship_type`       | `target_ref`                |
| --------- | ---------- | --------------------- |
| event     | led-to     | event                 |
| event     | impacts    | infrastructure, _sco  |
| event     | located-at | location              |
| event     | observed   | _sco                  |
| indicator | based-on   | event                 |
| malware   | performed  | event                 |

The Event objects are referenced in the `event_refs` field. the other objects associated with the Event, are usually contained in the Incident object's `other_object_refs`, or other `_refs` fields.


### 1.5 the Task is integrated with many other objects through its SRO Relationships

The Task object properties are

| **Property Name** | **Type** | **Description** |
|-------------------|----------|-----------------|
| **outcome** (required) | `task-outcome-enum` | The outcome of the task. |
| **type** (required) | `string` | The value of this property **MUST** be set to `task`. |
| **changed_objects** (optional) | `list` of type `state-change` | A list of changes that this task has caused. This is typically used to indicate how a task has affected impacts. |
| **task_types** (optional) | `list` of type `open-vocabulary` | A list of high level types for the task in order to enable aggregation and summaries. This should be drawn from `task-type-ov`. |
| **description** (optional) | `string` | A description of task that occurred. |
| **end_time** (optional) | `timestamp` | The date and time the task was last recorded. If this is not present it is assumed to be unknown. |
| **end_time_fidelity** (optional) | `timestamp-fidelity-enum` | The level of fidelity that the end_time is recorded in. This value **MUST** come from `timestamp-fidelity-enum`. If no value is provided the timestamp should be considered to be accurate up to the number of decimals it includes. |
| **error** (optional) | `string` | Details about any failures or deviations that occurred in the task. |
| **impacted_entity_counts** (optional) | `entity-count` | An optional listing of the entity types that were impacted and how many of each were affected. This is primarily used when recording victim notifications. |
| **name** (optional) | `string` | An optional name used to identify the task. |
| **priority** (optional) | `integer` | The priority or importance of the task. This value **MUST** be between 0 to 100. This can be translated into qualitative values as described in Appendix B. |
| **start_time** (optional) | `timestamp` | The date and time the task was first recorded. If this is not present it is assumed to be unknown. This property **SHOULD** be populated. |
| **start_time_fidelity** (optional) | `timestamp-fidelity-enum` | The level of fidelity that the start_time is recorded in. This value **MUST** come from `timestamp-fidelity-enum`. If no value is provided the timestamp should be considered to be accurate up to the number of decimals it includes. |

The [Task object](Block_Families\StixORM\SDO\Task\Task_template.json) is mostly connected in a subgraph through different SRO `relationship_type` values, apart from its `created_by_ref`

| \`source_ref\` | \`relationship_type\` | \`target_ref\`        |
| -------------- | --------------------- | --------------------- |
| task           | uses                  | course-of-action      |
| task           | blocks                | event                 |
| task           | causes                | event                 |
| task           | detects               | event                 |
| task           | creates               | indicator             |
| task           | impacts               | infrastructure, _sco  |
| task           | located-at            | location              |
| task           | errored-to            | task                  |
| task           | followed-by           | task                  |
| identity       | assigned              | task                  |
| identity       | contact-for           | task                  |
| identity       | participated-in       | task                  |
| identity       | performed             | task                  |
| tool           | performed             | task                  |

The Task objects are referenced in the `task_refs` field. the other objects associated with the Event, are usually contained in the Incident object's `other_object_refs`, or other `_refs` fields.

### 1.6 The Impact object has  7 different types of extension

The [Impact Object](Block_Families\StixORM\SDO\Impact\Impact_template.json) connects through its `impacted_refs` field, which can relate directly to Infrastructure, SCOs, and other SDOs. There are 7 different US DoD Impact Extensions that can be used to capture different types of impact data:

Impact Extension Types
All Impact objects require an extension matching the impact_category value.

#### 1.6.1. Impact Core Extension (ImpactCoreExt)

- extension_type* (string): Must be new-sdo
- Extension ID: extension-definition--7cc33dd6-f6a1-489b-98ea-522d351d71b9

#### 1.6.2. Availability (Availability)

- availability_impact* (integer): Impact score 0-100 on system/service availability

#### 1.6.3. Confidentiality (Confidentiality)

- loss_type* (enum): Type of confidentiality loss
- information_type (open-vocab): Type of compromised information
- record_count (integer): Number of compromised records
- record_size (integer): Bytes of compromised data

#### 1.6.4. External (External)

- impact_type* (open-vocab): Impact type outside direct organization

#### 1.6.5. Integrity (Integrity)

- alteration* (enum): Type of alteration (modification/deletion/etc)
- information_type (open-vocab): Type of compromised information
- record_count (integer): Number of affected records
- record_size (integer): Bytes of affected data

#### 1.6.6. Monetary (Monetary)

- variety* (open-vocab): Type of monetary impact
- currency (string): ISO 4217 code for reported amounts
- currency_actual (string): Original currency of impact
- min_amount (number): Minimum damage estimate
- max_amount (number): Maximum damage estimate
- conversion_rate (number): Exchange rate between currencies
- conversion_time (timestamp): When rate was queried

#### 1.6.7. Physical (Physical)

- impact_type* (enum): Type of physical damage
- asset_type (open-vocab): Affected property/system type

#### 1.6.8. Traceability (Traceability)

- traceability_impact* (enum): Impact on audit/non-repudiation capability

The Impact objects are referenced in the `impact_refs` field. the other objects associated with the Event, are usually contained in the Incident object's `other_object_refs`, or other `_refs` fields.

### 1.7 The Email Message Contents, its Email Addresses, URL's  and Relations

The [Email Message](Block_Families\StixORM\SCO\EmailMessage\EmailMessage_template.json) object contains embedded references to [email-addr SCO's](Block_Families\StixORM\SCO\EmailAddress\EmailAddress_template.json) in the `from_ref`, `to_refs`, `cc_refs`, and `bcc_refs` fields. The [url SCO](Block_Families\StixORM\SCO\Url\Url_template.json) cannot connect to the email message through embedded rfeferences, but instead connects through SRO relationship objects with the `relationship_type` value of `contained-in`, where the `source_ref` is the [url SCO](Block_Families\StixORM\SCO\Url\Url_template.json) id, and the `target_ref` is the [email message SCO](Block_Families\StixORM\SCO\EmailMessage\EmailMessage_template.json) id.


### 1.8 The Sequencing of Tasks and Events through the Sequence object
The [Sequence object](Block_Families\StixORM\SRO\Sequence\Sequence_template.json) enables the sequencing of [event SDO's](Block_Families\StixORM\SDO\Event\Event_template.json) and [task SDO's](Block_Families\StixORM\SDO\Task\Task_template.json) into ordered workflows, by connecting to them through the `sequenced_object_ref` field. The value of the field `sequence_type`  **MUST** be of type `event` or `task`., and, based on the value of `step_type` **MUST** be one of `(single_step, parallel_step)`. The sequence object connects to other sequence objects to set the conditions to sequence to the next task/event id,  `on_completion_ref`, `on_success_ref`, and `on_failure_ref`. 

Sequence objects for both values of the `sequence_type` field must be created in a chain starting from the start sequence, where each sequence object connects to the next sequence object in the workflow.  Sequences are chained together using the [chain_sequence block](Block_Families\OS_Triage\Save_Context\chain_sequence.py), which automatically create a start sequence for the first sequence (`step_type` = "start_step"), and then sets the `next_step_refs` field in the previous sequence object to match the current.



| **Property Name** | **Type** | **Description** |
|-------------------|----------|-----------------|
| **type** (required) | `string` | The value of this property **MUST** be set to `sequence`. |
| **step_type** (required) | `step-type-enum` | The type of step, **MUST** be one of `(start_step, end_step, single_step, parallel_step)` |
| **sequence_type** (required) | `string` | The type of sequence, **MUST** be `(event or task)` |
| **sequenced_object_ref** (optional) | `identifier` | The SDO that is part of the sequence, **MUST** be of type `event` or `task`. |
| **on_completion_ref** (optional) | `identifier` | The `sequence` object to follow, **MUST** be of type `sequence` |
| **on_success_ref** (optional) | `identifier` | The `sequence` object to follow, **MUST** be of type `sequence` |
| **on_failure_ref** (optional) | `identifier` | The `sequence` object to follow, **MUST** be of type `sequence` |
| **next_step_refs** (optional) | `list` of type `identifier` | The `sequence` objects to follow, **MUST** be of type `sequence` |

## 1.8 Summary of the Graph Nature of Stix Incidents

Thus we can see that there is a hierarchy of object types based on what types of objects they can reference, and the various types of subgraph patterns, as shown above. Thus, an object that takes in any sco, like the observed-data object, will be lower in the hierarchy than an object that takes in any sdo in addition to he observations, like the sighting object.

The aim is to form rich interconnection patterns between data in the Stix Incident, via both embedded references and relationship objects, to form a complete picture of the incident being described.
