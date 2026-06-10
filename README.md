# harness-eval-lab

Evaluate AI agent setups for best practices, redundancy, and cross-component issues.

## What it does

Most agent evaluation tools test whether a **skill** completes a task correctly. This tool evaluates the **entire setup** that surrounds the agent: CLAUDE.md, skills, commands, hooks, MCP configs, and sub-agents.

It checks whether each component follows Claude Code best practices, whether components work well together, and whether anything is redundant or conflicting.

Two evaluation layers:

- **Layer 1 (`lint`):** 35 deterministic Python rules + system-level analysis (token budget, trigger overlaps, dependencies, context utilization). No LLM. Fast. Good for CI.
- **Layer 2 (`review`):** LLM-based qualitative review. Checks each component against best practices, runs 21 cross-type optimization checks (should this skill be a hook? are these two commands redundant?), and flags conflicts and redundancy. Produces KEEP/REVIEW/REMOVE verdicts. Works in CLI (via API key) and as a Claude Code plugin (in-session).

## Install

```bash
uv sync
```

With LLM support (for `review` and `eval-skill --review`):

```bash
uv sync --extra llm
```

## Usage

### As a CLI

```bash
# Layer 1: static analysis + system analysis (no LLM, fast, CI-suitable)
harness-eval-lab eval-setup-lint /path/to/project
harness-eval-lab eval-setup-lint /path/to/project --preset strict --format json
harness-eval-lab eval-setup-lint /path/to/project --fail-on-error

# Layer 2: LLM-based review per component (requires API key)
export GEMINI_API_KEY=your-key  # or ANTHROPIC_API_KEY
harness-eval-lab eval-setup-review /path/to/project
harness-eval-lab eval-setup-review /path/to/project --provider anthropic --model claude-sonnet-4-20250514

# Deep-evaluate one skill (with setup context)
harness-eval-lab eval-skill /path/to/skills/my-skill --context /path/to/project
harness-eval-lab eval-skill /path/to/skills/my-skill --context /path/to/project --review
```

### As a Claude Code plugin

Install by adding the plugin directory, then use:

- `/eval-setup-lint` - Layer 1: fast static analysis (no LLM)
- `/eval-setup-review` - Layer 2: full qualitative review with KEEP/REVIEW/REMOVE verdicts
- `/eval-skill <skill-name>` - deep-evaluate one skill in context

## CLI Commands

| Command | Description |
|---------|-------------|
| `eval-setup-lint` | Layer 1: 35 rules + system analysis (budget, triggers, dependencies, context utilization). No LLM, CI-suitable. |
| `eval-setup-review` | Layer 2: LLM-based best-practices review per component. Requires API key. |
| `eval-skill` | Deep-evaluate a single skill individually and in context |

## Plugin Skills

| Skill | Description |
|-------|-------------|
| `/eval-setup-lint` | Layer 1 only: 35 rules, system analysis. No LLM, fast, CI-suitable. |
| `/eval-setup-review` | Layer 2 + Layer 1 context: best-practices review, 21 cross-type checks, redundancy/conflict detection, KEEP/REVIEW/REMOVE verdicts. |
| `/eval-skill` | Layer 1 + Layer 2: deep-evaluate one skill against best practices + contextual analysis |

## Inspection Rules (35)

| Category | Rules | What they check |
|----------|-------|-----------------|
| Structural | 1 | SKILL.md exists |
| Frontmatter | 3 | Description required/quality (POV, use-case, length), format valid |
| Content | 3 | Duplicate detection (TF-IDF), broken references, token budget |
| Security | 5 | Credential access, prompt injection (17 patterns), data exfiltration, obfuscation, reverse shells |
| Commands | 7 | Description, script exists, duplicates, credentials, injection, skill overlap, shadows built-in |
| CLAUDE.md | 3 | Exists, skill duplication, generic advice detection |
| Hooks | 1 | Structure validation, dangerous patterns |
| Agents | 9 | Description, skills exist, tool format, constraint matching, credentials, injection |

Three additional security rules were added for data exfiltration (webhooks, DNS tunneling, base64 piping), obfuscation detection (eval+decode, zero-width characters, unicode escapes), and reverse shell patterns.

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
| [test-coverage](future-plans/test-coverage/) | Expanding tests to cover all 35 rules with edge cases |
| [runner-abstraction](future-plans/runner-abstraction/) | Evaluating setups for other agent tools (Cursor, Copilot, Windsurf) |
| [impact-dimension](future-plans/impact-dimension/) | Measuring whether a setup actually helps the agent (A/B testing) |
| [scoring-calibration](future-plans/scoring-calibration/) | Validating review accuracy against human judgment |

## Contributing

See [`how-to-contribute.md`](how-to-contribute.md) for guidelines on adding rules, future plans, and submitting PRs.

## Changelog

See [`CHANGELOG.md`](CHANGELOG.md) for release history and notable changes.
