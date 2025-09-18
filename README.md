# Word Game LLM Benchmark

A benchmark system for evaluating Large Language Models' ability to construct valid English sentences from directed acyclic graph (DAG) path structures.

## Overview

This project tests LLMs on their ability to:
1. Generate meaningful English sentences where each letter represents a single word
2. Follow specific path structures derived from directed acyclic graphs
3. Maintain grammatical correctness across multiple sentence variants

## Features

- **Graph Generation**: Creates random DAGs with configurable nodes and edges
- **Path Analysis**: Identifies all possible paths from starting nodes (no incoming edges)
- **Sentence Generation**: Prompts LLMs to create valid sentences following graph paths
- **Automated Validation**: Checks sentence validity using LLM-based evaluation
- **Score Aggregation**: Runs systematic tests across different graph complexities

## Project Structure

```
word_game_llm_benchmark/
├── call.py          # Synchronous LLM API interface
├── graph.py         # DAG generation and path analysis
├── evaluator.py     # Sentence testing and validation
├── eval.py          # Main evaluation pipeline
├── README.md        # This file
└── .gitignore       # Git ignore patterns
```

## Files Description

### Core Components

- **`call.py`**: Simple synchronous interface to OpenAI-compatible APIs
- **`graph.py`**: 
  - `random_dag()`: Generates random directed acyclic graphs
  - `print_dag()`: Display graph structure
  - `get_all_variants_string()`: Extract all paths as formatted strings
- **`evaluator.py`**:
  - `send_test()`: Send path variants to LLM for sentence generation
  - `check_answer()`: Validate generated sentences using LLM
  - `score()`: Count correct/total results from validation
- **`eval.py`**: Main evaluation pipeline with score aggregation

## Usage

### Basic Evaluation
```bash
python3 eval.py
```

This runs:
1. Initial LLM test ("hello world")
2. Single graph test (4 nodes, 6 edges)
3. Score aggregator testing combinations of 3-4 nodes × 3-4 edges

### Configuration

Edit `call.py` to configure LLM settings:
```python
base_url = "https://chat.martintech.co.uk/v1"  # Your API endpoint
model = "qwen32-awq"                          # Model name
```

## Example Output

```
Testing: 4 nodes, 6 edges...
Directed Acyclic Graph:
Nodes: ['A', 'B', 'C', 'D']
Edges:
  D -> B -> C -> A
  D -> B -> A
  D -> C -> A
  D -> A

Generated sentences:
  D="She", B="quickly", C="then", A="arrived"
  1: "She quickly then arrived"
  2: "She quickly arrived"
  3: "She then arrived"
  4: "She arrived"

Validation: [true, true, true, true]
Score: correct 4 out of 4
```

## Requirements

- Python 3.7+
- OpenAI Python library (`pip install openai`)
- Access to OpenAI-compatible API endpoint

## Key Features

### Graph Generation
- Cycle prevention using real-time detection
- Configurable node count and edge density
- Automatic starting node identification

### Sentence Validation
- LLM-based grammatical correctness checking
- JSON-formatted validation responses
- Path-structure adherence verification

### Score Aggregation
- Systematic testing across graph complexities
- 2D result matrices for analysis
- Real-time progress feedback

## Benchmark Results Format

Results are presented as 2D arrays:
- **Rows**: Number of nodes (3-4)
- **Columns**: Number of edges (3-4)
- **Values**: Correct/Total sentence counts

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test with `python3 eval.py`
5. Submit a pull request

## License

MIT License - feel free to use and modify for research purposes.

## Technical Notes

- Uses synchronous API calls to avoid async event loop issues
- Real-time output with flush statements for immediate feedback
- Error handling prevents crashes during batch processing
- JSON output mode for structured validation responses
