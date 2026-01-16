import os
import subprocess
import sys
from pathlib import Path
import venv


CONSOLE_SCRIPTS = (
    "chaos-cli",
    "chaos-exec",
    "chaos-agent",
    "chaos-validate",
    "chaos",
    "chaos-fuzz",
    "edencore",
)


def create_venv(venv_dir: Path) -> Path:
    builder = venv.EnvBuilder(with_pip=True, clear=True)
    builder.create(venv_dir)
    if os.name == "nt":
        return venv_dir / "Scripts" / "python.exe"
    return venv_dir / "bin" / "python"


def run_command(args: list[str], repo_root: Path, env: dict[str, str]) -> subprocess.CompletedProcess:
    return subprocess.run(
        args,
        capture_output=True,
        text=True,
        cwd=repo_root,
        env=env,
        check=True,
    )


def resolve_entrypoint(bin_dir: Path, script: str) -> Path:
    executable = bin_dir / script
    if os.name == "nt":
        executable = executable.with_suffix(".exe")
    return executable


def test_console_entrypoints_show_help(tmp_path):
    repo_root = Path(__file__).resolve().parents[1]
    venv_dir = tmp_path / "venv"
    python_path = create_venv(venv_dir)
    bin_dir = python_path.parent
    env = os.environ.copy()
    env.pop("PYTHONPATH", None)
    env["PATH"] = f"{bin_dir}{os.pathsep}{env['PATH']}"
    env["VIRTUAL_ENV"] = str(venv_dir)

    run_command(
        [str(python_path), "-m", "pip", "install", "-e", "."],
        repo_root,
        env,
    )

    for script in CONSOLE_SCRIPTS:
        executable = resolve_entrypoint(bin_dir, script)
        result = run_command(
            [str(executable), "--help"],
            repo_root,
            env,
        )
        combined = (result.stdout + result.stderr).lower()
        assert "traceback" not in combined
        assert "usage" in combined or "help" in combined
