# harness-eval-lab

## Overview

AI agent setup evaluation tool. Inspects the environment around AI coding agents: CLAUDE.md, skills, commands, hooks, MCP configs, and sub-agents. Catches structural issues, security problems, redundancy, and token budget waste.

Two interfaces: CLI (3 commands) and Claude Code plugin (3 skills). Both call the same Python engine.

**Two evaluation layers:**
- **Layer 1:** 26 deterministic Python rules + system-level analysis (token budget, trigger overlaps, dependencies, context utilization). No LLM. Fast. Good for CI.
- **Layer 2:** LLM-based qualitative review. Per-component rubric scoring, 21 cross-type optimization checks, KEEP/REVIEW/REMOVE verdicts. In the plugin, Claude does the review in-session. In the CLI, an external LLM API call does it (requires API key).

## Development

- Python 3.11+, managed with `uv`
- Run tests: `uv run pytest`
- Lint: `uv run ruff check src/ tests/`
- Type check: `uv run mypy src/`
- See [`how-to-contribute.md`](how-to-contribute.md) for adding rules, plans, and PRs

## Commands

### CLI
- `harness-eval-lab eval-setup-lint <path>` - Layer 1: 26 rules + system analysis (budget, triggers, dependencies, context utilization). No LLM, deterministic, CI-suitable. Supports `--fail-on-error`, `--fix`, `--format json`.
- `harness-eval-lab eval-setup-review <path>` - Layer 2 only: LLM rubric scoring per component. Requires `GEMINI_API_KEY` or `ANTHROPIC_API_KEY` in environment. Use `--provider` and `--model` to configure.
- `harness-eval-lab eval-skill <skill-path>` - deep-evaluate one skill + contextual analysis. Add `--context <path>` for setup context. Add `--rubric` for LLM scoring.

All CLI commands support `--user-config <path>` to discover user-level CLAUDE.md files from `~/.claude/`.

### Plugin (slash commands)
- `/eval-setup-lint` - Layer 1 only: run 26 rules + system-level analysis. No LLM, fast, CI-suitable.
- `/eval-setup-review` - Layer 2 + Layer 1 context: Claude reads every file, applies per-component rubrics, runs 21 cross-type checks, produces health summary with KEEP/REVIEW/REMOVE verdicts.
- `/eval-skill` - Layer 1 + Layer 2: deep-evaluate one skill individually and in context

## Project structure

- `src/harness_eval_lab/` - main package (the engine)
  - `cli.py` - Click CLI (3 commands: eval-setup-lint, eval-setup-review, eval-skill)
  - `config/` - rule presets (recommended/strict/security/pre-workflow)
  - `core/` - setup discovery, fingerprinting, component types
  - `inspection/` - static analysis: parsers, lint engine, 26 rules, suppression, auto-fix
  - `rubric/` - LLM-based issue detection with per-component-type categories
  - `analysis/` - system-level analysis (budget, triggers, dependencies, context utilization)
  - `output/` - report generation (terminal + JSON)
  - `utils/` - token counting, TF-IDF similarity, frontmatter parsing, LLM client
- `skills/` - plugin skills (eval-setup-lint, eval-setup-review, eval-skill) with SKILL.md + rubric files + scripts
- `.claude-plugin/` - plugin registration
- `tests/` - pytest test suite with fixtures
- `future-plans/` - planned improvements, each in its own subfolder with status

## Conventions

- Use `uv run` for all commands
- Frozen dataclasses for domain objects, Pydantic for config
- CLI uses Click command groups
- Plugin skills call Python scripts that use the same engine as the CLI
- Cross-component state in rules uses `context.scan_state`, not module-level variables
- Tests go in `tests/` mirroring the source structure
