import os
import subprocess
import sys
from pathlib import Path


def test_cli_executes_sn_file(tmp_path):
    script = tmp_path / "ritual.sn"
    script.write_text(
        """
        [EVENT]: memory
        [EMOTION:JOY:7]
        { Warm day. }
        """.strip()
    )

    repo_root = Path(__file__).resolve().parents[1]
    env = os.environ.copy()
    env["PYTHONPATH"] = str(repo_root / "src")
    result = subprocess.run(
        [sys.executable, "scripts/chaos_cli.py", str(script), "--json"],
        capture_output=True,
        text=True,
        cwd=repo_root,
        env=env,
        check=True,
    )

    lines = [line for line in result.stdout.splitlines() if line.strip()]
    assert any("structured_core" in line for line in lines)


def test_complete_build_runs_without_warnings(tmp_path):
    repo_root = Path(__file__).resolve().parents[1]
    script_path = repo_root / "src" / "chaos_language" / "complete_build.py"
    assert script_path.exists(), "Complete-build script is missing"

    output_path = tmp_path / "chaos_digest.md"
    env = os.environ.copy()
    env.setdefault("PYTHONWARNINGS", "error")

    result = subprocess.run(
        [
            sys.executable,
            str(script_path.relative_to(repo_root)),
            "--output",
            str(output_path),
        ],
        capture_output=True,
        text=True,
        cwd=repo_root,
        env=env,
        check=True,
    )

    assert output_path.exists()
    assert result.stderr.strip() == ""
    combined = (result.stdout + result.stderr).lower()
    assert "warning" not in combined

