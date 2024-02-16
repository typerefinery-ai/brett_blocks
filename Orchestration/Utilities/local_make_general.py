import json
import os

context_base = "../Orchestration/Context_Mem/"
path_base = "../Block_Families/Objects/"
results_base = "../Orchestration/Results/"
TR_Context_Memory_Path = "./Context_Mem/OS_Threat_Context.json"

from Block_Families.Context.Save_Context.save_incident_context import main as save_incident_context
from Block_Families.Context.Save_Context.save_options_context import main as save_options_context
from Block_Families.Context.Get_Context.get_context import main as get_context
from Block_Families.Context.Update_Context.update_company_relations import main as update_company_relations



def invoke_update_company_relations_block(stix_object_path, results_path):
    #
    # 1. Set the Relative Input and Output Paths for the block
    #
    #
    # NOTE: This code is only To fake input ports
    # Add the User Account object and the  EmailAddress
    # NOTE: This code is only To fake input ports
    ##
    # Make the Observed Data object
    update_company_relations(stix_object_path,results_path)
    #
    # Remove the context type record
    #
    #
    if os.path.exists(results_path):
        with open(results_path, "r") as script_input:
            export_data = json.load(script_input)
            return export_data



def invoke_save_options_context_block(stix_object_path, results_path, context_type):
    #
    # 1. Set the Relative Input and Output Paths for the block
    #
    #
    # NOTE: This code is only To fake input ports
    # Add the User Account object and the  EmailAddress
    # NOTE: This code is only To fake input ports
    ##
    results_data = {}
    if os.path.exists(stix_object_path):
        with open(stix_object_path, "r") as sdo_form:
            temp_data = json.load(sdo_form)
            results_data["stix_object"] = temp_data
            if context_type:
                results_data["context_type"] = context_type
        with open(stix_object_path, 'w') as f:
            f.write(json.dumps(results_data))
    # Make the Observed Data object
    save_options_context(stix_object_path,results_path)
    #
    # Remove the context type record
    #
    rewrite_data = {}
    for key, value in results_data.items():
        if key == "stix_object":
            rewrite_data = value
        else:
            continue
    #  Rewrite the original object
    with open(stix_object_path, 'w') as f:
        f.write(json.dumps(rewrite_data))
    #
    #
    if os.path.exists(results_path):
        with open(results_path, "r") as script_input:
            export_data = json.load(script_input)
            return export_data


def invoke_save_incident_context_block(stix_object_path, results_path, context_type):
    #
    # 1. Set the Relative Input and Output Paths for the block
    #
    #
    # NOTE: This code is only To fake input ports
    # Add the User Account object and the  EmailAddress
    # NOTE: This code is only To fake input ports
    ##
    results_data = {}
    if os.path.exists(stix_object_path):
        with open(stix_object_path, "r") as sdo_form:
            temp_data = json.load(sdo_form)
            results_data["stix_object"] = temp_data
            if context_type:
                results_data["context_type"] = context_type
        with open(stix_object_path, 'w') as f:
            f.write(json.dumps(results_data))
    # Make the Observed Data object
    save_incident_context(stix_object_path,results_path)
    #
    # Remove the context type record
    #
    rewrite_data = {}
    for key, value in results_data.items():
        if key == "stix_object":
            rewrite_data = value
        else:
            continue
    #  Rewrite the original object
    with open(stix_object_path, 'w') as f:
        f.write(json.dumps(rewrite_data))
    #
    #
    if os.path.exists(results_path):
        with open(results_path, "r") as script_input:
            export_data = json.load(script_input)
            return export_data



def invoke_context_get_block(context_path=None):
    #
    # 1. Set the Relative Input and Output Paths for the block
    #
    #
    # NOTE: This code is only To fake input ports
    # Add the User Account object and the  EmailAddress
    #  Form data file
    context_temp_path = "../Block_Families/General/Save_Context/temp_context_path.json"
    context_temp_save_path = "../Block_Families/General/Save_Context/init_context.json"
    local_context_file = {}
    if context_path:
        context_get = context_path
        local_context_file["context_path"] = context_get
    else:
        context_get = TR_Context_Memory_Path
        local_context_file["context_path"] = context_get
    #
    #
    with open(context_temp_path, 'w') as f:
        f.write(json.dumps(local_context_file))
    #
    # Make the Email Address object
    #
    get_context(context_temp_path,context_temp_save_path)
    # Retrieve the saved file
    if os.path.exists(context_temp_save_path):
        with open(context_temp_save_path, "r") as script_input:
            export_data = json.load(script_input)
            return export_data
