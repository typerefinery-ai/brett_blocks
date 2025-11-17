# Refine Notebook 2 and 3 to Handle Tasks, and Sequences Better

Recently, you developed a storyboard for the phisihing incident response process, which includes Notebook 2 (Incident Triage) and Notebook 3 (Incident Analysis). However, these notebooks currently do not effectively manage tasks and sequences, which are crucial for a smooth incident response workflow. I will get you to make two specific changes, to tasks and sequences, to improve the overall functionality of these notebooks.

I have made some signficant changes to the seed document, a_seed\5_graph_pattern_nature_of_stix.md, to better define tasks and sequences. Further, I have developed a new python block to chain together sequences, available through  the function invoke_chain_sequence_block(sequence_object_path, results_path) in the module Orchestration\Utilities\local_make_general.py. the function of these changes is described below.


## Issue 1 Tasks are Not Utilised Effectively

Tasks are essential for resolviong incidents to decide whether they are a false positive or not. The current notebooks do not leverage tasks effectively, leading to potential delays and inefficiencies in the incident response process. If you start an incident with a sighting, then you must have at least one task to refine and validate that sighting. You probably also have another task in the sequence to decide if the incident is a false positive or not.

If you look at line 124 of a_seed\5_graph_pattern_nature_of_stix.md, you will see a definition of tasks, with the properties. More importantly you should be making use of the task relationships defined in lines 135-145. These relationships allow you to link tasks to sequences, ensuring that each task is executed in the correct order. You can use the invoke create relationship block in the Orchestration\Utilities\local_make_sro.py module to create these relationships, once you have made the approaite data forms and saved them in the SRO directory.

## Issue 2 Sequences were not Chained Together Correctly

Previously, the method of chaining sequences together was not well defined, leading to confusion and potential errors in the incident response workflow. This can be seen in the noteobook Orchestration\Step_2_Create_Incident_with_an_Alert.ipynb, when comparing the variable seq_E_1 and variable seq_E_0. The setup of seq_E_1 is correct, but the setup of seq_E_0 is not correct, as this method of setting up a start step and connecting the sequences manually is error prone and not efficient. Even worse you dont save the sequence objects or SRO relationship objects into the incident. Incorrectly you try to update references on the incident object directly, which is not the correct way to do this. You must use the provided functions to save sequence objects and relationship objects into the incident, invoke_save_incident_context_block.

The new function invoke_chain_sequence_block(sequence_object_path, results_path) in the Orchestration\Utilities\local_make_general.py module provides a clear and efficient way to chain sequences together. The aim is to make variable seq_E_1 as-is, and to replace the setup of variable seq_E_0 with a call to the new function invoke_chain_sequence_block(sequence_object_path, results_path). This will ensure that sequences are chained together correctly, improving the overall workflow of the incident response process. this situation is then repeated with variables seq_T_1 and seq_T_0 later in the notebook.

If you look at the second incident notebook, Orchestration\Step_3_Get the Anecdote.ipynb, you will see that the sequence object is amde by itself, and its not chained to any other sequence. You should modify this notebook to chain the sequence object to the previous sequence using the new function invoke_chain_sequence_block(sequence_object_path, results_path).

In short to make each Sequence object, we need to go through three steps:

1. Create the Sequence object as normal, using the invoke_make_sequence_block
2. Chain the Sequence object to the previous Sequence object using the new function invoke_chain_sequence_block(sequence_object_path, results_path)
3. Save the Sequence object to the Incident as normal using the function

## Issue 3: Relationship objects are not saved to the incident correctly

In both nptebooks, every time an object is created using the approriate utility function, that same object must be savd to the icnident using the function invoke_save_incident_context_block. This includes relationship objects created to link tasks to sequences, and sequences to other sequences. Please ensure that every object created is saved to the incident using the correct function.

## Tasks

1. Read and understand the changes made to a_seed\5_graph_pattern_nature_of_stix.md regarding tasks and sequences.
2. Then modify the storyboard .github\architecture\phishing-incident.md to reflect the changes made to tasks and sequences.
3. Update Notebook 2 (Orchestration\Step_2_Create_Incident_with_an_Alert.ipynb) to effectively utilize tasks and correctly chain sequences together using the new function invoke_chain_sequence_block.
4. Update Notebook 3 (Orchestration\Step_3_Get the Anecdote.ipynb) to chain its sequence object to the previous sequence using the new function invoke_chain_sequence_block.
5. Ensure that all created objects, including relationship objects, are saved to the incident using the function invoke_save_incident_context_block.
6. Try to use more tasks and use relationships to map them to sequences appropriately, to improve the incident response workflow.