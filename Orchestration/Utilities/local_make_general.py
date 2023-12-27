import stixorm
from stixorm.module.definitions.stix21 import (
    Identity, EmailAddress, UserAccount, Relationship, Bundle, URL, EmailMessage
)
from stixorm.module.definitions.os_threat import (
    IdentityContact, EmailContact, SocialMediaContact, ContactNumber
)
from stixorm.module.authorise import import_type_factory
from stixorm.module.typedb_lib.instructions import ResultStatus, Result
from stixorm.module.parsing import parse_objects
import json
import os

context_base = "../Orchestration/Context_Mem/"
path_base = "../Block_Families/Objects/"
results_base = "../Orchestration/Results/"
TR_Context_Memory_Path = "./Context_Mem/Type_Refinery_Context.json"

from Block_Families.General.Save_Context.save_context import main as save_context
from Block_Families.General.Get_Context.get_context import main as get_context


def invoke_context_save_block(context, context_path=None):
    #
    # 1. Set the Relative Input and Output Paths for the block
    #
    #
    # NOTE: This code is only To fake input ports
    # Add the User Account object and the  EmailAddress
    #  Form data file
    local_context_file = {"context": context}
    if context_path:
        context_save = context_path
        local_context_file["context_path"] = context_save
    else:
        context_save = TR_Context_Memory_Path
        local_context_file["context_path"] = context_save
    #
    context_results_rel_path = results_base + context_save
    #
    context_temp_path = "../Block_Families/General/Save_Context/temp_context.json"
    with open(context_temp_path, 'w') as f:
        f.write(json.dumps(local_context_file))
    #
    # Make the Email Address object
    #
    save_context(context_temp_path,context_save)
    # Retrieve the saved file
    if os.path.exists(context_save):
        with open(context_save, "r") as script_input:
            export_data = json.load(script_input)



def invoke_context_get_block(context_path=None):
    #
    # 1. Set the Relative Input and Output Paths for the block
    #
    #
    # NOTE: This code is only To fake input ports
    # Add the User Account object and the  EmailAddress
    #  Form data file
    context_temp_path = "../Block_Families/General/Save_Context/temp_context_path.json"
    context_temp_save_path = "../Block_Families/General/Save_Context/temp_context.json"
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
