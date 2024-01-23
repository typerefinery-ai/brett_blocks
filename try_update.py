
from stixorm.module.typedb import TypeDBSink, TypeDBSource
from stixorm.module.authorise import import_type_factory
from stixorm.module.definitions.stix21 import (
    Identity, EmailAddress, UserAccount, Relationship, Bundle, Incident, URL, EmailMessage, ObservedData
)
from stixorm.module.definitions.os_threat import (
    EventCoreExt, Event, SocialMediaContact, ContactNumber, IncidentCoreExt, TaskCoreExt,
    Task, SightingEvidence, Sequence, SequenceExt, AnecdoteExt, Anecdote,
    SightingAnecdote, SightingAlert, SightingContext, SightingExclusion,
    SightingEnrichment, SightingHunt, SightingFramework, SightingExternal
)
from stixorm.module.authorise import import_type_factory
from stixorm.module.typedb_lib.instructions import ResultStatus, Result
from stixorm.module.parsing import parse_objects
from deepdiff import DeepDiff, parse_path
from pprint import pprint
from Block_Families.General._library.update import handle_object_diff, value_is_id

import_type = import_type_factory.get_all_imports()
import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
import json
import os

connection = {
    "uri": "localhost",
    "port": "1729",
    "database": "stix_test",
    "user": None,
    "password": None
}
def load_context():
    # 1. Load the Context
    TR_Context_Memory_Path = "./Orchestration/Context_Mem/OS_Threat_Context.json"
    cwd = os.getcwd()
    print(f"cwd -> {cwd}")
    with open(TR_Context_Memory_Path, "r") as context_file:
        Type_Refinery_Context = json.load(context_file)
    #
    # 2. Setup the  TR User Context
    #
    local = Type_Refinery_Context["local"]
    local_context = local["context"]
    me = local_context["me"]
    team = local_context["team"]
    company = local_context["company"]
    systems = local_context["systems"]
    assets = local_context["assets"]
    #
    # 3. Setup the Incident Context
    #
    incident = local["incident"]
    sequence_start_objs = incident["sequence_start_objs"]
    sequence_objs = incident["sequence_objs"]
    task_objs = incident["task_objs"]
    event_objs = incident["event_objs"]
    impact_objs = incident["impact_objs"]
    other_object_objs = incident["other_object_objs"]
    incident_obj = incident["incident_obj"]

    #
    # 4. Load the TypeDB Context
    #
    remote = Type_Refinery_Context["remote"]
    remote_incident = remote["incident"]
    t_sequence_start_objs = remote_incident["sequence_start_objs"]
    t_sequence_objs = remote_incident["sequence_objs"]
    t_task_objs = remote_incident["task_objs"]
    t_event_objs = remote_incident["event_objs"]
    t_impact_objs = remote_incident["impact_objs"]
    t_other_object_objs = remote_incident["other_object_objs"]
    t_incident_obj = remote_incident["incident_obj"]
    #
    # 5. Add the lists together and put them into typedb
    #
    typedb_add_list = t_sequence_start_objs + t_sequence_objs + t_task_objs + t_event_objs + t_other_object_objs + t_impact_objs
    typedb_add_list = typedb_add_list + me + team + company + systems + assets
    second_list = sequence_start_objs + sequence_objs + task_objs + event_objs + impact_objs + other_object_objs
    second_list = second_list + me + team + company + systems + assets
    # typedb_add_list.append(t_incident_obj)
    # typedb_sink = TypeDBSink(connection, True, import_type)
    # results_raw = typedb_sink.add(typedb_add_list)
    # result_list = [res.model_dump_json() for res in results_raw]
    # for res in result_list:
    #     print(f"\n result is -> {res}")
    return typedb_add_list, t_incident_obj, second_list, incident_obj


def find_list_diff(original_list, changed_list):
    original_id_list = [x["id"] for x in original_list]
    changed_id_list = [x["id"] for x in changed_list]
    set_original_id  = set(original_id_list)
    set_changed_id = set(changed_id_list)
    delete_object_ids = set_original_id - set_changed_id
    add_object_ids = set_changed_id - set_original_id
    add_objects_list = [x for x in changed_list if x["id"] in list(add_object_ids)]
    obj_ids_that_may_have_changed = set_original_id & set_changed_id
    may_have_changed_list = [x for x in changed_list if x["id"] in list(obj_ids_that_may_have_changed)]
    return delete_object_ids, add_objects_list, may_have_changed_list

