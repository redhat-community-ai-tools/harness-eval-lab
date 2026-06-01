"""Tests for rubric scoring with mocked LLM."""

from __future__ import annotations

from harness_eval_lab.rubric.scorer import RubricScorer


class MockLLMClient:
    def generate(self, system: str, prompt: str) -> str:
        return (
            "DIMENSION: specificity | SCORE: 4 | JUSTIFICATION: Instructions are concrete with specific patterns\n"
            "DIMENSION: redundancy | SCORE: 3 | JUSTIFICATION: Some overlap with built-in behavior\n"
            "DIMENSION: trigger_quality | SCORE: 5 | JUSTIFICATION: Clear 'use when' phrasing\n"
            "DIMENSION: token_efficiency | SCORE: 4 | JUSTIFICATION: Good ratio at 34 tokens\n"
            "DIMENSION: content_quality | SCORE: 3 | JUSTIFICATION: Basic structure, no examples\n"
            "SUMMARY: Solid skill with room to reduce redundancy and add examples."
        )


def test_rubric_scorer_skill() -> None:
    scorer = RubricScorer(MockLLMClient())
    result = scorer.score(
        component_type="skill",
        component_name="code-review",
        content="---\nname: code-review\ndescription: Review code\n---\n\nReview code.",
    )

    assert result.component_name == "code-review"
    assert result.component_type == "skill"
    assert len(result.dimensions) == 5
    assert result.overall > 0
    assert result.verdict in ("KEEP", "REVIEW", "REMOVE")
    assert result.summary


def test_rubric_scorer_weighted_average() -> None:
    scorer = RubricScorer(MockLLMClient())
    result = scorer.score(
        component_type="skill",
        component_name="test",
        content="test content",
    )

    expected = 4 * 0.25 + 3 * 0.25 + 5 * 0.20 + 4 * 0.15 + 3 * 0.15
    assert abs(result.overall - expected) < 0.01


def test_rubric_scorer_unknown_type() -> None:
    scorer = RubricScorer(MockLLMClient())
    result = scorer.score(
        component_type="unknown_thing",
        component_name="test",
        content="test content",
    )

    assert result.dimensions == []
    assert "No rubric dimensions" in result.summary


def test_rubric_verdict_keep() -> None:
    scorer = RubricScorer(MockLLMClient())
    result = scorer.score(
        component_type="skill",
        component_name="test",
        content="test",
    )
    assert result.verdict == "KEEP"


class LowScoreLLM:
    def generate(self, system: str, prompt: str) -> str:
        return (
            "DIMENSION: specificity | SCORE: 1 | JUSTIFICATION: Vague\n"
            "DIMENSION: redundancy | SCORE: 1 | JUSTIFICATION: Duplicates defaults\n"
            "DIMENSION: trigger_quality | SCORE: 2 | JUSTIFICATION: Too broad\n"
            "DIMENSION: token_efficiency | SCORE: 1 | JUSTIFICATION: Bloated\n"
            "DIMENSION: content_quality | SCORE: 1 | JUSTIFICATION: No structure\n"
            "SUMMARY: Should be removed."
        )


def test_rubric_verdict_remove() -> None:
    scorer = RubricScorer(LowScoreLLM())
    result = scorer.score(
        component_type="skill",
        component_name="bad-skill",
        content="do stuff",
    )
    assert result.verdict == "REMOVE"
