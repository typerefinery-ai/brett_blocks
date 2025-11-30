# Run Notebooks and Watch Context Memory Changes

**Cleared content Memory**

Cleared context memory means that the Orchestration\generated\os-triage\context_mem directory has been emptied of all files and subdirectories, but the directory itself remains intact. This ensures that the system can continue to function properly without losing the necessary directory structure for context memory storage.

## Tasks
Use #sequentialthinking to run each notebook step, cell by cell and watch the development of the context memory structure in Orchestration/generated/os-triage/context_mem/.

1. Step 0: User Setup
   - Run Step_0_User_Setup.ipynb
   - Observe creation of usr/cache_me.json, usr/cache_team.json, and usr/edges.json
2. Step 1: Company Setup
   - Run Step_1_Company_Setup.ipynb
    - Observe creation of identity--{uuid}/company.json, users.json, systems.json, assets.json, and edges.json
3. Step 2: Create Incident with an Alert
   - Run Step_2_Create_Incident_with_an_Alert.ipynb
    - Observe creation of incident--{uuid}/incident.json, indicators.json, observed_data.json, sightings.json, events.json, tasks.json, sequences.json, impacts.json, sro_relationships.json, and edges.json
4. Step 3: Get the Anecdote
   - Run Step_3_Get_Anecdote.ipynb
    - Observe creation of additional sightings.json, events.json, tasks.json, sequences.json, impacts.json, sro_relationships.json, and edges.json in the incident--{uuid}/ directory