import os
import json

def conv(stix_object):
    # Convert Stix Object to valid Python dict
    if type(stix_object) is dict:
        return stix_object
    string_dict = stix_object.serialize()
    jdict = json.loads(string_dict)
    return jdict
