
from Orchestration.Utilities.local_make_sdo import (
    invoke_make_observed_data_block, invoke_make_indicator_block, invoke_make_event_block, invoke_make_sequence_block,
    invoke_make_task_block, invoke_make_incident_block
)


def try_block():
    observed_ids = []
    observed_ids.append("email-addr--eb38d07e-6ba8-56c1-b107-d4db4aacf212")
    # 2. Setup path to form and results
    obs_path = "SDO/Observed_Data/observation-alert.json"
    results_path = "step1/observation-alert.json"
    # 3. Invoke the Make Observed Data Block
    obs_1 = invoke_make_observed_data_block(obs_path, results_path, observation=observed_ids)


# if this file is run directly, then start here
if __name__ == '__main__':
    #try_update(connection)
    #testuuid()
    #report = update_context("./Orchestration/Context_Mem/OS_Threat_Context.json", connection, import_type)
    # print("=================================================")
    # print(report)
    # print("==================================================")
    try_block()