import os
import subprocess
import sys
import venv
from pathlib import Path

import pytest


def create_venv(venv_dir: Path) -> Path:
    builder = venv.EnvBuilder(with_pip=True)
    builder.create(venv_dir)
    python_dir = "Scripts" if os.name == "nt" else "bin"
    return venv_dir / python_dir / "python"


def run_command(args, repo_root: Path, env: dict[str, str]) -> subprocess.CompletedProcess:
    return subprocess.run(
        args,
        capture_output=True,
        text=True,
        cwd=repo_root,
        env=env,
        check=True,
    )


@pytest.mark.slow
def test_console_entrypoints_show_help(tmp_path):
    repo_root = Path(__file__).resolve().parents[1]
    venv_dir = tmp_path / "venv"
    python_path = create_venv(venv_dir)

    run_command(
        [str(python_path), "-m", "pip", "install", "-e", "."],
        repo_root,
        os.environ.copy(),
    )

    python_dir = "Scripts" if os.name == "nt" else "bin"
    exe_suffix = ".exe" if os.name == "nt" else ""
    entrypoints = [
        "chaos-cli",
        "chaos-exec",
        "chaos-agent",
        "chaos-validate",
        "chaos",
        "chaos-fuzz",
        "edencore",
    ]

    for entrypoint in entrypoints:
        executable = venv_dir / python_dir / f"{entrypoint}{exe_suffix}"
        assert executable.exists(), f"Missing console entrypoint: {entrypoint}"
        result = run_command(
            [str(executable), "--help"],
            repo_root,
            os.environ.copy(),
        )
        combined = (result.stdout + result.stderr).lower()
        assert "usage" in combined
