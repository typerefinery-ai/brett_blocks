# Plan Notebooks as Storyboards for a Stix Incident Reporting System

## Aim

The aim is to refine and perfect 3 prompts to:
- update current notebooks to storyboards - .github\prompts\update-current-notebooks-to-storyboards.md
- create new notebooks for the phishing incident story - .github\prompts\create-new-notobooks-for-phishing-incident.md
- create new notebooks as storyboards - .github\prompts\create-new-notebooks-as-storyboards.md

The first prompt is to convert the 4 existing notebooks so as to focus on the story of what is happening in each notebook, rather than just the code itself. Every time a particular object is made, and then saved to context memory, we should describe what is happening in the story. setup each cell to describe what is happening in the story, and why. There are 3 separate stories to tell here:

1. The story to describe the creation of the user and team objects, and saving them to context memory
2. The story to deascribe the creation of a fictional company, its IT systems and assets, and saving them to context memory
3. The story to describe the creation of a phishing incident, its observed data, indicators, tasks, impacts, events and sequences, and saving them to context memory

By focusing on the story, we can make it clearer what is happening in each notebook, and why. This will help users understand the purpose of each notebook, and how they fit together to create a complete Stix Incident Reporting System.

Then we can:
A. Use the second prompt to extend the Phishing Incidents with additional Observed Data, Tasks, Events, Impacts and Sequences around further Sightings (see detail on building out incidents in a_seed/content.md)
B. Use the third prompt to create further notebooks for other types of incidents, e.g., Malware Incident, Data Breach Incident, Ransomware Incident etc.

The key for the design of each notebook, beyond the import section, is to focus each cell on the story of making that specific object and saving it to context memory, all part of a sequence which tells the overall story of the incident reporting system.


At the moment, the number of Stix objects available to us are limited by the number of directories with "make_object.py" format.

Lets register a current set of Python make_object.py files that collects the currently available list of SDO's, SCO's and SRO's. 

Note  that we use the Identity object for multiple purposes, based on fields like "identity_class" including:

- An Individual e.g. -> Block_Families/StixORM/SDO/Identity/identity_IT_user1.json
- A Company e.g. -> Block_Families/StixORM/SDO/Identity/identity_TR_user_company.json
- A Laptop e.g.-> Block_Families/StixORM/SDO/Identity/identity_Laptop1.json
- A system e.g. -> Block_Families/StixORM/SDO/Identity/identity_IT_user1.json


First read a_seed/content.md, which describes how different types of content, python file, class template and json, data template json files in a content directory interact. Then look through the below list, opening and reading the 3 files for each stix type. By comparing how this works you will see how the design of the class template, sets the layout of the Python function. How the first, mandatory input in the main is always the data form, and the other optional inputs are embedded references, mostly fields ending with `_ref` or `_refs`.  Further you can see how the data form tamplate is based on the class template, except the "sub" section, which holds sub-objects is emplaced within the actual data form.

