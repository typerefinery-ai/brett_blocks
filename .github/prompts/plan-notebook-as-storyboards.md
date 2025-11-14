# Plan Notebooks as Storyboards for the OS-Triage Stix Incident Reporting System

## Aim

The aim is to use #sequential-thinking mcp server to research and document the graph nature of Stix Incidents through a multi-step process in the architecture and instructions.

You will then use this knowledge to refine and perfect 3 prompts to:

- update current notebooks to storyboards, the create user, create company and two stages of developing a phishing incident story - .github\prompts\update-current-notebooks-to-storyboards.md
- create new notebook storyboards current the phishing incident story - .github\prompts\create-new-notobooks-for-phishing-incident.md
- create new notebooks as storyboards - .github\prompts\create-new-notebooks-as-storyboards.md

The first prompt is to convert the 4 existing notebooks so as to focus on the story of what is happening in each notebook, rather than just the code itself. Every time a particular object is made, and then saved to context memory, we should describe what is happening in the story. setup each cell to describe what is happening in the story, and why. There are 3 separate stories to tell here:

1. The story to describe the creation of the user and team objects, and saving them to context memory
2. The story to describe the creation of a fictional company, its IT systems and assets, and saving them to context memory. any user can support multiple companies
3. The story to describe the creation of a hypothetical incident, its observed data, indicators, tasks, impacts, events and sequences, and saving them to context memory. the first incident is phishing.

By focusing on the story, we can make it clearer what is happening in each notebook, and why. This will help users understand the purpose of each notebook, and how they fit together to create a complete Stix Incident Reporting System.

Then we can:

- Use the second prompt to extend the Phishing Incidents with additional Observed Data, Tasks, Events, Impacts and Sequences around further Sightings (see detail on building out incidents in a_seed/content.md)
- Use the third prompt to create further notebooks for other types of incidents, e.g., Malware Incident, Data Breach Incident, Ransomware Incident etc.

Developing this data is critical to developing a useful demonstration context memory we can use for developing and demonstrating the OS-Triage Stix Incident Management System.

## Rules for Storyboards

We want the storyboard of each notebook to clearly describe the story of what is happening in each notebook, and why. Some of the notebooks are self-contained, e.g., the user setup and company setup notebooks. Others are part of a larger story, e.g., the incident setup and multiple incident development notebooks. 

Our initial setup has 4 notebooks so far, that establish the story of:
- setting up a user and team
- setting up a company
- setting up a phishing incident with an alert, based on an email message receieved by email-addr in the company, containing an url, with SRO relationship with `relationship_type` = `contains` between the email-message and the url. The SCO's, including the url, must be contained within an observed-data object  `object_ref` field, with a SRO sighting object linking the email-message to the url through the observed-data object. The incident is continued by adding an indicator object based on the observed-data, with a SRO relationship of `indicates` between the indicator and the incident. The incident is further continued by adding a task object to investigate the indicator, with a SRO relationship of `investigates` between the task and the indicator. The incident is further continued by adding an event object to record the investigation, with a SRO relationship of `related-to` between the event and the task. The incident is further continued by adding an impact object to record the impact of the incident, with a SRO relationship of `impacts` between the impact and the incident. The incident is finally continued by adding a sequence object to record the sequence of events in the incident, with a SRO relationship of `has-sequence` between the sequence and the incident.
- continuing the incident by adding a user report in an anecdote SCO object, a report from a user about the email message, with similar ideas for further notebooks to extend the phishing incident, and to create new incidents.

A story for the fourth step, a sketch of the 3rd stage in the Incident story is ready, but a notebook has not yet been designed for the story:

- The story for the notebook is a sighting of context data, from the Microsoft Exchange, retrieved based on whoever received the phishing email. Other users from the company receiving the email messsage, "sbilly@example.com, wwhilly@example.com, strange@mycompany.com, dumbo@mycompany.com" had received the same email. Warning, Identity, email Address and User Account details for these users must be addded to the second notebook, the initial user setup notebook, but with appropriate names, email addresses and user account details in order to support this story. Each of these users should have sightings of the same email message, and observed data containing the email message and url. The incident should be updated to include these sightings, and the indicator, task, event, impact and sequence objects should be updated to include references to these new sightings.

