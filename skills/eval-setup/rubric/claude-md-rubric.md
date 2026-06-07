# CLAUDE.md Rubric

Score on 5 dimensions. Include a one-sentence justification citing specific evidence.

## Conciseness (weight 0.25)

Can each line pass "would removing this cause Claude to make mistakes?" Ruthlessly prune.

## Signal-to-noise (weight 0.25)

Only contains things Claude can't figure out from code? No generic advice like "write clean code", "be helpful", "follow best practices", "think step by step"? These waste tokens every session. Also check: no standard language conventions (use linters instead), no detailed API docs (link instead), no file-by-file descriptions.

## Skill separation (weight 0.20)

Domain-specific rules are in skills (on-demand), not CLAUDE.md (every session)? If CLAUDE.md contains rules that only matter for specific tasks, they should be skills.

## Structure (weight 0.15)

Clear sections? Critical rules marked? Scannable? Headers and organization that let Claude find information quickly.

## Conflict-free (weight 0.15)

No contradictions with any skill? Check that CLAUDE.md rules don't say the opposite of what a skill says.

## Scoring

Overall = round(conciseness*0.25 + signal_to_noise*0.25 + skill_separation*0.20 + structure*0.15 + conflict_free*0.15)

Verdict: **KEEP** (4-5), **REVIEW** (3), **REMOVE** (1-2)
