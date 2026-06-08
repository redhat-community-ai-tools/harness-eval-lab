"""Tests for rubric issue detection with mocked LLM."""

from __future__ import annotations

from harness_eval_lab.rubric.scorer import RubricChecker


class MockLLMWithIssues:
    def generate(self, system: str, prompt: str) -> str:
        return (
            "ISSUE: Vague instructions in lines 5-8 | CATEGORY: specificity | EVIDENCE: 'be thorough and helpful' is generic advice | SUGGESTION: Replace with concrete patterns like 'always use raise from'\n"
            "ISSUE: Duplicates Claude default | CATEGORY: redundancy | EVIDENCE: 'write clean code' on line 3 | SUGGESTION: Remove this line\n"
            "SUMMARY: Skill has specificity and redundancy issues."
        )


class MockLLMClean:
    def generate(self, system: str, prompt: str) -> str:
        return "SUMMARY: Well-built skill with no issues."


def test_rubric_checker_finds_issues() -> None:
    checker = RubricChecker(MockLLMWithIssues())
    result = checker.check(
        component_type="skill",
        component_name="code-review",
        content="---\nname: code-review\ndescription: Review code\n---\n\nReview code.",
    )

    assert result.component_name == "code-review"
    assert result.component_type == "skill"
    assert len(result.issues) == 2
    assert result.issues[0].category == "specificity"
    assert result.issues[0].description == "Vague instructions in lines 5-8"
    assert result.issues[0].evidence
    assert result.issues[0].suggestion
    assert result.issues[1].category == "redundancy"
    assert result.summary


def test_rubric_checker_clean_component() -> None:
    checker = RubricChecker(MockLLMClean())
    result = checker.check(
        component_type="skill",
        component_name="good-skill",
        content="---\nname: good-skill\ndescription: Does something unique\n---\n\nSpecific instructions.",
    )

    assert result.issues == []
    assert "no issues" in result.summary.lower()


def test_rubric_checker_unknown_type() -> None:
    checker = RubricChecker(MockLLMClean())
    result = checker.check(
        component_type="unknown_thing",
        component_name="test",
        content="test content",
    )

    assert result.issues == []
    assert "No issue categories" in result.summary


def test_rubric_issue_fields() -> None:
    checker = RubricChecker(MockLLMWithIssues())
    result = checker.check(
        component_type="skill",
        component_name="test",
        content="test content",
    )

    for issue in result.issues:
        assert issue.category
        assert issue.description
        assert issue.evidence
        assert issue.suggestion
        assert issue.severity == "warning"
