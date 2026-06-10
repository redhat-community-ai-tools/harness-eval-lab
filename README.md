# harness-eval-lab

Evaluate AI agent setups across 5 dimensions: Soundness, Safety, Coherence, Efficiency, Impact.

## What it does

Most agent evaluation tools test whether a **skill** completes a task correctly. This tool evaluates the **entire setup** that surrounds the agent: CLAUDE.md, skills, commands, hooks, MCP configs, and sub-agents.

It evaluates setups across five dimensions: **Soundness** (does each piece work?), **Safety** (can any piece cause harm?), **Coherence** (do the pieces work together?), **Efficiency** (is the token budget well-distributed?), and **Impact** (does the setup actually help the agent?).

Two evaluation layers:

- **Layer 1 (`lint`):** 26 deterministic Python rules + system-level analysis (token budget, trigger overlaps, dependencies, context utilization). No LLM. Fast. Good for CI.
- **Layer 2 (`review`):** LLM-based qualitative review. Per-component rubric scoring, 21 cross-type optimization checks, KEEP/REVIEW/REMOVE verdicts. Works in CLI (via API key) and as a Claude Code plugin (in-session).

## Install

```bash
uv sync
```

With LLM support (for `review` and `eval-skill --rubric`):

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

# Layer 2: LLM rubric scoring per component (requires API key)
export GEMINI_API_KEY=your-key  # or ANTHROPIC_API_KEY
harness-eval-lab eval-setup-review /path/to/project
harness-eval-lab eval-setup-review /path/to/project --provider anthropic --model claude-sonnet-4-20250514

# Deep-evaluate one skill (with setup context)
harness-eval-lab eval-skill /path/to/skills/my-skill --context /path/to/project
harness-eval-lab eval-skill /path/to/skills/my-skill --context /path/to/project --rubric
```

### As a Claude Code plugin

Install by adding the plugin directory, then use:

- `/eval-setup-lint` - Layer 1: fast static analysis (no LLM)
- `/eval-setup-review` - Layer 2: full qualitative review with KEEP/REVIEW/REMOVE verdicts
- `/eval-skill <skill-name>` - deep-evaluate one skill in context

## CLI Commands

| Command | Description |
|---------|-------------|
| `eval-setup-lint` | Layer 1: 26 rules + system analysis (budget, triggers, dependencies, context utilization). No LLM, CI-suitable. |
| `eval-setup-review` | Layer 2: LLM rubric scoring per component. Requires API key. |
| `eval-skill` | Deep-evaluate a single skill individually and in context |

## Plugin Skills

| Skill | Description |
|-------|-------------|
| `/eval-setup-lint` | Layer 1 only: 26 rules, system analysis. No LLM, fast, CI-suitable. |
| `/eval-setup-review` | Layer 2 + Layer 1 context: per-component qualitative review, 21 cross-type checks, KEEP/REVIEW/REMOVE verdicts. |
| `/eval-skill` | Layer 1 + Layer 2: deep-evaluate one skill with individual rubric + contextual analysis |

## Inspection Rules (26)

| Category | Rules | What they check |
|----------|-------|-----------------|
| Structural | 1 | SKILL.md exists |
| Frontmatter | 3 | Description required/quality (POV, use-case, length), format valid |
| Content | 3 | Duplicate detection (TF-IDF), broken references, token budget |
| Security | 2 | Credential access, prompt injection (17 patterns) |
| Commands | 7 | Description, script exists, duplicates, credentials, injection, skill overlap, shadows built-in |
| CLAUDE.md | 3 | Exists, skill duplication, generic advice detection |
| Hooks | 1 | Structure validation, dangerous patterns |
| Agents | 6 | Description, skills exist, tool format, constraint matching, credentials, injection |

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
| [impact-dimension](future-plans/impact-dimension/) | Measuring whether a setup actually helps the agent (A/B testing, activation rates) |
| [adjusting-to-dynamic-workflows](future-plans/adjusting-to-dynamic-workflows/) | Adapting to Claude Code's dynamic workflows (pre-flight checks, workflow evaluation, quality gates) |
| [scoring-calibration](future-plans/scoring-calibration/) | Validating score thresholds against real-world setups |
| [test-coverage](future-plans/test-coverage/) | Expanding tests to cover all 26 rules with edge cases |

## Contributing

See [`how-to-contribute.md`](how-to-contribute.md) for guidelines on adding rules, future plans, and submitting PRs.
