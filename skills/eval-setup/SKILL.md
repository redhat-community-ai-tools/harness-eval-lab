---
name: eval-setup
description: Evaluate the full agent setup (CLAUDE.md, skills, commands, hooks, agents, MCP configs) across 5 dimensions with static analysis and qualitative scoring. Use when the user wants to check their setup health, find redundancy, detect issues, or get a quality report.
allowed-tools:
  - Bash
  - Read
---

# Evaluate Setup

Evaluate the user's full agent setup across 5 dimensions: **Soundness, Safety, Coherence, Efficiency, Impact.**

Uses two layers: static analysis (Layer 1, deterministic) and qualitative scoring (Layer 2, Claude reads every file).

## Hard Rules

1. **Never give a verdict without reading the files.** Layer 1 counts are input data, not the verdict. A component with warnings can still be healthy.
2. **Read before you judge.** Read every file's actual content before scoring.
3. **Don't manufacture problems.** If the setup is good, say so.
4. **Always end with the 5-dimension scorecard and summary.**

## Step 1: Run Layer 1 (Static Analysis)

Determine the setup path. If the user doesn't specify one, use the current working directory.

```bash
uv run python skills/eval-setup/scripts/run_assessment.py <setup-path> recommended
```

Read the JSON output. This gives you per-component diagnostics, token budget, trigger overlaps, and dependency findings.

## Step 2: Read Actual Files (Layer 2)

Read the actual content of every component: SKILL.md files (including reference files in subdirectories), command files, agent files, CLAUDE.md, and settings.json for hooks.

## Step 3: Analyze Each Component

For each component, provide:
- Layer 1 results (which rules passed/failed)
- A 2-3 sentence qualitative assessment (what it does, whether it adds value, whether it's well-built)
- +/!/x notes (good, improve, broken)
- Per-component verdict: KEEP, REVIEW, or REMOVE

Use the per-component rubric files for detailed criteria:
- Skills: read `rubric/skills-rubric.md`
- CLAUDE.md: read `rubric/claude-md-rubric.md`
- Commands: read `rubric/commands-rubric.md`
- Agents: read `rubric/agents-rubric.md`
- Hooks: read `rubric/hooks-rubric.md`

## Step 4: Cross-Type Optimization

Read `rubric/cross-type-checks.md` and answer all 21 checks with YES/NO and a one-line explanation. These check whether components should be transformed (skill to hook?), merged, or removed.

## Step 5: Score the 5 Dimensions

Based on everything from Steps 1-4, score the setup on 5 dimensions (1-5 each):

**Soundness:** Does each piece work? Based on Layer 1 structural/frontmatter errors. All components parse correctly, have required fields, references resolve.

**Safety:** Can any piece cause harm? Based on Layer 1 security findings + Layer 2 review. No credential exposure, no injection patterns, no dangerous hooks, agent constraints are enforced.

**Coherence:** Do the pieces work together? Based on duplicates, conflicts between components, trigger overlaps, broken dependencies, cross-type issues from Step 4.

**Efficiency:** Is the token budget well-distributed? Based on always-loaded vs on-demand ratio, heaviest component, trigger overlaps causing unnecessary loading, monolithic skills that should use progressive disclosure.

**Impact:** Does the setup actually help the agent? Based on Layer 2 qualitative assessment. Does each component teach Claude something it doesn't already know? Would removing any component change Claude's behavior? Are descriptions specific enough to trigger correctly?

## Step 6: Produce the Report

Read `report-format.md` for the full report structure. The report must include:
1. The 5-dimension scorecard (the headline)
2. Inventory table
3. Token budget breakdown
4. Per-component analysis (Layer 1 + Layer 2)
5. Cross-type optimization (21 checks)
6. Numbered suggestions
7. Terminal summary with the scorecard
