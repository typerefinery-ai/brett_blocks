
################################################################################
## header start                                                               ##
################################################################################
# allow importing og service local packages
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
# Title: Move "Unattached" to "Other" Context Memory
# Author: OS-Threat
# Organisation Repo: https://github.com/typerefinery-ai/brett_blocks
# Contact Email: denis@cloudaccelerator.co
# Date: 07/08/2023
#
# Description: This script is designed to take in a Stix Object ID
#       and return a Stix object
#
# One Mandatory Input:
# 1. Stix_list
# One Outpute
# 1. Context Return
#
# This code is licensed under the terms of the BSD.
##############################################################################

from stixorm.module.definitions.os_threat import (
    StateChangeObject, EventCoreExt, Event, ImpactCoreExt,
    Availability, Confidentiality, External, Integrity, Monetary, Physical,
    Traceability, Impact, IncidentScoreObject, IncidentCoreExt, TaskCoreExt,
    Task, SightingEvidence, Sequence, SequenceExt, ContactNumber, EmailContact,
    SocialMediaContact, IdentityContact, AnecdoteExt, Anecdote,
    SightingAnecdote, SightingAlert, SightingContext, SightingExclusion,
    SightingEnrichment, SightingHunt, SightingFramework, SightingExternal
)
from stixorm.module.authorise import authorised_mappings, import_type_factory
import copy
from posixpath import basename
import json
import os

import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

import_type = import_type_factory.get_all_imports()

TR_Context_Memory_Dir = "./Context_Mem"
local = {
    "me" : "/cache_me.json",
    "team" : "/cache_team.json",
    "users": "/company_1/cache_users.json",
    "company" : "/company_1/cache_company.json",
    "assets" : "/company_1/cache_assets.json",
    "systems" : "/company_1/cache_systems.json",
    "relations" : "/company_1/cache_relations.json"
}
refs = {
    "incident" : "/incident_1/incident.json",
    "start" : "/incident_1/sequence_start_refs.json",
    "sequence" : "/incident_1/sequence_refs.json",
    "impact" : "/incident_1/impact_refs.json",
    "event" : "/incident_1/event_refs.json",
    "task" : "/incident_1/task_refs.json",
    "other" : "/incident_1/other_object_refs.json",
    "unattached" : "/incident_1/unattached_objs.json"
}
key_list = ["start", "sequence", "impact", "event", "task", "other"]


######################################################################################
#
# Setup Nodes and Edges Array Stuff for Force Graph Display - including icons
#
########################################################################################


def make_nodes_and_edges(obj_list):
    nodes_edges = {}
    nodes = []
    edges = []
    for obj in obj_list:
        if obj["type"] == "relationship":
            edges = setup_relationship(obj, edges)
        elif obj["type"] == "sighting":
            nodes, edges = setup_sighting(obj, nodes, edges)
        else:
            nodes, edges = setup_nodes(obj, nodes, edges)
    check_icons = []
    legend = []
    node_ids = []
    for node in nodes:
        node_ids.append(node["id"])
        if node["icon"] not in check_icons:
            check_icons.append(node["icon"])
            layer = {}
            layer["icon"] = node["icon"]
            layer["label"] = node["label"]
            legend.append(layer)
    # remove any edges without nodes
    edges = [x for x in edges if (x["source"] in node_ids and x["target"] in node_ids)]
    nodes_edges["nodes"] = nodes
    nodes_edges["edges"] = edges
    nodes_edges["legend"] = legend
    return nodes_edges


def setup_relationship(obj, edges):
    edge = {}
    edge["id"] = obj["id"]
    edge["type"] = "relationship"
    edge["label"] = obj["relationship_type"]
    edge["source"] = obj["source_ref"]
    edge["target"] = obj["target_ref"]
    edges.append(edge)
    return edges


