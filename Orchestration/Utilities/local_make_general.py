import json
import os

context_base = "../Orchestration/Context_Mem/"
path_base = "../Block_Families/Objects/"
results_base = "../Orchestration/Results/"

from Block_Families.Context.Save_Context.save_incident_context2 import main as save_incident_context
from Block_Families.Context.Save_Context.save_options_context2 import main as save_options_context
from Block_Families.Context.Get_Context.get_from_incident import main as get_from_incident
from Block_Families.Context.Get_Context.get_from_options import main as get_from_options
from Block_Families.Context.Update_Context.update_company_relations import main as update_company_relations
from Block_Families.Context.Update_Context.move_unattached_to_other import main as move_unattached_to_other


TR_Context_Memory_Dir = "./Context_Mem"
local = {
    "me" : "/cache_me.json",
    "team" : "/cache_team.json",
    "users": "/company_1/cache_users.json",
    "company" : "/company_1/cache_company.json",
    "assets" : "/company_1/cache_assets.json",
    "systems" : "/company_1/cache_systems.json",
    "relations" : "/company_1/cache_relations.json"
}
refs = {
    "start" : "/incident_1/sequence_start_refs",
    "sequence" : "/incident_1/sequence_refs",
    "impact" : "/incident_1/impact_refs",
    "event" : "/incident_1/event_refs",
    "task" : "/incident_1/task_refs",
    "other" : "/incident_1/other_object_refs",
    "unattached" : "/incident_1/unattached_objs"
}



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




def invoke_move_unattached_to_other_block(stix_object_path, results_path, object_list):
    #
    # 1. Set the Relative Input and Output Paths for the block
    #
    #
    # NOTE: This code is only To fake input ports
    # Add the User Account object and the  EmailAddress
    # NOTE: This code is only To fake input ports
    ##
    stix_list = {"stix_list": object_list}
    with open(stix_object_path, 'w') as f:
        f.write(json.dumps(stix_list))
    # Make the Observed Data object
    move_unattached_to_other(stix_object_path,results_path)
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
    slices = stix_object_path.split('/')
    full_filename = slices[-1]
    filename = full_filename[:-5]
    results_data = {}
    context_path = "../Orchestration/Results/step1/context/"+ filename + "_options_context.json"
    if os.path.exists(stix_object_path):
        with open(stix_object_path, "r") as sdo_form:
            temp_data = json.load(sdo_form)
            results_data["stix_object"] = temp_data
            if context_type:
                results_data["context_type"] = context_type
        with open(context_path, 'w') as f:
            f.write(json.dumps(results_data))
    # Make the Observed Data object
    save_options_context(context_path,results_path)
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
    # we get in the path to an actual stix object json, but we dont want to be writing back changes in that,
    # instead we will create a new one based on a reliable transform to contaon object pust context data
    ##
    slices = stix_object_path.split('/')
    full_filename = slices[-1]
    filename = full_filename[:-6]
    results_data = {}
    context_path = "../Orchestration/Results/step1/context/" + filename + "_incident_context.json"
    results_data = {}
    if os.path.exists(stix_object_path):
        with open(stix_object_path, "r") as sdo_form:
            temp_data = json.load(sdo_form)
            results_data["stix_object"] = temp_data
            if context_type:
                results_data["context_type"] = context_type
        with open(context_path, 'w') as f:
            f.write(json.dumps(results_data))
    # Make the Observed Data object
    save_incident_context(context_path,results_path)
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



def invoke_get_from_options_block(get_query, context_type, source_value=None, source_id=None):
    #
    # 1. Set the Relative Input and Output Paths for the block
    #
    #
    # NOTE: This code is only To fake input ports
    # Add the User Account object and the  EmailAddress
    #  Form data file
    context_temp_path = results_base + "goq--" + str(get_query["type"]) + " .json"
    context_res_path = results_base + "goq-results--" + str(get_query["type"]) + " .json"
    local_context = {}
    local_context["get_query"] = get_query
    local_context["context_type"] = context_type
    local_context["source_value"] = source_value
    local_context["source_id"] = source_id
    #
    #
    with open(context_temp_path, 'w') as f:
        f.write(json.dumps(local_context))
    #
    # Make the Email Address object
    #
    get_from_options(context_temp_path,context_res_path)
    # Retrieve the saved file
    if os.path.exists(context_res_path):
        with open(context_res_path, "r") as script_input:
            export_data = json.load(script_input)
            return export_data


def invoke_get_from_incident_block(get_query, context_type, source_value=None, source_id=None):
    #
    # 1. Set the Relative Input and Output Paths for the block
    #
    #
    # NOTE: This code is only To fake input ports
    # Add the User Account object and the  EmailAddress
    #  Form data file
    context_temp_path = results_base + "giq--" + str(get_query) + " .json"
    context_res_path = results_base + "giq-results--" + str(get_query) + " .json"
    local_context = {}
    local_context["get_query"] = get_query
    local_context["context_type"] = context_type
    local_context["source_value"] = source_value
    local_context["source_id"] = source_id
    #
    #
    with open(context_temp_path, 'w') as f:
        f.write(json.dumps(local_context))
    #
    # Make the Email Address object
    #
    get_from_options(context_temp_path,context_res_path)
    # Retrieve the saved file
    if os.path.exists(context_res_path):
        with open(context_res_path, "r") as script_input:
            export_data = json.load(script_input)
            return export_data
