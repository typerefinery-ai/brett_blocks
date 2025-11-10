
At the moment, the number of Stix objects available to us are limited by the number of directories with "make_object.py" format.

Lets register a current set of Python make_object.py files that collects the currently available list of SDO's, SCO's and SRO's. 

Note  that we use the Identity object for multiple purposes, based on fields like "identity_class" including:

- An Individual e.g. -> Block_Families/StixORM/SDO/Identity/identity_IT_user1.json
- A Company e.g. -> Block_Families/StixORM/SDO/Identity/identity_TR_user_company.json
- A Laptop e.g.-> Block_Families/StixORM/SDO/Identity/identity_Laptop1.json
- A system e.g. -> Block_Families/StixORM/SDO/Identity/identity_IT_user1.json


First read a_seed/content.md, which describes how different types of content, python file, class template and json, data template json files in a content directory interact. Then look through the below list, opening and reading the 3 files for each stix type. By comparing how this works you will see how:

1. the design of the class template, defines both the layout of the Python function and the data forms. Note how it includes the Python class name as part of the template. The Python class is guaranteed to be unique, but there may be multiple different stix objects with the same stix type, for example the AttackPattern, Technique and Subtechnique classes all have the same stix type "attack-pattern". Every sub-directory in Block_Families\StixORM\SCO or SDO or SRO, corresponds to a specific Python class, and the class template names it explicitly. Every directory needs a class template as a minimum, once it has been developed properly it will contain a make_object.py file and one or more data form json file as well.
2. How the number of inputs to the Python file are determined by the class template. The first, mandatory input in a StixORM, make_object python block's main function is always the data form, and the python block knows how to decompose data from this. The other optional inputs are all embedded references, mostly fields ending with `_ref` or `_refs`.
3. Further you can see how the data form template contains the same properties as the class template, except the "sub" section, which in the class template describes sub-objects. In the data form examples, the sub section "sub" objects are contained within the values of the other sections, instead of being in their own section like the class template.

