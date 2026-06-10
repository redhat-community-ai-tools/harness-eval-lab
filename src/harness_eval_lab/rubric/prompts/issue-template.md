Check the following {component_type} for issues in each category listed below.

## Component: {component_name}

### Content:
```
{content}
```

{context_section}

## Categories to check:

{categories_section}

## Preferred response format (JSON)

Respond with a JSON block. Wrap it in ```json ... ``` fences.

```json
{{
  "issues": [
    {{
      "description": "short description of the issue",
      "category": "category_name",
      "severity": "error|warning|info",
      "evidence": "cite specific content from the component",
      "suggestion": "concrete fix"
    }}
  ],
  "summary": "one sentence overall assessment",
  "verdict": "KEEP|REVIEW|REMOVE"
}}
```

If there are no issues, return an empty `"issues"` array.

VERDICT meanings: KEEP = solid, no significant issues. REVIEW = has issues worth fixing. REMOVE = actively harmful or pure noise.

## Alternative format (if JSON is not possible)

For each issue found, respond with EXACTLY this format (one per line, no wrapping):
ISSUE: <short description> | CATEGORY: <category_name> | SEVERITY: <error/warning/info> | EVIDENCE: <cite specific content> | SUGGESTION: <concrete fix>

If a category has no issues, do not output a line for it.

After all issues, add exactly one of:
VERDICT: KEEP | REVIEW | REMOVE
SUMMARY: <one sentence overall assessment>

## Examples

JSON example (issues found):
```json
{{
  "issues": [
    {{"description": "Restates default git knowledge", "category": "redundancy", "severity": "warning", "evidence": "Always commit with descriptive messages", "suggestion": "Remove; Claude already writes descriptive commit messages"}},
    {{"description": "References nonexistent script", "category": "script_integrity", "severity": "error", "evidence": "Run ./scripts/deploy.sh but file does not exist", "suggestion": "Create the script or remove the reference"}}
  ],
  "summary": "Useful command with two fixable issues; worth keeping after corrections.",
  "verdict": "REVIEW"
}}
```

JSON example (clean):
```json
{{
  "issues": [],
  "summary": "Well-structured skill with clear triggers and actionable patterns.",
  "verdict": "KEEP"
}}
```

Text example (issues found):
ISSUE: Restates default git knowledge | CATEGORY: redundancy | SEVERITY: warning | EVIDENCE: "Always commit with descriptive messages" | SUGGESTION: Remove; Claude already writes descriptive commit messages
ISSUE: References nonexistent script | CATEGORY: script_integrity | SEVERITY: error | EVIDENCE: "Run ./scripts/deploy.sh" but file does not exist | SUGGESTION: Create the script or remove the reference
VERDICT: REVIEW
SUMMARY: Useful command with two fixable issues; worth keeping after corrections.

Text example (clean):
VERDICT: KEEP
SUMMARY: Well-structured skill with clear triggers and actionable patterns.
