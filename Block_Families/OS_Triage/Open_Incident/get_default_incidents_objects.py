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
# Title: Get All Incidents
# Author: OS-Threat
# Organisation Repo: https://github.com/typerefinery-ai/brett_blocks
# Contact Email: brett@osthreat.com
# Date: 07/08/2023
#
# Description: This script is designed to take in a Stix Object
#       and save it in the unattached list for the currently selected incident
#
# No Input, Just Trigger:
#
# One Output
# 1. List of Incidents
#
#
# This code is licensed under the terms of the Apache 2.
##############################################################################

from networkx import nodes
from stixorm.module.authorise import import_type_factory
# from Block_Families.General._library.
# from Orchestration.Common.
from urllib.request import urlretrieve
import json
import sys
import importlib.util
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
import os

import_type = import_type_factory.get_all_imports()
from typing import List, Dict, Union, Optional, Any


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

TR_Settings_Dir = "./generated/os-triage/context_mem/settings"
TR_Settings_File = "/options.json"
TR_Settings_URL = "https://raw.githubusercontent.com/typerefinery-ai/brett_blocks/refs/heads/main/Block_Families/OS_Triage/User_Options/options.json"

def download_settings():
    if not os.path.exists(TR_Settings_Dir):
        os.makedirs(TR_Settings_Dir)
    result = urlretrieve(TR_Settings_URL, TR_Settings_Dir + "/options.json")
    print(f'settings file result ->', result)



#============================================================================

from collections import deque

# If Incident Management, then check for these promotoables
prom_types = [
	'task',
	'impact',
	'event',
	'sighting',
	'attack-flow',
	'x-oca-behavior'
]

