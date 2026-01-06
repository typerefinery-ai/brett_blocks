# Creating a Single Incident Notebook, a step in an Incident story, with its own storyboard and properly structured code cells


## 1. Overall Incident Context

Any Incident will contain multiple notebooks, each one representing a step in the incident response workflow, essentially collecting evidence for a single new sighting object. Each notebook then, will have its own storyboard and properly structured code cells, based on this evidence sighting, following the section-based structure outlined below.

At the moment there is limited objects and hence the first incident is cast as a phishing email, and so the storyboard is the same as the old notebooks. However, to create a richer storyboard, you can create new data forms for existing object types by copying and modifying existing data forms in the StixORM directories, as described in section 1.2 below.

### 1.1 Currently, an Incident Can Only Be Based on the following Objects from the StixORM directories

To make Stix objects, there must be both a make object python block, and as a minimim one data form, for every object type used in the incident notebook. Currently, only the following object types have make object blocks and data forms in the StixORM directories:

```python
invoke_make_objects = {
    "sdo_make_files": [
        {
            "python_class": "Identity",
            "stix_type": "identity",
            "data_example": "Block_Families/StixORM/SDO/Identity/identity_IT_user1.json"
        },
        {
            "python_class": "Indicator",
            "stix_type": "indicator",
            "data_example": "Block_Families/StixORM/SDO/Indicator/indicator_alert.json"
        },
        {
            "python_class": "Impact",
            "stix_type": "impact",
            "data_example": "Block_Families/StixORM/SDO/Impact/anecdote_impact.json"
        },
        {
            "python_class": "Incident",
            "stix_type": "incident",
            "data_example": "Block_Families/StixORM/SDO/Incident/phishing_incident.json"
        },
        {
            "python_class": "Event",
            "stix_type": "event",
            "data_example": "Block_Families/StixORM/SDO/Event/event_alert.json"
        },
        {
            "python_class": "ObservedData",
            "stix_type": "observed-data",
            "data_example": "Block_Families/StixORM/SDO/Observed_Data/observation-alert.json"
        },
        {
            "python_class": "Sequence",
            "stix_type": "sequence",
            "data_example": "Block_Families/StixORM/SDO/Sequence/sequence_alert.json"
        }
        {
            "python_class": "Task",
            "stix_type": "task",
            "data_example": "Block_Families/StixORM/SDO/Task/task_alert.json"
        }
    ],
    "sco_make_files": [
        {
            "python_class": "Anecdote",
            "stix_type": "anecdote",
            "data_example": "Block_Families/StixORM/SCO/Anecdote/anecdote_on_impact.json"
        },
        {
            "python_class": "EmailAddress",
            "stix_type": "email-addr",
            "data_example": "Block_Families/StixORM/SCO/EmailAddress/email_addr_IT_user1.json"
        },
        {
            "python_class": "UserAccount",
            "stix_type": "user-account",
            "data_example": "Block_Families/StixORM/SCO/UserAccount/usr_account_IT_user1.json"
        },
        {
            "python_class": "URL",
            "stix_type": "url",
            "data_example": "Block_Families/StixORM/SCO/URL/suspicious_url.json"
        },
        {
            "python_class": "EmailMessage",
            "stix_type": "email-message",
            "data_example": "Block_Families/StixORM/SCO/Email_Message/suspicious_email_msg.json"
        }
    ],
    "sro_make_files": [
        {
            "python_class": "Relationship",
            "stix_type": "relationship",
            "data_example": "Block_Families/StixORM/SRO/Relationship/sro_employed_by.json"
        },
        {
            "python_class": "Sighting",
            "stix_type": "sighting",
            "data_example": "Block_Families/StixORM/SRO/Sighting/sighting_context.json"
        }
    ]
}
```

Thus, storyboards are currently limited to the existing objects, and the data forms used in the old notebooks:

- old step 1 notebook: Orchestration\history\Step_1 _Create_Incident_with_an_Alert.ipynb
- old step 2 notebook: Orchestration\history\Step_2 _Get the Anecdote.ipynb

However in order to create a better stroyboard, you can create and customise new data forms by copying and modifying existing forms as shown below

### 1.2 You Can Create Custom Data Forms to Vary the Storyboard, while still using only the Existing Objects

When extending or modifying the storyboard of an incident notebook, you can create new data forms for any of the existing object types, by copying and modifying existing data forms. For example, in the old step 1 notebook, only a single task is created, task_alert, using the data form: Block_Families\StixORM\SDO\Task\task_alert.json.

