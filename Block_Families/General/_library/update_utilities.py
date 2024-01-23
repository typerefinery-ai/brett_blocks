import datetime
from typing import List, Dict
import copy

import logging

from stixorm.module.parsing.conversion_decisions import get_source_from_id
from stixorm.module.typedb_lib.factories.auth_factory import get_auth_factory_instance
from stixorm.module.typedb_lib.factories.definition_factory import get_definition_factory_instance
from stixorm.module.typedb_lib.factories.import_type_factory import ImportType
from stixorm.module.typedb_lib.model.definitions import DefinitionName

from stixorm.module.parsing.conversion_decisions import sdo_type_to_tql, sro_type_to_tql, sco_type_to_tql, \
    meta_type_to_tql, get_embedded_match
stix_models = get_definition_factory_instance().lookup_definition(DefinitionName.STIX_21)
logger = logging.getLogger(__name__)


def follow_pathway(term, value, obj_var, source_var, key_list, import_type, inc, op_type, protocol):
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
    match = ""
    insert = ""
    delete = ""
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
        match, insert, delete, op_type = granular_markings(term, value, obj_var, source_var, key_list, import_type, inc, op_type, protocol)

    # hashes type
    elif (term == "hashes"
          or term == "file_header_hashes"):
        logger.debug("in hashes")
        # handle hashes scenario, with add, delete, update
        match, insert, delete, op_type = hashes(term, value, obj_var, source_var, key_list, import_type, inc, op_type, protocol)

    # insert key value store
    elif term in auth["reln_name"]["key_value_relations"]:
        logger.debug("in key value")
        # handle key-value scenario, with add, delete, update
        match, insert, delete, op_type = key_value_store(term, value, obj_var, source_var, key_list, import_type, inc, op_type, protocol)

    # insert list of object relation
    elif term in auth["reln_name"]["list_of_objects"]:
        logger.debug("list of objects")
        # handle list of objects scenario, with add, delete, or update
        match, insert, delete, op_type = list_of_objects(term, value, obj_var, source_var, key_list, import_type, inc, op_type, protocol)

    # insert embedded relations based on stix-id
    elif term in auth["reln_name"]["embedded_relations"]:
        logger.debug("embedded")
        # handle embedded object, with add, delete, or update object
        match, insert, delete, op_type = embedded_relation(term, value, obj_var, source_var, key_list, import_type, inc, op_type, protocol)

    # insert plain sub-object with relation
    elif (term == "x509_v3_extensions"
          or term == "optional_header"):
        logger.debug("X509")
        # handle sub object scenario, with add, delete, or update
        match, insert, delete, op_type = load_object(term, value, obj_var, source_var, key_list, import_type, inc, op_type, protocol)

    # insert  SCO Extensions here, a possible dict of sub-objects
    elif term in auth["reln_name"]["extension_relations"] or term == "extensions":
        logger.debug("extension")
        # handle extension scenario, with add, delete, or update
        match, insert, delete, op_type = extensions(term, value, obj_var, source_var, key_list, import_type, inc, op_type, protocol)

    # ignore the following relations as they are already processed, for Relationships, Sightings and Extensions
    elif term in auth["reln_name"]["standard_relations"] or term == "definition" or "definition_type":
        logger.debug("standard")
        match = insert = ''

    else:
        logger.debug(f'relation type not known, ignore if "source_ref" or "target_ref" -> {term}')
        logger.debug("in else")
        match = insert = ""

    return match, insert, delete, op_type

def extensions(term, value, obj_var, source_var, key_list, import_type, inc, op_type, protocol):
    """
        Create the Typeql for the extensions sub object
    Args:
        prop_name (): the name of the extension
        prop_dict (): the dict for the extension
        parent_var (): the var of the Stix object that is the owner
        import_type: the dict describing import preferences

    Returns:
        match: the typeql match string
        insert: the typeql insert string
    """
    match = ""
    insert = ""
    delete = ""
    auth_factory = get_auth_factory_instance()
    auth = auth_factory.get_auth_for_import(import_type)
    match = insert = ''
    dep_list = []
    term2 = key_list.pop(0)
    # for each key in the dict (extension type)
    # logger.debug('--------------------- extensions ----------------------------')
    for ext_type_ql in auth["reln"]["extension_relations"]:
        if term2 == ext_type_ql["stix"]:
            match2, insert2, delete2, op_type = load_object(term2, value, obj_var, source_var, key_list, import_type, inc, op_type, protocol)
            match = match + match2
            delete = delete + delete2
            insert = insert + insert2
            break

    return match, insert, delete, op_type


