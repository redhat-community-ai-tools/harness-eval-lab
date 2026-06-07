---
name: eval-setup
description: Evaluate the full agent setup (CLAUDE.md, skills, commands, hooks, agents, MCP configs) with static analysis and qualitative rubric scoring. Use when the user wants to check their setup health, find redundancy, detect issues, or get a quality report.
allowed-tools:
  - Bash
  - Read
---

# Evaluate Setup

Evaluate the user's full agent setup using two layers: static analysis (Layer 1) and qualitative rubric scoring (Layer 2).

## Hard Rules

1. **Never give a verdict without running the rubric.** Read the actual file content and score all rubric dimensions before assigning a star rating or verdict. Layer 1 error/warning counts are input data, not the verdict.
2. **Every item must have a full rubric score block.** Every skill, command, agent, CLAUDE.md, and hook MUST have all dimensions scored with one-sentence justifications. No exceptions.
3. **Read before you judge.** Do not summarize based on Layer 1 output alone. Read the actual file content to evaluate quality, clarity, and redundancy.
4. **Don't manufacture problems.** If the setup is good, say so. Only recommend changes that would make a real difference. "You could trim 50 tokens" is not a real recommendation.
5. **Always end with a short summary.** The last thing the user sees must be the terminal summary.

## Step 1: Run Layer 1 (Static Analysis)

Determine the setup path. If the user doesn't specify one, use the current working directory.

```bash
uv run python skills/eval-setup/scripts/run_assessment.py <setup-path> recommended
```

Read the JSON output. This gives you per-component diagnostics with rule IDs, severities, token counts, budget analysis, trigger overlaps, and dependency findings.

## Step 2: Read Actual Files (Layer 2 Preparation)

Read the actual content of:
1. Every skill file (SKILL.md) in the setup. If a skill has reference files in subdirectories, read those too and score the COMBINED content.
2. Every command file (command.md or flat .md files in commands/)
3. Every agent file (.md files in .claude/agents/)
4. The CLAUDE.md file(s)
5. The hooks in .claude/settings.json

You need the actual content to evaluate quality, redundancy, and coherence.

## Step 3: Score Each Component (Layer 2)

For each component, read the actual file content (Step 2), then apply the rubric.

### Skills
Read `rubric/skills-rubric.md` for dimension definitions and scoring criteria.
Score each skill on all 5 dimensions with one-sentence justifications.

### CLAUDE.md
Read `rubric/claude-md-rubric.md` for dimension definitions.
Score on all 5 dimensions.

### Commands
Read `rubric/commands-rubric.md` for dimension definitions.
Score each command on all 7 dimensions. For clean commands, use a compact one-line format.

### Agents
Read `rubric/agents-rubric.md` for dimension definitions.
Score each agent on all 5 dimensions.

### Hooks
Read `rubric/hooks-rubric.md` for what to check.
Evaluate each hook on safety, reliability, scope, and performance.

### Scoring formula
Overall = round(weighted sum of dimensions). Weights are in each rubric file.
Verdict: **KEEP** (4-5 stars), **REVIEW** (3 stars), **REMOVE** (1-2 stars).

## Step 4: Cross-Type Optimization

Read `rubric/cross-type-checks.md` and answer all 21 checks explicitly with YES or NO and a one-line explanation. Do not skip any check.

This is where you look at the whole setup and suggest transformations between types: should a skill be a hook? Can two skills be merged? Is CLAUDE.md duplicating skill content?

## Step 5: Produce the Report

Read `report-format.md` for the full report structure.

The report must include:
- Inventory table (component counts, tokens, errors, warnings)
- Per-component sections with Layer 1 checklist + Layer 2 rubric scores
- Cross-type optimization (all 21 checks)
- Numbered suggestions (actionable items only)
- Terminal summary (always printed last)

If the user asks follow-up questions, use the data to answer specifically. Reference exact components, token counts, and rule IDs.