Now, assume you know want to create two new tasks, a task to create an indicator and a task to determine false positive, to extend the incident response workflow. You can create two new data forms by copying and modifying the existing data form for task_alert, as follows:

#### 1.2.1 Create a new data form for task to create an indicator

Open the existing data form for task_alert: Block_Families\StixORM\SDO\Task\task_alert.json, and save a copy as Block_Families\StixORM\SDO\Task\task_validate.json. Then modify the fields in the new data form to reflect the details of the create indicator task, such as changing the name, description, and any other relevant fields, as shown below.

```json
{
    "task_form": {
        "base_required": {
            "type": "task",
            "spec_version": "2.1",
            "id": "",
            "created": "",
            "modified": ""
        },
        "base_optional": {
            "created_by_ref": "",
            "revoked": null,
            "labels": [],
            "lang": "",
            "external_references": [],
            "object_marking_refs": [],
            "granular_markings": []
        },
        "object": {
            "name": "Task to Create Indicator",
            "description": "Task to create an indicator based on the analysis of the alert.",
			"task_type": "investigation",
			"priority": "medium",
			"status": "in_progress",
			"start_time": "",
			"due_time": ""
        },
        "extensions": {
            "extension-definition--4ca6de00-5b0d-45ef-a1dc-ea7279ea910e": {
                "extension_type": "new-sdo"
            }
        },
        "sub": {}
    }
}
```


#### 1.2.2 Create a new data form for task to determine false positive

Open the existing data form for task_alert: Block_Families\StixORM\SDO\Task\task_alert.json, and save a copy as Block_Families\StixORM\SDO\Task\task_determine_fp.json. Then modify the fields in the new data form to reflect the details of the task_determine_fp task, such as changing the name, description, and any other relevant fields, as shown below.

```json
{
    "task_form": {
        "base_required": {
            "type": "task",
            "spec_version": "2.1",
            "id": "",
            "created": "",
            "modified": ""
        },
        "base_optional": {
            "created_by_ref": "",
            "revoked": null,
            "labels": [],
            "lang": "",
            "external_references": [],
            "object_marking_refs": [],
            "granular_markings": []
        },
        "object": {
            "name": "Task to Determine False Positive	",
            "description": "Task to determine if an alert is a false positive based on the analysis.",
			"task_type": "investigation",
			"priority": "medium",
			"status": "in_progress",
			"start_time": "",
			"due_time": ""
        },
        "extensions": {
            "extension-definition--4ca6de00-5b0d-45ef-a1dc-ea7279ea910e": {
                "extension_type": "new-sdo"
            }
        },
        "sub": {}
    }
}
```

### 1.2.3 You must create a new data form to extend the storyboard pas the old Notebooks

To extend the storyboard to make it as rich as possible, you must  create many new data form json files in the StixORM directories, by copying and modifying existing data forms as shown above. This allows you to create a rich storyboard with many steps, while still using only the existing object types that have make object blocks in the StixORM directories.

### 1.3 Incident Context Must be Initialised in the first Notebook in the Storyboard, then it is set as the current incident for subsequent Notebooks

The incident context must be initialised in the first notebook of the incident, by creating the new Incident object itself, with minimal data, and then using to to create the incident context. Subsequent notebooks in the incident can then build upon this incident context, since it will be set as the current incident in the Orchestration\generated\os-triage\context_mem\context_map.json file (when the context memory is not cleared).

## 2. Section-based Structure of every Incident Notebook

Apart from the incident context initialisation in the first notebook, every incident notebook follows a structured approach to organize the investigation process. Each notebook is divided into several sections, each with a specific purpose, as outlined below:

## 3. Section A: Header Storyboard and Code Cells

The Header includes a series of cells that provide essential information about the incident notebook. This section typically includes:

### 3.1 Title and overview storyboard markdown cell

The first markdown cell contains the title and the overview storyboard in markdown format, outlining the purpose and scope of the incident notebook.

### 3.2 Setup Logging and Relative Path Imports Code Cell

The first code cell sets up logging for the notebook and imports necessary modules using relative paths to ensure that all dependencies are correctly referenced.

```python
import sys
!{sys.executable} -m pip install stixorm
import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
sys.path.append('../')
```


### 3.3 Import of Make Object StixORM blocks, OS Triage Context blocks Code Cell and Setup Basic Paths

The next code cell imports the necessary make object blocks from the StixORM directories, as well as the OS Triage context blocks. Blocks can only be executed by using a middle layer, of invoke functions from the Utilities directory.

It also sets up basic paths required for the notebook's operations, as an example the old Step 1.