In order to build your insight on this, compare how this pattern works
```json
{
  "sdo_make_files": [
	{
		"python_class": "Identity",
		"stix_type": "identity",
		"python": "Block_Families/StixORM/SDO/Identity/make_identity.py",
		"template": "Block_Families/StixORM/SDO/Identity/Identity_template.json",
		"data_example": "Block_Families/StixORM/SDO/Identity/identity_IT_user1.json"
	},
	{
		"python_class": "Indicator",
		"stix_type": "indicator",
		"python": "Block_Families/StixORM/SDO/Indicator/make_indicator.py",
		"template": "Block_Families/StixORM/SDO/Indicator/Indicator_template.json",
		"data_example": "Block_Families/StixORM/SDO/Indicator/indicator_alert.json"
	},
	{
		"python_class": "Impact",
		"stix_type": "impact",
		"python": "Block_Families/StixORM/SDO/Impact/make_impact.py",
		"template": "Block_Families/StixORM/SDO/Impact/Impact_template.json",
		"data_example": "Block_Families/StixORM/SDO/Impact/anecdote_impact.json"
	},
	{
		"python_class": "Incident",
		"stix_type": "incident", 
		"python": "Block_Families/StixORM/SDO/Incident/make_incident.py",
		"template": "Block_Families/StixORM/SDO/Incident/Incident_template.json",
		"data_example": "Block_Families/StixORM/SDO/Incident/phishing_incident.json"
	},
	{
		"python_class": "Event",
		"stix_type": "event",
		"python": "Block_Families/StixORM/SDO/Event/make_event.py",
		"template": "Block_Families/StixORM/SDO/Event/Event_template.json",
		"data_example": "Block_Families/StixORM/SDO/Event/event_alert.json"
	},
	{
		"python_class": "ObservedData",
		"stix_type": "observed-data",
		"python": "Block_Families/StixORM/SDO/Observed_Data/make_observed_data.py",
		"template": "Block_Families/StixORM/SDO/Observed_Data/ObservedData_template.json",
		"data_example": "Block_Families/StixORM/SDO/Observed_Data/observation-alert.json"
	},
	{
		"python_class": "Sequence",
		"stix_type": "sequence",
		"python": "Block_Families/StixORM/SDO/Sequence/make_sequence.py",
		"template": "Block_Families/StixORM/SDO/Sequence/Sequence_template.json",
		"data_example": "Block_Families/StixORM/SDO/Sequence/sequence_alert.json"
	},
	{
		"python_class": "Task",
		"stix_type": "task",
		"python": "Block_Families/StixORM/SDO/Task/make_task.py",
		"template": "Block_Families/StixORM/SDO/Task/Task_template.json",
		"data_example": "Block_Families/StixORM/SDO/Task/task_alert.json"
	}
  ],
  "sco_make_files": [
	{
		"python_class": "Anecdote",
		"stix_type": "anecdote",
		"python": "Block_Families/StixORM/SCO/Anecdote/make_anecdote.py",
		"template": "Block_Families/StixORM/SCO/Anecdote/Anecdote_template.json",
		"data_example": "Block_Families/StixORM/SCO/Anecdote/anecdote_on_impact.json"
	},
	{
		"python_class": "EmailAddress",
		"stix_type": "email-addr",
		"python": "Block_Families/StixORM/SCO/EmailAddress/make_email_addr.py",
		"template": "Block_Families/StixORM/SCO/EmailAddress/EmailAddress_template.json",
		"data_example": "Block_Families/StixORM/SCO/EmailAddress/email_addr_IT_user1.json"
	},
	{
		"python_class": "UserAccount",
		"stix_type": "user-account",
		"python": "Block_Families/StixORM/SCO/UserAccount/make_user_account.py",
		"template": "Block_Families/StixORM/SCO/UserAccount/UserAccount_template.json",
		"data_example": "Block_Families/StixORM/SCO/UserAccount/usr_account_IT_user1.json"
	},
	{
		"python_class": "URL",
		"stix_type": "url",
		"python": "Block_Families/StixORM/SCO/URL/make_url.py",
		"template": "Block_Families/StixORM/SCO/URL/URL_template.json",
		"data_example": "Block_Families/StixORM/SCO/URL/suspicious_url.json"
	},
	{
		"python_class": "EmailMessage",
		"stix_type": "email-message",
		"python": "Block_Families/StixORM/SCO/Email_Message/make_email_msg.py",
		"template": "Block_Families/StixORM/SCO/Email_Message/EmailMessage_template.json",
		"data_example": "Block_Families/StixORM/SCO/Email_Message/suspicious_email_msg.json"
	}
  ],
  "sro_make_files": [
	{
		"python_class": "Relationship",
		"stix_type": "relationship",
		"python": "Block_Families/StixORM/SRO/Relationship/make_sro.py",
		"template": "Block_Families/StixORM/SRO/Relationship/Relationship_template.json",
		"data_example": "Block_Families/StixORM/SRO/Relationship/sro_employed_by.json"
	},
	{
		"python_class": "Sighting",
		"stix_type": "sighting",
		"python": "Block_Families/StixORM/SRO/Sighting/make_sighting.py",
		"template": "Block_Families/StixORM/SRO/Sighting/Sighting_template.json",
		"data_example": "Block_Families/StixORM/SRO/Sighting/sighting_context.json"
	}
  ]
}
```

## Additional STIX Object Types

### Standard STIX 2.1 Objects with Templates (Not Yet Implemented)

**stix_sdo_types = [**
```json
{
  "python_class": "AttackPattern",
  "stix_type": "attack-pattern",
  "python": "",
  "template": "Block_Families/StixORM/SDO/AttackPattern/AttackPattern_template.json",
  "data_example": "Block_Families/StixORM/SDO/AttackPattern/Test_attack_pattern.json"
},
{
  "python_class": "Campaign",
  "stix_type": "campaign",
  "python": "",
  "template": "Block_Families/StixORM/SDO/Campaign/Campaign_template.json",
  "data_example": ""
},
{
  "python_class": "CourseOfAction",
  "stix_type": "course-of-action",
  "python": "",
  "template": "Block_Families/StixORM/SDO/CourseOfAction/CourseOfAction_template.json",
  "data_example": ""
},
{
  "python_class": "Grouping",
  "stix_type": "grouping",
  "python": "",
  "template": "Block_Families/StixORM/SDO/Grouping/Grouping_template.json",
  "data_example": ""
},
{
  "python_class": "Infrastructure",
  "stix_type": "infrastructure",
  "python": "",
  "template": "Block_Families/StixORM/SDO/Infrastructure/Infrastructure_template.json",
  "data_example": ""
},
{
  "python_class": "IntrusionSet",
  "stix_type": "intrusion-set",
  "python": "",
  "template": "Block_Families/StixORM/SDO/IntrusionSet/IntrusionSet_template.json",
  "data_example": ""
},
{
  "python_class": "Location",
  "stix_type": "location",
  "python": "",
  "template": "Block_Families/StixORM/SDO/Location/Location_template.json",
  "data_example": ""
},
{
  "python_class": "MalwareAnalysis",
  "stix_type": "malware-analysis",
  "python": "",
  "template": "Block_Families/StixORM/SDO/MalwareAnalysis/MalwareAnalysis_template.json",
  "data_example": ""
},
{
  "python_class": "Note",
  "stix_type": "note",
  "python": "",
  "template": "Block_Families/StixORM/SDO/Note/Note_template.json",
  "data_example": ""
},
{
  "python_class": "Opinion",
  "stix_type": "opinion",
  "python": "",
  "template": "Block_Families/StixORM/SDO/Opinion/Opinion_template.json",
  "data_example": ""
},
{
  "python_class": "Report",
  "stix_type": "report",
  "python": "",
  "template": "Block_Families/StixORM/SDO/Report/Report_template.json",
  "data_example": ""
},
{
  "python_class": "ThreatActor",
  "stix_type": "threat-actor",
  "python": "",
  "template": "Block_Families/StixORM/SDO/ThreatActor/ThreatActor_template.json",
  "data_example": ""
},
{
  "python_class": "Vulnerability",
  "stix_type": "vulnerability",
  "python": "",
  "template": "Block_Families/StixORM/SDO/Vulnerability/Vulnerability_template.json",
  "data_example": ""
}
```
**]**

