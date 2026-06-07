# Measuring Impact: Does the Setup Actually Help?

> **Status:** future

## The problem

The tool can tell you a setup is well-structured, secure, and efficient. But none of that answers the most important question: does it make the agent better at its job?

A setup can pass every rule, have perfect token distribution, and zero security issues, while every skill contains generic advice Claude already follows by default. The setup looks great on paper but does nothing. We need a way to measure whether the setup changes the agent's behavior for the better.

This is the hardest problem in the project and the most valuable to solve.

## Why existing checks can't answer this

Layer 1 (the 26 rules) checks structure and syntax. It can verify that a description exists, that references aren't broken, that there's no prompt injection. But it cannot read a skill and determine whether the instructions would actually change what Claude does. That requires running Claude on a real task and observing the difference.

Layer 2 (Claude reading the files and scoring rubric dimensions) gets closer. Claude can judge whether instructions are "specific" or "redundant with defaults." But that's still a prediction. The only way to know for sure is to test it empirically.

## Approaches explored

### Approach 1: A/B probe tasks

Run the agent on the same task twice: once with the setup loaded, once without. Compare the outputs using a judge.

**How it works:**
1. Define 3-5 small tasks that exercise different aspects of a setup (fix a bug, add a test, explain a function, review code, debug an error)
2. For each task, spawn two subagents: Agent A with the full setup, Agent B with nothing
3. Spawn a judge agent that compares both outputs on 5 dimensions (accuracy, specificity, actionability, completeness, response quality)
4. Impact score = win rate of Agent A across all tasks

**Trade-offs:**
- Most direct measurement of impact
- Expensive: each probe = 3 LLM calls minimum (2 agents + 1 judge)
- Non-deterministic: same task can produce different results each run
- Tasks must be portable across different projects (or customizable per project)
- The judge itself can be biased (longer responses tend to score higher)

**Mitigation for bias:** Use blind judging (the judge doesn't know which response had the setup) and dimension-based scoring (not "which is better overall" but "which is more accurate, more specific, etc.")

### Approach 2: Skill activation rate

Instead of testing task completion quality, test whether skills actually get triggered. Feed the agent a prompt that should activate each skill and check if it does.

**How it works:**
1. For each skill, generate a prompt that matches the skill's description (e.g., for a "data-pipeline" skill, the prompt might be "help me build a data pipeline")
2. Check if Claude loads the skill in response to that prompt
3. Skills that never activate have zero impact regardless of their content quality

**Trade-offs:**
- Much cheaper than A/B testing (one prompt per skill)
- Only measures activation, not whether the skill helps once activated
- Doesn't require a judge
- Can be gamed by overly broad descriptions (skill activates but doesn't help)

### Approach 3: Differential analysis

Remove one component at a time and observe the effect.

**How it works:**
1. Run the full setup through Layer 1 + Layer 2
2. For each component, create a variant setup with that component removed
3. Re-run the analysis on the variant
4. If removing a component doesn't change anything, it has no measurable impact

**Trade-offs:**
- Works with existing infrastructure (no new LLM calls needed for Layer 1)
- Only measures impact on other components, not on task completion
- Cheap and deterministic
- Good for identifying truly dead components but poor at measuring positive impact

## Recommended direction

Start with **Approach 1 (A/B probe tasks)** but in the simplest possible form:
- 3 tasks, not 5
- 1 judge call per task, not 3
- Simple win/loss/tie verdict, not weighted dimension scoring
- Run it via a dynamic workflow (see [adjusting-to-dynamic-workflows/impact-via-workflows.md](../adjusting-to-dynamic-workflows/impact-via-workflows.md))

Use **Approach 2 (activation rate)** as a cheap pre-screen: if a skill never activates, skip the expensive A/B test.

**Approach 3** is useful but insufficient on its own. Keep it as a complement.

## How to build it

**Where it lives:** `src/harness_eval_lab/experiment/` (create the package)

**What to build:**
1. A `ProbeTask` dataclass: task description, target repo path, expected skill activation
2. A set of 3 default probe tasks (review, write, debug) that work on any repo
3. A `run_probe` function that spawns two subagents and a judge
4. A `compute_impact` function that aggregates probe results into a 1-5 score
5. Integration with `eval-setup` plugin (not CLI) via an `--with-impact` flag or a separate step in the SKILL.md protocol

**Entry point for the plugin:**
```
Step N: Measure Impact (optional, expensive)
If the user asks for impact measurement, run the probe tasks.
Read `experiment/probes.md` for task definitions.
For each probe, spawn agents and judge results.
```

## Open questions

- Should probe tasks be generic (work on any project) or customizable per project?
- How many probe runs are needed to get a stable signal? (Non-determinism means one run might not be enough)
- What's an acceptable cost per evaluation? (3 probes x 3 LLM calls = 9 calls minimum)
- Should the judge be the same model as the agents, or a different one?
- How to handle projects with no test repo available?
