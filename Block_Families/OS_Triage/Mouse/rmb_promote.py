################################################################################
## header start                                                               ##
################################################################################
# allow importing og service local packages
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
# Title: Right Mouse Button Promote Subgraph
# Author: OS-Threat
# Organisation Repo: https://github.com/typerefinery-ai/brett_blocks
# Contact Email: brett@osthreat.com
# Date: 29/10/2025
#
# Description: This script is designed to promote a subgraph from unattached 
#       context memory to incident context memory. It finds a promotable object
#       type in unattached context, collects its connected subgraph, removes
#       it from unattached context, and saves it to incident context.
#
# One Mandatory Input:
# 1. Object Type to promote
# One Output
# 1. Promotion result message
#
# This code is licensed under the terms of the Apache 2.
##############################################################################

from stixorm.module.authorise import import_type_factory
from urllib.request import urlretrieve
import json
import sys
import importlib.util
import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
import os
import_type = import_type_factory.get_all_imports()

# Common File Stuff
TR_Common_Files = "./generated/os-triage/common_files"
common = [
    {"module": "convert_n_and_e", "file": "convert_n_and_e.py", "url" : "https://raw.githubusercontent.com/typerefinery-ai/brett_blocks/main/Block_Families/General/_library/convert_n_and_e.py"}
]

# OS_Triage Memory Stuff
TR_Context_Memory_Dir = "./generated/os-triage/context_mem"
context_map = "context_map.json"

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

# Promotable object types as defined in the governance process
promotable_object_types = [
    "sighting",
    "task",
    "event", 
    "impact",
    "x-oca-behavior",
    "attack-flow"
]

def download_common(module_list):
    """Download common utility modules if they don't exist"""
    for module in module_list:
        # Step 1: download the module
        result = urlretrieve(module["url"], TR_Common_Files + "/" + module["file"])
        print(f'common file result ->', result)

def add_node(node, context_dir, context_type):
    """Add a node to the specified context file"""
    exists = False
    stix_nodes_list = []
    if os.path.exists(context_dir + incident_data[context_type]):
        with open(context_dir + incident_data[context_type], "r") as mem_input:
            stix_nodes_list = json.load(mem_input)
            for i in range(len(stix_nodes_list)):
                if stix_nodes_list[i]["id"] == node["id"]:
                    stix_nodes_list[i] = node
                    exists = True
            if not exists:
                stix_nodes_list.append(node)
    else:
        stix_nodes_list = [node]
    with open(context_dir + incident_data[context_type], 'w') as f:
        f.write(json.dumps(stix_nodes_list))

def add_edge(edge, context_dir, context_type):
    """Add an edge to the specified context file"""
    exists = False
    stix_edge_list = []
    if os.path.exists(context_dir + incident_data[context_type]):
        with open(context_dir + incident_data[context_type], "r") as mem_input:
            stix_edge_list = json.load(mem_input)
            for i in range(len(stix_edge_list)):
                if stix_edge_list[i]["source"] == edge["source"] and stix_edge_list[i]["target"] == edge["target"]:
                    stix_edge_list[i] = edge
                    exists = True
            if not exists:
                stix_edge_list.append(edge)
    else:
        stix_edge_list = [edge]
    with open(context_dir + incident_data[context_type], 'w') as f:
        f.write(json.dumps(stix_edge_list))

def register_id(id, field, TR_Incident_Context_Dir):
    """Register an ID in the incident object's reference lists"""
    incident_list = []
    with open(TR_Incident_Context_Dir + incident_data["incident"], "r") as incident_object:
        incident_list = json.load(incident_object)
        wrapped_incident = incident_list[0]
        incident = wrapped_incident["original"]
        incident_ext = incident["extensions"]["extension-definition--ef765651-680c-498d-9894-99799f2fa126"]
        # check whether field exists first
        if field_names[field] in incident_ext:
            id_list = incident_ext[field_names[field]]
            if id not in id_list:
                id_list.append(id)
        else:
            id_list = []
            id_list.append(id)
            incident_ext[field_names[field]] = id_list

    with open(TR_Incident_Context_Dir + incident_data["incident"], 'w') as f:
        f.write(json.dumps(incident_list))

