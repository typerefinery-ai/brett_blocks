
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
from stixorm.module.typedb_lib.factories.mappings_factory import get_mapping_factory_instance
from stixorm.module.typedb_lib.instructions import ResultStatus, Result
from stixorm.module.parsing import parse_objects
from deepdiff import DeepDiff, parse_path
from Block_Families.General._library.update_utilities import follow_pathway
from stixorm.module.definitions.property_definitions import is_stix_type, _check_uuid
from pprint import pprint
from stixorm.module.typedb_lib.factories.auth_factory import get_auth_factory_instance
from stixorm.module.typedb_lib.factories.definition_factory import get_definition_factory_instance
from stixorm.module.typedb_lib.factories.import_type_factory import ImportType
from stixorm.module.typedb_lib.model.definitions import DefinitionName
from stixorm.module.orm.import_utilities import val_tql
from stixorm.module.parsing.conversion_decisions import sdo_type_to_tql, sro_type_to_tql, sco_type_to_tql, \
    meta_type_to_tql, get_embedded_match
from stixorm.module.orm.import_objects import marking
attack_model = get_definition_factory_instance().lookup_definition(DefinitionName.ATTACK)
stix_model = get_definition_factory_instance().lookup_definition(DefinitionName.STIX_21)
os_threat_model = get_definition_factory_instance().lookup_definition(DefinitionName.OS_THREAT)
from typedb.driver import TypeDB
from typedb.api.connection.session import SessionType
from typedb.api.connection.transaction import TransactionType

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


def find_obj_diff(original_object, changed_incident_obj):
    verbose_level = 2
    ignore_order = True
    group_by = 'id'
    diff = DeepDiff(original_object, changed_incident_obj, verbose_level=verbose_level, ignore_order=ignore_order)
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
    return list(delete_object_ids), list(add_objects_list), list(may_have_changed_list)


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
        obj_tql, sco_tql_name, is_list, protocol = sco_type_to_tql(sco_tql_name, import_type)
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


def value_is_id(valuestring):
    answer = False
    if valuestring.find("--") > 0:
        x = valuestring.split('--', 1)
        type = x[0]
        uuid_str = x[1]
        valid_obj = get_mapping_factory_instance().get_all_types()
        spec_version = "2.1"
        if is_stix_type(type, spec_version, valid_obj) and _check_uuid(uuid_str, spec_version):
            answer = True
    return answer

def consume_path_token(obj_tql, key_list, value, obj_var, source_var, i, op_type, protocol):
    match = ""
    insert = ""
    delete = ""
    if len(key_list) > 0:
        term = key_list.pop(0)
        if obj_tql[term] == "":
            # its a relationship
            match, insert, delete, op_type = follow_pathway(term, value, obj_var, source_var, key_list, import_type, i, op_type, protocol)
        else:
            # its  a value
            prop_var = "$" + obj_tql[term]
            new_var = "$" + "new_" + obj_tql[term]
            if op_type == "add":
                insert += obj_var + " has " + obj_tql[term] + " " + prop_var + ";"
                insert += prop_var + " " + val_tql(value) + ";"
            elif op_type == "change":
                match += obj_var + " has " + obj_tql[term] + " " + prop_var + ";"
                delete += obj_var + " has " + obj_tql[term] + " " + prop_var + ";"
                insert += obj_var + " has " + obj_tql[term] + " " + new_var + ";"
                insert += new_var + " " + val_tql(value['new_value']) + ";"
            if op_type == "remove":
                match += obj_var + " has " + obj_tql[term] + " " + prop_var + ";"
                delete += obj_var + " has " + obj_tql[term] + " " + prop_var + ";"

    return match, insert, delete, op_type


