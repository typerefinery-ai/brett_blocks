# Refine Incident Notebooks for Enhanced Storyboarding and Correct Sequences

Use #sequentialthinking  to think through and execute the following.

Trying to improve the Step 2 and Step 3 notebooks is not working efficiently, mostly because each incrementatl task is under-specified by myself. To counter this, I have moved your new Step 2 and Step 3 notebooks to the Orchestration\test directory, and instead we will try to generate them more accurately using a better specification.

I have created a much better specification of how to build an incident notebook in the seed documents, and so now it is easier for you to develop higher quality output notebooks.

## Tasks to build a Great Notebook from two old notebooks:

2. **Understand STIX patterns**: Read a_seed\5_graph_pattern_nature_of_stix.md to understand the sub-graph patterns available for phishing incident storyboards, including:
   - US DoD Incident Extension pattern with _refs fields
   - 8 different Sighting Extension types for evidence provenance
   - Sequence workflow patterns for Tasks and Events
   - Identity/UserAccount/EmailAddress patterns
   - Observed-Data and Sighting patterns
   
1. **Understand notebook structure**: Read a_seed\6_creating_an_incident_notebook.md to understand the required notebook layout with Sections A-H:
   - Section A: Header, setup, imports, context initialization
   - Section B: Get objects from previous notebooks
   - Section C: Create/save objects for sighting
   - Section D: Create/save events and tasks
   - Section E: Create/chain/save sequences (3-step: create→chain→save)
   - Section F: Create/save impacts
   - Section G: Create/save SRO relationships
   - Section H: Summary

2. **Skim the 2 old Notebooks to See the Story so Far**: Quickly review Orchestration\history\Step_1 _Create_Incident_with_an_Alert.ipynb and Orchestration\history\Step_2 _Get the Anecdote.ipynb to get a sense of the incident story being told so far, that you want to improve within the constraints.

3. **Study the old Step 1**: Read Orchestration\history\Step_1 _Create_Incident_with_an_Alert.ipynb to understand:
   - How incident context is created (first notebook only)
   - Which data forms are used and their structure
   - How the inputs and outputs for each invoke function are specified
   - The storyboard flow and object creation patterns
   - **Important**: The Sequence handling is outdated - use the specification instead (3-step process: create→chain→save)
   
4. **Create richer storyboard for the new Step 2**: Design a more varied incident response workflow by:
   - Creating multiple Event objects (not just one) to show timeline progression
   - Creating multiple Task objects (e.g., validate_alert, create_indicator, determine_fp, escalate, notify) with proper dependencies
   - Adding SRO relationships to connect tasks/events (followed-by, detects, creates, etc.)
   - Including multiple sighting types (alert, context, exclusion) if appropriate
   - Creating new data forms in StixORM directories by copying and modifying existing ones
   - Ensuring the data paths and input paths are exactly as specified
   - Document in .github\architecture\step2_storyboard.md the full storyboard plan for review before building the notebook
   
5. **Add user variety (optional)**: If the storyboard needs different users/identities:
   - Create new identity/user-account/email-addr data forms in StixORM directories
   - Base them on examples from Step_1_Company_Setup.ipynb or Step_0_User_Setup.ipynb
   - Ensure they fit the narrative (e.g., security analyst, team lead, affected user)
   
6. **Build new Step 2 notebook**: Create Orchestration\Step_2_Create_Incident_with_an_Alert.ipynb:
   - Follow Sections A-H structure from the specification
   - Use the richer storyboard with new data forms
   - Implement correct Sequence handling (3-step: create→chain→save for EACH sequence)
   - Ensure each code cell has a preceding markdown story cell
   - Save all objects to incident context properly

7. **Study the old Step 2**: Read Orchestration\history\Step_2 _Get the Anecdote.ipynb to understand:
   - Which data forms are used and their structure
   - How the inputs and outputs for each invoke function are specified
   - The storyboard flow and object creation patterns
   - **Important**: The Sequence handling is outdated - use the specification instead (3-step process: create→chain→save)
   
8. **Create richer storyboard for the new Step 3**: Design a more varied incident response workflow by:
   - Creating multiple Event objects (not just one) to show timeline progression
   - Creating multiple Task objects (e.g., validate_alert, create_indicator, determine_fp, escalate, notify) with proper dependencies
   - Adding SRO relationships to connect tasks/events (followed-by, detects, creates, etc.)
   - Including multiple sighting types (alert, context, exclusion) if appropriate
   - Creating new data forms in StixORM directories by copying and modifying existing ones
   - Ensuring the data paths and input paths are exactly as specified
   - Document in .github\architecture\step3_storyboard.md the full storyboard plan for review before building the notebook
   