Reviewing these three types of objects all Compare how this pattern works
```json
{
  "sdo_make_files": [
	{
		"stix_type": "identity",
		"python": "Block_Families/StixORM/SDO/Identity/make_identity.py",
		"template": "Block_Families/StixORM/SDO/Identity/Identity_template.json",
		"data_example": "Block_Families/StixORM/SDO/Identity/identity_IT_user1.json"
	},
	{
		"stix_type": "indicator",
		"python": "Block_Families/StixORM/SDO/Indicator/make_indicator.py",
		"template": "Block_Families/StixORM/SDO/Indicator/Indicator_template.json",
		"data_example": "Block_Families/StixORM/SDO/Indicator/indicator_alert.json"
	},
	{
		"stix_type": "impact",
		"python": "Block_Families/StixORM/SDO/Impact/make_impact.py",
		"template": "Block_Families/StixORM/SDO/Impact/Impact_template.json",
		"data_example": "Block_Families/StixORM/SDO/Impact/anecdote_impact.json"
	},
	{	
		"stix_type": "incident", 
		"python": "Block_Families/StixORM/SDO/Incident/make_incident.py",
		"template": "Block_Families/StixORM/SDO/Incident/Incident_template.json",
		"data_example": "Block_Families/StixORM/SDO/Incident/phishing_incident.json"
	},
	{
		"stix_type": "event",
		"python": "Block_Families/StixORM/SDO/Event/make_event.py",
		"template": "Block_Families/StixORM/SDO/Event/Event_template.json",
		"data_example": "Block_Families/StixORM/SDO/Event/event_alert.json"
	},
	{
		"stix_type": "observed-data",
		"python": "Block_Families/StixORM/SDO/Observed_Data/make_observed_data.py",
		"template": "Block_Families/StixORM/SDO/Observed_Data/ObservedData_template.json",
		"data_example": "Block_Families/StixORM/SDO/Observed_Data/observation-alert.json"
	},
	{
		"stix_type": "sequence",
		"python": "Block_Families/StixORM/SDO/Sequence/make_sequence.py",
		"template": "Block_Families/StixORM/SDO/Sequence/Sequence_template.json",
		"data_example": "Block_Families/StixORM/SDO/Sequence/sequence_alert.json"
	},
	{
		"stix_type": "task",
		"python": "Block_Families/StixORM/SDO/Task/make_task.py",
		"template": "Block_Families/StixORM/SDO/Task/Task_template.json",
		"data_example": "Block_Families/StixORM/SDO/Task/task_alert.json"
	}
  ],
  "sco_make_files": [
	{
		"stix_type": "anecdote",
		"python": "Block_Families/StixORM/SCO/Anecdote/make_anecdote.py",
		"template": "Block_Families/StixORM/SCO/Anecdote/Anecdote_template.json",
		"data_example": "Block_Families/StixORM/SCO/Anecdote/anecdote_on_impact.json"
	},
	{
		"stix_type": "email-addr",
		"python": "Block_Families/StixORM/SCO/EmailAddress/make_email_addr.py",
		"template": "Block_Families/StixORM/SCO/EmailAddress/EmailAddress_template.json",
		"data_example": "Block_Families/StixORM/SCO/EmailAddress/email_addr_IT_user1.json"
	},
	{
		"stix_type": "user-account",
		"python": "Block_Families/StixORM/SCO/UserAccount/make_user_account.py",
		"template": "Block_Families/StixORM/SCO/UserAccount/UserAccount_template.json",
		"data_example": "Block_Families/StixORM/SCO/UserAccount/usr_account_IT_user1.json"
	},
	{
		"stix_type": "url",
		"python": "Block_Families/StixORM/SCO/URL/make_url.py",
		"template": "Block_Families/StixORM/SCO/URL/URL_template.json",
		"data_example": "Block_Families/StixORM/SCO/URL/suspicious_url.json"
	},
	{
		"stix_type": "email-message",
		"python": "Block_Families/StixORM/SCO/Email_Message/make_email_msg.py",
		"template": "Block_Families/StixORM/SCO/Email_Message/EmailMessage_template.json",
		"data_example": "Block_Families/StixORM/SCO/Email_Message/suspicious_email_msg.json"
	}
  ],
  "sro_make_files": [
	{
		"stix_type": "relationship",
		"python": "Block_Families/StixORM/SRO/Relationship/make_sro.py",
		"template": "Block_Families/StixORM/SRO/Relationship/Relationship_template.json",
		"data_example": "Block_Families/StixORM/SRO/Relationship/sro_employed_by.json"
	},
	{
		"stix_type": "sighting",
		"python": "Block_Families/StixORM/SRO/Sighting/make_sighting.py",
		"template": "Block_Families/StixORM/SRO/Sighting/Sighting_template.json",
		"data_example": "Block_Families/StixORM/SRO/Sighting/sighting_context.json"
	}
  ]
}
```

[text](../../Block_Families/StixORM/SRO/Sighting/sighting_context.json)