```python
import json
from Utilities.local_make_sro import invoke_sro_block, invoke_sighting_block
from Utilities.local_make_sdo import (
    invoke_make_observed_data_block, invoke_make_indicator_block, invoke_make_event_block, invoke_make_sequence_block,
    invoke_make_task_block, invoke_make_incident_block, invoke_make_identity_block, invoke_make_impact_block
)
from Utilities.local_make_sco import (
    invoke_make_email_addr_block, invoke_make_url_block, invoke_make_e_msg_block, invoke_make_anecdote_block, invoke_make_user_account_block
)
from Utilities.local_make_general import invoke_create_incident_context, invoke_save_incident_context_block, invoke_get_from_company_block, invoke_get_from_user_block
from conv import conv

context_base = "../Orchestration/generated/os-triage/context_mem/"
path_base = "../Block_Families/StixORM/"
results_base = "../Orchestration/Results/"
```
This cell will also setup any data structurees needed to describe data for the storyboard steps in this notebook, such as the alert data in the old Step 1 notebook. Revall that new data forms must be created by copying and modifying existing data forms in the StixORM directories, as described in section 1.2 above.

### 3.4 Initialize Incident Context Code Cell

The first notebook in the incident must include a code cell to initialize the incident context, by creating the new Incident object itself, with minimal data, and then using to to create the incident context. Subsequent notebooks in the incident can then build upon this incident context, since it will be set as the current incident in the Orchestration\generated\os-triage\context_mem\context_map.json file (when the context memory is created).

## 4. Section B: "Get Objects from Previous Notebooks"  for use in this incident, with Storyboard and Code Cells

The second section of each notebook provides a markdown cell for the storyboard, outlining the objects that need to be retrieved from previous notebooks in the incident. This is followed by code cells that execute the necessary functions to fetch these objects from the context memory, ensuring that all relevant data is available for analysis in the current notebook.

To get objects from previous notebooks, the following code pattern is used to get objects from the Company context memory, or the User context memory, as shown below in the old Step 1 notebook. Note that a query is setup to find the object based on a property value, such as the email address value or the identity name, and the context type is set.

```python
# 1. For Naive Smith, find the user account and the email. Plus get my own identity
reporter_name = alert_data["reporter"]
to_email_addr = alert_data["to"]
TR_name = "Trusty Jones"
#
# 2. Setup variables and queries to get the objects from the company context memory
#
context_type = {
    "context_type": "users"
}
email_query = {
    "type" : "email-addr",
    "property": {
        "path": ["value"],
        "source_value": to_email_addr,
        "comparator": "EQ"
    }
}
reporter_email_addr = invoke_get_from_company_block(email_query, context_type, source_value=None, source_id=None)
#
# 3. Setup variables and queries to get the objects from the user context memory
#
context_type = {
    "context_type": "me"
}
TR_ident_query = {
    "type" : "identity",
    "property": {
        "path": ["name"],
        "source_value": TR_name,
        "comparator": "EQ"
    }
}
TR_identity = invoke_get_from_user_block(TR_ident_query, context_type, source_value=None, source_id=None)
```

## 5. Section C: Create and Save New Objects to Assemble the Sighting in this Incident Notebook, with Storyboard and Code Cells

This section includes a series of markdown cell's and code cell's, where each of the SCO objects, SDO objects and SRO objects needed to assemble the sighting in this incident notebook are created and saved to the context memory in a single code cell. Each code cell corresponds to the two-step process to create a specific object and save it to the incident context step, following the storyboard outlined in the markdown cell.

All invoke make object block functions have a defined parameter signature:

- first is the path to the data form from the StixORM directory, either existing or one you have amde
- second is the results path to save the new object json file
- third and subsequent parameters are based on embedded reference parameters described in the stix graph document

The invoke_save_incident_context_block function has a defined parameter signature:

- first is the path to the new object json file created in the previous step
- second is the path to save the context memory json file for this object in the incident context


```python
msg_path = "SCO/EmailMessage/suspicious_email_msg.json"
results_path = "step2/SUSS__email_msg.json"
from_ref = threat_email_addr
to_ref = [reporter_email_addr]
cc_ref = []
bcc_ref = []
# make the email object
sus_msg = invoke_make_e_msg_block(msg_path, results_path, from_ref, to_ref, cc_ref, bcc_ref)
# add the record to the in-session bundles and lists
msg_results_context_path = results_base + "step2/THREAT__email_msg_context.json"
result = invoke_save_incident_context_block(results_base + results_path, msg_results_context_path)
print(f" result->{result}")
```

