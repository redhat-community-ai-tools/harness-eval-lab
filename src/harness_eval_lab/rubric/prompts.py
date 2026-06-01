"""Prompt templates for LLM-based rubric scoring."""

from __future__ import annotations

from harness_eval_lab.rubric.types import DimensionDef

SYSTEM_PROMPT = """\
You are an expert evaluator of AI agent configurations. \
You score components on specific dimensions using a 1-5 scale. \
Be rigorous and evidence-based. Every score must cite specific content from the component."""

SCORE_TEMPLATE = """\
Score the following {component_type} on each dimension listed below.

## Component: {component_name}

### Content:
```
{content}
```

{context_section}

## Dimensions to score (1-5 each):

{dimensions_section}

## Response format:
For each dimension, respond with EXACTLY this format (one per line):
DIMENSION: <name> | SCORE: <1-5> | JUSTIFICATION: <one sentence citing specific evidence>

After all dimensions, add:
SUMMARY: <one sentence overall assessment>
"""


def build_scoring_prompt(
    component_type: str,
    component_name: str,
    content: str,
    dimensions: list[DimensionDef],
    context: str | None = None,
) -> str:
    dims_text = "\n".join(
        f"- **{d.name}** (weight {d.weight}): {d.description}" for d in dimensions
    )

    context_section = ""
    if context:
        context_section = f"### Context (other components in the setup):\n{context}\n"

    return SCORE_TEMPLATE.format(
        component_type=component_type,
        component_name=component_name,
        content=content,
        context_section=context_section,
        dimensions_section=dims_text,
    )
