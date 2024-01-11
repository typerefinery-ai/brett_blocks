
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
from stixorm.module.typedb_lib.factories.auth_factory import get_auth_factory_instance
from stixorm.module.typedb_lib.factories.definition_factory import get_definition_factory_instance
from stixorm.module.typedb_lib.factories.import_type_factory import ImportType
from stixorm.module.typedb_lib.model.definitions import DefinitionName
from stixorm.module.orm.import_utilities import val_tql
from stixorm.module.parsing.conversion_decisions import sdo_type_to_tql, sro_type_to_tql, sco__type_to_tql, \
    meta_type_to_tql, get_embedded_match
from stixorm.module.orm.import_objects import marking
attack_model = get_definition_factory_instance().lookup_definition(DefinitionName.ATTACK)
stix_model = get_definition_factory_instance().lookup_definition(DefinitionName.STIX_21)
os_threat_model = get_definition_factory_instance().lookup_definition(DefinitionName.OS_THREAT)

import_type = import_type_factory.get_all_imports()
default_import_type = import_type_factory.get_default_import()
import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
import json
import os
import copy

connection = {
    "uri": "localhost",
    "port": "1729",
    "database": "stix_test",
    "user": None,
    "password": None
}


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


def stix_to_tql_basis(stix_dict, import_type):
    if import_type is None:
        import_type = default_import_type

    auth_factory = get_auth_factory_instance()
    auth = auth_factory.get_auth_for_import(import_type)
    logger.debug(f'stix object type {stix_dict["type"]}\n')

    auth_types = copy.deepcopy(auth["types"])
    # case variables
    obj_tql = {}
    obj_tql_name = ""
    is_list = False
    protocol = ""
    if stix_dict["type"] in auth_types["sdo"]:
        family = "sdo"
        logger.debug(f' going into sdo ---? {stix_dict}')
        # 1. Characterise the type of SCO it is
        sdo_tql_name = stix_dict["type"]
        attack_object = False if not stix_dict.get("x_mitre_version", False) else True
        step_type = ""
        if stix_dict["type"] == "sequence":
            step_type = stix_dict.get("step_type", "sequence")
        sub_technique = False
        if attack_object:
            sub_technique = False if not stix_dict.get("x_mitre_is_subtechnique", False) else True
        # 2. Retrieve the data set for the object
        obj_tql, obj_tql_name, is_list, protocol = sdo_type_to_tql(sdo_tql_name, import_type, attack_object,
                                                                   sub_technique, step_type)
        # 3. Setup the variable, and the base match statement
        obj_var = "$" + sdo_tql_name
        core_ql = obj_var + ' isa ' + sdo_tql_name + ', has stix-id $stix-id;\n$stix-id "' + stix_dict["id"] + '";\n'
        return obj_tql, obj_tql_name, is_list, protocol, obj_var, core_ql, family

    elif stix_dict["type"] in auth_types["sro"]:
        family = "sro"
        logger.debug(f' going into sro ---> {stix_dict}')
        # - work out the type of object
        uses_relation = False
        is_procedure = False
        attack_object = False if not stix_dict.get("x_mitre_version", False) else True
        if attack_object:
            uses_relation = False if not stix_dict.get("relationship_type", False) == "uses" else True
            if stix_dict.get("target_ref", False):
                target = stix_dict.get("target_ref", False)
                is_procedure = False if not target.split('--')[0] == "attack-pattern" else True
        obj_tql = {}
        sro_tql_name = stix_dict["type"]
        sro_sub_rel = "" if not stix_dict.get("relationship_type", False) else stix_dict["relationship_type"]

        obj_tql, sro_tql_name, is_list, protocol = sro_type_to_tql(sro_tql_name, sro_sub_rel, import_type, attack_object, uses_relation, is_procedure)
        # 3. Setup the variable, and the base match statement
        obj_var = "$" + sro_tql_name
        core_ql = obj_var + ' isa ' + sro_tql_name + ', has stix-id $stix-id;\n$stix-id "' + stix_dict["id"] + '";\n'
        return obj_tql, obj_tql_name, is_list, protocol, obj_var, core_ql, family

    elif stix_dict["type"] in auth_types["sco"]:
        family = "sco"
        logger.debug(f' going into sco ---> {stix_dict}')
        # - work out the type of object
        sco_tql_name = stix_dict["type"]
        # - get the object-specific typeql names, sighting or relationship
        obj_tql, sco_tql_name, is_list, protocol = sco__type_to_tql(sco_tql_name, import_type)
        # - variable for use in typeql statements
        obj_var = '$' + stix_dict["type"]
        core_ql = obj_var + ' isa ' + sco_tql_name + ', has stix-id $stix-id;\n$stix-id '  + stix_dict["id"] + ';\n'
        return obj_tql, obj_tql_name, is_list, protocol, obj_var, core_ql, family

    elif stix_dict["type"] == 'marking-definition':
        family = "marking"
        # 1.A) if one of the existing colours, return an empty string
        if stix_dict["id"] in marking:
            return {}, "", [], "", "", "", ""
        # 1.B) Test for attack object and handle statement if a statement marking
        attack_object = False if not stix_dict.get("x_mitre_attack_spec_version", False) else True
        if stix_dict.get("definition", False):
            statement = stix_dict["definition"]
            stix_dict.update(statement)

        obj_tql, meta_tql_name, is_list, protocol = meta_type_to_tql(stix_dict["type"], import_type, attack_object)
        # - variable for use in typeql statements
        obj_var = '$' + stix_dict["type"]
        core_ql = obj_var + ' isa ' + stix_dict["type"] + ', has stix-id $stix-id;\n$stix-id '  + stix_dict["id"] + ';\n'
        return obj_tql, obj_tql_name, is_list, protocol, obj_var, core_ql, family

    else:
        logger.error(f'object type not supported: {stix_dict["type"]}, import type {import_type}')
        dep_list = []
        return {}, "", [], "", "", "", ""


