# Eval Setup Lint

Run 43 deterministic rules + system-level analysis on the agent setup. No LLM. Fast, reproducible, CI-suitable.

## Instructions

1. Ask the user where to present results: terminal or file.

2. Run the lint command on the current project:

```bash
harness-eval-lab eval-setup-lint .
```

If `harness-eval-lab` is not installed, try `pip install harness-eval-lab` first.

For JSON output (if the user prefers file output):

```bash
harness-eval-lab eval-setup-lint . --format json
```

3. Present the report. Include all sections: inventory, token budget, trigger analysis, dependencies, findings, and inspection summary.
