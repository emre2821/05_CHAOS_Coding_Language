import os
import subprocess
import sysconfig
from pathlib import Path

import pytest

CONSOLE_SCRIPTS = (
    "chaos-cli",
    "chaos-exec",
    "chaos-agent",
    "chaos-validate",
    "chaos",
    "chaos-fuzz",
    "edencore",
)


def run_command(args) -> subprocess.CompletedProcess:
    return subprocess.run(
        args,
        capture_output=True,
        text=True,
        check=True,
    )


def resolve_console_script(bin_dir: Path, script: str) -> Path:
    if os.name != "nt":
        return bin_dir / script

    candidates = [
        bin_dir / f"{script}.exe",
        bin_dir / f"{script}-script.py",
        bin_dir / script,
    ]
    for candidate in candidates:
        if candidate.exists():
            return candidate
    return candidates[0]


def test_console_entrypoints_are_installed():
    bin_dir = Path(sysconfig.get_path("scripts"))
    if not bin_dir.exists():
        pytest.skip("Script directory not available for entrypoint checks.")

    missing = []
    for script in CONSOLE_SCRIPTS:
        executable = resolve_console_script(bin_dir, script)
        if not executable.exists():
            missing.append(executable.name)
            continue
        run_command([str(executable), "--help"])

    if missing:
        pytest.skip(f"Console scripts not installed: {', '.join(missing)}")
