# harness-eval-lab

## Overview

AI agent setup evaluation tool. Inspects the environment around AI coding agents: CLAUDE.md, skills, commands, hooks, MCP configs, and sub-agents. Catches structural issues, security problems, redundancy, and token budget waste.

Two interfaces: CLI (3 commands) and Claude Code plugin (2 skills). Both call the same Python engine.

**Two evaluation layers:**
- **Layer 1 (CLI):** 26 deterministic Python rules + system-level analysis (token budget, trigger overlaps, dependencies). No LLM. Fast. Good for CI.
- **Layer 2 (plugin only):** Claude reads every file and scores components on weighted rubric dimensions. Qualitative evaluation that catches things rules can't (redundancy with defaults, type appropriateness, merge candidates).

## Development

- Python 3.11+, managed with `uv`
- Run tests: `uv run pytest`
- Lint: `uv run ruff check src/ tests/`
- Type check: `uv run mypy src/`
- See [`how-to-contribute.md`](how-to-contribute.md) for adding rules, plans, and PRs

## Commands

### CLI
- `harness-eval-lab scan <path>` - run 26 rules, print errors and warnings. No LLM, deterministic, good for CI.
- `harness-eval-lab eval-setup <path>` - run 26 rules + system-level analysis (token budget, trigger overlaps, dependencies). No scoring, no LLM.
- `harness-eval-lab eval-skill <skill-path>` - inspect one skill + contextual analysis (overlap with other skills, CLAUDE.md duplication). Add `--context <path>` for setup context. Add `--rubric` for LLM-based scoring (optional, costs money).

### Plugin (slash commands)
- `/eval-setup` - Layer 1 + Layer 2: run the engine, then Claude reads every file and scores on rubric dimensions
- `/eval-skill` - Layer 1 + Layer 2: deep-evaluate one skill individually and in context

## Project structure

- `src/harness_eval_lab/` - main package (the engine)
  - `cli.py` - Click CLI (3 commands)
  - `config/` - rule presets (recommended/strict/security)
  - `core/` - setup discovery, fingerprinting, component types
  - `inspection/` - static analysis: parsers, lint engine, 26 rules, suppression, auto-fix
  - `rubric/` - LLM-based scoring with weighted dimensions per component type
  - `analysis/` - system-level analysis (budget, triggers, dependencies)
  - `output/` - report generation (terminal + JSON)
  - `utils/` - token counting, TF-IDF similarity, frontmatter parsing, LLM client
- `skills/` - plugin skills (eval-setup, eval-skill) with SKILL.md + scripts
- `.claude-plugin/` - plugin registration
- `tests/` - pytest test suite with fixtures
- `future-plans/` - planned improvements, each in its own subfolder with status and optional Jira link

## Conventions

- Use `uv run` for all commands
- Frozen dataclasses for domain objects, Pydantic for config
- CLI uses Click command groups
- Plugin skills call Python scripts that use the same engine as the CLI
- Cross-component state in rules uses `context.scan_state`, not module-level variables
- Tests go in `tests/` mirroring the source structure
