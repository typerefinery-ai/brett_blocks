



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