##############################################################################
#
#  Using Print and Dummy Data to Test the update code
#
#  This file aims to:
#  1. Open an Incident and its objects from Context Memory
#  2. Modify the Incident, delete an object, add an object and change an object
#  3. Save the modified Incident, as a dummy TypeDB Incident object
#  4. Compare the two objects
#  5. Print the changed and deleted objects, plus print the update TypeQL
#
#
##############################################################################

from stixorm.module.typedb import TypeDBSink, TypeDBSource
from stixorm.module.authorise import import_type_factory
from deepdiff import DeepDiff, parse_path
from Block_Families.General._library.update import handle_object_diff, find_list_diff, find_obj_diff
from Block_Families.OS_Triage.Update_Context.update_context import load_context, synch_context
from Block_Families.OS_Triage.Open_Incident.get_default_incidents_objects import get_default_incidents_objects

import_type = import_type_factory.get_all_imports()
all_imports = import_type_factory.get_all_imports()
import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
import json
import os
import copy


# Common File Stuff
TR_Common_Files = "./generated/os-triage/common_files"
common = [
    {"module": "convert_n_and_e", "file": "convert_n_and_e.py", "url" : "https://raw.githubusercontent.com/typerefinery-ai/brett_blocks/main/Block_Families/General/_library/convert_n_and_e.py"}
]

# OS_Triage Memory Stuff
TR_Context_Memory_Dir = "./generated/os-triage/context_mem"
TR_User_Dir = "/usr"
context_map = "context_map.json"
user_data = {
    "global": "/global_variables_dict.json",
    "me": "/cache_me.json",
    "team": "/cache_team.json",
    "relations" : "/relations.json",
    "edges" : "/edges.json",
    "relation_edges" : "/relation_edges.json",
    "relation_replacement_edges" : "/relation_replacement_edges.json"
}
comp_data = {
    "users": "/users.json",
    "company" : "/company.json",
    "assets" : "/assets.json",
    "systems" : "/systems.json",
    "relations" : "/relations.json",
    "edges" : "/edges.json",
    "relation_edges" : "/relation_edges.json",
    "relation_replacement_edges" : "/relation_replacement_edges.json"
}
incident_data = {
    "incident" : "/incident.json",
    "start" : "/sequence_start_refs.json",
    "sequence" : "/sequence_refs.json",
    "impact" : "/impact_refs.json",
    "event" : "/event_refs.json",
    "task" : "/task_refs.json",
    "behavior" : "/behavior_refs.json",
    "other" : "/other_object_refs.json",
    "unattached" : "/unattached_objs.json",
    "unattached_relations" : "/unattached_relation.json",
    "relations" : "/incident_relations.json",
    "edges" : "/incident_edges.json",
    "relation_edges" : "/relation_edges.json",
    "relation_replacement_edges" : "/relation_replacement_edges.json"
}
field_names = {
    "start" : "sequence_start_refs",
    "sequence" : "sequence_refs",
    "impact" : "impact_refs",
    "event" : "event_refs",
    "task" : "task_refs",
    "other" : "other_object_refs"
}
key_list = ["start", "sequence", "impact", "event", "task", "other"]

connection = {
    "uri": "localhost",
    "port": "1729",
    "database": "stix_test",
    "user": None,
    "password": None
}

def vary_incident_list(current_objects_list,current_incident_obj):
    """Vary Incident stuff in a predictable way

    Take current object and current object list, and vary it in a known way:
    1. Find a specific email message
    2. Find the observed data object that contains it
    3. Add a new email addr to the list
    4. Register the new email addr on the cc list in the message
    5. register the new email addr on the observed data object
    6. Register the new email addr on the incident
    7. Find a specific task and the sequence linked to it
    8. Delete both of them
    9. Deregister both from the incident

    Parameters
    ----------
    current_objects_list : list
        List of wrapped stix objects
    current_incident_obj : dict
        Wrapped, Stix Incident object

    Returns
    -------
    varied_list : list
        Varied list of objects
    varied_obj : dict
        Varied incident object
    """
    varied_list = []
    varied_obj = {}
    task_name = "Query Exchange Server"
    email_subject = "we are coming for you"
    email_object = {}
    observation_object = {}
    task = {}
    sequence = {}
    new_email_addr = {
        "type": "email-addr",
        "spec_version": "2.1",
        "id": "email-addr--0e889020-a432-5676-aa03-ba1e1851e6c4",
        "value": "zelda@example.com",
        "display_name": "Zelda Doe"
    }
    # 1. Setup the return lists
    varied_list = copy.deepcopy(current_objects_list)
    varied_obj = copy.deepcopy(current_incident_obj)
    # 2. Get hold of lists of each type of object
    seq_id = ""
    tsk_id = ""
    email_id = ""
    for obj in varied_list:
        if obj["type"] == "email-message":
            if obj["subject"] == email_subject:
                obj["cc_refs"] = []
                obj["cc_refs"].append(new_email_addr["id"])
                email_id = obj["id"]
        elif obj["type"] == "task":
            if obj["name"] == task_name:
                tsk_id = obj["id"]
    for obj in varied_list:
        if obj["type"] == "observed-data":
            obs_refs = obj["object_refs"]
            add_address = False
            for obs_id in obs_refs:
                if obs_id == email_id:
                    add_address = True
            if add_address:
                obj["object_refs"].append(new_email_addr["id"])
        elif obj["type"] == "sequence" and obj["step_type"] == "single_step":
            print(f"\n\nsequence->{obj}\n")
            if obj["sequenced_object"] == tsk_id:
                seq_id = obj["id"]
    # 4. Add the email address to the list and connect it to the incident
    varied_list.append(new_email_addr)
    incident_ext = varied_obj["extensions"]["extension-definition--ef765651-680c-498d-9894-99799f2fa126"]
    incident_ext["other_object_refs"].append(new_email_addr["id"])
    # 5. Delete Task and Sequence from the list
    print(f"\n\n========= ids ===========\n{email_id}\n{seq_id}\n{tsk_id}\n\n")
    del_ssq_varied_list = [x for x in varied_list if x["id"] != seq_id]
    deleted_varied_list = [x for x in del_ssq_varied_list if x["id"] != tsk_id]
    # 6. Delete the id's from the Incident
    incident_ext["sequence_refs"] = [x for x in incident_ext["sequence_refs"] if x != seq_id]
    incident_ext["task_refs"] = [x for x in incident_ext["task_refs"] if x != tsk_id]
    varied_obj["extensions"]["extension-definition--ef765651-680c-498d-9894-99799f2fa126"] = incident_ext

    return deleted_varied_list, varied_obj