def save_object_to_incident_context(stix_object, TR_Incident_Context_Dir, n_and_e):
    """Save a single STIX object to incident context using the exact method from save_incident_context.py"""
    wrapped = False
    if "original" in stix_object:
        wrapped = True
    
    if stix_object["type"] == "relationship":
        if wrapped:
            add_node(stix_object, TR_Incident_Context_Dir, "relations")
            register_id(stix_object["id"], "other", TR_Incident_Context_Dir)
        else:
            nodes, edges, relation_edges, relation_replacement_edges = n_and_e.convert_relns(stix_object)
            add_node(nodes[0], TR_Incident_Context_Dir, "relations")
            register_id(stix_object["id"], "other", TR_Incident_Context_Dir)
            for edge in edges:
                add_edge(edge, TR_Incident_Context_Dir, "edges")
            for edge in relation_edges:
                add_edge(edge, TR_Incident_Context_Dir, "relation_edges")
            for edge in relation_replacement_edges:
                add_edge(edge, TR_Incident_Context_Dir, "relation_replacement_edges")

    elif stix_object["type"] == "sighting":
        if wrapped:
            add_node(stix_object, TR_Incident_Context_Dir, "other")
            register_id(stix_object["id"], "other", TR_Incident_Context_Dir)
        else:
            nodes, edges = n_and_e.convert_sighting(stix_object)
            add_node(nodes[0], TR_Incident_Context_Dir, "other")
            register_id(stix_object["id"], "other", TR_Incident_Context_Dir)
            for edge in edges:
                add_edge(edge, TR_Incident_Context_Dir, "edges")
    else:
        # its a node-type of object
        if stix_object["type"] == "sequence":
            if stix_object.get("step_type") == "start_step":
                if wrapped:
                    add_node(stix_object, TR_Incident_Context_Dir, "start")
                    register_id(stix_object["id"], "start", TR_Incident_Context_Dir)
                else:
                    nodes, edges = n_and_e.convert_node(stix_object)
                    add_node(nodes[0], TR_Incident_Context_Dir, "start")
                    register_id(stix_object["id"], "start", TR_Incident_Context_Dir)
                    for edge in edges:
                        add_edge(edge, TR_Incident_Context_Dir, "edges")
            else:
                if wrapped:
                    add_node(stix_object, TR_Incident_Context_Dir, "sequence")
                    register_id(stix_object["id"], "sequence", TR_Incident_Context_Dir)
                else:
                    nodes, edges = n_and_e.convert_node(stix_object)
                    add_node(nodes[0], TR_Incident_Context_Dir, "sequence")
                    register_id(stix_object["id"], "sequence", TR_Incident_Context_Dir)
                    for edge in edges:
                        add_edge(edge, TR_Incident_Context_Dir, "edges")
        elif stix_object["type"] == "task":
            if wrapped:
                add_node(stix_object, TR_Incident_Context_Dir, "task")
                register_id(stix_object["id"], "task", TR_Incident_Context_Dir)
            else:
                nodes, edges = n_and_e.convert_node(stix_object)
                add_node(nodes[0], TR_Incident_Context_Dir, "task")
                register_id(stix_object["id"], "task", TR_Incident_Context_Dir)
                for edge in edges:
                    add_edge(edge, TR_Incident_Context_Dir, "edges")
        elif stix_object["type"] == "event":
            if wrapped:
                add_node(stix_object, TR_Incident_Context_Dir, "event")
                register_id(stix_object["id"], "event", TR_Incident_Context_Dir)
            else:
                nodes, edges = n_and_e.convert_node(stix_object)
                add_node(nodes[0], TR_Incident_Context_Dir, "event")
                register_id(stix_object["id"], "event", TR_Incident_Context_Dir)
                for edge in edges:
                    add_edge(edge, TR_Incident_Context_Dir, "edges")
        elif stix_object["type"] == "impact":
            if wrapped:
                add_node(stix_object, TR_Incident_Context_Dir, "impact")
                register_id(stix_object["id"], "impact", TR_Incident_Context_Dir)
            else:
                nodes, edges = n_and_e.convert_node(stix_object)
                add_node(nodes[0], TR_Incident_Context_Dir, "impact")
                register_id(stix_object["id"], "impact", TR_Incident_Context_Dir)
                for edge in edges:
                    add_edge(edge, TR_Incident_Context_Dir, "edges")
        elif stix_object["type"] in ["x-oca-behavior", "attack-flow"]:
            if wrapped:
                add_node(stix_object, TR_Incident_Context_Dir, "behavior")
                register_id(stix_object["id"], "other", TR_Incident_Context_Dir)
            else:
                nodes, edges = n_and_e.convert_node(stix_object)
                add_node(nodes[0], TR_Incident_Context_Dir, "behavior")
                register_id(stix_object["id"], "other", TR_Incident_Context_Dir)
                for edge in edges:
                    add_edge(edge, TR_Incident_Context_Dir, "edges")
        else:
            # All other object types go to "other"
            if wrapped:
                add_node(stix_object, TR_Incident_Context_Dir, "other")
                register_id(stix_object["id"], "other", TR_Incident_Context_Dir)
            else:
                nodes, edges = n_and_e.convert_node(stix_object)
                add_node(nodes[0], TR_Incident_Context_Dir, "other")
                register_id(stix_object["id"], "other", TR_Incident_Context_Dir)
                for edge in edges:
                    add_edge(edge, TR_Incident_Context_Dir, "edges")

