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
    result = subprocess.run(
        [sys.executable, "chaos_cli.py", str(script), "--json"],
        capture_output=True,
        text=True,
        cwd=repo_root,
        check=True,
    )

    lines = [line for line in result.stdout.splitlines() if line.strip()]
    assert any("structured_core" in line for line in lines)


def test_complete_build_runs_without_warnings(tmp_path):
    repo_root = Path(__file__).resolve().parents[1]
    output_path = tmp_path / "chaos_digest.md"
    result = subprocess.run(
        [
            sys.executable,
            "chaos_language.complete_build.py",
            "--output",
            str(output_path),
        ],
        capture_output=True,
        text=True,
        cwd=repo_root,
        check=True,
    )

    assert output_path.exists()
    assert result.stderr.strip() == ""

