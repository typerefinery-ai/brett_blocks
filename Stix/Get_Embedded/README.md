# Get Embedded Objects

This block is designed to load the cluster of embedded objects that are in Cluster Objects (e.g. Reports, Collection, Feed, Incident)

It takes two inputs:
1. A Connection object
2. A string containing a valid Stix_ID for a cluser object

It has a single output:
1. A json file containing a list of objects, inlcuding the Cluster object and all of its sub-objects

Note this can take quite some time to sequentially pulll all of the objects in the collection list if the list is big enough, as for example the list in the Mitre ATT&CK Enterprise v13.1 collection contains more than 20,000 objects.