def collect_subgraph_for_object(target_object, unattached_objects):
    """Collect the complete subgraph for a target object based on its type"""
    subgraph = []
    subgraph_ids = set()
    
    # Add the target object to subgraph
    subgraph.append(target_object)
    subgraph_ids.add(target_object["id"])
    
    object_type = target_object["type"]
    
    if object_type == "sighting":
        # For sighting: collect observed-data and sighting_of (indicator) references
        if "original" in target_object:
            original = target_object["original"]
            
            # Collect observed-data objects
            obs_refs = original.get("observed_data_refs", [])
            for obs_id in obs_refs:
                for obj in unattached_objects:
                    if obj["id"] == obs_id and obj["id"] not in subgraph_ids:
                        subgraph.append(obj)
                        subgraph_ids.add(obj["id"])
                        
                        # If this is observed-data, collect its object_refs
                        if obj["type"] == "observed-data" and "original" in obj:
                            obj_refs = obj["original"].get("object_refs", [])
                            for ref_id in obj_refs:
                                for ref_obj in unattached_objects:
                                    if ref_obj["id"] == ref_id and ref_obj["id"] not in subgraph_ids:
                                        subgraph.append(ref_obj)
                                        subgraph_ids.add(ref_obj["id"])
            
            # Collect sighting_of reference (indicator)
            indicator_ref = original.get("sighting_of_ref")
            if indicator_ref:
                for obj in unattached_objects:
                    if obj["id"] == indicator_ref and obj["id"] not in subgraph_ids:
                        subgraph.append(obj)
                        subgraph_ids.add(obj["id"])
                        
    elif object_type in ["task", "event", "impact", "x-oca-behavior", "attack-flow"]:
        # For these types, collect directly connected objects
        # This is a simplified approach - in practice you might want more sophisticated graph traversal
        if "original" in target_object:
            original = target_object["original"]
            
            # Collect any reference fields that point to other objects
            for key, value in original.items():
                if key.endswith("_ref") and isinstance(value, str):
                    # Single reference
                    for obj in unattached_objects:
                        if obj["id"] == value and obj["id"] not in subgraph_ids:
                            subgraph.append(obj)
                            subgraph_ids.add(obj["id"])
                elif key.endswith("_refs") and isinstance(value, list):
                    # Multiple references
                    for ref_id in value:
                        for obj in unattached_objects:
                            if obj["id"] == ref_id and obj["id"] not in subgraph_ids:
                                subgraph.append(obj)
                                subgraph_ids.add(obj["id"])
    
    return subgraph

