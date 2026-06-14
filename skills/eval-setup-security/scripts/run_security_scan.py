# /// script
# requires-python = ">=3.11"
# dependencies = ["harness-eval-lab"]
# ///
"""Run security-focused setup assessment and output JSON results."""

import json
import sys
from pathlib import Path


def main() -> None:
    setup_path = sys.argv[1] if len(sys.argv) > 1 else "."
    user_config = sys.argv[2] if len(sys.argv) > 2 and sys.argv[2] != "-" else None

    from harness_eval_lab.analysis.system import analyze_system
    from harness_eval_lab.config.presets import SECURITY
    from harness_eval_lab.core.setup import discover_setup
    from harness_eval_lab.inspection.engine import inspect_setup
    from harness_eval_lab.output.report import format_json

    setup = discover_setup(
        name=Path(setup_path).name, path=setup_path, user_config_dir=user_config
    )
    results = inspect_setup(setup, SECURITY)
    system = analyze_system(setup)

    output = json.loads(format_json(system, results))
    output["security_scan"] = True

    skip_notices = []
    for r in results:
        for d in r.diagnostics:
            if d.severity.value == "info" and d.rule_id in (
                "security/yara-signatures",
                "security/cve-lookup",
            ):
                skip_notices.append(d.message)

    if skip_notices:
        output["skip_notices"] = skip_notices

    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
