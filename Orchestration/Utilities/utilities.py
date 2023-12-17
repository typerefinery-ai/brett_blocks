import os
import json

def conv(stix_object):
    # Convert Stix Object to valid Python dict
    string_dict = stix_object.serialize()
    jdict = json.loads(string_dict)
    return jdict

def emulate_ports(results_rel_path, object_data_paths):
    obj_dicts = []
    if object_data_paths is None or object_data_paths == []:
        return
    if os.path.exists(results_rel_path):
        with open(results_rel_path, "r") as acct_input:
             results_data = json.load(acct_input)
             for obj in object_data_paths:
                 if obj and os.path.exists(obj):
                    with open(obj, "r") as email_input:
                        obj_data = json.load(email_input)
                        obj_dicts.append((obj_data))

    for d in obj_dicts:
        results_data.update(d)

    with open(results_rel_path, 'w') as f:
        f.write(json.dumps(results_data))



def unwind_ports(results_rel_path):
    returns = {}
    if os.path.exists(results_rel_path):
        with open(results_rel_path, "r") as acct_input:
            results_data = json.load(acct_input)
            for k, v in results_data.items():
                if k[-4:] == "form":
                    returns[k] = v
        with open(results_rel_path, 'w') as f:
            f.write(json.dumps(returns))