def setup_sighting(obj, nodes, edges):
    # sighting_of_ref
    print(f"==== {obj['id']}")
    edge = {}
    edge["id"] = obj["id"]
    edge["type"] = "sighting"
    edge["label"] = "Sighting of " + obj["sighting_of_ref"].split('--')[0]
    edge["source"] = obj["id"]
    edge["target"] = obj["sighting_of_ref"]
    edges.append(edge)
    # list of observed_data_refs
    for obs in obj["observed_data_refs"]:
        edge = {}
        edge["id"] = obj["id"]
        edge["type"] = "sighting"
        edge["label"] = "Observed Data"
        edge["source"] = obj["id"]
        edge["target"] = obs
        edges.append(edge)
    # list of where_sighted_refs
    if "where_sighted_refs" in obj:
        for where in obj["where_sighted_refs"]:
            edge = {}
            edge["id"] = obj["id"]
            edge["type"] = "sighting"
            edge["label"] = "Where Sighted " + where.split('--')[0]
            edge["source"] = obj["id"]
            edge["target"] = where
            edges.append(edge)
    # sort out node
    node = {}
    node["id"] = obj["id"]
    node["original"] = copy.deepcopy(obj)
    node["label"] = "Sighting"
    if "extensions" in obj:
        for key, value in obj["extensions"].items():
            if key == "extension-definition--0d76d6d9-16ca-43fd-bd41-4f800ba8fc43":
                continue
            else:
                node["icon"] = key
    else:
        node["icon"] = "sighting"

    nodes.append(node)
    return nodes, edges

def setup_nodes(obj, nodes, edges):
    obj_id = obj["id"]
    node = {}
    node["id"] = obj_id
    node["original"] = copy.deepcopy(obj)
    edges = find_embedded(obj, edges, obj_id)
    node = find_icon(obj, node)
    nodes.append(node)
    return nodes, edges


def find_embedded(obj, edges, obj_id):
    auth = authorised_mappings(import_type)
    for key, prop in obj.items():
        if key == "id":
            continue
        elif key in auth["reln_name"]["embedded_relations"]:
            edges = extract_ids(key, prop, edges, obj_id)
        elif isinstance(prop, list):
            edges = embedded_list(key, prop, edges, obj_id)
        elif isinstance(prop, dict):
            edges = find_embedded(prop, edges, obj_id)
        else:
            continue
    return edges


def embedded_list(key, prop, edges, obj_id):
    logger.debug(f"embedded_list {key} {prop}")
    for pro in prop:
        if isinstance(pro, dict):
            edges = find_embedded(pro, edges, obj_id)
        else:
            continue
    return edges


def extract_ids(key, prop, edges, obj_id):
    auth = authorised_mappings(import_type)
    for ex in auth["reln"]["embedded_relations"]:
        if ex["rel"] == key:
            label = ex["label"]
            source_owner = ex["owner-is-source"]
    edge = {"label": label, "type": "embedded"}
    if isinstance(prop, list):
        for pro in prop:
            if pro.split('--')[0] == "relationship":
                continue
            elif source_owner:
                edge["source"] = obj_id
                edge["target"] = pro
                edges.append(copy.deepcopy(edge))
            else:
                edge["source"] = pro
                edge["target"] = obj_id
                edges.append(copy.deepcopy(edge))
    else:
        if source_owner:
            edge["source"] = obj_id
            edge["target"] = prop
        else:
            edge["source"] = prop
            edge["target"] = obj_id
        edges.append(copy.deepcopy(edge))
    return edges


def find_icon(stix_object, node):
    auth = authorised_mappings(import_type)
    logger.debug(f'stix object type {stix_object["type"]}\n')
    label = ""
    icon = ""
    auth_types = copy.deepcopy(auth["types"])
    if stix_object["type"] in auth_types["sdo"]:
        logger.debug(f' going into sdo ---? {stix_object}')
        icon, label = sdo_icon(stix_object)
    elif stix_object["type"] in auth_types["sco"]:
        logger.debug(f' going into sco ---> {stix_object}')
        icon, label = sco_icon(stix_object)
    elif stix_object["type"] in auth_types["sro"]:
        logger.debug(f' going into sro ---> {stix_object}')
        icon, label = sro_icon(stix_object)
    elif stix_object["type"] == 'marking-definition':
        icon, label = meta_icon(stix_object)
    else:
        logger.error(f'object type not supported: {stix_object.type}, import type {import_type}')
    node["icon"] = icon
    node["label"] = label
    return node


