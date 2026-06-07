---
name: eval-skill
description: Deep-evaluate a single skill with static analysis and qualitative rubric scoring, both individually and in context of the full setup. Use when the user wants to check if a specific skill is worth keeping, well-built, or redundant.
allowed-tools:
  - Bash
  - Read
---

# Evaluate Skill

Deep-evaluate a single skill using two layers: static analysis (Layer 1) and qualitative rubric scoring (Layer 2), both individually and in context of the full setup.

## Hard Rules

1. **Never give a verdict without running the rubric.** Read the actual file content and score all rubric dimensions before assigning a star rating or verdict.
2. **Every dimension must have a score and justification.** Both the individual rubric AND the contextual analysis must be fully scored before the verdict.
3. **Read before you judge.** Read the actual SKILL.md content (and reference files if they exist) to evaluate quality.
4. **Don't manufacture problems.** If the skill is good, say so. Only recommend changes that make a real difference.
5. **Always end with a short summary.**

## Step 1: Select the Skill

Determine the skill path. If the user says a skill name, find it under `skills/<name>/SKILL.md`.

## Step 2: Run Layer 1 (Static Analysis)

Determine the setup context path (usually the current working directory).

```bash
uv run python skills/eval-skill/scripts/run_skill_eval.py <skill-path> <context-path> recommended
```

If no context path, pass `-` as the second argument.

Read the JSON output. It contains diagnostics, token count, and contextual findings from Layer 1.

## Step 3: Read Actual Files (Layer 2 Preparation)

Read the skill's actual content:
1. The SKILL.md file
2. All files in the skill's subdirectories (reference files). Score the COMBINED content.
3. The skill's guidelines.md (if it exists)

Also read for context (don't score these, they're context for evaluating the target skill):
4. All OTHER skill SKILL.md files in the workspace
5. CLAUDE.md
6. Hooks in .claude/settings.json

## Step 4: Individual Rubric (Layer 2)

Read `rubric/skills-rubric.md` for dimension definitions and scoring criteria.

Score the skill on all 5 dimensions with one-sentence justifications citing specific evidence from the skill content.

Calculate overall: round(specificity*0.25 + redundancy*0.25 + trigger*0.20 + efficiency*0.15 + quality*0.15)

Verdict: **KEEP** (4-5 stars), **REVIEW** (3 stars), **REMOVE** (1-2 stars)

## Step 5: Contextual Analysis (Layer 2)

Read `rubric/contextual-analysis.md` and evaluate all 5 contextual dimensions.

Check redundancy against three sources:
- Claude's default behavior (generic advice = redundant)
- Other skills in the workspace (overlap = partially redundant)
- CLAUDE.md content (duplication = wasted tokens)

## Step 6: Produce the Report

Read `report-format.md` for the full report structure.

The report must include:
- Layer 1 results (rule checklist with PASS/FAIL)
- Layer 2 individual rubric (all 5 dimensions scored)
- Layer 2 contextual analysis (all 5 dimensions rated)
- +/!/x sections (good, improve, broken)
- Final verdict with suggestions
