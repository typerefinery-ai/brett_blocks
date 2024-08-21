import stixorm
from stixorm.module.definitions.stix21 import (
    Identity, EmailAddress, UserAccount, Relationship, Bundle, ObservedData, Indicator, Incident
)
from stixorm.module.definitions.os_threat import (
    IdentityContact, EmailContact, SocialMediaContact, ContactNumber, Event, Sequence, Task, Impact
)
from stixorm.module.authorise import import_type_factory
from stixorm.module.typedb_lib.instructions import ResultStatus, Result
from stixorm.module.parsing import parse_objects
import json
import os

context_base = "../Orchestration/Context_Mem/"
path_base = "../Block_Families/StixORM/"
results_base = "../Orchestration/Results/"

from Block_Families.StixORM.SDO.Identity.make_identity import main as make_identity
from Block_Families.StixORM.SDO.Observed_Data.make_observed_data import main as make_observed_data
from Block_Families.StixORM.SDO.Indicator.make_indicator import main as make_indicator
from Block_Families.StixORM.SDO.Event.make_event import main as make_event
from Block_Families.StixORM.SDO.Sequence.make_sequence import main as make_sequence
from Block_Families.StixORM.SDO.Task.make_task import main as make_task
from Block_Families.StixORM.SDO.Incident.make_incident import main as make_incident
from Block_Families.StixORM.SDO.Impact.make_impact import main as make_impact
from .util import emulate_ports, unwind_ports, conv


def invoke_make_observed_data_block(obs_path, results_path, observation=None,):
    # Set the Relative Input and Output Paths for the block
    obs_data_rel_path = path_base + obs_path
    obs_results_rel_path = results_base + results_path
    #
    # NOTE: This code is only To fake input ports
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
            stix_object = json.load(script_input)
            # convert it into a Stix Object and append to the bundle
            obs = ObservedData(**stix_object)
            print(obs.serialize(pretty=True))
            return conv(obs)


def invoke_make_indicator_block(ind_path, results_path, pattern=None,):
    # Set the Relative Input and Output Paths for the block
    ind_data_rel_path = path_base + ind_path
    ind_results_rel_path = results_base + results_path
    #
    # NOTE: This code is only To fake input ports
    #
    ##
    if os.path.exists(ind_data_rel_path):
        with open(ind_data_rel_path, "r") as sdo_form:
            results_data = json.load(sdo_form)
            if pattern:
                temp_data = {}
                temp_data["pattern"] = pattern
                results_data["pattern"] = temp_data["pattern"]
        with open(ind_data_rel_path, 'w') as f:
            f.write(json.dumps(results_data))
    # Make the Observed Data object
    make_indicator(ind_data_rel_path,ind_results_rel_path)
    #
    # Remove Port Emulation if used - Fix the data file so it only has form data
    #
    unwind_ports(ind_data_rel_path)
    # Retrieve the saved file
    if os.path.exists(ind_results_rel_path):
        with open(ind_results_rel_path, "r") as script_input:
            stix_object = json.load(script_input)
            # convert it into a Stix Object and append to the bundle
            ind = Indicator(**stix_object)
            print(ind.serialize(pretty=True))
            return conv(ind)


def invoke_make_event_block(event_path, results_path, changed_objects=None,sighting_refs=None):
    # Set the Relative Input and Output Paths for the block
    event_data_rel_path = path_base + event_path
    event_results_rel_path = results_base + results_path
    #
    # NOTE: This code is only To fake input ports
    ##
    if os.path.exists(event_data_rel_path):
        with open(event_data_rel_path, "r") as sdo_form:
            results_data = json.load(sdo_form)
            if changed_objects:
                results_data["changed_objects"] = changed_objects
            if sighting_refs:
                results_data["sighting_refs"] = sighting_refs
        with open(event_data_rel_path, 'w') as f:
            f.write(json.dumps(results_data))
    # Make the Event object
    make_event(event_data_rel_path,event_results_rel_path)
    #
    # Remove Port Emulation if used - Fix the data file so it only has form data
    #
    unwind_ports(event_data_rel_path)
    # Retrieve the saved file
    if os.path.exists(event_results_rel_path):
        with open(event_results_rel_path, "r") as script_input:
            stix_object = json.load(script_input)
            # convert it into a Stix Object and append to the bundle
            obs = Event(**stix_object)
            print(obs.serialize(pretty=True))
            return conv(obs)


def invoke_make_sequence_block(sequence_path, results_path, step_type=None, sequence_type=None, sequenced_object=None, on_completion=None, on_success=None, on_failure=None, next_steps=None):
    # Set the Relative Input and Output Paths for the block
    sequence_data_rel_path = path_base + sequence_path
    sequence_results_rel_path = results_base + results_path
    #
    # NOTE: This code is only To fake input ports
    ##
    if os.path.exists(sequence_data_rel_path):
        with open(sequence_data_rel_path, "r") as sdo_form:
            results_data = json.load(sdo_form)
            if step_type:
                results_data["step_type"] = step_type
            if sequence_type:
                results_data["sequence_type"] = sequence_type
            if sequenced_object:
                results_data["sequenced_object"] = sequenced_object
            if on_completion:
                results_data["on_completion"] = on_completion
            if on_success:
                results_data["on_success"] = on_success
            if sequence_type:
                results_data["on_failure"] = on_failure
            if step_type:
                results_data["next_steps"] = next_steps
        with open(sequence_data_rel_path, 'w') as f:
            f.write(json.dumps(results_data))
    # Make the Event object
    make_sequence(sequence_data_rel_path, sequence_results_rel_path)
    #
    # Remove Port Emulation if used - Fix the data file so it only has form data
    #
    unwind_ports(sequence_data_rel_path)
    # Retrieve the saved file
    if os.path.exists(sequence_results_rel_path):
        with open(sequence_results_rel_path, "r") as script_input:
            stix_object = json.load(script_input)
            # convert it into a Stix Object and append to the bundle
            seq = Sequence(**stix_object)
            print(seq.serialize(pretty=True))
            return conv(seq)