9. **Add user variety (optional)**: If the storyboard needs different users/identities:
   - Create new identity/user-account/email-addr data forms in StixORM directories
   - Base them on examples from Step_1_Company_Setup.ipynb or Step_0_User_Setup.ipynb
   - Ensure they fit the narrative (e.g., security analyst, team lead, affected user)
   
10. **Build new Step 3 notebook**: Create Orchestration\Step_3_Get_the_Anecdote.ipynb:
   - Follow Sections A-H structure from the specification
   - Repeat the same process (storyboard design, data forms, notebook structure)
   - Ensure it builds coherently on Step 2 (uses objects from previous notebooks)
   - Follow Sections A-H structure with anecdote-based sighting
   - The storyboard should show how user-reported evidence extends the incident

## Approach to the Project

This is a large and complex task that requires creating entirely new notebooks from scratch. Follow this iterative approach:

1. **Storyboard Planning Phase**: 
   - Create a detailed storyboard document in `.github/architecture/` for each notebook
   - Outline section-by-section what happens: which objects are created, their relationships, the narrative flow
   - List all required data forms and identify which need to be created vs. which exist
   - Be very specific about what the inputs and the outputs of the invoke functions must be to exactly match the patterns from the old notebooks
   - Define the sequence workflows showing task dependencies and event progression
   - This blueprint should be reviewed before starting notebook creation

2. **Data Form Creation Phase**: 
   - Based on the storyboard, identify all new data forms needed
   - First check the directory to see if you have already created a suitable data form in a previous effort
   - If not, then copy existing data forms from StixORM directories as templates
   - Modify field values to match your narrative (names, descriptions, properties)
   - Ensure consistency: if storyboard mentions "validate_alert" task, create `task_validate_alert.json`
   - Organize forms by type (Task/, Event/, Indicator/, etc.)

3. **Notebook Development Phase**: 
   - Build section by section following the A-H structure from the specification
   - **Each code cell must have a preceding markdown story cell** explaining what happens
   - Implement the 3-step sequence pattern consistently (create→chain→save)
   - Test each section's code cells incrementally as you build
   - Verify objects are saved to context correctly with proper references
   - Ensure the final notebook reads as a coherent story with proper narrative flow

4. **Validation Phase**:
   - Review the complete notebook against the specification checklist
   - Verify all sequences use the 3-step process (not the old 2-step)
   - Check that Section B properly retrieves objects from previous notebooks
   - Make sure you have created data forms for all new objects used in the storyboard
   - Ensure all markdown cells tell the story clearly
   - Validate that Act/Section numbering is consistent throughout

## Success Criteria

Each completed notebook must meet the following criteria:

**Structure Compliance:**
- ✅ Follows Sections A-H structure exactly as specified in the Incident Notebook specification
- ✅ Section A includes proper header, setup, imports, and context initialization (first notebook only)
- ✅ Section B retrieves required objects from previous notebooks with proper queries
- ✅ Sections C-G create and save objects in the correct order with proper dependencies
- ✅ Section H provides a clear summary of all operations performed

**Sequence Handling:**
- ✅ All sequences use the 3-step process: create→chain→save (NOT the old 2-step pattern)
- ✅ Each sequence has: invoke_make_sequence_block → invoke_chain_sequence_block → invoke_save_incident_context_block
- ✅ No manual creation of start_step sequences (chain_sequence.py handles this automatically)
- ✅ Sequence workflows show clear task dependencies and event progression

**Storyboarding Quality:**
- ✅ Every code cell has an explanatory markdown cell immediately before it
- ✅ Markdown cells tell a clear, coherent narrative that flows naturally
- ✅ Act/Section numbering is consistent throughout the entire notebook
- ✅ At least 3-5 Task objects with meaningful different purposes (not just one generic task)
- ✅ At least 2-3 Event objects showing timeline progression
- ✅ Multiple SRO relationships connecting objects (followed-by, detects, creates, impacts, etc.)

**Data Form Completeness:**
- ✅ All objects referenced in code have corresponding data form JSON files in StixORM directories
- ✅ Data forms are properly customized with relevant names, descriptions, and properties
- ✅ No placeholder or template values remain in data forms (all fields are meaningful)

**Context Management:**
- ✅ Objects are saved to incident context with proper invoke_save_incident_context_block calls
- ✅ Results paths are consistent and properly organized (e.g., step2/, step3/ subdirectories)
- ✅ Objects from previous notebooks are successfully retrieved and used
- ✅ Context memory structure follows the specification (incident refs, task refs, event refs, etc.)

**Code Quality:**
- ✅ All imports are correct and necessary modules are available
- ✅ Code cells execute without errors when run in sequence
- ✅ Variable names are descriptive and consistent with the narrative
- ✅ Print statements provide useful feedback about operations performed
