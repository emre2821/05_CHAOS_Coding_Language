import os
import subprocess
import sys
from pathlib import Path

import pytest


def run_command(
    args: list[str],
    repo_root: Path,
    env: dict[str, str],
    input_text: str | None = None,
    timeout: float = 30.0,
) -> subprocess.CompletedProcess:
    try:
        return subprocess.run(
            args,
            capture_output=True,
            input=input_text,
            text=True,
            cwd=repo_root,
            env=env,
            check=True,
            timeout=timeout,
        )
    except subprocess.TimeoutExpired as exc:
        stdout = exc.stdout or ""
        stderr = exc.stderr or ""
        pytest.fail(
            "Command timed out after "
            f"{timeout} seconds: {' '.join(map(str, args))}\n"
            f"stdout:\n{stdout}\n"
            f"stderr:\n{stderr}"
        )


@pytest.mark.parametrize(
    ("shim_script", "extra_args"),
    [
        ("chaos_cli.py", ["--json"]),
        ("chaos_exec.py", []),
    ],
)
@pytest.mark.slow
def test_cli_executes_sn_file(tmp_path, shim_script, extra_args):
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
    result = run_command(
        [sys.executable, "tools/cli_shims/chaos_cli.py", str(script), "--json"],
        [
            sys.executable,
            str(repo_root / "tools" / "cli_shims" / shim_script),
            str(script),
            *extra_args,
        ],
        repo_root,
        env,
    )

    lines = [line for line in result.stdout.splitlines() if line.strip()]
    assert any("structured_core" in line for line in lines)


@pytest.mark.slow
def test_agent_cli_shim_exits():
    repo_root = Path(__file__).resolve().parents[1]
    env = os.environ.copy()
    env["PYTHONPATH"] = str(repo_root / "src")
    result = run_command(
        [sys.executable, str(repo_root / "tools" / "cli_shims" / "chaos_agent_cli.py")],
        repo_root,
        env,
        input_text=":quit\n",
    )

    assert "CHAOS Agent CLI" in result.stdout


@pytest.mark.slow
def test_fuzz_cli_shim_runs():
    repo_root = Path(__file__).resolve().parents[1]
    env = os.environ.copy()
    env["PYTHONPATH"] = str(repo_root / "src")
    result = run_command(
        [sys.executable, str(repo_root / "tools" / "cli_shims" / "chaos_fuzz.py")],
        repo_root,
        env,
        timeout=120.0,
    )

    assert "[OK]" in result.stdout or "[FAIL]" in result.stdout


@pytest.mark.slow
def test_complete_build_runs_without_warnings(tmp_path):
    repo_root = Path(__file__).resolve().parents[1]
    script_path = repo_root / "src" / "chaos_language" / "complete_build.py"
    assert script_path.exists(), "Complete-build script is missing"

    output_path = tmp_path / "chaos_digest.md"
    env = os.environ.copy()
    env.setdefault("PYTHONWARNINGS", "error")

    result = run_command(
        [
            sys.executable,
            str(script_path.relative_to(repo_root)),
            "--output",
            str(output_path),
        ],
        repo_root,
        env,
    )

    assert output_path.exists()
    assert result.stderr.strip() == ""
    combined = (result.stdout + result.stderr).lower()
    assert "warning" not in combined