def sdo_icon(stix_object):
    sdo_type = stix_object["type"]
    label = sdo_type
    icon_type = ""
    attack_type = ""
    attack_object = False if not stix_object.get("x_mitre_version", False) else True
    if attack_object:
        sub_technique = False if not stix_object.get("x_mitre_is_subtechnique", False) else True
        if sdo_type[:7] == "x-mitre":
            attack_type = sdo_type[8:]
        elif sdo_type == "attack-pattern":
            attack_type = "technique"
            if sub_technique:
                attack_type = "subtechnique"
        elif sdo_type == "course-of-action":
            attack_type = "mitigation"
        elif sdo_type == "intrusion-set":
            attack_type = "group"
        elif sdo_type == "malware" or sdo_type == "tool":
            attack_type = "software"
        elif sdo_type == "campaign":
            attack_type = "campaign"
        else:
            attack_type = "unknown"

        if "attack-" in attack_type:
            pass
        else:
            attack_type = "attack-" + attack_type
        icon_type = attack_type
        label = attack_type
    else:
        if sdo_type == "identity":
            if "extensions" in stix_object:
                icon_type = "identity-contact"
            else:
                if stix_object.get("identity_class", False):
                    if stix_object["identity_class"] == "individual":
                        icon_type = "identity-individual"
                    elif stix_object["identity_class"] == "organization":
                        icon_type = "identity-organization"
                    elif stix_object["identity_class"] == "class":
                        icon_type = "identity-class"
                    elif stix_object["identity_class"] == "system":
                        icon_type = "identity-system"
                    elif stix_object["identity_class"] == "group":
                        icon_type = "identity-group"
                    else:
                        icon_type = "identity-unknown"
                else:
                    icon_type = "identity-unknown"

        elif sdo_type == "malware":
            if stix_object.get("is_family", False):
                icon_type = "malware-family"
            else:
                icon_type = "malware"
        elif sdo_type == "impact":
            if "extensions" in stix_object:
                for key, value in stix_object["extensions"].items():
                    if key == "extension-definition--7cc33dd6-f6a1-489b-98ea-522d351d71b9":
                        continue
                    else:
                        icon_type = "impact-" + key
            else:
                icon_type = "impact"
        elif sdo_type == "incident":
            if "extensions" in stix_object:
                icon_type = "incident-ext"
                label = "extended incident"
            else:
                icon_type = "incident"
        elif sdo_type == "sequence":
            if stix_object["step_type"] == "start_step" or stix_object["step_type"] == "end_step":
                icon_type = "step-terminal"
                label = stix_object["step_type"].replace("_", " ")
            elif stix_object["step_type"] == "single_step":
                if "on_completion" in stix_object:
                    icon_type = "step-single"
                    label = stix_object["step_type"].replace("_", " ")
                elif "on_success" in stix_object:
                    icon_type = "step-xor"
                    label = stix_object["step_type"].replace("_", " ")
                else:
                    icon_type = "step-single"
                    label = stix_object["step_type"].replace("_", " ")
            else:
                icon_type = "step-parallel"
                label = stix_object["step_type"].replace("_", " ")
        else:
            icon_type = sdo_type
    return icon_type, label