def remove_objects_from_unattached(objects_to_remove, TR_Incident_Context_Dir):
    """Remove specified objects from unattached context memory"""
    unattached_file = TR_Incident_Context_Dir + incident_data["unattached"]
    
    if not os.path.exists(unattached_file):
        return []
    
    # Load current unattached objects
    with open(unattached_file, "r") as f:
        unattached_objects = json.load(f)
    
    # Get IDs to remove
    ids_to_remove = {obj["id"] for obj in objects_to_remove}
    
    # Filter out the objects to remove
    remaining_objects = [obj for obj in unattached_objects if obj["id"] not in ids_to_remove]
    
    # Save the updated unattached list
    with open(unattached_file, 'w') as f:
        json.dump(remaining_objects, f)
    
    return remaining_objects

def promote_subgraph(object_type_to_promote):
    """Main function to promote a subgraph from unattached to incident context"""
    
    # Validate that the object type is promotable
    if object_type_to_promote not in promotable_object_types:
        return f"Error: Object type '{object_type_to_promote}' is not promotable. Valid types: {promotable_object_types}"
    
    # Find Current Incident directory
    local_map = {}
    with open(TR_Context_Memory_Dir + "/" + context_map, "r") as current_context:
        local_map = json.load(current_context)
        current_incident_dir = local_map["current_incident"]
        TR_Incident_Context_Dir = TR_Context_Memory_Dir + "/" + current_incident_dir

        # Check if the key directories exist, if not make them, and download common files
        if not os.path.exists(TR_Common_Files):
            os.makedirs(TR_Common_Files)
            download_common(common)
        if not os.path.exists(TR_Context_Memory_Dir):
            os.makedirs(TR_Context_Memory_Dir)

        # Import the convert_n_and_e module
        module_path = TR_Common_Files + '/' + common[0]["file"]
        spec = importlib.util.spec_from_file_location('n_and_e', module_path)
        n_and_e = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(n_and_e)

        # Load unattached context memory
        unattached_file = TR_Incident_Context_Dir + incident_data["unattached"]
        if not os.path.exists(unattached_file):
            return f"No unattached context found for incident {current_incident_dir}"

        with open(unattached_file, "r") as f:
            unattached_objects = json.load(f)

        # Find the first object of the specified type
        target_object = None
        for obj in unattached_objects:
            if obj["type"] == object_type_to_promote:
                target_object = obj
                break

        if not target_object:
            return f"No object of type '{object_type_to_promote}' found in unattached context"

        # Collect the complete subgraph for this object
        subgraph = collect_subgraph_for_object(target_object, unattached_objects)
        
        # Remove the subgraph objects from unattached context
        remaining_unattached = remove_objects_from_unattached(subgraph, TR_Incident_Context_Dir)
        
        # Save each object in the subgraph to incident context using the exact method
        promoted_count = 0
        for stix_object in subgraph:
            save_object_to_incident_context(stix_object, TR_Incident_Context_Dir, n_and_e)
            promoted_count += 1

        subgraph_ids = [obj["id"] for obj in subgraph]
        
        return {
            "promotion_result": f"Successfully promoted {promoted_count} objects of subgraph starting with {object_type_to_promote}",
            "promoted_objects": subgraph_ids,
            "remaining_unattached_count": len(remaining_unattached),
            "target_object_id": target_object["id"]
        }

def main(inputfile, outputfile):
    """Main function with standard block interface"""
    
    if os.path.exists(inputfile):
        with open(inputfile, "r") as script_input:
            input_data = json.load(script_input)
            print(f"input data->{input_data}")
            
            object_type_to_promote = None
            
            if "object_type" in input_data:
                object_type_to_promote = input_data["object_type"]
            elif "api" in input_data:
                api_input_data = input_data["api"]
                if "object_type" in api_input_data:
                    object_type_to_promote = api_input_data["object_type"]
            
            if not object_type_to_promote:
                result = {"error": "No object_type specified in input"}
            else:
                print(f"Promoting object type: {object_type_to_promote}")
                result = promote_subgraph(object_type_to_promote)

            with open(outputfile, "w") as outfile:
                json.dump(result, outfile)
    else:
        result = {"error": f"Input file {inputfile} not found"}
        with open(outputfile, "w") as outfile:
            json.dump(result, outfile)

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