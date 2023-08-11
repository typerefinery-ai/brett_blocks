# brett_blocks

This is an experimental repo for containg data flow blocks for use in Type Refinery.

Each block is documented in a sub-directory, named after the block, and contains:
- Script - a python or javascript file containing the exact script to be executed in the block
- Config - a JSON file that contains the exact data needed to fill out the other config fields
- UI_Code - a HTML file that contians the javascript and HTML from the Edit part of the block
- README - a markdown file that contains the description of how the block works, and how to get the best out of it (unlike those TotalJS tossers)

The Python blocks can be loaded and tested locally. Each Script wil take imports and export a file, and so testing and glue code can be written

It is not clear yet how the HTLM code, or javascript code could be tested locally, so we are open to suggestions.

Note Poetry Install, Python v3.9

## StixORM Blocks
There are a a series of different block libraries needed:
- General: Block that apply across all protocol types
- Stix: Blocsk tht apply to Stix objects
- Attack: Blocks that apply to Attack objects only
- Incident: Blocks that apply to the Incident process only

### General Blocks
| Library | Name                   |   Type    | Inputs            |        Outputs        | Description                                                      |
|:-------:|:-----------------------|:---------:|:------------------|:---------------------:|:-----------------------------------------------------------------|
| General | 	Import Bundle         |  Import   | 	Connection, URL  |      	Stix_List       | 	Given n URL, open the JSON Bundle and add it to TypeDB          |
| General | 	Get Object            | 	Retrieve | 	Connection, id	  |      Stix_List	       | Given an id, retrieve a single JSON object in a list             |
| General | 	Get Objects of a Type | 	Retrieve | 	Connection, type |      	Stix_List       | 	Given a string StixObject type, return all objects of that type |
| General | 	URL                   | Constant  | 	Trigger          |      	URL String      | 	Given n URL, open the JSON Bundle and add it to TypeDB          |
| General | 	Email Address         | 	Constant | 	Trigger	         | Email address String	 | Given an id, retrieve a single JSON object in a list             |
| General | 	IPv4 Address          | 	Constant | 	Trigger          |     	IPv4 String      | 	Given a string StixObject type, return all objects of that type |
| General | 	IPv6 Address          | 	Constant | 	Trigger          |     	IPv6 String      | 	Given a string StixObject type, return all objects of that type |


### Stix Blocks
| Library | Name          |   Type    | Inputs                      |  Outputs   | Description                                                |
|:-------:|:--------------|:---------:|:----------------------------|:----------:|:-----------------------------------------------------------|
|  Stix   | 	Get Report   | Retrieve  | 	Connection, id             | 	Stix_List | 	Given an id, retireve the report and all connected assets |
|  Stix   | 	Get Email    | 	Retrieve | 	Connection, email address	 | Stix_List	 | Given an email address, retireve the email object          |
|  Stix   | 	Get IPv4     | 	Retrieve | 	Connection, IPv4 address   | 	Stix_List | 	Given an ipv4 retrieve the IPv4 object                    |
|  Stix   | 	Get IPv6     | 	Retrieve | 	Connection, IPv6 address	  | Stix_List	 | Given an IPv6 address, retireve the IPv6 object            |
|  Stix   | 	Get Location | 	Retrieve | 	Connection, Location       | 	Stix_List | 	Given a Location retrieve the Location object             |

### Incident Blocks
| Library  | Name                |   Type    | Inputs                 |  Outputs   | Description                                                            |
|:--------:|:--------------------|:---------:|:-----------------------|:----------:|:-----------------------------------------------------------------------|
| Incident | 	Get Incident       | Retrieve  | 	Connection, id        | 	Stix_List | 	Given a Connection id, retireve the incident and all connected assets |
| Incident | 	Get User Incidents | 	Retrieve | 	Connection, Identity	 | Stix_List	 | GGiven a User id, retireve all incidents related to it                 |
| Incident | 	Get Team Incidents | 	Retrieve | 	Connection, Identity  | 	Stix_List | 	Given a Team id, retireve all incidents related to it                 |



### Attack Blocks
| Library | Name          |   Type    | Inputs                      |  Outputs   | Description                                                |
|:-------:|:--------------|:---------:|:----------------------------|:----------:|:-----------------------------------------------------------|
| Attack  | 	Get Report   | Retrieve  | 	Connection, id             | 	Stix_List | 	Given an id, retireve the report and all connected assets |
| Attack  | 	Get Email    | 	Retrieve | 	Connection, email address	 | Stix_List	 | Given an email address, retireve the email object          |
| Attack  | 	Get IPv4     | 	Retrieve | 	Connection, IPv4 address   | 	Stix_List | 	Given an ipv4 retrieve the IPv4 object                    |
| Attack  | 	Get IPv6     | 	Retrieve | 	Connection, IPv6 address	  | Stix_List	 | Given an IPv6 address, retireve the IPv6 object            |
| Attack  | 	Get Location | 	Retrieve | 	Connection, Location       | 	Stix_List | 	Given a Location retrieve the Location object             |
| Attack  | 	Get Report   | Retrieve  | 	Connection, id             | 	Stix_List | 	Given an id, retireve the report and all connected assets |
| Attack  | 	Get Email    | 	Retrieve | 	Connection, email address	 | Stix_List	 | Given an email address, retireve the email object          |
| Attack  | 	Get IPv4     | 	Retrieve | 	Connection, IPv4 address   | 	Stix_List | 	Given an ipv4 retrieve the IPv4 object                    |
| Attack  | 	Get IPv6     | 	Retrieve | 	Connection, IPv6 address	  | Stix_List	 | Given an IPv6 address, retireve the IPv6 object            |
| Attack  | 	Get Location | 	Retrieve | 	Connection, Location       | 	Stix_List | 	Given a Location retrieve the Location object             |