def sco_icon(stix_object):
    sco_type = stix_object["type"]
    label = stix_object.get("name", "")
    if sco_type == "email-message":
        if stix_object.get("is_multipart", False):
            icon_type = "email-message-mime"
            label = stix_object.get("subject", "")
        else:
            icon_type = "email-message"
            label = stix_object.get("subject", "")
    elif sco_type == "file":
        if "extensions" in stix_object:
            if stix_object["extensions"].get("archive-ext", False):
                icon_type = "file-archive"
                label = stix_object.get("name", "")
            elif stix_object["extensions"].get("pdf-ext", False):
                icon_type = "file-pdf"
                label = stix_object.get("name", "")
            elif stix_object["extensions"].get("raster-image-ext", False):
                icon_type = "file-img"
                label = stix_object.get("name", "")
            elif stix_object["extensions"].get("windows-pebinary-ext", False):
                icon_type = "file-bin"
                label = stix_object.get("name", "")
            elif stix_object["extensions"].get("ntfs-ext", False):
                icon_type = "file-ntfs"
                label = stix_object.get("name", "")
            else:
                icon_type = "file"
                label = stix_object.get("name", "")
        else:
            icon_type = "file"
            label = stix_object.get("name", "")
    elif sco_type == "network-traffic":
        if "extensions" in stix_object:
            if stix_object["extensions"].get("http-request-ext", False):
                icon_type = "network-traffic-http"
                label = "http-request"
            elif stix_object["extensions"].get("icmp-ext", False):
                icon_type = "network-traffic-icmp"
                label = "icmp"
            elif stix_object["extensions"].get("tcp-ext", False):
                icon_type = "network-traffic-tcp"
                label = "tcp"
            elif stix_object["extensions"].get("sock-ext", False):
                icon_type = "network-traffic-sock"
                label = "socket"
            else:
                icon_type = "network-traffic"
                for prot in stix_object["protocols"]:
                    label += prot + ", "
        else:
            icon_type = "network-traffic"
            for prot in stix_object["protocols"]:
                label += prot + ", "
    elif sco_type == "user-account":
        if "extensions" in stix_object:
            if stix_object["extensions"].get("unix-account-ext", False):
                icon_type = "user-account-unix"
                label = "unix-account"
            else:
                icon_type = "user-account"
                label = "standard-account"
        else:
            icon_type = "user-account"
            label = "standard-account"
    else:
        icon_type = sco_type
        if sco_type == "artifact":
            label = stix_object.get("mime_type", "")
        elif sco_type == "directory":
            label = stix_object.get("path", "")
        elif sco_type in ["domain-name", "email-addr", "ipv4-addr", "ipv6-addr", "mac-addr", "mutex", "url", "anecdote"]:
            label = stix_object.get("value", "")
        elif sco_type == "process":
            if "extensions" in stix_object:
                if stix_object["extensions"].get("windows-process-ext", False):
                    label = "windows process"
                elif stix_object["extensions"].get("windows-service-ext", False):
                    label = "windows service"
                else:
                    label = "standard process"
            else:
                label = "standard process"
        elif sco_type == "windows-registry-key":
            label = stix_object.get("key", "")
        elif sco_type == "x509-certificate":
            label = stix_object.get("serial_number", "")
    if icon_type == "domain-name":
        icon_type = "domain"
    return icon_type, label


def sro_icon(stix_object):
    sro_type = stix_object["type"]
    if sro_type == "sighting":
        icon_type = "sighting"
        label = "sighting"
    else:
        icon_type = "relationship"
        label = stix_object.get("retlationship_type", "relationship")
    return icon_type, label


def meta_icon(stix_object):
    return "marking", stix_object.get("definition_type", "")




def main(inputfile, outputfile):
    n_and_e = None
    if os.path.exists(inputfile):
        with open(inputfile, "r") as script_input:
            input = json.load(script_input)
    if "n_and_e" in input:
        n_and_e = input["n_and_e"]

    # setup logger for execution
    nodes_and_edges = make_nodes_and_edges(n_and_e)
    context_result = {}
    context_result["n_and_e"] = nodes_and_edges

    with open(outputfile, "w") as outfile:
        json.dump(context_result, outfile)


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