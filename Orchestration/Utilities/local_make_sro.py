import stixorm
from stixorm.module.definitions.stix21 import (
    Identity, EmailAddress, Sighting, Relationship, Bundle
)
from stixorm.module.definitions.os_threat import (
    IdentityContact, EmailContact, SocialMediaContact, ContactNumber
)
from stixorm.module.authorise import import_type_factory
from stixorm.module.typedb_lib.instructions import ResultStatus, Result
from stixorm.module.parsing import parse_objects
import json
import os

# context_base = "../Orchestration/Context_Mem/"
path_base = "../Block_Families/StixORM/"
results_base = "../Orchestration/Results/"


from Block_Families.StixORM.SCO.URL.make_url import main as make_url
from Block_Families.StixORM.SCO.EmailAddress.make_email_addr import main as make_email_addr
from Block_Families.StixORM.SRO.Sighting.make_sighting import main as make_sighting
from Block_Families.StixORM.SRO.Relationship.make_sro import main as make_sro
from .util import emulate_ports, unwind_ports, conv

def invoke_sro_block(sro_data_path, results_path, source=None, target=None, relationship_type=None):
    # Set the Relative Input and Output Paths for the block
    sro_data_rel_path = path_base + sro_data_path
    sro_results_rel_path = results_base + results_path + "__rel.json"
    #
    # NOTE: This code is only To fake input ports
    # Add the source and target identities and the reltaionship type
    ##
    if os.path.exists(sro_data_rel_path):
        with open(sro_data_rel_path, "r") as sro_form:
            results_data = json.load(sro_form)
            if source:
                results_data["source"] = source
            if target:
                results_data["target"] = target
            if relationship_type:
                results_data["relationship_type"] = relationship_type
        with open(sro_data_rel_path, 'w') as f:
            f.write(json.dumps(results_data))
    # Make the Identity object
    make_sro(sro_data_rel_path,sro_results_rel_path)
    #
    # Remove Port Emulation if used - Fix the data file so it only has form data
    #
    unwind_ports(sro_data_rel_path)
    # Retrieve the saved file
    if os.path.exists(sro_results_rel_path):
        with open(sro_results_rel_path, "r") as script_input:
            stix_object = json.load(script_input)
            # convert it into a Stix Object and append to the bundle
            sro = Relationship(**stix_object)
            print(sro.serialize(pretty=True))
            return conv(sro)



def invoke_sighting_block(sighting_data_path, results_path, observed=None, sighted=None, where=None):
    # Set the Relative Input and Output Paths for the block
    sighting_data_rel_path = path_base + sighting_data_path
    sighting_results_rel_path = results_base + results_path
    #
    # NOTE: This code is only To fake input ports
    # Add the source and target identities and the reltaionship type
    ##
    if os.path.exists(sighting_data_rel_path):
        with open(sighting_data_rel_path, "r") as sro_form:
            results_data = json.load(sro_form)
            if observed:
                results_data["observed_data_refs"] = observed
            if where:
                results_data["where_sighted_refs"] = where
            if sighted:
                results_data["sighting_of_ref"] = sighted
        with open(sighting_data_rel_path, 'w') as f:
            f.write(json.dumps(results_data))
    # Make the Identity object
    make_sighting(sighting_data_rel_path, sighting_results_rel_path)
    #
    # Remove Port Emulation if used - Fix the data file so it only has form data
    #
    unwind_ports(sighting_data_rel_path)
    # Retrieve the saved file
    if os.path.exists(sighting_results_rel_path):
        with open(sighting_results_rel_path, "r") as script_input:
            stix_object = json.load(script_input)
            # convert it into a Stix Object and append to the bundle
            sighting = Sighting(**stix_object)
            print(sighting.serialize(pretty=True))
            return conv(sighting)

