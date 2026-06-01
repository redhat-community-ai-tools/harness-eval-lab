"""RubricScorer: score components via LLM-based rubric evaluation."""

from __future__ import annotations

import re

from harness_eval_lab.rubric.dimensions import DIMENSIONS_BY_TYPE
from harness_eval_lab.rubric.prompts import SYSTEM_PROMPT, build_scoring_prompt
from harness_eval_lab.rubric.types import DimensionDef, DimensionScore, RubricResult
from harness_eval_lab.utils.llm import LLMClient

_DIMENSION_RE = re.compile(
    r"DIMENSION:\s*(\S+)\s*\|\s*SCORE:\s*(\d)\s*\|\s*JUSTIFICATION:\s*(.+)"
)
_SUMMARY_RE = re.compile(r"SUMMARY:\s*(.+)")


class RubricScorer:
    def __init__(self, client: LLMClient) -> None:
        self.client = client

    def score(
        self,
        component_type: str,
        component_name: str,
        content: str,
        context: str | None = None,
        dimension_overrides: list[DimensionDef] | None = None,
    ) -> RubricResult:
        dimensions = dimension_overrides or DIMENSIONS_BY_TYPE.get(component_type, [])
        if not dimensions:
            return RubricResult(
                component_name=component_name,
                component_type=component_type,
                summary=f"No rubric dimensions defined for type '{component_type}'",
            )

        prompt = build_scoring_prompt(
            component_type=component_type,
            component_name=component_name,
            content=content,
            dimensions=dimensions,
            context=context,
        )

        response = self.client.generate(SYSTEM_PROMPT, prompt)
        return self._parse_response(response, component_name, component_type, dimensions)

    def _parse_response(
        self,
        response: str,
        component_name: str,
        component_type: str,
        dimensions: list[DimensionDef],
    ) -> RubricResult:
        dim_weights = {d.name: d.weight for d in dimensions}
        scores: list[DimensionScore] = []
        summary = ""

        for line in response.strip().split("\n"):
            line = line.strip()

            dim_match = _DIMENSION_RE.match(line)
            if dim_match:
                name = dim_match.group(1)
                score_val = int(dim_match.group(2))
                justification = dim_match.group(3).strip()
                score_val = max(1, min(5, score_val))
                weight = dim_weights.get(name, 0.0)
                scores.append(DimensionScore(
                    name=name,
                    score=score_val,
                    weight=weight,
                    justification=justification,
                ))
                continue

            sum_match = _SUMMARY_RE.match(line)
            if sum_match:
                summary = sum_match.group(1).strip()

        result = RubricResult(
            component_name=component_name,
            component_type=component_type,
            dimensions=scores,
            summary=summary,
        )
        result.compute_overall()
        return result