**stix_sco_types = [**
```json
{
  "python_class": "Artifact",
  "stix_type": "artifact",
  "python": "",
  "template": "Block_Families/StixORM/SCO/Artifact/Artifact_template.json",
  "data_example": ""
},
{
  "python_class": "AutonomousSystem",
  "stix_type": "autonomous-system",
  "python": "",
  "template": "Block_Families/StixORM/SCO/AutonomousSystem/AutonomousSystem_template.json",
  "data_example": ""
},
{
  "python_class": "Directory",
  "stix_type": "directory",
  "python": "",
  "template": "Block_Families/StixORM/SCO/Directory/Directory_template.json",
  "data_example": ""
},
{
  "python_class": "DomainName",
  "stix_type": "domain-name",
  "python": "",
  "template": "Block_Families/StixORM/SCO/DomainName/DomainName_template.json",
  "data_example": ""
},
{
  "python_class": "File",
  "stix_type": "file",
  "python": "",
  "template": "Block_Families/StixORM/SCO/File/File_template.json",
  "data_example": "Block_Families/StixORM/SCO/File/Test_file.json"
},
{
  "python_class": "IPv4Address",
  "stix_type": "ipv4-addr",
  "python": "",
  "template": "Block_Families/StixORM/SCO/IPv4Address/IPv4Address_template.json",
  "data_example": "Block_Families/StixORM/SCO/IPv4Address/Test_ipv4_addr.json"
},
{
  "python_class": "IPv6Address",
  "stix_type": "ipv6-addr",
  "python": "",
  "template": "Block_Families/StixORM/SCO/IPv6Address/IPv6Address_template.json",
  "data_example": "Block_Families/StixORM/SCO/IPv6Address/Test_ipv6_addr.json"
},
{
  "python_class": "MACAddress",
  "stix_type": "mac-addr",
  "python": "",
  "template": "Block_Families/StixORM/SCO/MACAddress/MACAddress_template.json",
  "data_example": "Block_Families/StixORM/SCO/MACAddress/Test_mac_addr.json"
},
{
  "python_class": "Mutex",
  "stix_type": "mutex",
  "python": "",
  "template": "Block_Families/StixORM/SCO/Mutex/Mutex_template.json",
  "data_example": "Block_Families/StixORM/SCO/Mutex/Test_mutex.json"
},
{
  "python_class": "Software",
  "stix_type": "software",
  "python": "",
  "template": "Block_Families/StixORM/SCO/Software/Software_template.json",
  "data_example": "Block_Families/StixORM/SCO/Software/Test_software.json"
},
{
  "python_class": "X509Cert",
  "stix_type": "x509-certificate",
  "python": "",
  "template": "Block_Families/StixORM/SCO/X509Certificate/X509Cert_template.json",
  "data_example": "Block_Families/StixORM/SCO/X509Certificate/Test_x509_cert.json"
}
```
**]**

### Non-STIX Dialect Objects (Requiring StixORM Library Upgrade)

