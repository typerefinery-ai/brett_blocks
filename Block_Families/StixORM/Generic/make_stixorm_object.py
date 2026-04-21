################################################################################
## header start                                                               ##
################################################################################
# allow importing of service local packages
import os
import sys
import os.path

where_am_i = os.path.dirname(os.path.abspath(__file__))
# sys.path.insert(0, os.environ["APP_SERVICE_PACKAGES_PATH"])
# sys.path.append(where_am_i)
# end of local package imports
################################################################################
## header end                                                                 ##
################################################################################


################################################################################
## body start                                                                 ##
################################################################################

##############################################################################
# Title: Make StixORM Object from Form
# Author: OS-Threat
# Organisation Repo: https://github.com/typerefinery-ai/brett_blocks
# Contact Email: brett@osthreat.com
# Date: 07/08/2023
#
# Description: This script is designed to take in a Stix Object ID
#       and return a Stix object
#
# One Mandatory Input:
# 1. StixORM_Form
# One Output
# 1. Serialised StixORM Object (JSON)
#
# This code is licensed under the terms of the Apache 2.
##############################################################################

from stixorm.module.definitions.stix21 import (
    AttackPattern, Campaign, CourseOfAction, CustomObject, Grouping, Identity, 
    Incident, Indicator, Infrastructure, IntrusionSet, Location, Malware, MalwareAnalysis, 
    Note, ObservedData, Opinion, Report, ThreatActor, Tool, Vulnerability, Bundle, 
    URL, Artifact, AutonomousSystem, CustomObservable, Directory, 
    DomainName, EmailAddress, EmailMessage, File, IPv4Address, IPv6Address, MACAddress, 
    Mutex, NetworkTraffic, Process, Software, UserAccount, WindowsRegistryKey, X509Certificate, 
    Relationship, Sighting, MarkingDefinition, AlternateDataStream, ArchiveExt, EmailMIMEComponent, 
    HTTPRequestExt, ICMPExt, NTFSExt, PDFExt, RasterImageExt, SocketExt, TCPExt, UNIXAccountExt, 
    WindowsPEBinaryExt, WindowsPEOptionalHeaderType, WindowsPESection, WindowsProcessExt, 
    WindowsRegistryValueType, WindowsServiceExt, X509V3ExtensionsType
)
from stixorm.module.definitions.os_threat import (
    Feeds, Feed, Event, Impact, Task, Sequence, Anecdote, ThreatSubObject, StateChangeObject, 
    EventCoreExt, ImpactCoreExt, Availability, Confidentiality, External, Integrity, Monetary, 
    Physical, Traceability, IncidentScoreObject, IncidentCoreExt, SequenceExt, SightingEvidence, 
    SightingAnecdote, SightingAlert, SightingContext, SightingExclusion, SightingEnrichment, 
    SightingHunt, SightingFramework, SightingExternal, TaskCoreExt, ContactNumber, EmailContact, 
    SocialMediaContact, IdentityContact, AnecdoteExt
)
from stixorm.module.definitions.attack import (
    Matrix, Tactic, Technique, SubTechnique, Mitigation, Group, SoftwareMalware, SoftwareTool, 
    DataSource, DataComponent, AttackCampaign, Collection, AttackIdentity, AttackRelation, 
    AttackMarking, ObjectVersion
)
from stixorm.module.authorise import import_type_factory
from posixpath import basename
import json
import os
import importlib.util
import logging
from urllib.request import urlretrieve
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

import_type = import_type_factory.get_all_imports()
from stixorm.module.typedb_lib.factories.auth_factory import get_auth_factory_instance
from datetime import datetime

TR_Common_Files = "./generated/os-triage/common_files"
common = [
    {"module": "parse", "file": "parse.py", "url" : "https://raw.githubusercontent.com/typerefinery-ai/brett_blocks/refs/heads/main/Block_Families/General/_library/parse.py"}
]
TR_Settings_Dir = "./generated/os-triage/context_mem/settings"
TR_Settings_URL = "https://raw.githubusercontent.com/typerefinery-ai/brett_blocks/refs/heads/main/Block_Families/OS_Triage/User_Options/options.json"

TR_Context_Memory_Dir = "./generated/os-triage/context_mem"
context_map = "context_map.json"


def download_settings():
    if not os.path.exists(TR_Settings_Dir):
        os.makedirs(TR_Settings_Dir)
    result = urlretrieve(TR_Settings_URL, TR_Settings_Dir + "/options.json")
    print(f'settings file result ->', result)

def convert_dt(dt_stamp_string):
    if dt_stamp_string.find(".") >0:
        dt = datetime.strptime(dt_stamp_string, "%Y-%m-%dT%H:%M:%S.%fZ")
        microsecs = dt.microsecond
        milisecs = (round(microsecs / 1000))
        dt_list = dt_stamp_string.split('.')
        actual = dt_list[0] + "." + str(milisecs) + "Z"
    else:
        if dt_stamp_string.find("T") > 0:
            dt_list = dt_stamp_string.split('T')
            t_list = dt_list[1].split(':')
            if len(t_list) == 3:
                secs = t_list[2]
                sec_list = secs.split('Z')
                actual = dt_list[0] + "T" + t_list[0] + ":" + t_list[1] + ":" + sec_list[0] + ".000Z"
            else:
                mins = t_list[1]
                mins_list = mins.split('Z')
                actual = dt_list[0] + "T" + t_list[0] + ":" + mins_list[0] + ":00.000Z"
        else:
            actual = dt_stamp_string + "T00:00:00.000Z"
    return actual



