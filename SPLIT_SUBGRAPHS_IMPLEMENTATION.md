# Subgraph Splitting Implementation

## Overview

Successfully implemented a system to split a nodes/edges graph structure into separate subgraphs, each anchored by a "promotable type" (incident, task, impact, event, sighting, attack-flow, x-oca-behavior).

## Implementation

### Files Modified/Created

1. **`Block_Families/General/_library/split_nodes_and_edges.py`**
   - Added `AdjacencyGraph` class for graph traversal
   - Added `split_subgraphs_by_promotables()` function
   - Added priority ordering for promotable types

2. **`test_split_subgraphs.py`**
   - Test script that validates the implementation
   - Uses `Orchestration/Results/examples/unattached.json` as test data

### Key Features

#### AdjacencyGraph Class
- Builds bidirectional adjacency list from edges
- Supports BFS traversal to find connected components
- Extracts edges within a subgraph

#### split_subgraphs_by_promotables Function
- Takes input: `{'nodes': [...], 'edges': [...]}`
- Returns:
  ```python
  {
      'subgraphs': [
          {
              'anchor': <promotable_node>,
              'anchor_type': <type_string>,
              'anchor_id': <id_string>,
              'promotables': [all promotable nodes in component],
              'nodes': [...],
              'edges': [...]
          }
      ],
      'orphaned': {
          'nodes': [...],  # nodes not connected to any promotable
          'edges': [...]
      }
  }
  ```

## Test Results

Using `Orchestration/Results/examples/unattached.json`:

```
Input data:
  Total nodes: 28
  Total edges: 42
  Promotable nodes: 1 (sighting)

Results:
  Subgraphs: 1
    - Anchor: sighting
    - Nodes: 23 (email-addr, identity, indicator, observed-data, relationship, user-account)
    - Edges: 42
  
  Orphaned: 5 nodes (all identities), 0 edges

Verification: ✓ PASS (all nodes accounted for)
```

## Usage Example

```python
import json
from Block_Families.General._library.split_nodes_and_edges import split_subgraphs_by_promotables

# Load your data
with open('data.json') as f:
    data = json.load(f)  # Must have 'nodes' and 'edges' keys

# Split into subgraphs
result = split_subgraphs_by_promotables(data)

# Process each subgraph
for sg in result['subgraphs']:
    print(f"Subgraph anchored by {sg['anchor_type']}")
    print(f"  Contains {len(sg['nodes'])} nodes")
    print(f"  Contains {len(sg['edges'])} edges")
    
    # Access the nodes and edges
    for node in sg['nodes']:
        # Process node
        pass
    
    for edge in sg['edges']:
        # Process edge
        pass

# Handle orphaned objects
orphaned = result['orphaned']
print(f"Found {len(orphaned['nodes'])} orphaned nodes")
```

## Algorithm Details

1. **Build adjacency graph**: Creates bidirectional connections from all edges
2. **Identify promotables**: Finds all nodes with type in `prom_types` list
3. **Extract components**: For each unvisited promotable:
   - Performs BFS to find all connected nodes
   - Extracts edges within the component
   - Marks nodes as visited
4. **Handle multiple promotables**: When multiple promotables exist in one component:
   - Chooses highest priority as anchor (incident > event > sighting > task > impact)
   - Includes all promotables in the `promotables` list
5. **Collect orphans**: Any unvisited nodes become orphaned

## Edge Cases Handled

- ✓ Multiple promotables in same component (priority-based anchor selection)
- ✓ Isolated promotables (single-node subgraph)
- ✓ Orphaned nodes (nodes not connected to any promotable)
- ✓ Empty input (returns empty results)
- ✓ Bidirectional edge traversal (finds all connections)

## Output Files

- `test_output_split_subgraphs.json` - Full detailed results of test run
