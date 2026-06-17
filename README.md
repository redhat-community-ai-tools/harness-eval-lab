# setup-eval

[![CI](https://github.com/redhat-community-ai-tools/harness-eval-lab/actions/workflows/ci.yml/badge.svg)](https://github.com/redhat-community-ai-tools/harness-eval-lab/actions/workflows/ci.yml)
[![PyPI](https://img.shields.io/pypi/v/setup-eval)](https://pypi.org/project/setup-eval/)
[![Python 3.11+](https://img.shields.io/badge/python-3.11%2B-blue)](https://www.python.org/downloads/)
[![License: Apache 2.0](https://img.shields.io/badge/license-Apache%202.0-green)](LICENSE)

Evaluate AI agent setups for best practices, redundancy, security, and cross-component issues.

Works with **Claude Code** and **Cursor**. Auto-detects which tool(s) a project uses.

## Install

```bash
pip install setup-eval
```

For YARA malware signature scanning, add: `pip install setup-eval[yara]`

## What it does

Most tools test whether a skill produces correct output. This tool checks the setup itself: CLAUDE.md, skills, commands, hooks, MCP configs, agents, `.cursor/rules/*.mdc`, `.cursorrules`.

Four commands, same engine:

| Command | What it does | Needs LLM? |
|---------|-------------|------------|
| `setup-eval-lint` | 43 deterministic rules + system analysis (token budget, trigger overlaps, dependencies). Fast, CI-suitable. | No |
| `setup-eval-review` | Per-component rubric review, 21 cross-type checks. KEEP/REVIEW/REMOVE verdicts. | Yes |
| `setup-eval-security` | All security rules + YARA + CVE lookups + 4-check semantic review. SAFE/CAUTION/UNSAFE. | Optional |
| `setup-eval-skill` | Deep-evaluate one skill individually and in context of the full setup. | Optional |

## How to use it

### CLI

```bash
setup-eval setup-eval-lint .
setup-eval setup-eval-lint . --preset strict --format json --fail-on-error

setup-eval setup-eval-review . --provider gemini
setup-eval setup-eval-security . --review
setup-eval setup-eval-skill ./skills/my-skill --context . --rubric
```

Requires `GEMINI_API_KEY` or `ANTHROPIC_API_KEY` for review/security/skill commands.

### Claude Code (plugin)

```
/plugin marketplace add redhat-community-ai-tools/harness-eval-lab
/plugin install setup-eval@setup-eval
/reload-plugins
```

After installing, use from the `/` menu: `/setup-eval:setup-eval-lint`, `/setup-eval:setup-eval-review`, `/setup-eval:setup-eval-security`, `/setup-eval:setup-eval-skill`. No API key needed; Claude evaluates in-session.

**Updating:** Re-run the install command to get the latest rules.

### Cursor

```bash
pip install setup-eval
```

Copy `.cursor/commands/` from [this repo](https://github.com/redhat-community-ai-tools/harness-eval-lab) into your project. The 4 commands appear in Cursor's command palette: `/setup-eval-lint`, `/setup-eval-review`, `/setup-eval-security`, `/setup-eval-skill`. No API key needed; Cursor evaluates in-session.

## Inspection Rules (43)

| Category | Rules | What they check |
|----------|-------|-----------------|
| Structural | 1 | SKILL.md exists |
| Frontmatter | 3 | Description required/quality, format valid |
| Content | 4 | Duplicate detection (TF-IDF), broken references, circular references, token budget |
| Security | 9 | Credential access, prompt injection (17 patterns), data exfiltration, obfuscation, reverse shells, AST analysis, taint tracking, MCP least-privilege, tool poisoning |
| Security (opt-in) | 2 | YARA signatures, CVE lookups via OSV.dev |
| Commands | 8 | Description, script exists, duplicates, credentials, injection, skill overlap, shadows built-in, references nonexistent skill |
| CLAUDE.md | 3 | Exists, skill duplication, generic advice detection |
| Hooks | 1 | Structure validation, dangerous patterns, network access |
| Agents | 9 | Description, skills exist, tool format, constraint matching, credentials, injection, exfiltration, obfuscation, reverse shells |

Four presets: `recommended` (default), `strict`, `security`, `pre-workflow`.

## Contributing

See [`how-to-contribute.md`](how-to-contribute.md) for adding rules and submitting PRs.

## Changelog

See [`CHANGELOG.md`](CHANGELOG.md) for release history.

## Future Plans

See [`future-plans/`](future-plans/) for planned improvements (SARIF output, security benchmarks, runner abstraction, dynamic workflows, impact measurement).