def handle_object_diff(obj_diff, orig_object, current_obj, connection, import_type=import_type):
    #
    # 1. First find the basic data for this object
    print(f"\n==========obj dif===========\n{obj_diff}")
    i = 0
    diff_report_list = []
    obj_tql, obj_tql_name, is_list, protocol, obj_var, core_ql, family = stix_to_tql_basis(orig_object, import_type)
    for diff_type, diff_value in obj_diff.items():
        if diff_type == "dictionary_item_added" or diff_type == "iterable_item_added":
            op_type = "add"
            for key, value in diff_value.items():
                value_list = []
                if type(value) is list:
                    value_list = value
                else:
                    value_list.append(value)
                for v in value_list:
                    match = ""
                    insert = ""
                    delete = ""
                    path_list = parse_path(key)
                    source_var = ""
                    i += 1
                    if value_is_id(v):
                        source_var, match2 = get_embedded_match(v, import_type=import_type, i=i, protocol=protocol)
                        match += match2
                    key_list = parse_path(key)
                    match2, insert2, delete2, op_type = consume_path_token(obj_tql, key_list, v, obj_var, source_var, i, op_type, protocol)
                    match += match2
                    insert += insert2
                    delete += delete2
                    print(f"\n----------------------- {orig_object['id']}")
                    print(f"match -> {core_ql+match}")
                    print(f"insert -> {insert}")
                    print(f"delete -> {delete}")
                    #update_typeql(core_ql+match, insert, delete, op_type, connection)
                    diff_report = {}
                    diff_report["original id"] = orig_object['id']
                    diff_report["type"] = diff_type
                    diff_report["value"] = diff_value
                    diff_report["match core"] = core_ql
                    diff_report["match object"] = match
                    diff_report["insert"] = insert
                    diff_report["delete"] = delete
                    diff_report_list.append(diff_report)
        elif diff_type == "dictionary_item_removed" or diff_type == "iterable_item_removed":
            op_type = "remove"
            for key, value in diff_value.items():
                value_list = []
                if type(value) is list:
                    value_list = value
                else:
                    value_list.append(value)
                for v in value_list:
                    match = ""
                    insert = ""
                    delete = ""
                    path_list = parse_path(key)
                    source_var = ""
                    i += 1
                    if value_is_id(v):
                        source_var, match2 = get_embedded_match(v, import_type=import_type, i=i, protocol=protocol)
                        match += match + match2
                    key_list = parse_path(key)
                    match2, insert2, delete2, op_type = consume_path_token(obj_tql, key_list, v, obj_var, source_var, i, op_type, protocol)
                    match += match2
                    insert += insert2
                    delete += delete2
                    print(f"\n----------------------- {orig_object['id']}")
                    print(f"match -> {core_ql+match}")
                    print(f"insert -> {insert}")
                    print(f"delete -> {delete}")
                    #update_typeql(core_ql+match, insert, delete, op_type, connection)
                    diff_report = {}
                    diff_report["original id"] = orig_object['id']
                    diff_report["type"] = diff_type
                    diff_report["value"] = diff_value
                    diff_report["match core"] = core_ql
                    diff_report["match object"] = match
                    diff_report["insert"] = insert
                    diff_report["delete"] = delete
                    diff_report_list.append(diff_report)
        elif diff_type == "values_changed":
            op_type = "change"
            for key, value in diff_value.items():
                value_list = []
                if type(value) is list:
                    value_list = value
                else:
                    value_list.append(value)
                for v in value_list:
                    match = ""
                    insert = ""
                    delete = ""
                    path_list = parse_path(key)
                    source_var = ""
                    i += 1
                    if isinstance(value, dict):
                        original_value = value["old_value"]
                        new_value = value["new_value"]
                        source_var = ""
                        if value_is_id(original_value):
                            source_var, match2 = get_embedded_match(original_value, import_type=import_type, i=i, protocol=protocol)
                            match += match + match2
                        key_list = parse_path(key)
                        match2, insert2, delete2, op_type = consume_path_token(obj_tql, key_list, value, obj_var, source_var, i, op_type, protocol)
                        match += match2
                        insert += insert2
                        delete += delete2
                        print(f"----------------------- {orig_object['id']}")
                        print(f"match -> {core_ql+match}")
                        print(f"insert -> {insert}")
                        print(f"delete -> {delete}")
                        #update_typeql(core_ql+match, insert, delete, op_type, connection)
                        diff_report = {}
                        diff_report["original id"] = orig_object['id']
                        diff_report["type"] = diff_type
                        diff_report["value"] = diff_value
                        diff_report["match core"] = core_ql
                        diff_report["match object"] = match
                        diff_report["insert"] = insert
                        diff_report["delete"] = delete
                        diff_report_list.append(diff_report)
        else:
            print(f"We dont account for diff-type -> {diff_type}")

    return diff_report_list


def update_typeql(match, insert, delete, op_type, stix_connection):
    url = stix_connection["uri"] + ":" + stix_connection["port"]
    with TypeDB.core_driver(url) as driver:
        # Stage 1: Create the schema
        with driver.session(stix_connection["database"], SessionType.DATA) as session:
            with session.transaction(TransactionType.WRITE) as write_transaction:
                logger.debug(f'Loading TLP markings')
                # check match exists
                match_exists = iterator_has_next(write_transaction.query.get("match " + match + " get; limit 1;"))
                if match_exists:
                    if op_type == "add":
                        typedb_iterator = write_transaction.query.insert("match " + match + " insert " + insert)
                        logger.debug(f'insert_iterator response ->\n{typedb_iterator}')
                        for result in typedb_iterator:
                            logger.info(f'typedb response ->\n{result}')
                    elif op_type == "remove":
                        typedb_iterator = write_transaction.query.delete("match " + match + " delete " + delete)
                        logger.debug(f'remove_iterator response ->\n{typedb_iterator}')
                        # for result in typedb_iterator:
                        #     logger.info(f'typedb response ->\n{result}')
                    elif op_type == "change":
                        typedb_iterator = write_transaction.query.update("match " + match + " delete " + delete + " insert " + insert)
                        logger.debug(f'update_iterator response ->\n{typedb_iterator}')
                        for result in typedb_iterator:
                            logger.info(f'typedb response ->\n{result}')
                else:
                    # ... do something dependent on the match not existing
                    logger.error(f"$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
                    logger.error(f"match error {match}")
                    logger.error(f"insert error {insert}")
                    logger.error(f"delete error {delete}\n")

                write_transaction.commit()


def iterator_has_next(possible_iter):
    try:
        next(possible_iter)
        return True
    except StopIteration:
        return False
