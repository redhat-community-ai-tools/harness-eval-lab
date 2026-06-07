# harness-eval-lab

Evaluate AI agent setups across 5 dimensions: Soundness, Safety, Coherence, Efficiency, Impact.

## What it does

Most agent evaluation tools test whether a **skill** completes a task correctly. This tool evaluates the **entire setup** that surrounds the agent: CLAUDE.md, skills, commands, hooks, MCP configs, and sub-agents.

It evaluates setups across five dimensions: **Soundness** (does each piece work?), **Safety** (can any piece cause harm?), **Coherence** (do the pieces work together?), **Efficiency** (is the token budget well-distributed?), and **Impact** (does the setup actually help the agent?).

Two evaluation modes:

- **`eval-setup`**: Evaluate the full setup. Inspects all components, runs system-level analysis (token budget, trigger overlaps, dependencies), and produces a 5-dimension scorecard.
- **`eval-skill`**: Deep-evaluate a single skill, both individually (is it well-built?) and in context of the setup (is it redundant? does it overlap?).

## Install

```bash
uv sync
```

With LLM support (for rubric scoring in `eval-skill`):

```bash
uv sync --extra llm
```

## Usage

### As a CLI

```bash
# Evaluate the full setup
harness-eval-lab eval-setup /path/to/project

# Deep-evaluate one skill (with setup context)
harness-eval-lab eval-skill /path/to/skills/my-skill --context /path/to/project

# Quick static scan (no LLM, fast, good for CI)
harness-eval-lab scan /path/to/project
harness-eval-lab scan /path/to/project --preset strict --format json
```

### As a Claude Code plugin

Install by adding the plugin directory, then use:

- `/eval-setup` - evaluate the full setup, get a 5-dimension scorecard
- `/eval-skill <skill-name>` - deep-evaluate one skill in context

## CLI Commands

| Command | Description |
|---------|-------------|
| `eval-setup` | Full setup evaluation: inspect + system analysis + 5-dimension scorecard |
| `eval-skill` | Deep-evaluate a single skill individually and in context |
| `scan` | Quick static analysis (26 rules, no LLM, deterministic) |

## Plugin Skills

| Skill | Description |
|-------|-------------|
| `/eval-setup` | Evaluate the full agent setup, present scorecard conversationally |
| `/eval-skill` | Deep-evaluate a single skill with contextual analysis |

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

## Rubric Dimensions

Scoring dimensions per component type (weights sum to 1.0):

- **Skills:** Specificity, Redundancy, Trigger Quality, Token Efficiency, Content Quality
- **Commands:** Description, Instruction Clarity, Script Integrity, Scope, Token Efficiency, Redundancy, Robustness
- **CLAUDE.md:** Conciseness, Signal-to-Noise, Skill Separation, Structure, Conflict-Free
- **Agents:** Specificity, Constraint Clarity, Zero-Trust Integrity, Token Efficiency, Content Quality
- **Hooks:** Safety, Reliability, Scope, Performance

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
