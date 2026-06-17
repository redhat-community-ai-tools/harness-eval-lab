# setup-eval

[![CI](https://github.com/redhat-community-ai-tools/harness-eval-lab/actions/workflows/ci.yml/badge.svg)](https://github.com/redhat-community-ai-tools/harness-eval-lab/actions/workflows/ci.yml)
[![Coverage](https://img.shields.io/badge/coverage-73%25-yellow)](https://github.com/redhat-community-ai-tools/harness-eval-lab)
[![Python 3.11+](https://img.shields.io/badge/python-3.11%2B-blue)](https://www.python.org/downloads/)
[![License: Apache 2.0](https://img.shields.io/badge/license-Apache%202.0-green)](LICENSE)

Evaluate AI agent setups for best practices, redundancy, security, and cross-component issues.

## What it does

Most agent evaluation tools test whether a **skill** completes a task correctly. This tool evaluates the **entire setup** that surrounds the agent: CLAUDE.md, skills, commands, hooks, MCP configs, and sub-agents.

It checks whether each component follows best practices, whether components work well together, and whether anything is redundant, conflicting, or insecure.

**Supported tools:** Claude Code and Cursor. The tool auto-detects which tool(s) a project uses and evaluates all discovered components.

## Overview

```
 ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐
 │ setup-eval-lint │  │ setup-eval-     │  │ setup-eval-     │  │ setup-eval-     │
 │                 │  │ review          │  │ security        │  │ skill           │
 │ 43 rules        │  │ per-component   │  │ all security    │  │ deep-dive on    │
 │ system analysis │  │ rubrics         │  │ rules           │  │ one skill       │
 │ token budget    │  │ 21 cross-type   │  │ AST + taint     │  │ lint + rubric   │
 │ trigger overlap │  │ checks          │  │ YARA + CVE      │  │ + contextual    │
 │ dependencies    │  │ instruction     │  │ 4-check         │  │ analysis        │
 │ context util    │  │ clarity         │  │ semantic review  │  │                 │
 │                 │  │ KEEP / REVIEW   │  │ SAFE / CAUTION  │  │ KEEP / REVIEW   │
 │ no LLM, fast   │  │ / REMOVE        │  │ / UNSAFE        │  │ / REMOVE        │
 └─────────────────┘  └─────────────────┘  └─────────────────┘  └─────────────────┘
   "does it pass?"      "is it effective?"     "is it safe?"       "how is this skill?"
```

## Install

### From PyPI

```bash
pip install setup-eval
```

This installs everything needed for lint, review, and security commands. For YARA signature scanning (malware, cryptominers, attack tools), add the `yara` extra:

```bash
pip install setup-eval[yara]
```

### From source

```bash
git clone https://github.com/redhat-community-ai-tools/harness-eval-lab.git
cd harness-eval-lab
uv sync
```

### As a Claude Code plugin

Install directly from within Claude Code:

```
/plugin marketplace add redhat-community-ai-tools/harness-eval-lab
/plugin install setup-eval@setup-eval
/reload-plugins
```

**Updating:** Re-run the install command periodically to get the latest rules and improvements. Follow the [repository](https://github.com/redhat-community-ai-tools/harness-eval-lab) for release announcements.

### For Cursor users

Install the CLI:

```bash
pip install setup-eval
setup-eval setup-eval-lint /path/to/your/project
```

To use the commands inside Cursor, copy the `.cursor/commands/` directory from this repo into your project's `.cursor/commands/`. The 4 eval commands will appear in Cursor's command palette:
- `setup-eval-lint` - fast static analysis (no LLM)
- `setup-eval-review` - full LLM review
- `setup-eval-security` - deep security audit
- `setup-eval-skill` - deep-evaluate one skill

Or test locally during development:

```bash
claude --plugin-dir /path/to/setup-eval
```

After installing, these commands become available in `/` autocomplete:
- `/setup-eval:setup-eval-lint` - fast static analysis, no LLM, CI-suitable
- `/setup-eval:setup-eval-review` - full qualitative review with KEEP/REVIEW/REMOVE verdicts
- `/setup-eval:setup-eval-security` - deep security audit with deterministic scan + semantic review
- `/setup-eval:eval-skill <skill-name>` - deep-evaluate one skill in context

## Usage

### CLI

```bash
setup-eval setup-eval-lint /path/to/project
setup-eval setup-eval-lint /path/to/project --preset strict --format json
setup-eval setup-eval-lint /path/to/project --fail-on-error

export GEMINI_API_KEY=your-key  # or ANTHROPIC_API_KEY
setup-eval setup-eval-review /path/to/project
setup-eval setup-eval-review /path/to/project --provider anthropic --model claude-sonnet-4-20250514

setup-eval setup-eval-security /path/to/project
setup-eval setup-eval-security /path/to/project --review --provider gemini

setup-eval eval-skill /path/to/skills/my-skill --context /path/to/project
setup-eval eval-skill /path/to/skills/my-skill --context /path/to/project --rubric
```

**Note on `/setup-eval-security`:** The YARA signature scanning check requires `yara-python`. If not installed, the YARA check is skipped automatically and the report notes it. All other security checks run without extra dependencies. To enable YARA scanning:

```bash
pip install setup-eval[yara]
```

## CLI Commands

| Command | Description | Needs LLM? |
|---------|-------------|------------|
| `setup-eval-lint` | 39 deterministic rules + system analysis (budget, triggers, deps, context utilization). | No |
| `setup-eval-review` | Per-component rubric review, 21 cross-type checks, KEEP/REVIEW/REMOVE verdicts. | Yes (API key) |
| `setup-eval-security` | All security rules + YARA + CVE lookups + optional LLM semantic review. | Optional (`--review`) |
| `setup-eval-skill` | Deep-evaluate a single skill individually and in context of the setup. | Optional (`--rubric`) |

## Plugin Skills

| Skill | Description | Needs LLM? |
|-------|-------------|------------|
| `/setup-eval-lint` | 43 rules, system analysis. Fast, CI-suitable. | No |
| `/setup-eval-review` | Per-component rubrics, 21 cross-type checks, KEEP/REVIEW/REMOVE verdicts. | Yes (Claude in-session) |
| `/setup-eval-security` | Deterministic security scan + semantic security review with 4-check checklist. | Yes (Claude in-session) |
| `/setup-eval-skill` | Deep-evaluate one skill against rubric + contextual analysis. | Yes (Claude in-session) |

## Inspection Rules (43)

| Category | Rules | What they check |
|----------|-------|-----------------|
| Structural | 1 | SKILL.md exists |
| Frontmatter | 3 | Description required/quality (POV, use-case, length), format valid |
| Content | 4 | Duplicate detection (TF-IDF), broken references, circular references, token budget |
| Security | 9 | Credential access, prompt injection (17 patterns), data exfiltration, obfuscation, reverse shells, AST behavioral analysis, taint tracking, MCP least-privilege, MCP tool poisoning |
| Security (opt-in) | 2 | YARA signature scanning, CVE lookups via OSV.dev (only in `setup-eval-security`) |
| Commands | 8 | Description, script exists, duplicates, credentials, injection, skill overlap, shadows built-in, references nonexistent skill |
| CLAUDE.md | 3 | Exists, skill duplication, generic advice detection |
| Hooks | 1 | Structure validation, dangerous patterns |
| Agents | 9 | Description, skills exist, tool format, constraint matching, credentials, injection, exfiltration, obfuscation, reverse shells |

Four presets: `recommended` (default), `strict`, `security`, `pre-workflow`.

## Future Plans

The [`future-plans/`](future-plans/) directory contains planned improvements, each in its own subfolder. Each doc explores a problem, presents approaches with trade-offs, and describes how to build it.

Every plan doc has a **Status** at the top:

| Status | Meaning |
|--------|---------|
| `future` | Idea documented, not yet planned for implementation |
| `in design` | Actively being designed, approaches being evaluated |
| `in progress` | Implementation underway |
| `built` | Implemented and merged |

| Plan | What it addresses |
|------|-------------------|
| [adjusting-to-dynamic-workflows](future-plans/adjusting-to-dynamic-workflows/) | Adapting to Claude Code's dynamic workflows (pre-flight checks, workflow evaluation, quality gates) |
| [test-coverage](future-plans/test-coverage/) | Expanding tests to cover all rules with edge cases |
| [runner-abstraction](future-plans/runner-abstraction/) | Evaluating setups for other agent tools (Cursor, Copilot, Windsurf) |
| [impact-dimension](future-plans/impact-dimension/) | Measuring whether a setup actually helps the agent (A/B testing) |
| [scoring-calibration](future-plans/scoring-calibration/) | Validating review accuracy against human judgment |
| [sarif-output](future-plans/sarif-output/) | SARIF output format for GitHub code scanning (inline PR annotations, Security tab alerts) |
| [security-benchmarks](future-plans/security-benchmarks/) | Benchmarking security rules against known-malicious and benign setups (TPR/FPR measurement) |
| [setup-recommend](future-plans/setup-recommend/) | Recommending missing components based on project stack profiling |

## Contributing

See [`how-to-contribute.md`](how-to-contribute.md) for guidelines on adding rules, future plans, and submitting PRs.

## Changelog

See [`CHANGELOG.md`](CHANGELOG.md) for release history and notable changes.
