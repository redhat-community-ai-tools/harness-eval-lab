# harness-eval-lab

## Overview

AI agent setup evaluation tool. Evaluates complete agent setups (CLAUDE.md, skills, commands, hooks, MCP configs, sub-agents) across 5 dimensions: Soundness, Safety, Coherence, Efficiency, Impact.

Two interfaces: CLI (3 commands) and Claude Code plugin (2 skills). Both call the same Python engine.

## Development

- Python 3.11+, managed with `uv`
- Run tests: `uv run pytest`
- Lint: `uv run ruff check src/ tests/`
- Type check: `uv run mypy src/`

## Commands

### CLI
- `harness-eval-lab eval-setup <path>` - full setup evaluation with 5-dimension scorecard
- `harness-eval-lab eval-skill <skill-path>` - deep-evaluate one skill (add `--context <path>` for setup context)
- `harness-eval-lab scan <path>` - quick static analysis, no LLM, good for CI

### Plugin (slash commands)
- `/eval-setup` - evaluate the full setup
- `/eval-skill` - deep-evaluate one skill

## Project structure

- `src/harness_eval_lab/` - main package (the engine)
  - `cli.py` - Click CLI (3 commands)
  - `config/` - rule presets (recommended/strict/security)
  - `core/` - setup discovery, fingerprinting, component types
  - `inspection/` - static analysis: parsers, lint engine, 26 rules, suppression, auto-fix
  - `rubric/` - LLM-based scoring with weighted dimensions per component type
  - `analysis/` - system-level analysis (budget, triggers, dependencies) + 5-dimension scoring
  - `output/` - report generation (terminal + JSON)
  - `utils/` - token counting, TF-IDF similarity, frontmatter parsing, LLM client
- `skills/` - plugin skills (eval-setup, eval-skill) with SKILL.md + scripts
- `.claude-plugin/` - plugin registration
- `tests/` - pytest test suite with fixtures

## Conventions

- Use `uv run` for all commands
- Frozen dataclasses for domain objects, Pydantic for config
- CLI uses Click command groups
- Plugin skills call Python scripts that use the same engine as the CLI
- Tests go in `tests/` mirroring the source structure
