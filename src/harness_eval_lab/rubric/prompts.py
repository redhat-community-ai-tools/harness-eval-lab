"""Prompt templates for LLM-based rubric issue detection."""

from __future__ import annotations

from harness_eval_lab.rubric.types import IssueCategory

SYSTEM_PROMPT = """\
You are an expert evaluator of AI agent configurations. \
You detect issues in components by checking specific categories. \
Be rigorous and evidence-based. Only report real issues, citing specific content. \
If a category has no issues, skip it."""

ISSUE_TEMPLATE = (
    "Check the following {component_type} for issues in each category listed below.\n"
    "\n"
    "## Component: {component_name}\n"
    "\n"
    "### Content:\n"
    "```\n"
    "{content}\n"
    "```\n"
    "\n"
    "{context_section}\n"
    "\n"
    "## Categories to check:\n"
    "\n"
    "{categories_section}\n"
    "\n"
    "## Response format:\n"
    "For each issue found, respond with EXACTLY this format (one per line):\n"
    "ISSUE: <short description> | CATEGORY: <category_name> "
    "| EVIDENCE: <cite specific content> | SUGGESTION: <concrete fix>\n"
    "\n"
    "If a category has no issues, do not output a line for it.\n"
    "\n"
    "After all issues, add:\n"
    "SUMMARY: <one sentence overall assessment>\n"
)


def build_issue_prompt(
    component_type: str,
    component_name: str,
    content: str,
    categories: list[IssueCategory],
    context: str | None = None,
) -> str:
    cats_text = "\n".join(
        f"- **{c.name}**: {c.description}" for c in categories
    )

    context_section = ""
    if context:
        context_section = f"### Context (other components in the setup):\n{context}\n"

    return ISSUE_TEMPLATE.format(
        component_type=component_type,
        component_name=component_name,
        content=content,
        context_section=context_section,
        categories_section=cats_text,
    )