def load_object(term, value, obj_var, source_var, key_list, import_type, inc, op_type, protocol):
    """
        Create the Typeql for a sub object
    Args:
        term (): the name of the extension
        value (): the vlue included in the deepdiff
        obj_var (): the var of the Stix object that is the owner
        source_var (): the var of an embedded relation if value is a stix-id
        key_list: the list of terms left

    Returns:
        match: the typeql match string
        insert: the typeql insert string
        delete: the typeql delete string
    """
    match = ""
    insert = ""
    delete = ""

    auth_factory = get_auth_factory_instance()
    auth = auth_factory.get_auth_for_import(import_type)
    # find the data record for the load object function
    for prop_type in auth["reln"]["extension_relations"]:
        if term == prop_type["stix"]:
            sub_obj_type = prop_type["object"]

            if sub_obj_type in auth["sub_objects"]:
                sub_obj_tql = copy.deepcopy(auth["sub_objects"][sub_obj_type])
            else:
                raise ValueError("no sub-object available")
            sub_obj_var = '$' + sub_obj_type + str(inc)
            reln = prop_type["relation"]
            rel_var = '$' + reln + str(inc)
            rel_owner = prop_type["owner"]
            rel_pointed_to = prop_type["pointed-to"]
            # Data must point either to a property, or a relation
            match += sub_obj_var + " isa " + sub_obj_type + ";"
            match += rel_var + " (" + rel_owner + ":" + obj_var + ", "
            match += rel_pointed_to + ":" + sub_obj_var + ") isa " + reln + ";"
            if len(key_list) > 0:
                term3 = key_list.pop(0)
                # Term3 is either a property or a relation
                if sub_obj_tql[term3] == "":
                    # its a relationship
                    match2, insert2, delete2, op_type = follow_pathway(term3, value, sub_obj_var, source_var, key_list,
                                                                    import_type, inc, op_type, protocol)
                    match = match + match2
                    delete = delete + delete2
                    insert = insert + insert2
                else:
                    # its  a value
                    prop_var = "$" + sub_obj_tql[term3]
                    new_var = "$" + "new_" + sub_obj_tql[term3]
                    if op_type == "add":
                        insert += sub_obj_var + " has " + sub_obj_tql[term3] + " " + new_var + ";"
                        insert += new_var + " " + val_tql(value) + ";"
                    elif op_type == "change":
                        match += sub_obj_var + " has " + sub_obj_tql[term3] + " " + prop_var + ";"
                        delete += sub_obj_var + " has " + sub_obj_tql[term3] + ";"
                        insert += sub_obj_var + " has " + sub_obj_tql[term3] + " " + val_tql(value['new_value']) + ";"
                    if op_type == "remove":
                        match += sub_obj_var + " has " + sub_obj_tql[term3] + " " + prop_var + ";"
                        delete += sub_obj_var + " has " + sub_obj_tql[term3] + ";"

            return match, insert, delete, op_type