def invoke_make_task_block(task_path, results_path, changed_objects=None):
    # Set the Relative Input and Output Paths for the block
    task_data_rel_path = path_base + task_path
    task_results_rel_path = results_base + results_path
    #
    # NOTE: This code is only To fake input ports
    ##
    if os.path.exists(task_data_rel_path):
        with open(task_data_rel_path, "r") as sdo_form:
            results_data = json.load(sdo_form)
            if changed_objects:
                results_data["changed_objects"] = changed_objects
        with open(task_data_rel_path, 'w') as f:
            f.write(json.dumps(results_data))
    # Make the Event object
    make_task(task_data_rel_path, task_results_rel_path)
    #
    # Remove Port Emulation if used - Fix the data file so it only has form data
    #
    unwind_ports(task_data_rel_path)
    # Retrieve the saved file
    if os.path.exists(task_results_rel_path):
        with open(task_results_rel_path, "r") as script_input:
            stix_object = json.load(script_input)
            # convert it into a Stix Object and append to the bundle
            task = Task(**stix_object)
            print(task.serialize(pretty=True))
            return conv(task)



def invoke_make_identity_block(ident_path, results_path, email_results=None, acct_results=None):
    # Set the Relative Input and Output Paths for the block
    ident_data_rel_path = path_base + ident_path
    ident_results_rel_path = results_base + results_path + "__ident.json"
    #
    # NOTE: This code is only To fake input ports
    #
    ##
    if os.path.exists(ident_data_rel_path):
        with open(ident_data_rel_path, "r") as sdo_form:
            results_data = json.load(sdo_form)
            if email_results:
                results_data["email-addr"] = email_results
            if acct_results:
                results_data["user-account"] = acct_results
        with open(ident_data_rel_path, 'w') as f:
            f.write(json.dumps(results_data))
    # Make the Observed Data object
    make_identity(ident_data_rel_path,ident_results_rel_path)
    #
    # Remove Port Emulation if used - Fix the data file so it only has form data
    #
    unwind_ports(ident_data_rel_path)
    # Retrieve the saved file
    if os.path.exists(ident_results_rel_path):
        with open(ident_results_rel_path, "r") as script_input:
            stix_object = json.load(script_input)
            # convert it into a Stix Object and append to the bundle
            ident = Identity(**stix_object)
            print(ident.serialize(pretty=True))
            return conv(ident)



def invoke_make_incident_block(inc_path, results_path, sequence_start_refs=None, sequence_refs=None, task_refs=None, event_refs=None, impact_refs=None, other_object_refs=None):
    # Set the Relative Input and Output Paths for the block
    inc_data_rel_path = path_base + inc_path
    inc_results_rel_path = results_base + results_path
    #
    # NOTE: This code is only To fake input ports
    #
    ##
    if os.path.exists(inc_data_rel_path):
        with open(inc_data_rel_path, "r") as sdo_form:
            results_data = json.load(sdo_form)
            if sequence_start_refs:
                results_data["sequence_start_refs"] = sequence_start_refs
            if sequence_refs:
                results_data["sequence_refs"] = sequence_refs
            if task_refs:
                results_data["task_refs"] = task_refs
            if event_refs:
                results_data["event_refs"] = event_refs
            if impact_refs:
                results_data["impact_refs"] = impact_refs
            if other_object_refs:
                results_data["other_object_refs"] = other_object_refs
        with open(inc_data_rel_path, 'w') as f:
            f.write(json.dumps(results_data))
    # Make the Observed Data object
    make_incident(inc_data_rel_path,inc_results_rel_path)
    #
    # Remove Port Emulation if used - Fix the data file so it only has form data
    #
    unwind_ports(inc_data_rel_path)
    # Retrieve the saved file
    if os.path.exists(inc_results_rel_path):
        with open(inc_results_rel_path, "r") as script_input:
            stix_object = json.load(script_input)
            # convert it into a Stix Object and append to the bundle
            ident = Incident(**stix_object)
            print(ident.serialize(pretty=True))
            return conv(ident)



def invoke_make_impact_block(impact_path, results_path, impacted_entity_counts=None, impacted_refs=None, superseded_by_ref=None):
    # Set the Relative Input and Output Paths for the block
    impact_data_rel_path = path_base + impact_path
    impact_results_rel_path = results_base + results_path
    #
    # NOTE: This code is only To fake input ports
    #
    ##
    if os.path.exists(impact_data_rel_path):
        with open(impact_data_rel_path, "r") as sdo_form:
            results_data = json.load(sdo_form)
            if impacted_entity_counts:
                results_data["impacted_entity_counts"] = impacted_entity_counts
            if impacted_refs:
                results_data["impacted_refs"] = impacted_refs
            if superseded_by_ref:
                results_data["superseded_by_ref"] = superseded_by_ref
        with open(impact_data_rel_path, 'w') as f:
            f.write(json.dumps(results_data))
    # Make the Observed Data object
    make_impact(impact_data_rel_path,impact_results_rel_path)
    #
    # Remove Port Emulation if used - Fix the data file so it only has form data
    #
    unwind_ports(impact_data_rel_path)
    # Retrieve the saved file
    if os.path.exists(impact_results_rel_path):
        with open(impact_results_rel_path, "r") as script_input:
            stix_object = json.load(script_input)
            # convert it into a Stix Object and append to the bundle
            impact = Impact(**stix_object)
            print(impact.serialize(pretty=True))
            return conv(impact)