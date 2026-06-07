# Agents Rubric

Score each agent on 5 dimensions. Include a one-sentence justification citing specific evidence.

## Specificity (weight 0.25)

- 1: Entirely vague: "implement the fix", "review the code", no concrete procedure
- 3: Mix of specific phases and vague steps
- 5: Every phase has specific steps, concrete rules, defined output format

## Constraint clarity (weight 0.25)

- 1: No constraints stated, agent can do anything
- 3: Constraints exist in body and disallowedTools but with gaps
- 5: Body constraints and disallowedTools form a coherent, complete security boundary; every "cannot" in the body is backed by enforcement; scope is explicitly bounded ("you do X, you do not do Y, Z, or W")

## Zero-trust integrity (weight 0.20)

- 1: No mention of input trust; agent blindly follows issue text or PR descriptions
- 3: States zero-trust principle but verification steps are inconsistent
- 5: Explicit zero-trust section; all external inputs treated as untrusted; concrete verification steps; injection-like patterns in input are flagged rather than followed

## Token efficiency (weight 0.15)

- 1: >5,000 tokens with low value density
- 3: Under 3,000 tokens, some padding
- 5: Every token earns its place; procedures delegated to skills (not inlined), no repeated boilerplate across agents

## Content quality (weight 0.15)

- 1: No structure, no output format, no failure handling
- 3: Decent structure; output format defined but incomplete; failure handling vague
- 5: Clear sections (identity, inputs, constraints, procedure, output, failure); output format with schema; exit codes documented; handoff contract explicit

## Scoring

Overall = round(specificity*0.25 + constraint_clarity*0.25 + zero_trust*0.20 + efficiency*0.15 + quality*0.15)

Verdict: **KEEP** (4-5), **REVIEW** (3), **REMOVE** (1-2)