Ideally, we have sufficient notebooks to tell the story of two different complete incident's, with multiple sightings, events, impacts, tasks and sequences, for two different companies. Each company, its assets and users details should be setup in a single notebook. Each notebook within an Incident should build on the previous one, and add new objects to the context memory. Each notebook should be self-contained, and should not require any external data although some key objects can be retrieved from contenxt memory using get context memory python blocks.

## Rules for Notebooks

Notebooks are each about a specific part of a larger story. The story of a user, who documents himself and his team, the multiple companies they work for, and the incidents they manage. Each incident is made up of multiple sightings, each sighting made up of multiple events, impacts, tasks and sequences. Notebooks can only include objects when the object's directory has make_object.py file in the StixORM structure.

Notebook cells do not import Python block modules and functions directly, instead they use helper functions in the Orchestration\Utilities\local_make_sdo.py and Orchestration\Utilities\local_make_sco.py files to make the objects. This ensures that all of the data formatting and embedded reference handling is done in a consistent way.

Thus, each notebook tells part of the overall story of either:

1. The user initialises the app, and creates the data for themselves and their cybersecurity team
2. The user creates the details for a specific Company (an "Identity" object with the role "organization") they are working for, one or more
3. The story of each step in an incident, including all of the Sightings, Events, Impacts, Tasks and Sequences involved. Objects are createvd and saved to context memory as the story progresses.
4. The first notebook for setting up an incident, or for setting up a company must use the create_incident_context.py utility to create the initial context memory for that incident or create_company_context.py for a company. The following notebooks retrieve tjhose details from context memory.

Notebooks are in sections, based on rows containing a markdown cell wich contains the story and a code cell, which tells the story in a minimilist method of creating and saving the stix objects. The Notebooks invoke the blocks code through helpers in the existing utilities (e.g. Orchestration\Utilities\local_make_sdo.py), always with an input data form, sometimes with multiple inputs of additional objects for embedded references. The utility will consolidate the data into the correct block input format and pass it to the Python make_object.py file, which will make the data object and hand it back. The first objective of the row is complete, the object is made, no it needs to be saved to context memory.

Overall, the entire notebook describes a story of building up the context memory for a particular sighting, event, task or impact of the overall incident story. A task used to step forward, a sighting made of an obervations or piece of evidence, in a the process of incident management.



Notebook's must contain:

- an initial set of rows for establishing the imports and data file setups
- one or more rows containing the context memory creation, or the recovery of objects from context memory
- a series of rows, where each row makes a single object, and saves it to incident context memory, and the sequences of cells add up to the graph pattern storyboard for that notebook
- a summary row

Each cell should have a good title and description that outlines its part in the story. At the end there should be a summary of all of the objects involved, and a mermaid diagram of the connections. The code cell below should be as simple as possible, with no extraneous code.

Notebooks should be made in the root of the ORchestration directory, and Start with an approriate Step number. There are 4 notebooks currently, but they do not have story board format and need refining into storyboards:

- Orchestration\Step_0_User_Setup.ipynb
- Orchestration\Step_1_Company_Setup.ipynb
- Orchestration\Step_2_Create_Incident_with_an_Alert.ipynb
- Orchestration\Step_3_Get the Anecdote.ipynb


## Understanding the Graph Nature of Stix Incidents, the Storyboard Elements

**Your instructions**

### Task 1 - Map Possible connections Between the Objects

Read the a_seed\5_graph_pattern_nature_of_stix.md to understand the graph nature of Stix Incidents. Your aim is to step by step using #sequential-thinking mcp server go through a series of sub-tasks:

1. Summarise Seed: First, can you create a complete summary of the seed document in the file `.github\architecture\stix-graph-patterns.md`, so that every piece of data is retained and it is as accurate as the seed document, but it is more succinctly documented and easier for you to retain. Is there any way you can report on the diffrences between the original seed document and your improved document.