**non_stix_sdo_types = [**
```json
{
  "python_class": "AttackAsset",
  "stix_type": "x-mitre-asset",
  "python": "",
  "template": "Block_Families/StixORM/SDO/AttackAsset/AttackAsset_template.json"
},
{
  "python_class": "AttackCampaign",
  "stix_type": "x-mitre-campaign",
  "python": "",
  "template": "Block_Families/StixORM/SDO/AttackCampaign/AttackCampaign_template.json"
},
{
  "python_class": "AttackDataComponent",
  "stix_type": "x-mitre-data-component",
  "python": "",
  "template": "Block_Families/StixORM/SDO/DataComponent/AttackDataComponent_template.json"
},
{
  "python_class": "AttackDataSource",
  "stix_type": "x-mitre-data-source",
  "python": "",
  "template": "Block_Families/StixORM/SDO/DataSource/AttackDataSource_template.json"
},
{
  "python_class": "AttackGroup",
  "stix_type": "intrusion-set",
  "python": "",
  "template": "Block_Families/StixORM/SDO/Group/AttackGroup_template.json"
},
{
  "python_class": "AttackMalware",
  "stix_type": "malware",
  "python": "",
  "template": "Block_Families/StixORM/SDO/SoftwareMalware/AttackMalware_template.json"
},
{
  "python_class": "AttackTool",
  "stix_type": "tool",
  "python": "",
  "template": "Block_Families/StixORM/SDO/SoftwareTool/AttackTool_template.json"
},
{
  "python_class": "AttackFlow",
  "stix_type": "x-attackflow",
  "python": "",
  "template": "Block_Families/StixORM/SDO/AttackFlow/AttackFlow_template.json"
},
{
  "python_class": "Behavior",
  "stix_type": "x-ibm-behavior",
  "python": "",
  "template": "Block_Families/StixORM/SDO/Behavior/Behavior_template.json"
},
{
  "python_class": "Detection",
  "stix_type": "x-ibm-detection",
  "python": "",
  "template": "Block_Families/StixORM/SDO/Detection/Detection_template.json"
},
{
  "python_class": "Detector",
  "stix_type": "x-ibm-detector",
  "python": "",
  "template": "Block_Families/StixORM/SDO/Detector/Detector_template.json"
},
{
  "python_class": "ExtensionDefinition",
  "stix_type": "extension-definition",
  "python": "",
  "template": "Block_Families/StixORM/SDO/ExtensionDefinition/ExtensionDefinition_template.json"
},
{
  "python_class": "FlowAction",
  "stix_type": "x-attackflow-action",
  "python": "",
  "template": "Block_Families/StixORM/SDO/FlowAction/FlowAction_template.json"
},
{
  "python_class": "FlowAsset",
  "stix_type": "x-attackflow-asset",
  "python": "",
  "template": "Block_Families/StixORM/SDO/FlowAsset/FlowAsset_template.json"
},
{
  "python_class": "FlowCondition",
  "stix_type": "x-attackflow-condition",
  "python": "",
  "template": "Block_Families/StixORM/SDO/FlowCondition/FlowCondition_template.json"
},
{
  "python_class": "FlowOperator",
  "stix_type": "x-attackflow-operator",
  "python": "",
  "template": "Block_Families/StixORM/SDO/FlowOperator/FlowOperator_template.json"
},
{
  "python_class": "Malware",
  "stix_type": "malware",
  "python": "",
  "template": "Block_Families/StixORM/SDO/Malware/Malware_template.json",
  "data_example": "Block_Families/StixORM/SDO/Malware/Test_malware.json"
},
{
  "python_class": "MalwareBehavior",
  "stix_type": "x-mitre-malware-behavior",
  "python": "",
  "template": "Block_Families/StixORM/SDO/MalwareBehavior/MalwareBehavior_template.json"
},
{
  "python_class": "MalwareMethod",
  "stix_type": "x-mitre-malware-method",
  "python": "",
  "template": "Block_Families/StixORM/SDO/MalwareMethod/MalwareMethod_template.json"
},
{
  "python_class": "MalwareObjective",
  "stix_type": "x-mitre-malware-objective",
  "python": "",
  "template": "Block_Families/StixORM/SDO/MalwareObjective/MalwareObjective_template.json"
},
{
  "python_class": "Matrix",
  "stix_type": "x-mitre-matrix",
  "python": "",
  "template": "Block_Families/StixORM/SDO/Matrix/Matrix_template.json"
},
{
  "python_class": "Mitigation",
  "stix_type": "course-of-action",
  "python": "",
  "template": "Block_Families/StixORM/SDO/Mitigation/Mitigation_template.json"
},
{
  "python_class": "Playbook",
  "stix_type": "playbook",
  "python": "",
  "template": "Block_Families/StixORM/SDO/Playbook/Playbook_template.json"
},
{
  "python_class": "SubTechnique",
  "stix_type": "attack-pattern",
  "python": "",
  "template": "Block_Families/StixORM/SDO/SubTechnique/SubTechnique_template.json"
},
{
  "python_class": "Tactic",
  "stix_type": "x-mitre-tactic",
  "python": "",
  "template": "Block_Families/StixORM/SDO/Tactic/Tactic_template.json"
},
{
  "python_class": "Technique",
  "stix_type": "attack-pattern",
  "python": "",
  "template": "Block_Families/StixORM/SDO/Technique/Technique_template.json"
},
{
  "python_class": "Tool",
  "stix_type": "tool",
  "python": "",
  "template": "Block_Families/StixORM/SDO/Tool/Tool_template.json",
  "data_example": ""
}
```
**]**

