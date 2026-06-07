# Report Format

## Structure

```
## How This Evaluation Works

This report evaluates the Claude Code setup across 5 dimensions:

- **Soundness** - Does each piece work? Are files valid, references real, descriptions present?
- **Safety** - Can any piece cause harm? Credential exposure, injection risk, dangerous hooks?
- **Coherence** - Do the pieces work together? Duplicates, conflicts, broken dependencies?
- **Efficiency** - Is the token budget well-distributed? Always-loaded vs on-demand?
- **Impact** - Does the setup actually help the agent? (Qualitative assessment)

Two layers produce the evidence:

**Layer 1 (Static Analysis)** runs 26 deterministic rules. No AI involved.
**Layer 2 (Qualitative Scoring)** Claude reads every file and evaluates quality,
redundancy, and coherence across the whole setup.

---

## 5-Dimension Scorecard

| Dimension | Score | Verdict | Key Evidence |
|-----------|-------|---------|-------------|
| Soundness | [N]/5 | [verdict] | [one-line summary] |
| Safety | [N]/5 | [verdict] | [one-line summary] |
| Coherence | [N]/5 | [verdict] | [one-line summary] |
| Efficiency | [N]/5 | [verdict] | [one-line summary] |
| Impact | [N]/5 | [verdict] | [one-line summary] |
| **Overall** | [N]/5 | [verdict] | |

Verdicts: HEALTHY (4-5), NEEDS WORK (3), PROBLEMATIC (1-2)

Scoring guide:
- **Soundness:** Based on Layer 1 structural/frontmatter errors. All pass = 5. Some errors = 3. Many errors = 1.
- **Safety:** Based on Layer 1 security findings + Layer 2 review of sensitive patterns. No issues = 5.
- **Coherence:** Based on duplicates, conflicts, trigger overlaps, broken dependencies, cross-type issues.
- **Efficiency:** Based on token budget ratio (always-loaded vs on-demand), heaviest component, trigger overlaps.
- **Impact:** Based on Layer 2 qualitative assessment. Does each component teach Claude something it doesn't already know? Would removing any component change Claude's behavior?

---

## Inventory

| Type | Count | Total Tokens | Errors | Warnings |
|------|-------|-------------|--------|----------|
| Skills | [N] | [N] | [N] | [N] |
| Commands | [N] | [N] | [N] | [N] |
| CLAUDE.md | [N] | [N] | [N] | [N] |
| Hooks | [N] | [N] | [N] | [N] |
| Agents | [N or 0] | [N] | [N] | [N] |

## Token Budget

  Always-loaded (CLAUDE.md, hooks): [N] tokens ([pct]%)
  On-demand (skills, commands, agents): [N] tokens ([pct]%)

  By type:
    [type]    [tokens] tokens ([pct]%)

---

## Per-Component Analysis

For each component, provide:

### component-name                              [stars]    [VERDICT]
  Tokens: [N]
  Type: [skill/command/agent/claude_md/hooks]

  Layer 1: [pass/fail checklist for relevant rules]

  Layer 2 Assessment:
    [2-3 sentences: what this component does, whether it adds value,
    whether it's well-built. Reference specific content.]

  + What's good
  ! What could improve
  x What's broken (from Layer 1 errors)

For clean components with no issues, use a compact one-line format:
### component-name                              [stars]    KEEP
  Tokens: [N] | Layer 1: all pass | [one-line assessment]

---

## Cross-Type Optimization

[All 21 checks from cross-type-checks.md, answered YES/NO with one-line explanation]

---

## Suggestions

[Numbered actionable items. Each is one line. Only recommend changes
that make a real difference.]
```

## Terminal Summary

Always print this at the end:

```
## Evaluation Summary

[stars] [overall score]/5 - [one-sentence verdict]

| Dimension | Score |
|-----------|-------|
| Soundness | [N]/5 |
| Safety | [N]/5 |
| Coherence | [N]/5 |
| Efficiency | [N]/5 |
| Impact | [N]/5 |

Reviewed [N] skills, [M] commands, CLAUDE.md, [H] hooks, [A] agents.
Total: [tokens] tokens.
Cross-type: [count]/21 checks flagged.

Suggestions:
  1. [one-line]
  2. [one-line]
  3. [one-line]
```