Recall that new data forms must be created by copying and modifying existing data forms in the StixORM directories, as described in section 1.2 above, in order to make a better storyboard that the old notebook, with varied SCO's and SDO's.

## 6. Section D: Create and Save new Events and Tasks in this Incident Notebook, with Storyboard and Code Cells

This section includes a series of markdown cell's and code cell's, where each of the Event objects and Task objects needed to document the investigation steps in this incident notebook are created and saved to the context memory in a single code cell. Each code cell corresponds to the two-step process to create a specific object and save it to the incident context step, following the storyboard outlined in the markdown cell.

Recall that new data forms must be created by copying and modifying existing data forms in the StixORM directories, as described in section 1.2 above, in order to make a better storyboard that the old notebook, with varied Events and Tasks.

## 7. Section E: Create, Chain and Save Sequences for Events and Tasks in this Incident Notebook, with Storyboard and Code Cells

This section includes a series of markdown cell's and code cell's, where each of the Sequence objects needed to chain the Event objects and Task objects in this incident notebook are created, chained together and saved to the context memory in a single code cell. Note that the approach taken in the old Notebook is incorrect. Each Sequence code cell corresponds to the three-step process to create a specific Sequence object that sequences an Event or Task object to it, chain that sequence object to the last sequence object of that sequence type, and then save it to the incident context step, following the storyboard outlined in the markdown cell. Eas an example, the code to create, chain and save the sequence for an Event object is shown below. Notice particularly how all of the paths are setup correctly.

```python
# E.1 Create sequence for event (alert detection)
sequence_data_path = "SDO/Sequence/sequence_alert.json"
results_path = "step2/sequence_event.json"
step_type = "single_step"
sequence_type = "event"
sequenced_object = event  # Pass whole event object

# Step 1: Create sequence
seq_event = invoke_make_sequence_block(
    sequence_data_path, 
    results_path, 
    step_type=step_type, 
    sequence_type=sequence_type, 
    sequenced_object=sequenced_object, 
    on_completion=None, 
    on_success=None, 
    on_failure=None, 
    next_steps=None
)

# Step 2: Chain sequence
chain_result_path = results_base + "step2/chain_event_result.json"
invoke_chain_sequence_block(results_base + results_path, chain_result_path)
print(f"✅ seq_event chained")

# Step 3: Save sequence
sequence_results_context_path = results_base + "step2/event_sequence_context.json"
result = invoke_save_incident_context_block(results_base + results_path, sequence_results_context_path)
print(f"✅ event sequence created: {seq_event['id']}")
print(f"   result->{result}")
```

Recall that new Sequence data forms to describe new situations must be created by copying and modifying existing data forms in the StixORM directories, as described in section 1.2 above, in order to make a better storyboard that the old notebook, with sequenced Events and Tasks.

## 8. Section F: Create and Save the Impact Objects in this Incident Notebook, with Storyboard and Code Cells

This section includes a series of markdown cell's and code cell's, where each of the Impact objects needed to document the impact of the incident in this incident notebook are created and saved to the context memory in a single code cell. Each code cell corresponds to the two-step process to create an Impact object and save it to the incident context step, following the storyboard outlined in the markdown cell.

Recall that new Impact data forms must be created by copying and modifying existing Impact data forms in the StixORM directories, as described in section 1.2 above, in order to make a better storyboard that the old notebook, with varied Impacts.

## 9. Section G: Create and Save SRO Reltationship Objects in this Incident Notebook, with Storyboard and Code Cells

This section includes a series of markdown cell's and code cell's, where each of the SRO Relationship objects needed to document the relationships between the various SCO and SDO objects in this incident notebook are created and saved to the context memory in a single code cell. Each code cell corresponds to the two-step process to create a specific Relationship object and save it to the incident context step, following the storyboard outlined in the markdown cell.

Recall that new Relationship data forms must be created by copying and modifying existing Relationship data forms in the StixORM directories, as described in section 1.2 above, in order to make a better storyboard that the old notebook, with varied Relationships. Note that Retlationship data-forms only have a single value that needs to be modified, the "relationship_type" field. This makes it easy to create the relationship types you wise, as long as they are from the existing Stix relationship types.


## 10. Section H: Summary of the page operations to get, create, chain or save objects in this Incident Notebook, with Storyboard and Code Cells

Ideally, at the end of the ntoebook, there should be a summary markdown cell that outlines all the operations performed in the notebook, including getting objects from previous notebooks, creating new objects, chaining sequences, and saving everything to the incident context. This provides a clear overview of the notebook's activities and ensures that all steps are documented for future reference. If code is required to add together the statistics, then this can be included in a final code cell.