**non_stix_sco_types = [**
```json
{
  "python_class": "NetworkTraffic",
  "stix_type": "network-traffic",
  "python": "",
  "template": "Block_Families/StixORM/SCO/NetworkTraffic/NetworkTraffic_template.json",
  "data_example": "Block_Families/StixORM/SCO/NetworkTraffic/Test_network_traffic.json"
},
{
  "python_class": "OCAAsset",
  "stix_type": "x-oca-asset",
  "python": "",
  "template": "Block_Families/StixORM/SCO/OCAAsset/OCAAsset_template.json"
},
{
  "python_class": "OCAFile",
  "stix_type": "x-oca-file",
  "python": "",
  "template": "Block_Families/StixORM/SCO/OCAFile/OCAFile_template.json"
},
{
  "python_class": "OCANetworkTraffic",
  "stix_type": "x-oca-network-traffic",
  "python": "",
  "template": "Block_Families/StixORM/SCO/OCANetworkTraffic/OCANetworkTraffic_template.json"
},
{
  "python_class": "OCAProcess",
  "stix_type": "x-oca-process",
  "python": "",
  "template": "Block_Families/StixORM/SCO/OCAProcess/OCAProcess_template.json"
},
{
  "python_class": "Process",
  "stix_type": "process",
  "python": "",
  "template": "Block_Families/StixORM/SCO/Process/Process_template.json",
  "data_example": "Block_Families/StixORM/SCO/Process/Test_process.json"
},
{
  "python_class": "OCASoftware",
  "stix_type": "x-oca-software",
  "python": "",
  "template": "Block_Families/StixORM/SCO/OCASoftware/OCASoftware_template.json"
},
{
  "python_class": "OCAUserAccount",
  "stix_type": "x-oca-user-account",
  "python": "",
  "template": "Block_Families/StixORM/SCO/OCAUserAccount/OCAUserAccount_template.json"
},
{
  "python_class": "OCAEvent",
  "stix_type": "x-oca-event",
  "python": "",
  "template": "Block_Families/StixORM/SCO/OCAEvent/OCAEvent_template.json"
},
{
  "python_class": "OCAFinding",
  "stix_type": "x-oca-finding",
  "python": "",
  "template": "Block_Families/StixORM/SCO/OCAFinding/OCAFinding_template.json"
},
{
  "python_class": "OCAGeo",
  "stix_type": "x-oca-geo",
  "python": "",
  "template": "Block_Families/StixORM/SCO/OCAGeo/OCAGeo_template.json"
},
{
  "python_class": "OCATTPTag",
  "stix_type": "x-oca-ttp-tag",
  "python": "",
  "template": "Block_Families/StixORM/SCO/OCATagging/OCATTPTag_template.json"
},
{
  "python_class": "WindowsRegistryKey",
  "stix_type": "windows-registry-key",
  "python": "",
  "template": "Block_Families/StixORM/SCO/WindowsRegistryKey/WindowsRegistryKey_template.json",
  "data_example": "Block_Families/StixORM/SCO/WindowsRegistryKey/Test_windows_registry.json"
}
```
**]**

**non_stix_sro_types = [**
```json
{
  "python_class": "AttackRelationship",
  "stix_type": "relationship",
  "python": "",
  "template": "Block_Families/StixORM/SRO/AttackRelationship/AttackRelationship_template.json"
}
```
**]**
