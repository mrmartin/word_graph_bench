from call import call
import json
import re


def send_test(test):
    """Send a test to the LLM asking it to construct valid English sentences from path variants."""
    prompt = f"""construct valid english sentences, where each letter (A, B, C, etc.) is one word, and the following are all valid sentences:
{test}

Please create meaningful English sentences where each letter represents one word, and the arrows (->) represent the flow or connection between words in the sentence structure."""
    
    response = call(prompt)
    return response


def check_answer(test, answer):
    """Check if the answer provides valid sentences for each path in the test."""
    # Extract the number of paths from the test
    path_lines = [line.strip() for line in test.split('\n') if re.match(r'\s*\d+:', line)]
    num_paths = len(path_lines)
    
    prompt = f"""Given this test:
{test}

And this answer:
{answer}

For each numbered path in the test, determine if the answer provides a valid English sentence that follows that exact path structure. Be very strict, do not be linient. Return a JSON array of {num_paths} boolean values (true/false), where each boolean corresponds to whether the path at that position has a valid sentence.

Example format: [{", ".join(["true"] * num_paths)}]

Only return the JSON array, nothing else."""
    
    response = call(prompt, json_output=True)
    return response


def score(validation_json):
    """Count the number of correct results from validation JSON."""
    try:
        # Parse the JSON string if it's a string
        if isinstance(validation_json, str):
            validation_data = json.loads(validation_json.strip())
        else:
            validation_data = validation_json
        
        # Count true values
        correct_count = sum(1 for result in validation_data if result is True)
        total_count = len(validation_data)
        
        return correct_count, total_count
    except (json.JSONDecodeError, TypeError) as e:
        print(f"Error parsing validation JSON: {e}")
        return 0, 0
