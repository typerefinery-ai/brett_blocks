import stixorm
from stixorm.module.definitions.stix21 import (
    Identity, EmailAddress, UserAccount, Relationship, Bundle, ObservedData, Indicator
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


from Block_Families.Objects.SDO.Observed_Data.make_observed_data import main as make_observed_data
from Block_Families.Objects.SCO.Email_Addr.make_email_addr import main as make_email_addr
from Block_Families.Objects.SCO.Email_Message.make_email_msg import main as make_email_msg
from Block_Families.Objects.SRO.Relationship.make_sro import main as make_sro
from .util import emulate_ports, unwind_ports, conv


def invoke_make_observed_data_block(obs_path, results_path, observation=None,):
    # Set the Relative Input and Output Paths for the block
    obs_data_rel_path = path_base + obs_path
    obs_results_rel_path = results_base + results_path
    #
    # NOTE: This code is only To fake input ports
    # Add the source and target identities and the reltaionship type
    ##
    if os.path.exists(obs_data_rel_path):
        with open(obs_data_rel_path, "r") as sdo_form:
            results_data = json.load(sdo_form)
            if observation:
                results_data["observations"] = observation
        with open(obs_data_rel_path, 'w') as f:
            f.write(json.dumps(results_data))
    # Make the Observed Data object
    make_observed_data(obs_data_rel_path,obs_results_rel_path)
    #
    # Remove Port Emulation if used - Fix the data file so it only has form data
    #
    unwind_ports(obs_data_rel_path)
    # Retrieve the saved file
    if os.path.exists(obs_results_rel_path):
        with open(obs_results_rel_path, "r") as script_input:
            export_data = json.load(script_input)
            export_data_list = export_data["observed-data"]
            stix_object = export_data_list[0]
            # convert it into a Stix Object and append to the bundle
            obs = ObservedData(**stix_object)
            print(obs.serialize(pretty=True))
            local_list = []
            local_list.append(conv(obs))
            return local_list


def invoke_make_indicator_block(ind_path, results_path, pattern=None,):
    # Set the Relative Input and Output Paths for the block
    obs_data_rel_path = path_base + ind_path
    obs_results_rel_path = results_base + results_path
    #
    # NOTE: This code is only To fake input ports
    # Add the source and target identities and the reltaionship type
    ##
    if os.path.exists(obs_data_rel_path):
        with open(obs_data_rel_path, "r") as sdo_form:
            results_data = json.load(sdo_form)
            if pattern:
                results_data["pattern"] = pattern
        with open(obs_data_rel_path, 'w') as f:
            f.write(json.dumps(results_data))
    # Make the Observed Data object
    make_observed_data(obs_data_rel_path,obs_results_rel_path)
    #
    # Remove Port Emulation if used - Fix the data file so it only has form data
    #
    unwind_ports(obs_data_rel_path)
    # Retrieve the saved file
    if os.path.exists(obs_results_rel_path):
        with open(obs_results_rel_path, "r") as script_input:
            export_data = json.load(script_input)
            export_data_list = export_data["indicator"]
            stix_object = export_data_list[0]
            # convert it into a Stix Object and append to the bundle
            ind = Indicator(**stix_object)
            print(ind.serialize(pretty=True))
            local_list = []
            local_list.append(conv(ind))
            return local_list