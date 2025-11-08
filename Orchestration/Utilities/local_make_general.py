import json
import os

context_base = "../Orchestration/Context_Mem/"
path_base = "../Block_Families/StixORM/"
results_base = "../Orchestration/Results/"
################################################################################################
#               os-triage Blocks
###############################################################################################
#          Form Actions
from Block_Families.OS_Triage.Mouse.get_relationship_types import main as get_relationship_type
from Block_Families.OS_Triage.Mouse.get_connection_types import main as get_connection_types
from Block_Families.OS_Triage.Form_Actions.get_connections import main as get_connections
###############################################################################################
#              RMB Menu Actions
from Block_Families.OS_Triage.Mouse.rmb_tree_copy import main as rmb_tree_copy
from Block_Families.OS_Triage.Mouse.rmb_tree_edit_DAG import main as rmb_tree_edit_DAG
###############################################################################################
#       Save to OS_Triage -> Incident, Company, User
from Block_Families.OS_Triage.Save_Context.save_incident_context import main as save_incident_context
from Block_Families.OS_Triage.Save_Context.save_company_context import main as save_company_context
from Block_Families.OS_Triage.Save_Context.save_user_context import main as save_user_context
from Block_Families.OS_Triage.Save_Context.save_unattached_context import main as save_unattached_context
from Block_Families.OS_Triage.Save_Context.save_team_context import main as save_team_context
##############################################################################################
#       Get From OS_Triage -> Incident, Company, User
from Block_Families.OS_Triage.Get_Context.get_from_incident import main as get_from_incident
from Block_Families.OS_Triage.Get_Context.get_from_company import main as get_from_options
from Block_Families.OS_Triage.Get_Context.get_from_user import main as get_from_user
################################################################################################
#       Create OS_Triage -> Incident, Company
from Block_Families.OS_Triage.Create_Context.create_incident_context import main as create_incident_context
from Block_Families.OS_Triage.Create_Context.create_company_context import main as create_company_context
################################################################################################
# Overview PAge and Table of Incidents
from Block_Families.OS_Triage.Open_Incident.get_an_incidents_objects import main as get_an_incidents_objects
from Block_Families.OS_Triage.Open_Incident.get_all_incidents import main as get_all_incidents
from Block_Families.OS_Triage.Open_Incident.get_default_incidents_objects import main as get_default_incidents_objects
################################################################################################
#       Ancillary
from Block_Families.OS_Triage.Update_Context.update_company_relations import main as update_company_relations
from Block_Families.OS_Triage.Update_Context.move_unattached_to_other import main as move_unattached_to_other
from Block_Families.OS_Triage.Update_Context.promote_objects import main as promote_objects

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

def invoke_create_company_context(stix_object_path, results_path):
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
    context_path = "../Orchestration/Results/step1/context/"+ filename + "_incident_context.json"
    if os.path.exists(stix_object_path):
        with open(stix_object_path, "r") as sdo_form:
            temp_data = json.load(sdo_form)
            results_data["company"] = temp_data
        with open(context_path, 'w') as f:
            f.write(json.dumps(results_data))
    # Make the Observed Data object
    create_company_context(context_path,results_path)
    #
    # Remove the context type record
    #
    #
    if os.path.exists(results_path):
        with open(results_path, "r") as script_input:
            export_data = json.load(script_input)
            return export_data



def invoke_create_incident_context(stix_object_path, results_path):
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
    context_path = "../Orchestration/Results/step1/context/"+ filename + "_incident_context.json"
    if os.path.exists(stix_object_path):
        with open(stix_object_path, "r") as sdo_form:
            temp_data = json.load(sdo_form)
            results_data["incident"] = temp_data
        with open(context_path, 'w') as f:
            f.write(json.dumps(results_data))
    # Make the Observed Data object
    create_incident_context(context_path,results_path)
    #
    # Remove the context type record
    #
    #
    if os.path.exists(results_path):
        with open(results_path, "r") as script_input:
            export_data = json.load(script_input)
            return export_data


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




def invoke_get_all_incidents_block(stix_object_path, results_path):
    #
    # 1. Set the Relative Input and Output Paths for the block
    #
    #
    # NOTE: This code is only To fake input ports
    # Add the User Account object and the  EmailAddress
    # NOTE: This code is only To fake input ports
    ##
    # Make the Observed Data object
    get_all_incidents(stix_object_path,results_path)
    #
    # Remove the context type record
    #
    #
    if os.path.exists(results_path):
        with open(results_path, "r") as script_input:
            export_data = json.load(script_input)
            return export_data




