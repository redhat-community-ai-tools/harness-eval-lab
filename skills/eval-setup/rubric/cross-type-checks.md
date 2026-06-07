# Cross-Type Optimization Checks

Answer each of the 21 checks with YES or NO and a one-line explanation. Do not skip any.

## Transformations (1-11)

1. **Skill -> Hook:** If a skill contains rules that MUST happen every time without exception, that's a hook, not a skill. Skills are advisory (~80% adherence). Hooks are deterministic (100%). Test: "If Claude ignores this instruction, would something break?" If yes, it should be a hook.

2. **Skill -> Command:** If a skill describes a specific workflow the user triggers explicitly (e.g., "audit my code", "deploy to staging"), it should be a command. Skills are for passive behavior. Commands are for active actions.

3. **Command -> Skill:** If a command describes general behavior that should always be active, it should be a skill that auto-triggers.

4. **Skill content -> CLAUDE.md:** If a skill contains rules that apply to EVERY conversation (e.g., "always use uv", "never commit .env"), those belong in CLAUDE.md.

5. **CLAUDE.md content -> Skill:** If CLAUDE.md contains domain-specific rules that only matter sometimes, those waste context in every session. Move to a skill.

6. **CLAUDE.md content -> Hook:** If CLAUDE.md says "always run tests before committing" but Claude sometimes forgets, make it a hook.

7. **Agent <-> Skill consistency:** Do agent's referenced skills exist? Do agent's instructions conflict with the referenced skill's instructions? Is the agent duplicating content already in its skills?

8. **Agent <-> Agent overlap:** Do multiple agents share large blocks of identical text? If so, extract to a shared skill.

9. **Agent <-> CLAUDE.md:** Are there rules in CLAUDE.md that should be in agent definitions, or vice versa?

10. **Skill structure optimization:** For skills with SKILL.md over ~800 tokens containing detailed procedures: recommend splitting into thin SKILL.md + reference files (progressive disclosure).

11. **Guidelines extraction:** For skills with hard limits inline (MUST/NEVER/ALWAYS) but no guidelines.md: recommend extracting. Not a requirement, just a recommendation.

## Setup-Wide (12-18)

12. **Merge candidates:** Skills covering related topics that would be stronger combined.

13. **Overlapping triggers:** Skills whose descriptions might cause multiple to load unnecessarily.

14. **Coverage gaps:** Obvious missing areas based on what's present.

15. **Total context budget:** Sum all tokens, warn if >20% of context window.

16. **Redundancy across types:** Same instruction appearing in CLAUDE.md AND a skill (double token cost).

17. **Conflicts across types:** CLAUDE.md says one thing, a skill says the opposite.

18. **Command shadows built-in:** Does any command share a name with a Claude Code built-in (init, review, security-review, help, clear, compact, config, cost, doctor, login, logout, memory, model, permissions, status, vim)?

## Behavioral Patterns (19-21)

19. **Mandate stacking:** Count skills with coercive language (MUST, ALWAYS, NEVER) in descriptions or hard gates in body. If >2 skills mandate pre-conditions, they create competing demands. Flag and suggest making most advisory.

20. **Autonomy erosion:** If skills intercept broad work categories AND contain hard gates, the user loses control. Flag broad-trigger + hard-gate combinations.

21. **Broad trigger collision:** Multiple skills with overlapping broad triggers waste context by loading redundant instructions.

## Output format

```
### Transformations
  1. Skill -> Hook:               [YES/NO] - [one-line explanation]
  2. Skill -> Command:            [YES/NO] - [one-line explanation]
  3. Command -> Skill:            [YES/NO] - [one-line explanation]
  4. Skill content -> CLAUDE.md:  [YES/NO] - [one-line explanation]
  5. CLAUDE.md -> Skill:          [YES/NO] - [one-line explanation]
  6. CLAUDE.md -> Hook:           [YES/NO] - [one-line explanation]
  7. Agent <-> Skill:             [YES/NO] - [one-line explanation]
  8. Agent <-> Agent:             [YES/NO] - [one-line explanation]
  9. Agent <-> CLAUDE.md:         [YES/NO] - [one-line explanation]
  10. Skill structure:            [YES/NO] - [which skills and why]
  11. Guidelines extraction:      [YES/NO] - [which skills and why]

### Setup-Wide
  12. Merge candidates:           [YES/NO] - [which or "none"]
  13. Overlapping triggers:       [YES/NO] - [which or "none"]
  14. Coverage gaps:              [YES/NO] - [what's missing or "none"]
  15. Total context budget:       [tokens] ([pct]%) - [OK/WARNING]
  16. Redundancy across types:    [YES/NO] - [what or "none"]
  17. Conflicts across types:     [YES/NO] - [what or "none"]
  18. Command shadows built-in:   [YES/NO] - [which or "none"]

### Behavioral Patterns
  19. Mandate stacking:           [YES/NO] - [how many, acceptable?]
  20. Autonomy erosion:           [YES/NO] - [which or "none"]
  21. Broad trigger collision:    [YES/NO] - [which or "none"]
```