def list_of_objects(term, value, obj_var, source_var, key_list, import_type, inc, op_type, protocol):
    """
        Create the Typeql for the list of object sub object
    Args:
        term (): the name of the extension
        value (): the vlue included in the deepdiff
        obj_var (): the var of the Stix object that is the owner
        source_var (): the var of an embedded relation if value is a stix-id
        key_list: the list of terms left

    Returns:
        match: the typeql match string
        insert: the typeql insert string
        delete: the typeql delete string
    """
    match = ""
    insert = ""
    delete = ""

    auth_factory = get_auth_factory_instance()
    auth = auth_factory.get_auth_for_import(import_type)
    for config in auth["reln"]["list_of_objects"]:
        if config["name"] == term:
            reln = config["typeql"]
            rel_var = '$' + reln + str(inc)
            rel_owner = config["owner"]
            rel_pointed_to = config["pointed_to"]
            sub_obj_type = config["object"]
            sub_obj_var = '$' + sub_obj_type + str(inc)

            if sub_obj_type in auth["sub_objects"]:
                sub_obj_tql = copy.deepcopy(auth["sub_objects"][sub_obj_type])
            else:
                raise ValueError("no sub-object available")

            # Data must point either to a property, or a relation
            match += sub_obj_var + " isa " + sub_obj_type + ";"
            match += rel_var + " (" + rel_owner + ":" + obj_var + ", "
            match += rel_pointed_to + ":" + sub_obj_var + ") isa " + reln + ";"
            if len(key_list) > 0:
                term3 = key_list.pop(0)
                # Term3 is either a property or a relation
                if sub_obj_tql[term3] == "":
                    # its a relationship
                    match2, insert2, delete2, op_type = follow_pathway(term3, value, sub_obj_var, source_var, key_list,
                                                                    import_type, inc, op_type, protocol)
                else:
                    # its  a value
                    prop_var = "$" + sub_obj_tql[term3]
                    new_var = "$" + "new_" + sub_obj_tql[term3]
                    if op_type == "add":
                        insert += sub_obj_var + " has " + sub_obj_tql[term3] + " " + prop_var + ";"
                        insert += prop_var + " " + val_tql(value) + ";"
                    elif op_type == "change":
                        match += sub_obj_var + " has " + sub_obj_tql[term3] + " " + prop_var + ";"
                        delete += sub_obj_var + " has " + sub_obj_tql[term3] + ";"
                        insert += sub_obj_var + " has " + sub_obj_tql[term3] + " " + val_tql(value['new_value']) + ";"
                    if op_type == "remove":
                        match += sub_obj_var + " has " + sub_obj_tql[term3] + " " + prop_var + ";"
                        delete += sub_obj_var + " has " + sub_obj_tql[term3] + ";"

            return match, insert, delete, op_type



def key_value_store(term, value, obj_var, source_var, key_list, import_type, inc, op_type, protocol):
    """
        Create the Typeql for the key-value store sub object
    Args:
        prop (): the name of the object
        prop_value_dict (): the dict of object
        obj_var (): the var of the Stix object that is the owner
        import_type: the dict describing import preferences

    Returns:
        match: the typeql match string
        insert: the typeql insert string
    """
    match = ""
    insert = ""
    delete = ""

    auth_factory = get_auth_factory_instance()
    auth = auth_factory.get_auth_for_import(import_type)
    for config in auth["reln"]["key_value_relations"]:
        if config["name"] == term:
            rel_typeql = config["typeql"]
            role_owner = config["owner"]
            role_pointed = config["pointed_to"]
            d_key = config["key"]
            d_value = config["value"]


    # match = ''
    # insert = '\n'
    # field_var_list = []
    # for i, key in enumerate(prop_value_dict):
    #     a_value = prop_value_dict[key]
    #     key_var = ' $' + d_key + str(i)
    #     field_var_list.append(key_var)
    #     insert += key_var + ' isa ' + d_key + '; ' + key_var + ' "' + key + '";\n'
    #     if isinstance(a_value, list):
    #         for j, n in enumerate(a_value):
    #             value_var = ' $' + d_value + str(j)
    #             insert += key_var + ' ' + 'has ' + d_value + ' "' + str(n) + '";\n'
    #     else:
    #         value_var = ' $' + d_value + str(i)
    #         insert += key_var + ' ' + 'has ' + d_value + ' "' + str(a_value) + '";\n'
    #
    # insert += ' $' + rel_typeql + ' (' + role_owner + ':' + obj_var
    # for var in field_var_list:
    #     insert += ', ' + role_pointed + ':' + var
    # insert += ') isa ' + rel_typeql + ';\n\n'
    return match, insert, delete, op_type