def invoke_get_default_incident_objects_block(stix_object_path, results_path):
    #
    # 1. Set the Relative Input and Output Paths for the block
    #
    #
    # NOTE: This code is only To fake input ports
    # Add the User Account object and the  EmailAddress
    # NOTE: This code is only To fake input ports
    ##
    # Make the Observed Data object
    get_default_incidents_objects(stix_object_path,results_path)
    #
    # Remove the context type record
    #
    #
    if os.path.exists(results_path):
        with open(results_path, "r") as script_input:
            export_data = json.load(script_input)
            return export_data



def invoke_get_an_incidents_objects_block(incident_id: str, source_path: str, results_path: str):
    #
    # 1. Set the Relative Input and Output Paths for the block
    #
    #
    # NOTE: This code is only To fake input ports
    # Add the User Account object and the  EmailAddress
    # NOTE: This code is only To fake input ports
    ##
    # Make the Observed Data object
    results_data = {
        "incident_id": incident_id
    }
    with open(source_path, 'w') as f:
        f.write(json.dumps(results_data))
    get_an_incidents_objects(source_path, results_path)
    #
    # Remove the context type record
    #
    #
    if os.path.exists(results_path):
        with open(results_path, "r") as script_input:
            export_data = json.load(script_input)
            return export_data





def invoke_get_relationship_type_block(source_dict_path, target_dict_path, results_path):
    #
    # 1. Set the Relative Input and Output Paths for the block
    #
    #
    # NOTE: This code is only To fake input ports
    # Add the User Account object and the  EmailAddress
    # NOTE: This code is only To fake input ports
    ##
    # Make the Observed Data object
    local_inputs = {}
    source_target_path = "../Orchestration/Results/step1/context/relationship_type_inputs.json"
    if os.path.exists(source_dict_path):
        with open(source_dict_path, "r") as sdo_form:
            temp_data = json.load(sdo_form)
            local_inputs["source"] = temp_data
    if os.path.exists(target_dict_path):
        with open(target_dict_path, "r") as sdo_form:
            temp_data = json.load(sdo_form)
            local_inputs["target"] = temp_data
        with open(source_target_path, 'w') as f:
            f.write(json.dumps(local_inputs))
    get_relationship_type(source_target_path,results_path)
    #
    # Remove the context type record
    #
    #
    if os.path.exists(results_path):
        with open(results_path, "r") as script_input:
            export_data = json.load(script_input)
            return export_data



def invoke_get_connection_type_block(source_dict_path, target_dict_path, results_path):
    #
    # 1. Set the Connection Types for two objects
    #
    #
    # NOTE: This code is only To fake input ports
    # Add the User Account object and the  EmailAddress
    # NOTE: This code is only To fake input ports
    ##
    # Make the Observed Data object
    local_inputs = {}
    source_target_path = "../Orchestration/Results/step1/context/connection_type_inputs.json"
    if os.path.exists(source_dict_path):
        with open(source_dict_path, "r") as sdo_form:
            temp_data = json.load(sdo_form)
            local_inputs["source"] = temp_data
    if os.path.exists(target_dict_path):
        with open(target_dict_path, "r") as sdo_form:
            temp_data = json.load(sdo_form)
            local_inputs["target"] = temp_data
        with open(source_target_path, 'w') as f:
            f.write(json.dumps(local_inputs))
    get_connection_types(source_target_path,results_path)
    #
    # Remove the context type record
    #
    #
    if os.path.exists(results_path):
        with open(results_path, "r") as script_input:
            export_data = json.load(script_input)
            return export_data





def invoke_get_connections_block(object_type, object_field, results_path):
    #
    # 1. Get the valid Connection objects from unattached for a given form and field
    #
    #
    # NOTE: This code is only To fake input ports
    # Add the User Account object and the  EmailAddress
    # NOTE: This code is only To fake input ports
    ##
    # Make the Observed Data object
    local_inputs = {}
    source_target_path = "../Orchestration/Results/step1/context/get_connections_from_unattached.json"
    local_inputs["object_type"] = object_type
    local_inputs["object_field"] = object_field
    with open(source_target_path, 'w') as f:
        f.write(json.dumps(local_inputs))
    get_connections(source_target_path,results_path)
    #
    # Remove the context type record
    #
    #
    if os.path.exists(results_path):
        with open(results_path, "r") as script_input:
            export_data = json.load(script_input)
            return export_data





