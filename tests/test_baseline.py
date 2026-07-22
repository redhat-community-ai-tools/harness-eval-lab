"""Tests for baseline snapshot and filtering."""

from __future__ import annotations

from harness_eval.baseline import create_baseline, filter_baselined
from harness_eval.inspection.types import (
    Finding,
    InspectionResult,
    Location,
    RuleCategory,
    Severity,
)


def _make_finding(rule_id: str, file: str, message: str) -> Finding:
    return Finding(
        rule_id=rule_id,
        severity=Severity.ERROR,
        message=message,
        location=Location(file=file, start_line=1),
        category=RuleCategory.SECURITY,
    )


def _make_result(findings: list[Finding]) -> InspectionResult:
    return InspectionResult(
        target_path="/tmp/test",
        target_name="test-skill",
        tokens=100,
        diagnostics=findings,
        error_count=len(findings),
    )


class TestCreateBaseline:
    def test_captures_findings(self) -> None:
        f1 = _make_finding("security/cred", "skill.md", "cred access")
        f2 = _make_finding("security/exfil", "skill.md", "data exfil")
        result = _make_result([f1, f2])
        baseline = create_baseline([result])

        assert baseline["version"] == "1.0"
        assert len(baseline["findings"]) == 2
        assert all(
            "rule_id" in f and "file" in f and "message_hash" in f for f in baseline["findings"]
        )

    def test_empty_results_produce_empty_baseline(self) -> None:
        result = _make_result([])
        baseline = create_baseline([result])
        assert baseline["findings"] == []


class TestFilterBaselined:
    def test_removes_known_findings(self) -> None:
        f1 = _make_finding("security/cred", "skill.md", "cred access")
        results = [_make_result([f1])]
        baseline = create_baseline(results)

        filtered = filter_baselined(results, baseline)
        assert all(len(r.diagnostics) == 0 for r in filtered)

    def test_keeps_new_findings(self) -> None:
        f1 = _make_finding("security/cred", "skill.md", "cred access")
        baseline = create_baseline([_make_result([f1])])

        f2 = _make_finding("security/exfil", "other.md", "new finding")
        new_results = [_make_result([f1, f2])]

        filtered = filter_baselined(new_results, baseline)
        remaining = [d for r in filtered for d in r.diagnostics]
        assert len(remaining) == 1
        assert remaining[0].message == "new finding"

    def test_empty_baseline_keeps_all(self) -> None:
        f1 = _make_finding("security/cred", "skill.md", "cred access")
        results = [_make_result([f1])]
        baseline = {"version": "1.0", "findings": []}

        filtered = filter_baselined(results, baseline)
        remaining = [d for r in filtered for d in r.diagnostics]
        assert len(remaining) == 1

    def test_recalculates_counts(self) -> None:
        f1 = _make_finding("security/cred", "skill.md", "cred access")
        f2 = _make_finding("security/exfil", "other.md", "data exfil")
        results = [_make_result([f1, f2])]
        baseline = create_baseline([_make_result([f1])])

        filtered = filter_baselined(results, baseline)
        assert filtered[0].error_count == 1
