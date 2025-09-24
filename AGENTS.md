# Repository Guidelines

## Project Structure & Module Organization
- `eval.py` orchestrates the benchmark run: seeds a DAG, dispatches LLM prompts, and aggregates scores.
- `graph.py` stores DAG helpers (`Graph`, `random_dag`, path printers) and is the place to extend traversal logic.
- `evaluator.py` contains the LLM interaction loop (`send_test`, `check_answer`, `score`) and handles result accounting.
- `call.py` centralizes API settings; treat it as the adaptor for whichever OpenAI-compatible endpoint you target.
- Logs such as `run_1.log` are kept in the repo root; clean or rotate them when adding new runs.

## Build, Test, and Development Commands
- `python3 eval.py` runs the full pipeline (smoke test, single DAG evaluation, score grid) and should succeed before every push.
- `python3 graph.py` prints randomly generated DAGs; useful for quickly verifying structural changes.
- `pip install openai` (or add to your virtualenv) satisfies the only required third-party dependency.

## Coding Style & Naming Conventions
- Follow standard Python 3 conventions: 4-space indentation, UTF-8 source, and descriptive snake_case for functions and variables.
- Keep module-level constants upper snake case (`MAX_ATTEMPTS`), use f-strings for formatting, and prefer explicit imports.
- Maintain docstrings in the style already present and add inline comments only when logic is non-obvious.

## Testing Guidelines
- Re-run `python3 eval.py` after modifying graph generation, scoring, or API plumbing; inspect the aggregated matrices for regressions.
- For deterministic comparisons, seed `random` at the top of your experiment or capture outputs in a fresh `run_*.log`.
- When touching LLM prompts, validate both the sentence generation and validation phases to ensure contract compatibility.

## Commit & Pull Request Guidelines
- Use short, descriptive commit subjects (imperative if possible: `Add path pruning guard`) and avoid batching unrelated changes.
- Reference issues or tickets in the body, and note any model/config tweaks that other contributors must mirror locally.
- Pull requests should summarize behavior changes, list manual test commands run, and attach log snippets for non-trivial runs.

## Configuration & Secrets
- Set `base_url` and `model` in `call.py`; never hard-code API keys—source them from environment variables or local config files.
- Document non-default parameters (node counts, edge limits, model versions) in the PR so future benchmarks remain reproducible.