def invoke_rmb_tree_editDAG(tree_object_path, results_path):
    #
    # 1. Set the Relative Input and Output Paths for the block
    #
    #
    # NOTE: This code is only To fake input ports
    # Add the User Account object and the  EmailAddress
    # NOTE: This code is only To fake input ports
    ##
    # with open(tree_object_path, 'w') as f:
    #     f.write(json.dumps(stix_list))
    # Make the Observed Data object
    rmb_tree_edit_DAG(tree_object_path,results_path)
    #
    # Remove the context type record
    #
    #
    if os.path.exists(results_path):
        with open(results_path, "r") as script_input:
            export_data = json.load(script_input)
            return export_data




def invoke_rmb_tree_copy(tree_object_path, results_path):
    #
    # 1. Set the Relative Input and Output Paths for the block
    #
    #
    # NOTE: This code is only To fake input ports
    # Add the User Account object and the  EmailAddress
    # NOTE: This code is only To fake input ports
    ##
    # with open(tree_object_path, 'w') as f:
    #     f.write(json.dumps(stix_list))
    # Make the Observed Data object
    rmb_tree_copy(tree_object_path,results_path)
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



def invoke_save_company_context_block(stix_object_path, results_path, context_type):
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
    save_company_context(context_path,results_path)
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


def invoke_save_user_context_block(stix_object_path, results_path):
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
    context_path = "../Orchestration/Results/step1/context/" + filename + "_user_context.json"
    results_data = {}
    if os.path.exists(stix_object_path):
        with open(stix_object_path, "r") as sdo_form:
            temp_data = json.load(sdo_form)
            results_data["stix_object"] = temp_data
        with open(context_path, 'w') as f:
            f.write(json.dumps(results_data))
    # Make the Observed Data object
    save_user_context(context_path,results_path)
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
        


def invoke_save_team_context_block(stix_object_path, results_path):
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
    context_path = "../Orchestration/Results/step1/context/" + filename + "_team_context.json"
    results_data = {}
    if os.path.exists(stix_object_path):
        with open(stix_object_path, "r") as sdo_form:
            temp_data = json.load(sdo_form)
            results_data["stix_object"] = temp_data
        with open(context_path, 'w') as f:
            f.write(json.dumps(results_data))
    # Make the Observed Data object
    save_team_context(context_path,results_path)
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

def invoke_save_unattached_context_block(stix_object_path, results_path):
    #
    # 1. Save object to unattached context (no context_type needed for unattached)
    #
    slices = stix_object_path.split('/')
    full_filename = slices[-1]
    filename = full_filename[:-5]
    results_data = {}
    context_path = "../Orchestration/Results/step1/context/"+ filename + "_context.json"
    if os.path.exists(stix_object_path):
        with open(stix_object_path, "r") as sdo_form:
            temp_data = json.load(sdo_form)
            results_data["stix_object"] = temp_data
        with open(context_path, 'w') as f:
            f.write(json.dumps(results_data))
    # Save to unattached context
    save_unattached_context(context_path, results_path)
    #
    # Rewrite the original object (clean format)
    #
    rewrite_data = {}
    for key, value in results_data.items():
        if key == "stix_object":
            rewrite_data = value
        else:
            continue
    with open(stix_object_path, 'w') as f:
        f.write(json.dumps(rewrite_data))
    #
    if os.path.exists(results_path):
        with open(results_path, "r") as script_input:
            export_data = json.load(script_input)
            return export_data

def invoke_make_object_from_data_form_block(data_form_path, results_path):
    """
    Create a STIX object from a data form file.
    This function loads a data form JSON and converts it to a STIX object,
    then saves it to the results path.
    
    Args:
        data_form_path: Path to the data form JSON file (relative to path_base)
        results_path: Path where the created object should be saved (relative to results_base)
    
    Returns:
        The created STIX object dictionary
    """
    from stixorm.module.authorise import import_type_factory
    from stixorm.module.typedb_lib.factories.import_type_factory import ImportTypeFactory
    import_type = import_type_factory.get_all_imports()
    
    # Load the data form
    full_data_form_path = path_base + data_form_path
    if not os.path.exists(full_data_form_path):
        raise FileNotFoundError(f"Data form not found: {full_data_form_path}")
    
    with open(full_data_form_path, "r") as f:
        data_form = json.load(f)
    
    # Create STIX object from data form
    # The data form should contain the object type as a key
    stix_object = None
    
    # Try to find the form type in the data
    for key in data_form.keys():
        if key.endswith('_form') or key.endswith('_Form'):
            form_data = data_form[key]
            # The form data is the STIX object structure
            stix_object = form_data
            break
    
    if stix_object is None:
        # If no _form key, the whole data_form might be the object
        stix_object = data_form
    
    # Save the object to results path
    full_results_path = results_base + results_path
    # Ensure directory exists
    os.makedirs(os.path.dirname(full_results_path), exist_ok=True)
    
    with open(full_results_path, 'w') as f:
        json.dump(stix_object, f, indent=2)
    
    return stix_object