def granular_markings(term, obj_var, source_var, key_list, import_type, inc, diff_type):
    if diff_type == "values_changed":
        pass
    elif diff_type == "dictionary_item_added" or diff_type == "iterable_item_added":
        pass
    elif diff_type == "dictionary_item_removed" or diff_type == "iterable_item_removed":
        pass
    else:
        pass

def hashes(term, obj_var, source_var, key_list, import_type, inc, diff_type):
    if diff_type == "values_changed":
        pass
    elif diff_type == "dictionary_item_added" or diff_type == "iterable_item_added":
        pass
    elif diff_type == "dictionary_item_removed" or diff_type == "iterable_item_removed":
        pass
    else:
        pass

def key_value(term, obj_var, source_var, key_list, import_type, inc, diff_type):
    if diff_type == "values_changed":
        pass
    elif diff_type == "dictionary_item_added" or diff_type == "iterable_item_added":
        pass
    elif diff_type == "dictionary_item_removed" or diff_type == "iterable_item_removed":
        pass
    else:
        pass


def list_of_objects(term, obj_var, source_var, key_list, import_type, inc, diff_type):
    if diff_type == "values_changed":
        pass
    elif diff_type == "dictionary_item_added" or diff_type == "iterable_item_added":
        pass
    elif diff_type == "dictionary_item_removed" or diff_type == "iterable_item_removed":
        pass
    else:
        pass


def embedded(term, obj_var, source_var, key_list, import_type, inc, diff_type):
    if diff_type == "values_changed":
        pass
    elif diff_type == "dictionary_item_added" or diff_type == "iterable_item_added":
        pass
    elif diff_type == "dictionary_item_removed" or diff_type == "iterable_item_removed":
        pass
    else:
        pass


def subobject(term, obj_var, source_var, key_list, import_type, inc, diff_type):
    if diff_type == "values_changed":
        pass
    elif diff_type == "dictionary_item_added" or diff_type == "iterable_item_added":
        pass
    elif diff_type == "dictionary_item_removed" or diff_type == "iterable_item_removed":
        pass
    else:
        pass


def extension(term, obj_var, source_var, key_list, import_type, inc, diff_type):
    if diff_type == "values_changed":
        pass
    elif diff_type == "dictionary_item_added" or diff_type == "iterable_item_added":
        pass
    elif diff_type == "dictionary_item_removed" or diff_type == "iterable_item_removed":
        pass
    else:
        pass


