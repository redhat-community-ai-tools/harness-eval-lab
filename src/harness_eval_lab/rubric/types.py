"""Types for rubric scoring."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class DimensionDef:
    """Definition of a scoring dimension."""

    name: str
    weight: float
    description: str


@dataclass
class DimensionScore:
    """Score for a single dimension."""

    name: str
    score: int  # 1-5
    weight: float
    justification: str


@dataclass
class RubricResult:
    """Complete rubric scoring result for a component."""

    component_name: str
    component_type: str
    dimensions: list[DimensionScore] = field(default_factory=list)
    overall: float = 0.0
    verdict: str = ""  # KEEP, REVIEW, REMOVE
    summary: str = ""

    def compute_overall(self) -> None:
        if not self.dimensions:
            return
        self.overall = sum(d.score * d.weight for d in self.dimensions)
        rounded = round(self.overall)
        if rounded >= 4:
            self.verdict = "KEEP"
        elif rounded == 3:
            self.verdict = "REVIEW"
        else:
            self.verdict = "REMOVE"