def invoke_get_from_company_block(get_query, context_type, source_value=None, source_id=None):
    #
    # 1. Set the Relative Input and Output Paths for the block
    #
    #
    # NOTE: This code is only To fake input ports
    # Add the User Account object and the  EmailAddress
    #  Form data file
    unique_str = "company-"
    print(f"company query->{get_query}")
    if "type" in get_query:
        unique_str += get_query["type"] + "-"
    if "property" in get_query:
        path = get_query["property"]["path"]
        source_value = get_query["property"]["source_value"]
        comparator = get_query["property"]["comparator"]
        unique_str += path[0] + "-" + comparator + "-" + source_value[0]
    if "embedded" in get_query:
        path = get_query["embedded"]["path"]
        source_value = get_query["embedded"]["source_value"]
        comparator = get_query["embedded"]["comparator"]
        unique_str += path[0] + "-" + comparator + "-" + source_value[0]

    context_temp_path = results_base + "giq--" + unique_str + " .json"
    context_res_path = results_base + "giq-results--" + unique_str + " .json"
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
    unique_str = "incident-"
    if "type" in get_query:
        unique_str += get_query["type"] + "-"
    if "property" in get_query:
        path = get_query["property"]["path"]
        source_value = get_query["property"]["source_value"]
        comparator = get_query["property"]["comparator"]
        unique_str += path[0] + "-" + comparator + "-" + source_value[0]
    if "embedded" in get_query:
        path = get_query["embedded"]["path"]
        source_value = get_query["embedded"]["source_value"]
        comparator = get_query["embedded"]["comparator"]
        unique_str += path[0] + "-" + comparator + "-" + source_value[0]

    context_temp_path = results_base + "giq--" + unique_str + " .json"
    context_res_path = results_base + "giq-results--" + unique_str + " .json"
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
    get_from_incident(context_temp_path,context_res_path)
    # Retrieve the saved file
    if os.path.exists(context_res_path):
        with open(context_res_path, "r") as script_input:
            export_data = json.load(script_input)
            return export_data


def invoke_get_from_user_block(get_query, context_type, source_value=None, source_id=None):
    #
    # 1. Set the Relative Input and Output Paths for the block
    #
    #
    # NOTE: This code is only To fake input ports
    # Add the User Account object and the  EmailAddress
    #  Form data file
    unique_str = "user-"
    if "type" in get_query:
        unique_str += get_query["type"] + "-"
    if "property" in get_query:
        path = get_query["property"]["path"]
        source_value = get_query["property"]["source_value"]
        comparator = get_query["property"]["comparator"]
        unique_str += path[0] + "-" + comparator + "-" + source_value[0]
    if "embedded" in get_query:
        path = get_query["embedded"]["path"]
        source_value = get_query["embedded"]["source_value"]
        comparator = get_query["embedded"]["comparator"]
        unique_str += path[0] + "-" + comparator + "-" + source_value[0]

    context_temp_path = results_base + "giq--" + unique_str + " .json"
    context_res_path = results_base + "giq-results--" + unique_str + " .json"
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
    get_from_user(context_temp_path,context_res_path)
    # Retrieve the saved file
    if os.path.exists(context_res_path):
        with open(context_res_path, "r") as script_input:
            export_data = json.load(script_input)
            return export_data


def invoke_save_incident_context_block(stix_object_path, context_results_path, context_type):
    """
    Save a STIX object to incident context memory
    
    Args:
        stix_object_path: Path to the STIX object JSON file
        context_results_path: Path where context result will be saved
        context_type: Dict with context_type key specifying where to save
    
    Returns:
        Context result from save operation
    """
    # Load the STIX object
    stix_object = None
    if os.path.exists(stix_object_path):
        with open(stix_object_path, "r") as obj_file:
            stix_object = json.load(obj_file)
    
    # Create input for save_incident_context
    save_input = {
        "stix_object": stix_object,
        "context_type": context_type
    }
    
    # Create temporary input file
    temp_input_path = context_results_path.replace(".json", "_input.json")
    with open(temp_input_path, 'w') as f:
        json.dump(save_input, f)
    
    # Call save_incident_context function
    save_incident_context(temp_input_path, context_results_path)
    
    # Clean up temp file
    if os.path.exists(temp_input_path):
        os.remove(temp_input_path)
    
    # Return result
    if os.path.exists(context_results_path):
        with open(context_results_path, "r") as result_file:
            return json.load(result_file)
    
    return {"context_result": "Save completed"}