def follow_pathway(term, obj_var, source_var, key_list, import_type, inc, diff_tyoe):
    """
        Top level function to add one of the sub objects to the stix object
    Args:
        term "": the stix name of the property
        obj_var (): the typeql variable string of the object
        source_var (): it not empty string, then the typeql variable string of the object to be linked
        key_list (): the property variable list
        import_type: the dict describing import preferences
        inc int: an incrementing variable that is used to add to the var string

    Returns:
        match: the typeql match strings
        insert: the typeql insert string
    """
    logger.debug(f'===============\n=====================\n===================\n')
    logger.debug(f'rel {term}')
    logger.debug(f'obj_var {obj_var}')
    logger.debug(f'source_var {source_var}')
    logger.debug(f'key_list {key_list}')
    auth_factory = get_auth_factory_instance()
    auth = auth_factory.get_auth_for_import(import_type)
    dep_list = []
    logger.debug("\nstarting into choices")
    if term == "granular_markings":
        logger.debug("in granular")
        # handle list of objects scenario, with add, delete, or update
        match, insert, delete, query_type = granular_markings(term, obj_var, source_var, key_list, import_type, inc, diff_tyoe)

    # hashes type
    elif (term == "hashes"
          or term == "file_header_hashes"):
        logger.debug("in hashes")
        # handle hashes scenario, with add, delete, update
        match, insert, delete, query_type = hashes(term, obj_var, source_var, key_list, import_type, inc, diff_tyoe)

    # insert key value store
    elif term in auth["reln_name"]["key_value_relations"]:
        logger.debug("in key value")
        # handle key-value scenario, with add, delete, update
        match, insert, delete, query_type = key_value(term, obj_var, source_var, key_list, import_type, inc, diff_tyoe)

    # insert list of object relation
    elif term in auth["reln_name"]["list_of_objects"]:
        logger.debug("list of objects")
        # handle list of objects scenario, with add, delete, or update
        match, insert, delete, query_type = list_of_objects(term, obj_var, source_var, key_list, import_type, inc, diff_tyoe)

    # insert embedded relations based on stix-id
    elif term in auth["reln_name"]["embedded_relations"]:
        logger.debug("embedded")
        # handle embedded object, with add, delete, or update object
        match, insert, delete, query_type = embedded(term, obj_var, source_var, key_list, import_type, inc, diff_tyoe)

    # insert plain sub-object with relation
    elif (term == "x509_v3_extensions"
          or term == "optional_header"):
        logger.debug("X509")
        # handle sub object scenario, with add, delete, or update
        match, insert, delete, query_type = subobject(term, obj_var, source_var, key_list, import_type, inc, diff_tyoe)

    # insert  SCO Extensions here, a possible dict of sub-objects
    elif term in auth["reln_name"]["extension_relations"] or term == "extensions":
        logger.debug("extension")
        # handle extension scenario, with add, delete, or update
        match, insert, delete, query_type = extension(term, obj_var, source_var, key_list, import_type, inc, diff_tyoe)

    # ignore the following relations as they are already processed, for Relationships, Sightings and Extensions
    elif term in auth["reln_name"]["standard_relations"] or term == "definition" or "definition_type":
        logger.debug("standard")
        match = insert = ''

    else:
        logger.debug(f'relation type not known, ignore if "source_ref" or "target_ref" -> {rel}')
        logger.debug("in else")
        match = insert = ""

    return match, insert, delete, query_type

def value_is_id(valuestring):
    answer = False
    return  answer

def consume_path_token(obj_tql, key_list, value, obj_var, source_var, inc, diff_tyoe):
    match = ""
    insert = ""
    delete = ""
    if len(key_list) > 0:
        term = key_list.pop(0)
        if obj_tql[term] == "":
            # its a relationship
            match, insert, delete, query_type  = follow_pathway(term, obj_var, source_var, key_list, import_type, inc, diff_tyoe)
        else:
            # its  a value
            prop_var = "$" + obj_tql[term]
            insert += obj_var + " has " + obj_tql[term] + " " + prop_var + ";"
            insert += prop_var + " " + val_tql(value) + ";"


    return match, insert, delete


def handle_object_diff(obj_diff, orig_object, current_obj, connection, import_type):
    #
    # 1. First find the basic data for this object
    match = "match \n"
    insert = ""
    delete = ""
    obj_tql, obj_tql_name, is_list, protocol, obj_var, core_ql, family = stix_to_tql_basis(orig_object, import_type)
    for diff_tyoe, diff_value in obj_diff.items():
        if diff_tyoe == "dictionary_item_added":
            for i, key, value in enumerate(diff_value.items()):
                path_list = parse_path(key)
                source_var = ""
                if value_is_id(value):
                    source_var, match2 = get_embedded_match(value, import_type=import_type, i=i, protocol=protocol)
                    match += match + match2
                key_list = parse_path(key)
                match, insert, delete = consume_path_token(obj_tql, key_list, value, obj_var, source_var, i, diff_tyoe)
        elif diff_tyoe == "iterable_item_added":
            pass
        elif diff_tyoe == "values_changed":
            pass
        elif diff_tyoe == "dictionary_item_removed":
            pass

