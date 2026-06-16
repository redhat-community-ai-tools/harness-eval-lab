# Security Audit Report Format

## Header

```
# Security Audit: [setup name]
```

## Summary

| Metric | Value |
|--------|-------|
| Components scanned | N |
| Checks run | N |
| Checks skipped | N |
| Errors | N |
| Warnings | N |
| Semantic issues | N |
| **Risk Assessment** | **SAFE / CAUTION / UNSAFE** |

Risk levels:
- **SAFE**: No errors, no warnings, no semantic issues
- **CAUTION**: Warnings present but no errors
- **UNSAFE**: One or more errors found

## Deterministic Findings

Group by component. For each component with findings:

```
### [type]/[name]

| Rule | Severity | Message |
|------|----------|---------|
| rule-id | error/warning | message |
```

If a component has no findings, omit it (don't list "PASS" entries in a security report).

## Semantic Security Review

For each component reviewed semantically, list findings:

```
### [type]/[name]

**[category]**: Description of finding.
- Evidence: what was found
- Recommendation: what to do about it
```

If no semantic issues found, write: "Semantic review found no additional issues beyond the deterministic scan."

## Skipped Checks

List any checks that were skipped and why:

```
- YARA signatures: yara-python not installed (pip install yara-python)
- CVE lookups: no dependency files found
```

If nothing was skipped, omit this section.
