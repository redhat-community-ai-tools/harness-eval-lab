"""RubricChecker: detect issues in components via LLM-based evaluation."""

from __future__ import annotations

import re

from harness_eval_lab.rubric.dimensions import CATEGORIES_BY_TYPE
from harness_eval_lab.rubric.prompts import SYSTEM_PROMPT, build_issue_prompt
from harness_eval_lab.rubric.types import IssueCategory, RubricIssue, RubricResult
from harness_eval_lab.utils.llm import LLMClient

_ISSUE_RE = re.compile(
    r"ISSUE:\s*(.+?)\s*\|\s*CATEGORY:\s*(\S+)\s*\|\s*EVIDENCE:\s*(.+?)\s*\|\s*SUGGESTION:\s*(.+)"
)
_SUMMARY_RE = re.compile(r"SUMMARY:\s*(.+)")


class RubricChecker:
    def __init__(self, client: LLMClient) -> None:
        self.client = client

    def check(
        self,
        component_type: str,
        component_name: str,
        content: str,
        context: str | None = None,
        category_overrides: list[IssueCategory] | None = None,
    ) -> RubricResult:
        categories = category_overrides or CATEGORIES_BY_TYPE.get(component_type, [])
        if not categories:
            return RubricResult(
                component_name=component_name,
                component_type=component_type,
                summary=f"No issue categories defined for type '{component_type}'",
            )

        prompt = build_issue_prompt(
            component_type=component_type,
            component_name=component_name,
            content=content,
            categories=categories,
            context=context,
        )

        response = self.client.generate(SYSTEM_PROMPT, prompt)
        return self._parse_response(response, component_name, component_type)

    def _parse_response(
        self,
        response: str,
        component_name: str,
        component_type: str,
    ) -> RubricResult:
        issues: list[RubricIssue] = []
        summary = ""

        for line in response.strip().split("\n"):
            line = line.strip()

            issue_match = _ISSUE_RE.match(line)
            if issue_match:
                issues.append(RubricIssue(
                    description=issue_match.group(1).strip(),
                    category=issue_match.group(2).strip(),
                    evidence=issue_match.group(3).strip(),
                    suggestion=issue_match.group(4).strip(),
                ))
                continue

            sum_match = _SUMMARY_RE.match(line)
            if sum_match:
                summary = sum_match.group(1).strip()

        return RubricResult(
            component_name=component_name,
            component_type=component_type,
            issues=issues,
            summary=summary,
        )
