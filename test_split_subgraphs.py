"""
Test script for split_subgraphs_by_promotables function
Tests the subgraph extraction from nodes/edges data
"""

import json
import sys
import os

# Add the library path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'Block_Families', 'General', '_library'))

from split_nodes_and_edges import split_subgraphs_by_promotables, prom_types


def test_with_example_data():
    """Test the function with the example unattached.json data"""
    
    # Load the example data
    example_file = os.path.join('Orchestration', 'Results', 'examples', 'unattached.json')
    
    if not os.path.exists(example_file):
        print(f"Error: Example file not found: {example_file}")
        return
    
    with open(example_file, 'r') as f:
        data = json.load(f)
    
    print("=" * 80)
    print("TESTING SPLIT SUBGRAPHS BY PROMOTABLES")
    print("=" * 80)
    print(f"\nInput data:")
    print(f"  Total nodes: {len(data.get('nodes', []))}")
    print(f"  Total edges: {len(data.get('edges', []))}")
    
    # Count promotables in input
    promotable_nodes = [n for n in data.get('nodes', []) if n.get('type') in prom_types]
    print(f"  Promotable nodes: {len(promotable_nodes)}")
    for pnode in promotable_nodes:
        print(f"    - {pnode['type']}: {pnode['id']}")
    
    # Split the subgraphs
    result = split_subgraphs_by_promotables(data)
    
    print("\n" + "=" * 80)
    print("RESULTS")
    print("=" * 80)
    
    # Display promo nodes/edges
    print(f"\nPromo (connected to promotables):")
    print(f"  Nodes: {len(result['promo']['nodes'])}")
    print(f"  Edges: {len(result['promo']['edges'])}")
    
    if result['promo']['nodes']:
        print(f"  Node types:")
        promo_types_count = {}
        for node in result['promo']['nodes']:
            ntype = node.get('type', 'unknown')
            promo_types_count[ntype] = promo_types_count.get(ntype, 0) + 1
        for ntype, count in sorted(promo_types_count.items()):
            print(f"    {ntype}: {count}")
        
        # Show promotables
        promo_promotables = [n for n in result['promo']['nodes'] if n.get('type') in prom_types]
        print(f"  Promotables: {len(promo_promotables)}")
        for prom in promo_promotables:
            print(f"    - {prom['type']}: {prom['id']}")
    
    print()
    
    # Display scratch objects
    print(f"Scratch (not connected to promotables):")
    print(f"  Nodes: {len(result['scratch']['nodes'])}")
    print(f"  Edges: {len(result['scratch']['edges'])}")
    
    if result['scratch']['nodes']:
        print(f"  Scratch node types:")
        scratch_types = {}
        for node in result['scratch']['nodes']:
            ntype = node.get('type', 'unknown')
            scratch_types[ntype] = scratch_types.get(ntype, 0) + 1
        for ntype, count in sorted(scratch_types.items()):
            print(f"    {ntype}: {count}")
    
    # Verify totals
    total_promo_nodes = len(result['promo']['nodes'])
    total_scratch_nodes = len(result['scratch']['nodes'])
    total_nodes = total_promo_nodes + total_scratch_nodes
    
    print("\n" + "=" * 80)
    print("VERIFICATION")
    print("=" * 80)
    print(f"Total input nodes: {len(data.get('nodes', []))}")
    print(f"Total output nodes: {total_nodes}")
    print(f"  Promo nodes: {total_promo_nodes}")
    print(f"  Scratch nodes: {total_scratch_nodes}")
    print(f"Match: {'✓ PASS' if total_nodes == len(data.get('nodes', [])) else '✗ FAIL'}")
    
    # Save results to file
    output_file = 'test_output_split_subgraphs.json'
    with open(output_file, 'w') as f:
        # Convert result to be JSON serializable
        output = {
            'summary': {
                'promo_node_count': len(result['promo']['nodes']),
                'promo_edge_count': len(result['promo']['edges']),
                'scratch_node_count': len(result['scratch']['nodes']),
                'scratch_edge_count': len(result['scratch']['edges'])
            },
            'promo': result['promo'],
            'scratch': result['scratch']
        }
        json.dump(output, f, indent=2)
    
    print(f"\nDetailed results saved to: {output_file}")


if __name__ == '__main__':
    test_with_example_data()
