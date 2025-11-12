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
A. Use the second prompt to extend the Phishing Incidents with additional Observed Data, Tasks, Events, Impacts and Sequences around further Sightings (see detail on building out incidents in a_seed/content.md)
B. Use the third prompt to create further notebooks for other types of incidents, e.g., Malware Incident, Data Breach Incident, Ransomware Incident etc.

Developing this data is critical to developing a useful demonstration context memory we can use for developing and demonstrating the OS-Triage Stix Incident Management System.

## Rules for Notebooks

Notebooks are each about a specific part of a larger story:

1. The story of the user and cybersecurity team
2. The story of the company they are working for. They can work for multiple companies
3. The story of each Sighting Extension step in the incident, including all of the Events, Impacts, Tasks and Sequences involved in that sighting

Notebooks are in sections with:
- an initial set of cells for establishing the imports and data file setups
- a cell containing the context memory creation, or the recovery of objects from context memory
- a series of cells, where each cell makes a single object, and saves it to incident context memory, and the sequences of cells add up to the graph pattern storyboard for that notebook

Each cell should have a good title and description that outlines its part in the story. At the end there should be a summary of all of the objects involved, and a mermaid diagram of the connections

Notebooks should be made in the root of the ORchestration directory, and Start with an approriate Step number. There are 4 notebooks currently, but they do not have story board format and need refining into storyboards:

- Orchestration\Step_0_User_Setup.ipynb
- Orchestration\Step_1_Company_Setup.ipynb
- Orchestration\Step_2_Create_Incident_with_an_Alert.ipynb
- Orchestration\Step_3_Get the Anecdote.ipynb


## Understanding the Graph Nature of Stix Incidents, the Storyboard Elements

**Your instructions**

### Task 1

Read the a_seed\5_graph_pattern_nature_of_stix.md to understand the graph nature of Stix Incidents Then, step by step using #sequential-thinking mcp server, go through each class template in the `current_objects`, and  record for each the types of objects it can connect to other objects through its various `ReferenceProperty` or `OSThreatReference` properties. Record all of the graph details for each object in in the \architecture directory, in the `stix-graph-patterns.md` file.

Build a complete graph linkage map of all the current StixORM objects, showing how they can connect to each other through embedded reference fields by looking through each template in `current_objects`, updating the markdown as you go. Add to this map, all of the different connections made through SRO Relationship objects, with various `relationship_types` based on the examples given in the a_seed\5_graph_pattern_nature_of_stix.md file. Build this map exhaustively over all of the objects in `current_objects`, in the most succinct diagram form, but with as much specific detail as possible, so each object class, field name with types of objects, and SRO relationship type's with its types of objects, is clearly defined. You need to be able to reconstitute every possible hierarchy by simply reading this document. Establish it in the \architecture directory and call it the `stix-graph-patterns.md` file in the \architecture directory.

### Task 2

Once it is created, read the `stix-graph-patterns.md` file and then review each of the notebooks using the #sequential-thinking mcop server, and for each notebook, identify the specific parts of the graph pattern that are being created in each notebook:
- Orchestration\Step_0_User_Setup.ipynb
- Orchestration\Step_1_Company_Setup.ipynb
- Orchestration\Step_2_Create_Incident_with_an_Alert.ipynb
- Orchestration\Step_3_Get the Anecdote.ipynb


For example, in the User Setup notebook, identify the parts of the graph pattern that relate to creating user identities, email addresses, and user accounts. In the Company Setup notebook, identify the parts of the graph pattern that relate to creating company identities, systems, and assets. In the Incident Setup notebook, identify the parts of the graph pattern that relate to creating incidents, observed data, indicators, tasks, impacts, events, and sequences. 

From these sequences,work out the story that lies behind each notebook, and document this story in a new file called `notebook-storyboards.md` in the architecture directory. For each notebook, describe the story that is being told, and how it relates to the graph pattern established in the `stix-graph-patterns.md` file.

Then, with  this understanding, work out a story absed on the current objects that can be used to extend the current phishing incident, and to develop an entirely new incident. Document these story boards in the file `incident-extension-storyboard.md` and `new-incident-storyboard.md` in the architecture directory.

### Task 3

Review the file `notebook-storyboards.md` and then use it to create detailed instructions for updating the existing notebooks to focus on the story being told, rather than just the code itself. For each notebook, provide specific instructions on how to update the cells to describe what is happening in the story, and why. Ensure that each cell clearly explains the purpose of the code, and how it fits into the overall story being told in the notebook. Develop this as a prompt in the file .github\prompts\update-current-notebooks-to-storyboards.md

Review the file `incident-extension-storyboard.md` and then use it to create detailed instructions for creating new notebooks that extend the current phishing incident with additional observed data, tasks, events, impacts, and sequences. For each new notebook, provide specific instructions on how to create the cells to describe what is happening in the story, and why. Ensure that each cell clearly explains the purpose of the code, and how it fits into the overall story being told in the notebook. Develop this as a prompt in the file .github\prompts\create-new-notebooks-for-phishing-incident.md

Review the file `new-incident-storyboard.md` and then use it to create detailed instructions for creating new notebooks that tell the story of a new type of incident, such as a malware incident, data breach incident, or ransomware incident. For each new notebook, provide specific instructions on how to create the cells to describe what is happening in the story, and why. Ensure that each cell clearly explains the purpose of the code, and how it fits into the overall story being told in the notebook. Develop this as a prompt in the file .github\prompts\create-new-notebooks-as-storyboards.md

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
