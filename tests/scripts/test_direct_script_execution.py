"""Tests that repo scripts can run directly without manual PYTHONPATH."""

import os
import subprocess
import sys
from pathlib import Path

SCRIPT_PATHS = [
    "scripts/run_audit.py",
    "scripts/access_probe.py",
    "scripts/access_probe_summarize.py",
    "scripts/run_weekly.py",
    "scripts/export_audit_reports.py",
    "scripts/export_longitudinal_summary.py",
    "scripts/export_research_package.py",
]


def test_consent_audit_scripts_show_help_without_pythonpath() -> None:
    env = os.environ.copy()
    env.pop("PYTHONPATH", None)

    for script_path in SCRIPT_PATHS:
        result = subprocess.run(
            [sys.executable, script_path, "--help"],
            cwd=Path.cwd(),
            env=env,
            capture_output=True,
            text=True,
            timeout=10,
            check=False,
        )

        assert result.returncode == 0, f"{script_path} failed:\n{result.stderr}"