def get_sub_class_name_for_typeql(stix_typeql):
    """
    Get the "sub"class name for a given TypeQL name
    """
    auth_factory = get_auth_factory_instance()
    auth = auth_factory.get_auth_for_import(import_type)
    class_name = ""
    for obj in auth["conv"]["sub"]:
        if obj["typeql"] == stix_typeql:
            class_name = obj["class"]
            break
    return class_name


def _is_empty_value(value):
    return value is None or value == "" or value == [] or value == {}


def _remove_empty_values(data):
    """
    Recursively drop empty placeholders from form payloads.
    This lets STIX defaults (id/timestamps/etc.) apply instead of forcing invalid blanks.
    """
    if isinstance(data, dict):
        cleaned = {}
        for key, val in data.items():
            next_val = _remove_empty_values(val)
            if _is_empty_value(next_val):
                continue
            cleaned[key] = next_val
        return cleaned
    if isinstance(data, list):
        cleaned = [_remove_empty_values(item) for item in data]
        return [item for item in cleaned if not _is_empty_value(item)]
    return data


def _flatten_nested_block(block):
    """
    Convert Pydantic nested-block shape to legacy dict shape expected by this module.
    Accepts either legacy dict or {"_meta":..., "properties": {...}}.
    """
    if not isinstance(block, dict):
        return {}
    if "properties" not in block:
        return block
    flattened = {}
    meta = block.get("_meta")
    if meta:
        flattened["_meta"] = meta
    props = block.get("properties", {})
    if isinstance(props, dict):
        flattened.update(props)
    for key, val in block.items():
        if key in ("_meta", "properties"):
            continue
        flattened[key] = val
    return flattened


def _prepare_template_legacy_dict(template_model):
    """
    Normalize template model/dict into legacy structure used by make_stixorm_object.
    """
    if isinstance(template_model, dict):
        return template_model
    if hasattr(template_model, "body") and hasattr(template_model, "class_name"):
        body_dict = template_model.body().model_dump(by_alias=True, exclude_none=True)
        for section in ("extensions", "sub"):
            if section in body_dict and isinstance(body_dict[section], dict):
                body_dict[section] = {
                    key: _flatten_nested_block(value)
                    for key, value in body_dict[section].items()
                }
        return {"class_name": template_model.class_name} | body_dict
    return template_model


def _build_embedded_object(class_name, raw_data, temp_sub):
    """
    Build embedded class instances from dict/list payloads.
    Falls back to original payload when instantiation fails.
    """
    if class_name not in globals():
        return raw_data

    def _convert_one(item):
        if not isinstance(item, dict):
            return item
        payload = dict(item)
        required_fields = []
        if class_name in temp_sub:
            for key, val in temp_sub[class_name].items():
                if not isinstance(val, dict) or "property" not in val:
                    continue
                if val.get("parameters", {}).get("required") is True:
                    required_fields.append(key)
                if val["property"] == "TimestampProperty" and key in payload:
                    payload[key] = convert_dt(payload[key])
        for req_key in required_fields:
            if req_key not in payload or _is_empty_value(payload.get(req_key)):
                return None
        try:
            return globals()[class_name](**payload)
        except Exception:
            return None

    if isinstance(raw_data, list):
        converted = [_convert_one(item) for item in raw_data]
        return [item for item in converted if item is not None]
    return _convert_one(raw_data)