def collect_comparison_data():
    """Create comparison data

    1. Open all of the objects in the default incident
    2. Separate into two, the incident object, and all other objects
    3. Run both through the variation funtion
    4. Return the list of objects, the incident object, the varied list and the varied incident object

    Parameters
    ----------
    nil

    Returns
    -------
    current_objects_list : list
        Current list of objects in the incident
    current_incident_obj : dict
        Current incident object
    varied_list : list
        Varied list of objects
    varied_obj : dict
        Varied incident object
    """
    current_context_list = get_default_incidents_objects()
    print(f"current context \n\n {current_context_list}")
    current_objects_list = [x["original"] for x in current_context_list if x["type"] != "incident"]
    current_incident_obj_list = [x["original"] for x in current_context_list if x["type"] == "incident"]
    print(f"incident object \n\n{current_incident_obj_list}")
    current_incident_obj = current_incident_obj_list[0]
    # make an artificial original set of data
    original_list, original_obj = vary_incident_list(current_objects_list,current_incident_obj)
    return current_objects_list, current_incident_obj, original_list, original_obj

def compare_incidents():
    """Compare incidents

    1. Collect the two datasets
    2. Compare the 2 lists to determine add, delete and may-have-changed list
    3. Compare the two incident objects and derive TQL update statements
    4. Compare each of the may-have-changed objects and derive TQL update statements
    5. Print out the results in sections

    Parameters
    ----------
    nil

    Returns
    -------
    report : list
        Current list of objects in the incident
    changed_incident_obj : dict
        Current incident object
    varied_list : list
        Varied list of objects
    varied_obj : dict
        Varied incident object
    """
    diff_report_list = []
    # 1. First add the Step 1 objects to typedb
    #
    changed_list, changed_incident_obj, original_list, original_incident_obj = collect_comparison_data()
    #
    #updated_list = vary_current_list(changed_list)
    #
    # 2. Find out the set operations between the lists of object already in TypeDB, and the list of objects now
    delete_object_ids, add_objects_list, may_have_changed_list = find_list_diff(original_list, changed_list)
    # 3. Calculate whether update is needed per object, if so push it
    for current_obj in may_have_changed_list:
        orig_object = [x for x in original_list if x["id"] == current_obj["id"]]
        obj_diff = find_obj_diff(orig_object[0], current_obj)
        if obj_diff != {}:
            diff_report_list.append(handle_object_diff(obj_diff, orig_object[0], current_obj, connection, all_imports))


    # 4. Now process the incident diff
    if original_incident_obj != {}:
        inc_diff = find_obj_diff(original_incident_obj, changed_incident_obj)
        if inc_diff != {}:
            diff_local_path = str(original_incident_obj["id"]) + ".json"
            print(f"\n its a change -> {diff_local_path}")
            diff_report_list.append(handle_object_diff(inc_diff, original_incident_obj, changed_incident_obj, connection, all_imports))
            print(f"\n{inc_diff}\n")
            with open(diff_local_path, 'w') as f:
                f.write(json.dumps(inc_diff))
        else:
            diff_local_path = str(changed_incident_obj["id"]) + ".json"
            print(f"no change -> {diff_local_path}")
    report = {}
    report["add_objects_list"] = add_objects_list
    report["delete_id_list"] = delete_object_ids
    report["may_have_changed_list"] = may_have_changed_list
    report["diff_report_list"] = diff_report_list
    report["original_data"] = {}
    report_original_data = report["original_data"]
    report_original_data["original_list"] = original_list
    report_original_data["original_incident"] = original_incident_obj
    report_original_data["changed_list"] = changed_list
    report_original_data["changed_incident_obj"] = changed_incident_obj

    return report






# if this file is run directly, then start here
if __name__ == '__main__':
    #try_update(connection)
    #testuuid()
    report = compare_incidents()
    print("=================================================")
    print(report)
    print("==================================================")
    with open("diff-results.json", "w") as f:
        f.write(json.dumps(report))