# The Subgraph of Stix Objects and other Subgraphs in a Single Stix Incident

## 1. The Graph Pattern Nature of Stix

Stix has two graph networks within it. Those:
- Embedded References - where an object's field contains a stix id, or list of stix id's, pointing to other objects
- Object Relationships - where a relationship object connects two other objects via their id's

Stix Incidents contain both types, but all objects in the incident must be registered as an embedded reference in the US DoD extension definition for the incident. This means that the full set of objects in an incident can be found by traversing the embedded references in the incident object extension itself.

Stix objects can be arranged hierarchically based on dependency, so that the object with no dependencies, and no embedded references at the bottom, and the object with the largest number of embedded reference fields, and thus many dependnacies is at the top. However, there is another, more subtle hierarchy based on what type of object the field takes as its value. 

For example, an observed-data object may contain embedded references to SCO's such as file, url, email-addr etc. But it will not contain embedded references to SDO's such as incident, event, impact etc. Instead one needs to embed the observed-data object in a sighting object, which links for the SDO's to describe "what was sighted" (e.g. Indicator) and "where" (e,g, Location, OCAGeo, Identity etc.). 

Thus we can see that there is a hierarchy of object types based on what types of objects they can reference. Thus, an object that takes in any sco, like the observed-data object, will be lower in the hierarchy than an object that takes in any sdo in addition to he observations, like the sighting object.

The aim is to form rich interconnection patterns between data in the Stix Incident, via both embedded references and relationship objects, to form a complete picture of the incident being described.


## 2. The US DoD Incident Extension Definition

