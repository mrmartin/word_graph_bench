from call import call, MAX_CONCURRENT_CALLS
from graph import random_dag, print_dag, get_all_variants_string
from evaluator import send_test, check_answer, score
import asyncio
import concurrent.futures
import threading


def process_single_test(node_idx, edge_idx, num_nodes, num_edges):
    """Process a single test case and return results."""
    try:
        print(f"\nTesting: {num_nodes} nodes, {num_edges} edges...", flush=True)
        
        # Create nodes as letters
        test_nodes = [chr(ord('A') + i) for i in range(num_nodes)]
        
        # Generate graph and get path variants
        test_graph = random_dag(test_nodes, num_edges)
        test_variants = get_all_variants_string(test_graph)
        path_count = len([l for l in test_variants.split('\n') if ':' in l and '->' in l])
        print(f"  Generated {path_count} paths", flush=True)
        
        # Send test and check answer (these will use parallel calls internally)
        print("  Generating sentences & validating...", flush=True)
        test_answer = send_test(test_variants)
        test_validation = check_answer(test_variants, test_answer)
        
        # Get score
        correct_count, total_count = score(test_validation)
        print(f"  Result: {correct_count}/{total_count}", flush=True)
        
        return (node_idx, edge_idx, correct_count, total_count)
        
    except Exception as e:
        print(f"  Error: {e}", flush=True)
        return (node_idx, edge_idx, 0, 0)

def run_parallel_evaluation():
    """Run the evaluation with parallel processing."""
    print(f"Starting parallel evaluation with up to {MAX_CONCURRENT_CALLS} concurrent LLM calls...", flush=True)
    
    # Prepare test cases
    test_cases = []
    for node_idx, num_nodes in enumerate(range(3, 8)):  # 3-7 nodes for manageable size
        for edge_idx, num_edges in enumerate(range(3, 8)):  # 3-7 edges
            test_cases.append((node_idx, edge_idx, num_nodes, num_edges))
    
    print(f"Total test cases: {len(test_cases)}", flush=True)
    
    # Initialize result arrays
    max_size = 10  # Generous size for results
    correct_scores = [[0 for _ in range(max_size)] for _ in range(max_size)]
    total_scores = [[0 for _ in range(max_size)] for _ in range(max_size)]
    
    # Process tests using ThreadPoolExecutor to handle the parallel calls
    with concurrent.futures.ThreadPoolExecutor(max_workers=32) as executor:
        # Submit all test cases
        futures = [
            executor.submit(process_single_test, node_idx, edge_idx, num_nodes, num_edges)
            for node_idx, edge_idx, num_nodes, num_edges in test_cases
        ]
        
        # Collect results as they complete
        for future in concurrent.futures.as_completed(futures):
            try:
                node_idx, edge_idx, correct_count, total_count = future.result()
                correct_scores[node_idx][edge_idx] = correct_count
                total_scores[node_idx][edge_idx] = total_count
            except Exception as e:
                print(f"Future error: {e}", flush=True)
    
    # Display results
    print("\n" + "═" * 60, flush=True)
    print("AGGREGATED RESULTS", flush=True)
    print("═" * 60, flush=True)
    print("Correct scores (first 5x5):", flush=True)
    for i in range(5):
        row = correct_scores[i][:5]
        print(f"  {i+3} nodes: {row}", flush=True)
    
    print("\nTotal scores (first 5x5):", flush=True)
    for i in range(5):
        row = total_scores[i][:5]
        print(f"  {i+3} nodes: {row}", flush=True)

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
    print("Score Aggregator: Testing combinations with parallel processing", flush=True)
    print("═" * 80, flush=True)
    
    # Run parallel evaluation
    run_parallel_evaluation()

if __name__ == "__main__":
    main()
