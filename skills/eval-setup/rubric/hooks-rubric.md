# Hooks Rubric

For each hook, check:

## Safety

No dangerous patterns (rm -rf, force push, curl|bash)? Is the hook read-only or does it modify state?

## Reliability

Does the referenced script/command exist? Is the command well-formed?

## Scope

Is this the right mechanism? Hooks are deterministic (100% execution). If the behavior is advisory, it should be in CLAUDE.md or a skill instead. Hooks are for things that MUST happen every time.

## Performance

Is the hook fast? Does it block the user? Non-blocking async hooks are preferred for advisory behavior.
