# Commands Rubric

Score each command on 7 dimensions. For clean commands, use a compact one-line format. For commands with issues, use the full format with per-dimension scores.

## Description quality (weight 0.20)

Clear, concise description for the UI menu?

## Instruction clarity (weight 0.20)

Claude knows exactly what to do, in what order?

## Script integrity (weight 0.15)

Referenced scripts exist? Discovery pattern works?

## Scope appropriateness (weight 0.10)

Should this be a command (user-triggered) or a skill (auto-triggered)? Commands are for explicit actions (/review, /deploy). Skills are for passive behavior (whenever you write Python, do X).

## Token efficiency (weight 0.10)

Concise or bloated?

Command size thresholds:
- Under 15KB: Fine
- 15-30KB: Recommend splitting. Score at most 2/5.
- Over 30KB: Strong recommendation to split. Score at most 1/5.

## Redundancy with defaults (weight 0.15)

Does Claude already do this without the command? Claude has built-in plan mode, generates commit messages, explains code, and reviews code by default. A command is only justified if it adds specific rules, constraints, or structure. Test: "if i deleted this command, could i get the same result by just asking Claude?" If yes, it's redundant.

## Robustness (weight 0.10)

Does the command handle edge cases? Does it hardcode assumptions (specific tools, languages, thresholds)? Does it gracefully handle missing dependencies?

## Scoring

Overall = round(description*0.20 + clarity*0.20 + script*0.15 + scope*0.10 + efficiency*0.10 + redundancy*0.15 + robustness*0.10)

Verdict: **KEEP** (4-5), **REVIEW** (3), **REMOVE** (1-2)
