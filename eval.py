from call import call
from graph import random_dag, print_dag, get_all_variants_string
from evaluator import send_test, check_answer, score


def main():
    """Complete evaluation with LLM call, DAG generation, sentence creation, and validation."""
    print("Starting evaluation...", flush=True)
    response = call("hello world")
    print(response, flush=True)
    
    print("\n" + "═" * 80, flush=True)
    print("Testing complete system with 4 nodes and 6 edges:", flush=True)
    print("═" * 80, flush=True)
    
    nodes = ['A', 'B', 'C', 'D']
    graph = random_dag(nodes, 6)
    print_dag(graph)
    
    # Get the path variants as a string
    path_variants = get_all_variants_string(graph)
    print(path_variants, flush=True)
    
    print("\n" + "═" * 60, flush=True)
    print("Step 1: Sending to LLM for sentence construction:", flush=True)
    print("═" * 60, flush=True)
    
    # Send to evaluator for sentence generation
    answer = send_test(path_variants)
    print(answer, flush=True)
    
    print("\n" + "═" * 60, flush=True)
    print("Step 2: Checking validity of each sentence:", flush=True)
    print("═" * 60, flush=True)
    
    # Check the answer
    validation = check_answer(path_variants, answer)
    print("Validation result:", validation, flush=True)
    
    # Calculate and display score
    correct, total = score(validation)
    print(f"Score: correct {correct} out of {total}", flush=True)
    
    print("\n" + "═" * 80, flush=True)
    print("Score Aggregator: Testing combinations (3-4 nodes × 3-4 edges)", flush=True)
    print("═" * 80, flush=True)
    
    # Initialize 2D arrays for results (2x2 grid for nodes 3-4 and edges 3-4)
    correct_scores = [[0 for _ in range(2)] for _ in range(2)]
    total_scores = [[0 for _ in range(2)] for _ in range(2)]
    
    for node_idx, num_nodes in enumerate(range(3, 5)):  # 3, 4 nodes
        for edge_idx, num_edges in enumerate(range(3, 5)):  # 3, 4 edges
            print(f"\nTesting: {num_nodes} nodes, {num_edges} edges...", flush=True)
            
            try:
                # Create nodes as letters
                test_nodes = [chr(ord('A') + i) for i in range(num_nodes)]
                
                # Generate graph and get path variants
                test_graph = random_dag(test_nodes, num_edges)
                test_variants = get_all_variants_string(test_graph)
                path_count = len([l for l in test_variants.split('\n') if ':' in l and '->' in l])
                print(f"  Generated {path_count} paths", flush=True)
                
                # Send test and check answer
                print("  Generating sentences...", end="", flush=True)
                test_answer = send_test(test_variants)
                print(" Validating...", end="", flush=True)
                test_validation = check_answer(test_variants, test_answer)
                
                # Get score and store in arrays
                correct_count, total_count = score(test_validation)
                correct_scores[node_idx][edge_idx] = correct_count
                total_scores[node_idx][edge_idx] = total_count
                
                print(f" Result: {correct_count}/{total_count}", flush=True)
                
            except Exception as e:
                print(f"  Error: {e}", flush=True)
                correct_scores[node_idx][edge_idx] = 0
                total_scores[node_idx][edge_idx] = 0
    
    print("\n" + "═" * 60, flush=True)
    print("AGGREGATED RESULTS", flush=True)
    print("═" * 60, flush=True)
    print("Correct scores (rows: nodes 3-4, columns: edges 3-4):", flush=True)
    for i, row in enumerate(correct_scores):
        print(f"  {i+3} nodes: {row}", flush=True)
    
    print("\nTotal scores (rows: nodes 3-4, columns: edges 3-4):", flush=True)
    for i, row in enumerate(total_scores):
        print(f"  {i+3} nodes: {row}", flush=True)


if __name__ == "__main__":
    main()
