
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
# Title: When any tab is selected, get all of the unattached
# Author: OS-Threat
# Organisation Repo: https://github.com/typerefinery-ai/brett_blocks
# Contact Email: brett@osthreat.com
# Date: 07/08/2023
#
# Description: This script is designed to take in a Stix Object ID
#       and return a Stix object
#
# No Input:
# 1.
# One Output
# 1. Unattached nodes and edges
#
# This code is licensed under the terms of the Apache 2.
##############################################################################

from stixorm.module.authorise import import_type_factory
import json
from typing import Dict, Union, List

import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

import_type = import_type_factory.get_all_imports()


# Common File Stuff
TR_Common_Files = "./generated/os-triage/common_files"
common = [
    {"module": "parse", "file": "parse.py", "url" : "https://raw.githubusercontent.com/typerefinery-ai/brett_blocks/refs/heads/main/Block_Families/General/_library/parse.py"}
]
# OS_Triage Memory Stuff
TR_Context_Memory_Dir = "./generated/os-triage/context_mem"
TR_User_Dir = "/usr"
context_map = "context_map.json"
user_data = {
    "global": "/global_variables_dict.json",
    "me": "/cache_me.json",
    "team": "/cache_team.json"
}
comp_data = {
    "users": "/users.json",
    "company" : "/company.json",
    "platforms" : "/platforms.json",
    "systems" : "/systems.json"
}
incident_data = {
    "incident" : "/incident.json",
    "start" : "/sequence_start_refs.json",
    "sequence" : "/sequence_refs.json",
    "impact" : "/impact_refs.json",
    "event" : "/event_refs.json",
    "task" : "/task_refs.json",
    "other" : "/other_object_refs.json",
    "unattached" : "/unattached_objs.json"
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

#============================================================================

from collections import deque

# If Incident Management, then check for these promotoables
prom_types = [
	'incident',
	'task',
	'impact',
	'event',
	'sighting',
	'attack-flow',
	'x-oca-behavior'
]

# Priority order for promotable types (higher priority = lower index)
prom_priority = {
	'incident': 0,
	'event': 1,
	'sighting': 2,
	'task': 3,
	'impact': 4,
	'attack-flow': 5,
	'x-oca-behavior': 6
}

# setup layout types for each object

level1_layouts = {
	'incident': [
		{"label": "Event List", "field": "event_refs", "datatype": "list"},
		{"label": "Impact List", "field": "impact_refs", "datatype": "list"},
		{"label": "Task List", "field": "task_refs", "datatype": "list"},
		{"label": "Sequence Start", "field": "sequence_start_refs", "datatype": "list"},
		{"label": "Sequences", "field": "sequence_refs", "datatype": "list"},
		{"label": "Other Objects", "field": "other_object_refs", "datatype": "list"},
	],
}

level2_layouts = {
	'sighting': [
		{"label": "What Sighted", "field": "sighting_of_ref", "datatype": "value"},
		{"label": "Data Observed", "field": "observed_data_refs", "datatype": "list"},
		{"label": "Where Sighted", "field": "where_sighted_refs", "datatype": "list"},
		{"label": "Recorded By", "field": "created_by_ref", "datatype": "value"},
	],
	'task': [
		{"label": "What Changed", "field": "changed_objects", "datatype": "list"},
		{"label": "Owned By", "field": "owner", "datatype": "value"},
		{"label": "Recorded By", "field": "created_by_ref", "datatype": "value"},
	],
	'event': [
		{"label": "What Changed", "field": "changed_objects", "datatype": "list"},
		{"label": "Sightings Made", "field": "sighting_refs", "datatype": "list"},
		{"label": "Recorded By", "field": "created_by_ref", "datatype": "value"},
	],
	'impact': [
		{"label": "What Impacted", "field": "impacted_refs", "datatype": "list"},
		{"label": "Superseded By", "field": "superseded_by_ref", "datatype": "value"},
		{"label": "Recorded By", "field": "created_by_ref", "datatype": "value"},
	],
}


class AdjacencyGraph:
	"""
	Manages bidirectional graph traversal for nodes and edges.
	Supports finding all connected components starting from seed nodes.
	"""
	
	def __init__(self, nodes, edges):
		"""
		Initialize the adjacency graph.
		
		Args:
			nodes: List of node dictionaries with 'id' field
			edges: List of edge dictionaries with 'source' and 'target' fields
		"""
		self.nodes_by_id = {node['id']: node for node in nodes}
		self.adjacency = {}  # {node_id: set of connected node_ids}
		self.edges = edges
		self._build_adjacency()
	
	def _build_adjacency(self):
		"""Build bidirectional adjacency list from edges"""
		# Initialize adjacency dict with empty sets
		for node_id in self.nodes_by_id:
			self.adjacency[node_id] = set()
		
		# Add bidirectional connections from edges
		for edge in self.edges:
			source = edge.get('source')
			target = edge.get('target')
			
			if source and target:
				if source in self.adjacency:
					self.adjacency[source].add(target)
				if target in self.adjacency:
					self.adjacency[target].add(source)
	
	def get_connected_component(self, start_id):
		"""
		Find all nodes connected to start_id using BFS.
		
		Args:
			start_id: Starting node ID
			
		Returns:
			Set of all connected node IDs (including start_id)
		"""
		if start_id not in self.nodes_by_id:
			return set()
		
		visited = set()
		queue = deque([start_id])
		visited.add(start_id)
		
		while queue:
			current = queue.popleft()
			
			# Visit all neighbors
			for neighbor in self.adjacency.get(current, []):
				if neighbor not in visited:
					visited.add(neighbor)
					queue.append(neighbor)
		
		return visited
	
	def get_subgraph_edges(self, node_ids):
		"""
		Get all edges that connect nodes within the node_ids set.
		
		Args:
			node_ids: Set of node IDs
			
		Returns:
			List of edges where both source and target are in node_ids
		"""
		node_ids_set = set(node_ids)
		subgraph_edges = []
		
		for edge in self.edges:
			source = edge.get('source')
			target = edge.get('target')
			
			if source in node_ids_set and target in node_ids_set:
				subgraph_edges.append(edge)
		
		return subgraph_edges


def split_subgraphs_by_promotables(data):
	"""
	Split a nodes/edges structure into separate subgraphs,
	each anchored by a promotable type.
	
	Args:
		data: dict with 'nodes' and 'edges' arrays
		
	Returns:
		{
			'promo': {
				'nodes': [...],  # all nodes from subgraphs connected to promotables
				'edges': [...]   # all edges from subgraphs connected to promotables
			},
			'scratch': {
				'nodes': [...],  # nodes not connected to any promotable
				'edges': [...]   # edges not connected to any promotable
			}
		}
	"""
	nodes = data.get('nodes', [])
	edges = data.get('edges', [])
	
	if not nodes:
		return {'promo': {'nodes': [], 'edges': []}, 'scratch': {'nodes': [], 'edges': []}}
	
	# Create adjacency graph
	graph = AdjacencyGraph(nodes, edges)
	
	# Identify all promotable nodes
	promotables = [node for node in nodes if node.get('type') in prom_types]
	
	# Track visited nodes
	visited = set()
	all_promo_nodes = []
	all_promo_edges = []
	
	# Process each promotable node
	for prom_node in promotables:
		prom_id = prom_node['id']
		
		if prom_id in visited:
			continue
		
		# Find all connected nodes (the component)
		component_ids = graph.get_connected_component(prom_id)
		
		# Mark all as visited
		visited.update(component_ids)
		
		# Get nodes and edges for this component
		component_nodes = [graph.nodes_by_id[nid] for nid in component_ids]
		component_edges = graph.get_subgraph_edges(component_ids)
		
		# Add to promo collections
		all_promo_nodes.extend(component_nodes)
		all_promo_edges.extend(component_edges)
	
	# Find scratch nodes (not visited)
	scratch_node_ids = set(graph.nodes_by_id.keys()) - visited
	scratch_nodes = [graph.nodes_by_id[nid] for nid in scratch_node_ids]
	scratch_edges = graph.get_subgraph_edges(scratch_node_ids)
	
	return {
		'promo': {
			'nodes': all_promo_nodes,
			'edges': all_promo_edges
		},
		'scratch': {
			'nodes': scratch_nodes,
			'edges': scratch_edges
		}
	}

#============================================================================


def create_edge(edge_label, source_id, target_id, edge_type)-> Dict[str, str]:
    edge = {}
    edge["source"] = source_id
    edge["target"] = target_id
    edge["name"] = edge_label.replace("_", "-")
    edge["type"] = edge_type
    return edge

def generate_nodes_and_edges(nodes):
    edges = []
    
    node_ids = [x['id'] for x in nodes]
    print(f"node ids->{node_ids}")
    for node in nodes:
        node_id = node["id"]
        references = node["references"]
        for edge_label, edge_list in references.items():
            for edge_id in edge_list:
                if edge_id in node_ids:
                    if node["type"] == "relationship" and (edge_label == "source_ref" or edge_label == "target_ref"):
                        edges.append(create_edge(node["original"]["relationship_type"], node_id, edge_id, "relationship"))
                    else:
                        edges.append(create_edge(edge_label, node_id, edge_id, "edge"))

    return nodes, edges


def get_unattached():
    show_sro = True
    unattached = {}
    # 1. Setup variables
    nodes = []
    edges = []

    # 1.B Find Current Incident directory
    local_map = {}
    with open(TR_Context_Memory_Dir + "/" + context_map, "r") as current_context:
        local_map = json.load(current_context)
        current_incident_dir = local_map["current_incident"]
        TR_Incident_Context_Dir = TR_Context_Memory_Dir + "/" + current_incident_dir
        # 2. open files and fill lists
        if os.path.exists(TR_Incident_Context_Dir + incident_data["unattached"]):
            with open(TR_Incident_Context_Dir + incident_data["unattached"], "r") as mem_input:
                nodes = json.load(mem_input)        # load unattached nodes list
                nodes, edges = generate_nodes_and_edges(nodes)

    unattached['nodes'] = nodes
    unattached['edges'] = edges
	
    split_unattached = split_subgraphs_by_promotables(unattached)
    return split_unattached


def main(inputfile, outputfile):
    context_type = None
    stix_object = None
    if os.path.exists(inputfile):
        with open(inputfile, "r") as script_input:
            input = json.load(script_input)

    # setup logger for execution
    unattached = get_unattached()

    with open(outputfile, "w") as outfile:
        json.dump(unattached, outfile)


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