def old_find_list_diff(original_list, changed_list):
    verbose_level = 2
    ignore_order = True
    group_by = 'id'
    diff = DeepDiff(original_list, changed_list, ignore_order=True, verbose_level=2, group_by='id')
    diff_local_path = "DeepDiff_list_output.json"
    diff_json = json.loads(diff.to_json())
    with open(diff_local_path, 'w') as f:
        f.write(json.dumps(diff_json))
    return diff_json


def find_obj_diff(original_object, current_object):
    verbose_level = 2
    ignore_order = True
    group_by = 'id'
    diff = DeepDiff(original_object, current_object, verbose_level=verbose_level, ignore_order=ignore_order)
    diff_local_path = "DeepDiff_object_output.json"
    diff_json = json.loads(diff.to_json())
    with open(diff_local_path, 'w') as f:
        f.write(json.dumps(diff_json))
    return diff_json


def log_it_list(object_list_diff):
    for obj_id, obj_value in object_list_diff.items():
        print("=================================")
        print(f"-------- id = {obj_id}, type of obj ->{type(obj_value)}")
        #print(f"obj value {obj_value}")
        for o_key, o_value in obj_value.items():
            print(f"\no_key ->{parse_path(o_key)}")
            print(f"o_value -> {o_value}")


def log_it_obj(object_diff):
    for obj_id, obj_value in object_diff.items():
        print("=================================")
        print(f"-------- id = {obj_id}, type of obj ->{type(obj_value)}")
        for o_key, o_value in obj_value.items():
            print(f"o_key ->{parse_path(o_key)}")
            print(f"o_value -> {o_value}")

def vary_current_list(current_list):
    for i, obj in enumerate(current_list):
        #print(f"obj id is {obj['id']}")
        if obj["id"] == "task--3f4c17f0-be79-4394-8cdb-289258a201bb":
            obj["name"] = "Potential Phishing Email is Crank"
            # print("&&&&&& Lampie &&&&&&&&&&&&&&")
            # print(obj)
        elif obj["id"] == "event--aee19ec9-84dc-4a8a-a88a-2dba8da07b08":
            del obj["end_time"]
            # print("****** anecdote$$$$$")
            # print(obj)
        # elif obj["id"] == "indicator--d51a80ba-bd28-46e4-902b-67f0c3ee4dfc":
        #     current_list.pop(1)
    short_list = current_list #[x for x in current_list if x["id"] !="indicator--d51a80ba-bd28-46e4-902b-67f0c3ee4dfc"]
    return short_list



def try_update(connection):
    # 1. First add the Step 1 objects to typedb
    #
    t_original_list, t_original_incident_obj, current_list, current_incident_obj = load_context()
    #
    updated_list = vary_current_list(current_list)
    # 2. Find out the set operations between the lists of object already in TypeDB, and the list of objects now
    delete_object_ids, add_objects_list, may_have_changed_list = find_list_diff(t_original_list, updated_list)
    # 3. First address the changed object operations
    for current_obj in may_have_changed_list:
        orig_object = [x for x in t_original_list if x["id"] == current_obj["id"]]
        obj_diff = find_obj_diff(orig_object[0], current_obj)
        if obj_diff != {}:
            diff_local_path = str(current_obj["id"]) + ".json"
            print(f"\n its a change -> {diff_local_path}")
            handle_object_diff(obj_diff, orig_object[0], current_obj, connection, import_type)
            print(f"\n{obj_diff}\n")
            with open(diff_local_path, 'w') as f:
                f.write(json.dumps(obj_diff))
            #handle_object_diff(obj_diff, orig_object, current_obj)
        else:
            diff_local_path = str(current_obj["id"]) + ".json"
            print(f"no change -> {diff_local_path}")
    # 4. Now process the incident diff
    inc_diff = find_obj_diff(t_original_incident_obj, current_incident_obj)
    if inc_diff != {}:
        diff_local_path = str(t_original_incident_obj["id"]) + ".json"
        print(f"\n its a change -> {diff_local_path}")
        handle_object_diff(inc_diff, t_original_incident_obj, current_incident_obj, connection, import_type)
        print(f"\n{inc_diff}\n")
        with open(diff_local_path, 'w') as f:
            f.write(json.dumps(inc_diff))
    else:
        diff_local_path = str(current_incident_obj["id"]) + ".json"
        print(f"no change -> {diff_local_path}")



# if this file is run directly, then start here
if __name__ == '__main__':
    try_update(connection)
    #testuuid()