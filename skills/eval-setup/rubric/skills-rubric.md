# Skills Rubric

Score each skill on 5 dimensions. Include a one-sentence justification citing specific evidence.

## Specificity (weight 0.25)

- 1: Entirely vague platitudes, no actionable instructions
- 2: Mostly generic advice with one or two specific rules
- 3: Mix of specific and generic; some rules change Claude's behavior
- 4: Mostly specific, actionable instructions with concrete patterns
- 5: Every instruction is specific, actionable, includes concrete patterns or examples

## Redundancy (weight 0.25)

- 1: Every instruction duplicates Claude's default behavior
- 2: 75%+ is default behavior, very little unique value
- 3: Some unique value, but 50%+ is default behavior
- 4: Mostly unique, with minor overlap with Claude's defaults
- 5: Entirely unique, teaches Claude something it genuinely doesn't know

Things Claude already does by default (always redundant):
- "Write clean, readable code"
- "Be helpful and thorough"
- "Handle errors properly" (too vague to add value)
- "Follow best practices"
- "Use proper formatting"
- "Think step by step"
- "Consider edge cases"

A skill is NOT redundant if it provides specific, actionable rules. "Always use `raise from` for exception chaining in Python" is specific enough to change behavior.

Also check overlap with Claude's built-in capabilities: plan mode, code review, commit messages, code explanation. A skill that wraps a built-in without adding specific rules is redundant. Test: "if i deleted this skill, would Claude behave differently?" If not, it's redundant.

## Trigger quality (weight 0.20)

- 1: No description, or triggers on everything, or uses coercive language with broad scope
- 2: Description exists but too broad, too narrow, or uses coercive language
- 3: Reasonable but could be more precise
- 4: Good description that targets the right tasks most of the time
- 5: Precisely targets the right tasks; starts with "Use when"; doesn't overlap with other skills

Autonomy checks (score within trigger quality):
- **Coercive language:** "MUST use this", "ALWAYS use this before", "NEVER skip" in the description. Cap at 2/5 if the description mandates activation.
- **Hard gates:** "Do NOT proceed until", "STOP and do X first" in the body. Appropriate for narrow safety concerns, not broad workflows.
- **Broad intercept:** "any creative work", "all code changes", "every project". Skills claiming authority over entire categories will over-trigger.
- **Test:** "Could a reasonable user want to skip this skill and go straight to coding?" If yes, the trigger shouldn't prevent that.

## Token efficiency (weight 0.15)

- 1: >3,000 tokens with low value density
- 2: 2,000-3,000 tokens, or under 1,500 with very low value
- 3: Under 1,500 tokens, some padding that could be trimmed
- 4: Well-sized, minor optimization possible
- 5: Every token earns its place; high value-to-token ratio

Token budget applies to SKILL.md only (always-loaded cost). Reference files in subdirectories load on demand and cost zero tokens until read. If SKILL.md is over ~800 tokens and contains detailed procedures or tables, recommend splitting into thin SKILL.md + reference files (progressive disclosure).

## Content quality (weight 0.15)

- 1: No structure, no examples, broken references
- 2: Minimal structure, vague instructions
- 3: Decent structure, some examples, no broken references
- 4: Well-organized with examples and clear sections
- 5: Well-organized, includes examples, references valid files, covers edge cases

Additional checks (score within content quality):
- **Cognitive load:** For workflow-type skills, are steps digestible? Does any phase require synthesizing more than 3 inputs?
- **Error handling:** For skills that execute commands or call APIs, does the skill define what happens when something fails?
- **Guidelines separation:** If the skill contains hard limits inline (MUST/NEVER/ALWAYS) but has no `guidelines.md`, recommend extracting. Not a negative score, just a recommendation.

## Scoring

Overall = round(specificity*0.25 + redundancy*0.25 + trigger*0.20 + efficiency*0.15 + quality*0.15)

Verdict: **KEEP** (4-5 stars), **REVIEW** (3 stars), **REMOVE** (1-2 stars)
