from __future__ import annotations

from harness_eval_lab.inspection.types import Rule, RuleCategory

_registry: dict[str, Rule] = {}


def register_rule(rule: Rule) -> None:
    if rule.meta.id in _registry:
        raise ValueError(f'Rule "{rule.meta.id}" already registered')
    _registry[rule.meta.id] = rule


def get_all_rules() -> list[Rule]:
    return list(_registry.values())


def get_rules_by_category(category: RuleCategory) -> list[Rule]:
    return [r for r in _registry.values() if r.meta.category == category]


def get_rule(rule_id: str) -> Rule | None:
    return _registry.get(rule_id)


def clear_rules() -> None:
    _registry.clear()
