Problem
The current OCA Extension docs were in prior version of Stix than v2.1, and so there may be some small errors in some of the docs. We admire this project and seek to update it so it is OASIS Stix v2.1 Best Practise and can be easily integrated with other projects.

Approach
We take the viewpoint of the OASIS Stix v2.1 Best Practices Guide and seek to update this documentation wherever needed to reflect a Stix v2.1 Best Practices layout as a second example. In all cases, we have provided our changes as a second example so you can peruse the differences.
We have ignored any of our misgivings with the classification of your objects, and just assumed everything in the SDO directory was actually an SDO, thus as outlined below we had to add Sighting SRO's to many of the examples to connect your SDO's to.

We also added fields for ID, created, modified, and spec_version as needed to all needed. We ran all standard SCO's in your examples, through the Stix2 Python library, so the majority of id's should be realistic for those SCO values. All SDO's were provided UUID4 through an online service

<style> </style>
SDO Type	Altered Definition	Altered Examples	Created Vocab/Enum	Injected Sighting
x-ibm-finding.md	Yes	Yes	No	Yes
x-ibm-ttp-tagging.md	Yes	Yes	No	No
x-oca-asset.md	Yes	Yes	Yes	Yes
x-oca-behavior.md	Yes	No	Yes	No
x-oca-coa-playbook-ext.md	Yes	No	No	No
x-oca-detection.md	No	No	No	No
x-oca-detector.md	Yes	No	No	No
x-oca-event.md	Yes	Yes	No	Yes
x-oca-geo.md	Yes	Yes	No	Yes
x-oca-playbook.md	No	No	Yes	No
x-oca-tool-hvt-ext.md	No	No	Yes	No
We Update According to Your Scheme
We updated the repo so all objects in the SDO sub directory were treated as SDO's, which means they cannot be reported through an Observed Data object, since they can only report on SCO's. Thus in places we had to provide Sighting objects to carry those SDO's with the observables.

Our aim is to integrate OCA Extensions, with a series of other extensions, including current Stix extension standards, as we think there is a natural fit, with some small adjustments. We conduct this experimental effort
so our shared understanding can increase, as we intend to implement your entire extension library in both Python class extensions to the popular OASIS Stix2 library, and to the powerful TypeDB type-based database

Overall its Brilliant, but we want some SDO's to Become SCO's as they seem Meant to Be
Some SDO's should be SCO's, as they are telemetry-based. Even when a piece of telemetry is a summary record of other telemetry, it is still telemetry, and thereby observable (i.e. x-ibm-finding, x-oca-asset, x-oca-event). As an example, compare your version of an event SDO with the event SDO from Incident Management.

These are very different objects and frankly the telemetry should be an SCO Event, as it is observable, while the analyst may put together an SDO Event using the above specification. There is definitely room for an Analyst-defined Asset SDO, versus an Asset SCO provided by telemetry. In short, by making some of your current SDO's into SCO's, we believe it can make Incident Management with Behaviours, even better.