def make_stixorm_object(stixorm_form):
    print(f"Step 1 >>")
    # 1. Extract the components of the form
    required = dict(stixorm_form["base_required"])
    optional = dict(stixorm_form["base_optional"])
    main = dict(stixorm_form["object"])
    extensions = dict(stixorm_form["extensions"])
    temp_contents = required | optional | main | extensions
    final_data = {}
    stix_dict = {}
    # 2. Get the Stix Template for the Object
    # Specify the path to the Nodes and Edges module
    module_path = TR_Common_Files + '/' + common[0]["file"]
    # 3. Load the module spec using importlib.util.spec_from_file_location
    spec = importlib.util.spec_from_file_location('parse', module_path)
    # Create the module from the specification
    parse = importlib.util.module_from_spec(spec)
    # Load the module
    spec.loader.exec_module(parse)
    # 4. Get the Stix Template for the Object
    stix_template = _prepare_template_legacy_dict(
        parse.get_stix_template_from_object(temp_contents)
    )
    temp_required = stix_template["base_required"]
    temp_optional = stix_template["base_optional"]
    temp_main = stix_template["object"]
    temp_extensions = stix_template["extensions"]
    temp_sub = stix_template["sub"]
    # Keep only fields defined by template sections.
    required = {k: v for k, v in required.items() if k in temp_required}
    optional = {k: v for k, v in optional.items() if k in temp_optional}
    main = {k: v for k, v in main.items() if k in temp_main}
    extensions = {k: v for k, v in extensions.items() if k in temp_extensions}
    for ext_key, ext_val in list(extensions.items()):
        temp_ext = temp_extensions.get(ext_key, {})
        if isinstance(ext_val, dict) and isinstance(temp_ext, dict):
            extensions[ext_key] = {k: v for k, v in ext_val.items() if k in temp_ext}

    # Remove empty placeholders before object construction.
    required = _remove_empty_values(required)
    optional = _remove_empty_values(optional)
    main = _remove_empty_values(main)
    extensions = _remove_empty_values(extensions)

    # 5. Process the template and create the class objects
    # 5.A Look for Properties in the temp_main, if they are EmbeddedObjectProperty then see if they exist in main, if they do then create their sub class objects
    for k, v in temp_main.items():
        if not isinstance(v, dict) or "property" not in v:
            continue
        if v["property"] == "EmbeddedObjectProperty":
            if k in main:
                # the sub object is in the main object, so
                # first get the class name from v["parameters"]["type"]
                class_name = v["parameters"]["type"]
                # second to fifth: build sub object(s) and place back in main
                main[k] = _build_embedded_object(class_name, main[k], temp_sub)
    # 5.B Look for the sub objects in the temp_extensions, if they have an EmbeddedObjectProperty then see if they exist in extensions, if they do then create their sub class objects
    for key, value in temp_extensions.items():
        for k, v in value.items():
            if not isinstance(v, dict) or "property" not in v:
                continue
            if v["property"] == "EmbeddedObjectProperty":
                if key in extensions and k in extensions[key]:
                    # there is a sub object in the extensions subobject, so
                    # first, get the class name 
                    class_name = v["parameters"]["type"]
                    # second to fifth: build sub object(s) and place back on extension
                    extensions[key][k] = _build_embedded_object(
                        class_name,
                        extensions[key][k],
                        temp_sub,
                    )
    # 5.C Keep extensions as dictionaries.
    # New templates and stix2 parsing expect extension entries under final_data["extensions"].
    # 5.D check the temp_main to see if there are any TimestampProperty properties in main, if there are then convert the values to the correct format
    for k, v in temp_main.items():
        if isinstance(v, dict) and v.get("property") == "TimestampProperty" and k in main:
            main[k] = convert_dt(main[k])
    # 5.D check the temp_required to see if there are any TimestampProperty properties in required, if there are then convert the values to the correct format
    for k, v in temp_required.items():
        if isinstance(v, dict) and v.get("property") == "TimestampProperty" and k in required:
            required[k] = convert_dt(required[k])
    # 5.E Remove empty values created during embedded conversion.
    required = _remove_empty_values(required)
    optional = _remove_empty_values(optional)
    main = _remove_empty_values(main)
    extensions = _remove_empty_values(extensions)
    # 5.F Put together the final object
    final_data = required | optional | main
    if extensions:
        final_data["extensions"] = extensions
    try:
        stix_obj = globals()[stix_template["class_name"]](**final_data)
    except Exception:
        # Some legacy forms carry extension payloads that are no longer valid for
        # current stixorm classes. Retry without extensions before failing.
        if "extensions" in final_data:
            retry_data = dict(final_data)
            retry_data.pop("extensions", None)
            stix_obj = globals()[stix_template["class_name"]](**retry_data)
        else:
            raise
    # 5.G Return the final, serialized object
    stix_dict = json.loads(stix_obj.serialize())

    return stix_dict


def main(inputfile, outputfile):
    stixorm_form = None
    if os.path.exists(inputfile):
        with open(inputfile, "r") as script_input:
            input_data = json.load(script_input)
            print(f"type identity->{input_data}")
            if "stixorm_form" in input_data:
                stixorm_form = input_data["stixorm_form"]
            elif "api" in input_data:
                api_input = input_data["api"]
                if "stixorm_form" in api_input:
                    stixorm_form = api_input["stixorm_form"]


    print(f"type stixorm_form->{type(stixorm_form)}")
    # setup logger for execution
    stix_dict = make_stixorm_object(stixorm_form)
    with open(outputfile, "w") as outfile:
        json.dump(stix_dict, outfile)


################################################################################
## body end                                                                   ##
################################################################################


################################################################################
## footer start                                                               ##
################################################################################
import argparse
import os


def getArgs():

  parser = argparse.ArgumentParser(description="Script params",
                                formatter_class=argparse.ArgumentDefaultsHelpFormatter)
  parser.add_argument("inputfile", nargs='?', default=f"{os.path.basename(__file__)}.input", help="input file (default: %(default)s)")
  parser.add_argument("outputfile", nargs='?', default=f"{os.path.basename(__file__)}.output", help="output file (default: %(default)s)")
  return parser.parse_args()

if __name__ == '__main__':
  args = getArgs()
  # setup logger for init
  # log = Logger
  # log.remove()
  # log.add(f'{os.path.basename(__file__)}.log', level="INFO")
  # log.info(args)
  main(args.inputfile, args.outputfile)


################################################################################
## footer end                                                                 ##
################################################################################