# Contextual Analysis

Evaluate the skill in context of the whole setup. Each dimension gets a severity rating.

## Overlap with other skills

**Rating:** NONE / MINOR / SIGNIFICANT

Does any other skill cover the same domain? How much content is shared? Name the overlapping skills and the specific shared content. Could they be merged?

## Conflict with CLAUDE.md

**Rating:** NONE / MINOR / SIGNIFICANT

Does the skill contradict anything in CLAUDE.md? Cite the specific conflicting instructions.

## Conflict with other skills

**Rating:** NONE / MINOR / SIGNIFICANT

Does this skill's advice conflict with another skill's? Name the skills and the contradiction.

## Type appropriateness

**Rating:** CORRECT / WRONG TYPE

Should this be a skill (auto-triggered), a command (user-triggered), or a hook (deterministic)?
- If the skill describes a user-triggered workflow -> should be a command
- If the skill contains rules that MUST happen every time -> should be a hook
- If the skill teaches passive behavior -> correct as a skill

## Structure optimization

**Rating:** OPTIMAL / COULD IMPROVE

- If SKILL.md is >800 tokens and monolithic: recommend splitting into thin SKILL.md + reference files
- If the skill has inline hard limits but no guidelines.md: recommend extracting

## Output format

```
### Contextual Analysis

  Overlap with other skills:   [NONE/MINOR/SIGNIFICANT] - [findings]
  Conflict with CLAUDE.md:     [NONE/MINOR/SIGNIFICANT] - [findings]
  Conflict with other skills:  [NONE/MINOR/SIGNIFICANT] - [findings]
  Type appropriateness:        [CORRECT/WRONG TYPE] - [assessment]
  Structure optimization:      [OPTIMAL/COULD IMPROVE] - [findings]
```