# specific methods
def hashes(term, value, obj_var, source_var, key_list, import_type, inc, op_type, protocol):
    """
        Create the Typeql for the hashes sub object
    Args:
        prop_name (): the name of the object
        prop_dict (): the dict of object
        parent_var (): the var of the Stix object that is the owner

    Returns:
        match: the typeql match string
        insert: the typeql insert string
    """

    match = ""
    insert = ""
    delete = ""

    # hash_var_list = []
    # for i, key in enumerate(prop_dict):
    #     hash_var = '$hash' + str(i)
    #     hash_var_list.append(hash_var)
    #     if key in stix_models.get_sub_objects("hash_typeql_dict"):
    #         insert += ' ' + hash_var + ' isa ' + stix_models.get_sub_objects("hash_typeql_dict")[
    #             key] + ', has hash-value ' + val_tql(prop_dict[key]) + ';\n'
    #     else:
    #         logger.error(f'Unknown hash type {key}')
    #
    # # insert the hash objects into the hashes relation with the parent object
    # insert += '\n $hash_rel (hash-owner:' + parent_var
    # for hash_var in hash_var_list:
    #     insert += ', hash-actual:' + hash_var
    #
    # insert += ') isa hashes;\n'
    return match, insert, delete, op_type


def granular_markings(term, value, obj_var, source_var, key_list, import_type, inc, op_type, protocol):
    """
        Create the Typeql for the granular markings sub object
    Args:
        prop_name (): the name of the object
        prop_value_List (): the list of object values
        parent_var (): the var of the Stix object that is the owner
        prop_var_list: the list of property variables

    Returns:
        match: the typeql match string
        insert: the typeql insert string
    """
    match = ""
    insert = ""
    delete = ""

    # if diff_type == "values_changed":
    #     pass
    # elif diff_type == "dictionary_item_added" or diff_type == "iterable_item_added":
    #     pass
    # elif diff_type == "dictionary_item_removed" or diff_type == "iterable_item_removed":
    #     pass
    # else:
    #     pass
    # match = insert = ''
    # for i, prop_dict in enumerate(prop_value_List):
    #     # setup and match in the marking, based on its id
    #     m_id = prop_dict['marking_ref']
    #     m_var = '$marking' + str(i)
    #     g_var = '$granular' + str(i)
    #     match += ' ' + m_var + ' isa marking-definition, has stix-id ' + '"' + m_id + '";\n'
    #     insert += ' ' + g_var + ' (marking:' + m_var + ', object:' + parent_var
    #     prop_list = prop_dict['selectors']
    #     for selector in prop_list:
    #         selector_var = get_selector_var(selector, prop_var_list)
    #         insert += ', marked:' + selector_var
    #
    #     insert += ') isa granular-marking;\n'

    return match, insert, delete, op_type


def get_selector_var(selector, prop_var_list):
    """
        Get the typeql variable for the property
    Args:
        selector (): the property to select
        prop_var_list (): the variable list to select from

    Returns:
        selector_var: the typeql variable for the property
    """
    if selector[-1] == ']':
        text = selector.split(".")
        selector = text[0]
        index = int(text[1][1])
    else:
        selector = selector
        index = -1

    # logger.debug(f'selector after processing -> {selector}, index after procesing -> {index}')
    for prop_var_dict in prop_var_list:
        if selector == prop_var_dict['prop'] and index == prop_var_dict['index']:
            selector_var = prop_var_dict['prop_var']
            break

    return selector_var


# ---------------------------------------------------
#        EMBEDDED RELATION METHODS
# ---------------------------------------------------
# object_refs
# sample_refs
# sample_ref
# host_vm_ref
# operating_system_ref
# installed_software_refs
# analysis_sco_refs
# etc.

