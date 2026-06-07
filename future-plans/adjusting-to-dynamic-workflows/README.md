# Adjusting to Dynamic Workflows

> **Status:** future
> **Jira:** n/a

## The landscape shift

Claude Code introduced dynamic workflows: the agent writes and runs its own multi-agent orchestration code at runtime. Instead of a fixed setup with static skills, Claude generates a JavaScript workflow that spawns subagents, routes them to different models, and coordinates their outputs using patterns like fan-out, adversarial verification, and tournaments.

This changes the role of the static setup (CLAUDE.md, skills, hooks, commands). It doesn't replace it. It builds on top of it. Every subagent spawned by a workflow still operates within the environment defined by the static setup. The skills it references, the rules in CLAUDE.md, the hooks that gate execution. If the foundation is broken, the workflow multiplies those problems across every subagent.

This means harness evaluation becomes more important in the dynamic workflow era, not less.

## Four directions

Each file in this folder explores one way harness-eval-lab could adapt. They range from near-term (pre-flight checks, quality gates) to ambitious (workflow evaluation, impact measurement).

| Direction | File | Complexity | Value |
|-----------|------|-----------|-------|
| Pre-flight check | [preflight-check.md](preflight-check.md) | Low | High |
| Skills quality gate | [skills-quality-gate.md](skills-quality-gate.md) | Low | High |
| Evaluating generated workflows | [evaluate-generated-workflows.md](evaluate-generated-workflows.md) | High | Medium |
| Impact measurement via workflows | [impact-via-workflows.md](impact-via-workflows.md) | High | High |

**Recommended order:** Start with the two low-complexity, high-value items (pre-flight and quality gate). They use existing infrastructure. Then tackle impact measurement, which connects to [../impact-dimension/](../impact-dimension/). Workflow evaluation is the most speculative and can wait.

## Open questions that span all four directions

- How does harness-eval-lab discover that a dynamic workflow is about to run? (Hook? API? File watcher?)
- Should the tool evaluate workflows at design time (before they run) or runtime (as they execute)?
- How to handle the cost question? Workflows already use significant tokens. Adding evaluation on top increases cost. Should there be a "light" vs "full" mode?