prom_y = {
	'task': 100,
	'impact': 350,
	'event': 600,
	'sighting': 850,
	'attack-flow': 1200,
	'x-oca-behavior': 1450
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
	'x-oca-behavior': [],
	'attack-flow': []
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

edge_id = 0

def create_edge(edge_label, source_id, target_id, edge_type)-> Dict[str, str]:
    edge = {}
    edge["source"] = source_id
    edge["target"] = target_id
    edge["name"] = edge_label.replace("_", "-")
    edge["type"] = edge_type
    # global edge_id
    # edge["id"] = edge_id
    # edge_id += 1
    # edge["id"] = f"{source_id}--{edge_label}--{target_id}"
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



def get_actual_layout_and_ids(prom_layout, prom_node):
	"""
	Get actual layout fields and corresponding 2nd level IDs from promotable node.
	
	Args:
		prom_layout: Layout configuration for the promotable type
		prom_node: The promotable node dict
	"""
	all_second_level_ids = []
	second_level_ids_by_field = []
	actual_layout = []
	for layout in prom_layout:
		level = {}
		if layout.get('field') in prom_node["original"]:
			actual_layout.append(layout)
			if layout['datatype'] == 'list':
				ids = prom_node["original"][layout['field']]
				all_second_level_ids.extend(ids)
				level[layout['field']] = ids
				second_level_ids_by_field.append({layout['field']: ids})
			else:
				id = prom_node["original"][layout['field']]
				all_second_level_ids.append(id)
				level[layout['field']] = [id]
				second_level_ids_by_field.append({layout['field']: [id]})

	return actual_layout, all_second_level_ids, second_level_ids_by_field

def annotate_2nd_level_node(node, i, centreX, secondY, distanceX, len_actual_layout, dummy_width) -> Dict:
	"""
	Annotate a single node with positionX and positionY.
	
	Args:
		node: Node dictionary
		i: Layout index
		centreX: X centre coordinate
		secondY: Y coordinate
		distanceX: Horizontal distance between nodes
		len_actual_layout: Number of fields in the actual layout
		dummy_width: Width of the area for layout
		
	Returns:
		Node dictionary with updated positionX and positionY
	"""
	# position based on field and index
	if len_actual_layout == 1:
		node['positionY'] = secondY
		node['positionX'] = centreX
	elif len_actual_layout == 2:
		node['positionY'] = secondY
		if i == 0:
			node['positionX'] = centreX - distanceX
		elif i == 1:
			node['positionX'] = centreX + distanceX
		else:
			pass
	elif len_actual_layout == 3:
		node['positionY'] = secondY
		if i == 0:
			node['positionX'] = centreX - distanceX
		elif i == 1:
			node['positionX'] = centreX 
		elif i == 2:
			node['positionX'] = centreX + distanceX
		else:
			pass
	elif len_actual_layout == 4:
		node['positionY'] = secondY
		if i == 0:
			node['positionX'] = centreX - dummy_width / 2 
		elif i == 1:
			node['positionX'] = centreX - dummy_width / 2 + distanceX
		elif i == 2:
			node['positionX'] = centreX - dummy_width / 2 + 2 * distanceX
		elif i == 3:
			node['positionX'] = centreX - dummy_width / 2 + 3 * distanceX
		else:
			pass
	else:
		pass
		
	return node

def annotate_nodes_with_positions(component_nodes, layout_options, prom_layout, prom_node, index) -> List[Dict]:
	"""
	Annotate nodes with positionX and positionY based on layout.

	Args:
		component_nodes: List of node dicts in the component
		layout_options: Layout configuration options
		prom_layout: Layout configuration for the promotable type
		prom_node: The promotable node dict
		index: Index of the promotable node (for horizontal offset)
	Returns:
		List of nodes with updated positionX and positionY
	"""
	# extract layout options
	top = prom_y.get(prom_node['type'], 100)
	dummy_width = layout_options.get("dummy_width", 400)
	distanceX = layout_options.get("distanceX", 200)
	distanceY = layout_options.get("distanceY", 100)
	left = layout_options.get("left", 50) + 50
	# setup prom node positions
	centreX = left +dummy_width/2 + index * dummy_width
	topY = top	

	# get list of 2nd level id's from layout and prom node
	all_second_level_ids = []
	second_level_ids_by_field = []
	actual_layout = []
	actual_layout, all_second_level_ids, second_level_ids_by_field = get_actual_layout_and_ids(prom_layout, prom_node)

	# setup horizontal positioning
	len_actual_layout = len(actual_layout)
	horizontal_spacing = dummy_width / (len_actual_layout + 1)
	# setup node positions
	for node in component_nodes:
		if node['id'] == prom_node['id']: # promotable node at top center
			node['positionX'] = centreX
			node['positionY'] = topY
		elif node['id'] in all_second_level_ids: # 2nd level nodes
			for i, level in enumerate(second_level_ids_by_field):
				for field, ids in level.items():
					if node['id'] in ids:
						# position based on field and index
						secondY = topY + distanceY
						node = annotate_2nd_level_node(node, i, centreX, secondY, distanceX, len_actual_layout, dummy_width)
		elif node["type"] == 'relationship': # relationship nodes are 4th level
			node['positionX'] = 0
			node['positionY'] = topY + 3 * distanceY  # fixed offset below 3rd level nodes
		else: # 3rd level  positioned below 2nd level
			node['positionX'] = 0
			node['positionY'] = topY + 2 * distanceY  # fixed offset at 3rd level below 2nd level node

	return component_nodes



def split_subgraphs_by_promotables(nodes, layout_options):
	"""
	Split a nodes/edges structure into separate subgraphs,
	each anchored by a promotable type.
	
	Args:
		nodes: list of node dicts
		layout_options: layout configuration options
		
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
	
	if not nodes:
		return {'promo': {'nodes': [], 'edges': []}, 'scratch': {'nodes': [], 'edges': []}}

	# 1. Set up the edges for this particular set of nodes
	nodes, edges = generate_nodes_and_edges(nodes)
	# 2. Create adjacency graph for this set of nodes/edges
	graph = AdjacencyGraph(nodes, edges)

	# 3. Identify all promotable nodes
	promotables = [node for node in nodes if node.get('type') in prom_types]
	num_promotables = len(promotables)
	logger.info(f"Found {num_promotables} promotable nodes.")

	# 4. Track visited nodes
	visited = set()
	all_promo_nodes = []
	all_promo_edges = []

	# 5. Process each promotable node
	index = {
		'task': 0,
		'impact': 0,
		'event': 0,
		'sighting': 0,
		'attack-flow': 0,
		'x-oca-behavior': 0
	}

	for prom_node in promotables:
		# 5.0 setup prom node details
		prom_id = prom_node['id']
		prom_type = prom_node['type']
		prom_layout = level2_layouts.get(prom_type, [])
		# 5.1 Setup and then update the index for this type
		i = index.get(prom_type, 0)
		index[prom_type] = i + 1
		
		if prom_id in visited or prom_layout == []:
			continue
		
		# 5.2 Find all connected nodes (the component)
		component_ids = graph.get_connected_component(prom_id)
		
		# 5.3 Mark all as visited
		visited.update(component_ids)
		
		# 5.4 Get nodes and edges for this component
		component_nodes = [graph.nodes_by_id[nid] for nid in component_ids]
		component_edges = graph.get_subgraph_edges(component_ids)

		# 5.5 Setup positions for 2nd level nodes
		component_nodes = annotate_nodes_with_positions(component_nodes, layout_options, prom_layout, prom_node, i)
		
		# 5.7 Add to promo collections
		all_promo_nodes.extend(component_nodes)
		all_promo_edges.extend(component_edges)

	return all_promo_nodes



def annotate_incident_nodes_with_positions(incident_nodes) -> List[Dict]:
	"""
	Annotate incident nodes with positionX and positionY based on layout.

	Args:
		incident_nodes: List of node dicts in the incident
	Returns:
		List of nodes with updated positionX and positionY
	"""
	# 1. get the settings
	if not os.path.exists(TR_Settings_Dir):
		download_settings()	
	with open(TR_Settings_Dir + "/options.json", "r") as mem_input:
		options = json.load(mem_input)        # load options json
		common_options = options.get("common", {})
		layout_options = common_options.get("layout", {})
		# 2. Find the incident node
		incident_node_list = [node for node in incident_nodes if node.get('type') == 'incident']
		if not incident_node_list:
			return incident_nodes
		incident_node = incident_node_list[0]
		incident_ids_list = [incident_node['id']]
		# 4. Get the list of all nodes except the incident node
		other_nodes = [node for node in incident_nodes if node['type'] != "incident"]
		other_nodes = split_subgraphs_by_promotables(other_nodes, layout_options)
		# 5. Annotate incident node positions
		incident_node['positionX'] = layout_options.get("left", 50)
		incident_node['positionY'] = layout_options.get("top", 50)
		# 6. Combine incident node and other nodes
		total_nodes = [incident_node] + other_nodes		

	return total_nodes


def get_default_incidents_objects():
    # 0 Check for "original"
    incident_list = []
    nodes_and_edges = {}
    changed = False
    # 1.B Find Current Incident directory
    if os.path.exists(TR_Context_Memory_Dir + "/" + context_map):
        with open(TR_Context_Memory_Dir + "/" + context_map, "r") as current_context:
            local_map = json.load(current_context)
            # 1. Since the map exists and the incident, then set the current incident details
            incident_id = local_map["current_incident"]
            TR_Incident_Dir = TR_Context_Memory_Dir + "/" + incident_id
            # 2. Open the Incident File, and extract the Ext (for checking/updating)
            with open(TR_Incident_Dir + "/" + incident_data["incident"]) as current_obj:
                incident_list = json.load(current_obj)
                wrapped_incident = incident_list[0]
                incident = wrapped_incident["original"]
                incident_ext = incident["extensions"]["extension-definition--ef765651-680c-498d-9894-99799f2fa126"]
                # 3. For each list of id's in the Incident, collect objects and check whether they are registered
                for key in key_list:
                    if os.path.exists(TR_Incident_Dir + "/" + incident_data[key]):
                        with open(TR_Incident_Dir + "/" + incident_data[key]) as prop_list:
                            current_refs_list = []
                            list_of_objs = json.load(prop_list)
                            field_name = field_names[key]
                            # Either get the list, or make the list
                            if field_name in incident_ext:
                                current_refs_list = incident_ext[field_name]
                            else:
                                incident_ext[field_name] = []
                                current_refs_list = incident_ext[field_name]
                                changed = True
                            # 4. Add each object to the list, and register the id on the incident, if it is not already
                            for stix_obj in list_of_objs:
                                incident_list.append(stix_obj)
                                if stix_obj["id"] not in current_refs_list:
                                    current_refs_list.append(stix_obj["id"])
                                    changed = True
                # 5. If the Incident has been changed, may as well update context mem
                if changed:
                    with open(TR_Incident_Dir + "/" + incident_data["incident"], 'w') as f:
                        f.write(json.dumps([wrapped_incident]))
                # 6. Finally, add the incident to the list
                # incident_list.append(wrapped_incident)
    
    nodes, edges = generate_nodes_and_edges(incident_list)
    # 8. Annotate nodes with positions
    nodes = annotate_incident_nodes_with_positions(nodes)
    nodes_and_edges["nodes"] = nodes
    nodes_and_edges["edges"] = edges

    return nodes_and_edges


def main(inputfile, outputfile):
    # No input data, just a trigger
    nodes_and_edges = get_default_incidents_objects()

    with open(outputfile, "w") as outfile:
        json.dump(nodes_and_edges, outfile)


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
    parser.add_argument("inputfile", nargs='?', default=f"{os.path.basename(__file__)}.input",
                        help="input file (default: %(default)s)")
    parser.add_argument("outputfile", nargs='?', default=f"{os.path.basename(__file__)}.output",
                        help="output file (default: %(default)s)")
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
