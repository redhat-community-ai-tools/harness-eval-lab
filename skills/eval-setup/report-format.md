# Report Format

## Structure

```
## How This Evaluation Works

This report evaluates the Claude Code setup using two layers:

**Layer 1 (Static Analysis)** runs deterministically, no AI involved. A Python
tool scans every file and checks 26 mechanical rules: does the file exist? Does
the YAML parse? Are referenced files real? Are there prompt injection patterns?
Credential references? Dangerous commands?

**Layer 2 (Rubric Scoring)** uses Claude to read every file and score it on
weighted rubric dimensions. This is where qualitative judgment happens: is this
skill teaching something Claude doesn't already know? Is the description good
enough to trigger at the right time?

---

## Inventory

| Type | Count | Total Tokens | Errors | Warnings |
|------|-------|-------------|--------|----------|
| Skills | [N] | [N] | [N] | [N] |
| Commands | [N] | [N] | [N] | [N] |
| CLAUDE.md | [N] | [N] | [N] | [N] |
| Hooks | [N] | [N] | [N] | [N] |
| Agents | [N or 0] | [N] | [N] | [N] |

## Skills

### skill-name                              ####    VERDICT
  Tokens: [N]

  Layer 1:
    [For each rule, show pass/warning/error]

  Rubric:
    Specificity:      [score]/5  [justification]
    Redundancy:       [score]/5  [justification]
    Trigger quality:  [score]/5  [justification]
    Token efficiency: [score]/5  [justification]
    Content quality:  [score]/5  [justification]

  + What's good
  ! What could improve
  x What's broken

## Commands

[Same pattern per command. For clean commands use compact format:]

### command-name                            ####    VERDICT
  Tokens: [N]
  Layer 1: [pass/fail summary]
  Rubric: [compact one-line per dimension]

## Hooks

[Per hook: Layer 1 result + safety/reliability/scope assessment]

## CLAUDE.md

### CLAUDE.md                               ####    VERDICT
  Tokens: [N] | Lines: [N]
  Layer 1: [pass/fail]
  Rubric:
    Conciseness:      [score]/5  [justification]
    Signal-to-noise:  [score]/5  [justification]
    Skill separation: [score]/5  [justification]
    Structure:        [score]/5  [justification]
    Conflict-free:    [score]/5  [justification]

## Agents

### agent-name                              ####    VERDICT
  Tokens: [N]
  Layer 1: [pass/fail per rule]
  Rubric:
    Specificity:        [score]/5  [justification]
    Constraint clarity: [score]/5  [justification]
    Zero-trust:         [score]/5  [justification]
    Token efficiency:   [score]/5  [justification]
    Content quality:    [score]/5  [justification]

## Cross-Type Optimization

[All 21 checks from cross-type-checks.md]

## Suggestions

[Numbered actionable items. Each is one line. Only recommend changes
that make a real difference.]
```

## Terminal Summary

Always print this at the end, regardless of output length:

```
## Evaluation Summary

<One sentence overall verdict>
Reviewed <N> skills, <M> commands, CLAUDE.md, <H> hooks, <A> agents.
Total: <tokens> tokens.

Cross-type: <count>/21 checks flagged issues.

Suggestions:
  1. <one-line suggestion>
  2. <one-line suggestion>
  3. <one-line suggestion>
```

Keep each suggestion to one line. If the setup is healthy, it's fine to have
just 1-2 suggestions or zero. Don't pad.
