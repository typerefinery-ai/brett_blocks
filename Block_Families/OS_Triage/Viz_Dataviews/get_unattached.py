
################################################################################
## header start                                                               ##
################################################################################
# allow importing og service local packages
import os.path
from urllib.request import urlretrieve

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
# Title: When an incident is selected, get all of the unattached objects
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
	top = layout_options.get("top", 50)
	dummy_width = layout_options.get("dummy_width", 400)
	distanceX = layout_options.get("distanceX", 200)
	distanceY = layout_options.get("distanceY", 100)
	left = layout_options.get("left", 50)
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
	
	# 1. get the settings
	if not os.path.exists(TR_Settings_Dir):
		download_settings()	
	with open(TR_Settings_Dir + "/options.json", "r") as mem_input:
		options = json.load(mem_input)        # load options json
		common_options = options.get("common", {})
		layout_options = common_options.get("layout", {})

		# 2. Create adjacency graph
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
		i = 0
		for prom_node in promotables:
			# 5.1 setup prom node details
			prom_id = prom_node['id']
			prom_type = prom_node['type']
			prom_layout = level2_layouts.get(prom_type, [])
			
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
			i += 1
			
			# 5.7 Add to promo collections
			all_promo_nodes.extend(component_nodes)
			all_promo_edges.extend(component_edges)
		
		# 6. Find scratch nodes (not visited)
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