2. Find Additional Graph Patterns for Seed from Templates: Go through every template file in the the `current_objects` collection, to determine if there are patterns of embedded relations and SRO `relationship_type` connections in the data that are not described in the seed document. Record for each template the types of other objects it can connect to through embedded references, the`ReferenceProperty` or `OSThreatReference` properties. Record these additionmal sub-graph patterns in the same format as the exsiting patterns.  Can you extend your summary document in the file `.github\architecture\stix-graph-patterns.md`, to include these additional connections, and highlight which ones are new compared to the seed document.


### Task 2 - Map Existing Notebooks to Graph Patterns and Record the Stories 

Once Task 1 is complete, read the `stix-graph-patterns.md` file and then review each of the notebooks using the #sequential-thinking mcop server, and for each notebook, identify the specific parts of the graph pattern that are being created in each notebook, and the storyboard that is being told in each notebook. Record the results in the markdown file identified in each item. We want to be able to review all of your sotry boards before giving you the go-ahead from reviewing the notebooks. The notebooks to review and the documents to write the story in are:

- User Initialisation: Orchestration\Step_0_User_Setup.ipynb -> Record the story in .github\architecture\new_user.md
- Company Setup: Orchestration\Step_1_Company_Setup.ipynb -> Record the story in.github\architecture\new_company.md
- Incident Setup: Orchestration\Step_2_Create_Incident_with_an_Alert.ipynb -> Record the story in .github\architecture\phising-incident.md
- Anecdote Retrieval: Orchestration\Step_3_Get the Anecdote.ipynb -> Record the story in .github\architecture\phising-incident.md

When each of these 4 notebooks is analysed, work out a series of instructions to yourself when building a particular notebook in `.github\architecture\notebook-storyboards.md` in the .architecture directory. Assume the AI gets your new Stix graph summary from 1, so it understands Stix graphs. What other details from this document should be included.

### Task 3 - Plan in Detail, Make complete Examples Before Creating the Ntotebooks

Delete any contents in the file `notebook-storyboards.md` and then use it to create detailed instructions for updating the existing notebooks to focus on the story being told, rather than just the code itself. For each notebook, provide specific instructions on how to update the cells to describe what is happening in the story, and why. Ensure that each cell clearly explains the purpose of the code, and how it fits into the overall story being told in the notebook. Develop this as a prompt in the file .github\prompts\update-current-notebooks-to-storyboards.md

Delete any contents in the file `incident-extension-storyboard.md` and then use it to create detailed instructions for creating new notebooks that extend the current phishing incident with additional observed data, tasks, events, impacts, and sequences. For each new notebook, provide specific instructions on how to create the cells to describe what is happening in the story, and why. Ensure that each cell clearly explains the purpose of the code, and how it fits into the overall story being told in the notebook. Develop this as a prompt in the file .github\prompts\create-new-notebooks-for-phishing-incident.md

Delete any contents in the file `new-incident-storyboard.md` and then use it to create detailed instructions for creating new notebooks that tell the story of a new type of incident, such as a malware incident, data breach incident, or ransomware incident. For each new notebook, provide specific instructions on how to create the cells to describe what is happening in the story, and why. Ensure that each cell clearly explains the purpose of the code, and how it fits into the overall story being told in the notebook. Develop this as a prompt in the file .github\prompts\create-new-notebooks-as-storyboards.md

## Limited Scope of Current, Next and Future StixORM Objects

At the moment, the number of Stix objects available to us are limited by the number of directories with "make_object.py" format. The objects currently available are given in the `current_objects` dictionary below. Each of these directories has a class template that can be used to identify fields for valuesand embedded references ( a `property` value of either `ReferenceProperty` or `OSThreatReference`) for dependency hierarchies.

Reviewing these three types of objects to document all of the possible embedded reference dependency hierarchies that can be included in our storyboards. In the future we can expand our storyboards to include the additional stix objects when we have completed their  `make_object.py` files.

```json
current_objects = {
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