These extensions allow tracking [incidents](#incidents) across their life cycle, and enable better evidentiary judgment processes where each type of [sighting](#sighting) has [evidence](#evidence) extensions to capture the provenance, and enable evidentiary value to be assessed. This enables semi-automated judgements and forensic evaluation of decision veracity.

Observed-data objects contain SCO observations, and must be reported within a [sighting](#sighting) object alongside the SDO's that describe "what" and "where". This sighting subgraph is connected to the Incident through the other object refs part of an incident.

Many sighting types create [events](#event), which are flagged for investigation resulting in [incidents](#incidents) with [tasks](#task) being worked to resolve these. [Events](#event) and [tasks](#task) can be organised into serial and parallel workflows using [sequence](#sequence) objects, or they can be considered as atomic and discrete if [sequences](#sequence) are not present.

Incidents have [impacts](#impact) that change over time. [Events](#event) can cause or influence these [impacts](#impact) which are in turn mitigated and potentially resolved by [tasks](#task) performed as part of the incident response process. Both [events](#event) and [tasks](#task) can exist independent of [incidents](#incidents) and in some workflows may occur prior to an incident being declared as malicious.

Incident objects represent cases composed of [events](#event) and [tasks](#task) as well as actual or potential [impacts](#impact). [Events](#event) and [tasks](#task) can be sequenced by [sequence](#sequence) objects. An Incident SDO can be created prior to a formal determination that the incident has an impact as a way to logically track case work in an attempt to investigate events or lower level alerts.

The Incident object should have sufficient properties to represent the current state of the incident or investigation while serving as an anchor point to record both related activities and the impact to an organization.

The most important properties for incident management are contained within the US DoD Incident Extension. This structure captures all of the key data, including:
- incident metadata - determination, investigation status, criticality, recoverability, scores
- sightings and observations contained in other objects
- events
- tasks
- sequences of events, sequences of tasks
- impacts

### 2.1 Incident Core Extension Properties

The properties and additional types within the Incident Core Extension are defined below. As this is not a top-level object, fields such as identifier are not present. This extension **MUST** use `extension-definition--ef765651-680c-498d-9894-99799f2fa126` as its extension ID.
The Python class name is `IncidentCoreExt`.

---

| Property Name | Type | Description |
|---------------|------|-------------|
| **determination** (required) | `incident-determination-enum` | A high level determination on the outcome of this incident. This **SHOULD** be suspected until enough information is available to provide a well researched result.<br><br>Some automated tools may flag results as blocked or low-value automatically depending on the tool type or activity. A tool that blocks a series of phishing emails may create an incident with a blocked determination automatically.<br><br>The values of this property **MUST** come from the `incident-determination-enum` enumeration. |
| **extension_type** (required) | string | The value of this property **MUST** be `property-extension` |
| **investigation_status** (required) | open-vocab | The current status of the incident investigation.<br><br>The values of this property **MUST** come from the `incident-investigation-ov` enumeration. |
| **criticality** (optional) | integer | The criticality of the incident. This value **MUST** be between 0 to 100. This can be translated into qualitative values as described in Appendix B. |
| **event_refs** (optional) | list of identifier | A list of events tied to this incident. It **MUST** contain references to one or more Event objects. |
| **impact_refs** (optional) | list of identifier | A list of impacts of this incident. It **MUST** contain references to one or more Impact objects.<br><br>The objects referenced in this list **MUST** be of type `impact` |
| **impacted_entity_counts** (optional) | `entity-count` | An optional listing of the entity types that were impacted by the incident, and how many of each type were affected. Individual impacts may also record more detailed counts as appropriate.<br><br>If this field is not present it should be assumed that this information is not being shared, not that there were no impacted entities. |
| **incident_types** (optional) | list of open-vocab | This property uses an Open Vocabulary that specifies the type of incident that occurred, if applicable.<br><br>This is an open vocabulary and values **SHOULD** come from the `event-type-ov`. |
| **other_object_refs** (required) | list of identifier | A list of all SDO, SCO and SRO objects contained in this incident, not including Task, Event, Impact or Sequence objects. It **MUST** contain references to one or more SDO, SCO or SRO objects. |
| **recoverability** (optional) | `recoverability-enum` | The recoverability of this particular Incident with respect to feasibility and required time and resources.<br><br>The values of this property **MUST** come from the `recoverability-enum` enumeration. |
| **scores** (optional) | list of `incident-score` | A list of scores from various automated or manual mechanisms along with optional descriptions. |
| **sequence_refs** (optional) | list of identifier | A list of Sequence Start objects tied to this incident. It **MUST** contain references only to Sequence objects. |
| **sequence_start_refs** (optional) | list of identifier | A list of sequence objects tied to this incident. It **MUST** contain references only to Sequence objects, where the step_type property is set to `start_step`. |
| **task_refs** (optional) | list of identifier | A list of tasks tied to this incident. It **MUST** contain references to one or more Task objects. |
|  |  | |

### 2.2 Incident Relationships

#### Common Relationships
- `derived-from`
- `duplicate-of`
- `related-to`

| Source | Type | Target | Description |
|--------|------|--------|-------------|
| `incident` | `led-to` | `incident` | One incident led to another. |
| `incident` | `impacts` | `identity`, `infrastructure` | An incident has an impact on the victim or specific infrastructure. |
| `incident` | `attributed-to` | `intrusion-set`, `threat-actor` | The incident has been attributed to the intrusion set or threat actor. |
| `incident` | `targets` | `identity`, `infrastructure` | An incident was targeted at the victim or specific infrastructure. |
| `incident` | `located-at` | `location` | The incident occurred at a specific location or locations. |

#### Reverse Relationships

| Source | Type | Target | Description |
|--------|------|--------|-------------|
| `campaign` | `associated-with` | `incident` | The incident in question is part of the campaign that is associated with. |
| `identity` | `contact-for` | `incident` | An identity should be considered a point of contact for an incident.<br><br>This can be used to supplement the created_by_ref in cases where external authorship would prevent using it for this purpose. |
| `indicator` | `detected` | `incident` | An indicator was responsible for detecting the incident. |




### 2.3 Minimal Example Incident Object

A minimal example of a Stix incident, with the US DoD extensions is shown below.

```json
{
	"type": "incident",
	"spec_version": "2.1",
	"id": "incident--4c76b69c-4011-40a0-be09-45bee08c6469",
	"created": "2025-10-30T05:26:20.109Z",
	"modified": "2025-10-30T05:26:20.109Z",
	"name": "potential phishing",
	"extensions": {
		"extension-definition--ef765651-680c-498d-9894-99799f2fa126": {
			"extension_type": "property-extension",
			"investigation_status": "new",
			"incident_types": [
				"dissemination-phishing-emails"
			],
			"other_object_refs": [
				"email-addr--eb38d07e-6ba8-56c1-b107-d4db4aacf212",
				"url--a824ef3f-83a0-51ae-9b5b-817580ec74ee",
				"indicator--9e6779bc-b1e2-4a7b-92e9-971a263de65c",
				"indicator--16747b4d-16ec-42fd-8686-001a6a588a73",
				"email-message--6090e3d4-1fa8-5b36-9d2d-4a66d824995d",
				"observed-data--fd29ec54-3c94-4353-b08f-5c38c101c9f3",
				"relationship--67278a8e-840c-4e7f-ad6e-9da40fc8ea93",
				"relationship--c0f7b429-3cf0-4933-a32f-113bf7f6402d",
				"anecdote--e1298bc0-818e-5cdb-9154-eac37c8e260f",
				"observed-data--25461c8a-889e-408c-8c4c-70a4e5efdb36",
				"sighting--8ccfd090-6616-4952-95b4-9c25afa87632"
			],
			"event_refs": [
				"event--771f04e3-9fc9-4d85-b364-44d3d84299ec"
			],
			"task_refs": [
				"task--60bb3851-233b-4d78-8d66-0fe6c479a3de",
				"task--43f9baeb-2654-4018-8c91-307ddc65e30a"
			],
			"sequence_start_refs": [
				"sequence--f11d8e6e-68e5-4231-83f7-3d6988077ec3",
				"sequence--3c60fa5f-8fa8-47e9-bc56-66c4d412e294"
			],
			"sequence_refs": [
				"sequence--d545c4b9-dce1-4c9c-9304-c00a3a25042a",
				"sequence--28e30261-f8e6-4524-b088-bde1d70cb585",
				"sequence--5f14c241-1e34-4eaf-a43e-230f0e7f3fe2"
			],
			"impact_refs": [
				"impact--e287f5c5-df3b-407f-9320-118e3eedbb59"
			]
		}
	}
}
```

## 3. Established Stix Patterns in Incidents

Note:
1. The stix id's of all of the objects and relationships mentioned below, will be contained in one of the reference lists in the above Incident Extension: `event_refs`, `task_refs`, `sequence_refs`, `sequence_start_refs`, `impact_refs`, `other_object_refs`. This happens automatically when using the 

### 3.1