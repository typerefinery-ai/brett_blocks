# Fixing the Sequences in the Get the Anecdote Notebook

## Background:

After some intial setup cells, the Step 2 noteobook (Orchestration\Step_2_Create_Incident_with_an_Alert.ipynb) uses a fixed pattern. Each code cell does two operations"
1. Create a STIX object using a "make_<object_class>.py" block
2. Save the object into incident context memory using a "save incident context" block

Despite this success, everything you have setup about the Sequence objects in Step 2 notebooks is incorrect following the string "# G.2 Create sequence for task_determine_fp". Instead of doing two ooperations, with a Sequence objectg one must do 3 operations:
1. Create a Sequence STIX object using the "make_Sequence.py" block
2. Chain the Sequence object into the workflow using the "chain_sequence.py" block
3. Save the Sequence object into incident context memory using a "save incident context" block

## Sequence Object Overview

The [Sequence object](Block_Families\StixORM\SRO\Sequence\Sequence_template.json) enables the sequencing of [event SDO's](Block_Families\StixORM\SDO\Event\Event_template.json) and [task SDO's](Block_Families\StixORM\SDO\Task\Task_template.json) into ordered workflows, based on the value of `step_type` **MUST** be one of `(start_step, end_step, single_step, parallel_step)`. There must always be a starting sequence object with `step_type` = "start_step" to begin the workflow.  The sequence object connects to other sequence objects with choices on how the tasks or events are connected, the `on_completion_ref`, `on_success_ref`, and `on_failure_ref` is for connecting tasks/events. 

Sequence objects for both values of the `sequence_type` field must be created in a chain starting from the start sequence, where each sequence object connects to the next sequence object in the workflow.  Sequences are chained together using the [chain_sequence block](Block_Families\OS_Triage\Save_Context\chain_sequence.py), which automatically create a start sequence for the first sequence (`step_type` = "start_step") if there is no start step, and sets the `next_step_refs` field in the previous sequence object to match the current. If there is a start sequence already, the chain_sequence block simply adds the new sequence to the end of the chain by updating the `next_step_refs` field in the last sequence object to point to the new sequence object.

The sequence object connects to the event or task SDO through the `sequenced_object_ref` field, and the value of the field `sequence_type`  **MUST** be of type `event` or `task`.

## Task 1: Change everything following the string "# G.2 Create sequence for task_determine_fp". 

Now, read your New Step 2 Notebook (Orchestration\Step_2_Create_Incident_with_an_Alert.ipynb), where every cell before the string "# G.2 Create sequence for task_determine_fp" now works flawlessly and the storyboard is solid. Every cell after this point is incorrect and needs changing. I have del;eted many of the code cells so you dont follow bad code patterns.

Each time a cell creates a sequence object, you must add a new cell after it to chain the sequence object into the workflow using the "chain_sequence.py" block. Then, the existing "save incident context" block must be updated to save the sequence object.

