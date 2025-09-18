import random
from collections import defaultdict, deque


class Graph:
    """Simple directed graph representation."""
    
    def __init__(self, nodes):
        self.nodes = list(nodes)
        self.edges = defaultdict(list)
    
    def add_edge(self, from_node, to_node):
        """Add an edge from from_node to to_node."""
        if to_node not in self.edges[from_node]:
            self.edges[from_node].append(to_node)
    
    def has_cycle(self):
        """Check if the graph has a cycle using DFS."""
        # States: 0 = unvisited, 1 = visiting, 2 = visited
        state = {node: 0 for node in self.nodes}
        
        def dfs(node):
            if state[node] == 1:  # Back edge found - cycle detected
                return True
            if state[node] == 2:  # Already processed
                return False
            
            state[node] = 1  # Mark as visiting
            
            for neighbor in self.edges[node]:
                if dfs(neighbor):
                    return True
            
            state[node] = 2  # Mark as visited
            return False
        
        for node in self.nodes:
            if state[node] == 0:
                if dfs(node):
                    return True
        return False


def random_dag(nodes, edges):
    """Create a random directed acyclic graph with specified nodes and edge count."""
    if not nodes:
        return Graph([])
    
    graph = Graph(nodes)
    node_list = list(nodes)
    edges_added = 0
    max_attempts = edges * 10  # Prevent infinite loops
    attempts = 0
    
    while edges_added < edges and attempts < max_attempts:
        attempts += 1
        
        # Pick two random nodes
        from_node = random.choice(node_list)
        to_node = random.choice(node_list)
        
        # Skip self-loops
        if from_node == to_node:
            continue
            
        # Skip if edge already exists
        if to_node in graph.edges[from_node]:
            continue
        
        # Try adding the edge
        graph.add_edge(from_node, to_node)
        
        # Check if it creates a cycle
        if graph.has_cycle():
            # Remove the edge if it creates a cycle
            graph.edges[from_node].remove(to_node)
        else:
            edges_added += 1
    
    return graph


def print_dag(graph):
    """Print the DAG in a readable format."""
    print("Directed Acyclic Graph:")
    print(f"Nodes: {sorted(graph.nodes)}")
    print("Edges:")
    
    if not any(graph.edges.values()):
        print("  (no edges)")
        return
    
    for node in sorted(graph.nodes):
        if graph.edges[node]:
            targets = sorted(graph.edges[node])
            for target in targets:
                print(f"  {node} -> {target}")
    
    print(f"Total edges: {sum(len(edges) for edges in graph.edges.values())}")


def print_all_variants(graph):
    """Print all paths starting from nodes with no incoming edges."""
    result = get_all_variants_string(graph)
    print(result)


def get_all_variants_string(graph):
    """Get all paths starting from nodes with no incoming edges as a string."""
    # Find nodes with no incoming edges (starting nodes)
    incoming_edges = {node: 0 for node in graph.nodes}
    for from_node in graph.nodes:
        for to_node in graph.edges[from_node]:
            incoming_edges[to_node] += 1
    
    starting_nodes = [node for node, count in incoming_edges.items() if count == 0]
    
    result = ["\nAll path variants:"]
    result.append(f"Starting nodes (no incoming edges): {sorted(starting_nodes)}")
    
    if not starting_nodes:
        result.append("No starting nodes found (all nodes have incoming edges)")
        return "\n".join(result)
    
    all_paths = []
    
    def find_paths(current_node, path):
        """Recursively find all paths from current node."""
        current_path = path + [current_node]
        
        # If no outgoing edges, this is a terminal path
        if not graph.edges[current_node]:
            all_paths.append(current_path)
        else:
            # Continue exploring each outgoing edge
            for next_node in graph.edges[current_node]:
                find_paths(next_node, current_path)
    
    # Find all paths from each starting node
    for start_node in starting_nodes:
        find_paths(start_node, [])
    
    if not all_paths:
        result.append("No complete paths found")
        return "\n".join(result)
    
    result.append("Paths:")
    # Sort paths by length (longest first), then alphabetically for same length
    sorted_paths = sorted(all_paths, key=lambda path: (-len(path), path))
    for i, path in enumerate(sorted_paths, 1):
        path_str = " -> ".join(path)
        result.append(f"  {i}: {path_str}")
    
    result.append(f"Total paths: {len(all_paths)}")
    return "\n".join(result)