def embedded_relation(term, value, obj_var, source_var, key_list, import_type, inc, op_type, protocol):
    """
        Create the Typeql for the embedded relation sub object
    Args:
        prop (): the name of the object
        prop_value (): the value of object
        obj_var (): the var of the Stix object that is the owner

    Returns:
        match: the typeql match string
        insert: the typeql insert string
    """
    match = ""
    insert = ""
    delete = ""
    logger.debug("I'm in embedded")
    auth_factory = get_auth_factory_instance()
    auth = auth_factory.get_auth_for_import(import_type)
    for ex in auth["reln"]["embedded_relations"]:
        if ex["rel"] == term:
            owner = ex["owner"]
            pointed_to = ex["pointed-to"]
            relation = ex["typeql"]
            rel_var = "$" + relation + str(inc)
            # its  an embedded relation
            if op_type == "add":
                insert += rel_var + ' (' + owner + ':' + obj_var
                insert += ', ' + pointed_to + ':' + source_var
                insert += ') isa ' + relation + ';\n'
            elif op_type == "change":
                if isinstance(value, dict):
                    source_id = value["old_value"]
                    new_id = value["new_value"]
                    new_var, match2 = get_embedded_match(new_id, import_type=import_type, i=inc, protocol=protocol)
                    match += match2
                    match += rel_var + ' (' + owner + ':' + obj_var
                    match += ', ' + pointed_to + ':' + source_var
                    match += ') isa ' + relation + ';\n'
                    delete += rel_var + " ( " + pointed_to + ':' + source_var + ");"
                    insert += rel_var + ' (' + pointed_to + ':' + new_var + ");"
            elif op_type == "remove":
                match += rel_var + ' (' + owner + ':' + obj_var
                match += ', ' + pointed_to + ':' + source_var
                match += ') isa ' + relation + ';\n'
                delete += rel_var + " isa " + relation + ";"

    return match, insert, delete, op_type

# ---------------------------------------------------
# 1.7) Helper Methods for
#           - converting a Python value --> typeql string
#           - splitting a list of total properties into properties and relations
# ---------------------------------------------------


def val_tql(val):
    """
        Modify the value used in a typeql statement, depending on its type
    Args:
        val (): the value being used

    Returns:
        val: the value formatted for typeql
    """
    if isinstance(val, str):
        replaced_val = val.replace('"', "'")
        replaced_val2 = replaced_val.replace('\\', '\\\\')
        return '"' + replaced_val2 + '"'
    elif isinstance(val, bool):
        return str(val).lower()
    elif isinstance(val, int):
        return str(val)
    elif isinstance(val, float):
        return str(val)
    elif isinstance(val, datetime.datetime):
        return str(val.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3])
    else:
        return logger.error(f'value  not supported: {val}')


def split_on_activity_type(total_props: dict, obj_tql: Dict[str, str]) -> [List[str], List[str]]:
    """
        Split the Stix object properties into flat properties and sub objects
    Args:
        total_props (): the total properties for this object
        obj_tql (): the mapping dict for this object

    Returns:
        prop_list, a list of the flat properties
        rel_list, a list of the sub objects
    """
    prop_list = []
    rel_list = []
    logger.debug("@@@@@@@@@@@@@@@@@@@@@@ splitting @@@@@@@@@@@@@@@")
    logger.debug("========================================")
    logger.debug(f'total props: {total_props}')
    # for k, v in total_props.items():
    #     logger.debug(k, v)
    # logger.debug("=========================================")
    logger.debug("========================================")
    logger.debug(f'obj tql: {obj_tql}')
    # for k, v in obj_tql.items():
    #     logger.debug(k, v)
    # logger.debug("=========================================")
    logger.debug("@@@@@@@@@@@@@@@@@@@@@@ end splitting @@@@@@@@@@@@@@@")
    for prop in total_props:
        tql_prop_name = obj_tql[prop]
        logger.debug(f'prop {prop}, object tql -> {tql_prop_name}')

        if tql_prop_name == "":
            rel_list.append(prop)
            # logger.debug(f'Im a rel --> {prop},        tql --> {tql_prop_name}')
        else:
            prop_list.append(prop)
            # logger.debug(f'Im a prop --> {prop},        tql --> {tql_prop_name}')

    return prop_list, rel_list

###################################################################################################