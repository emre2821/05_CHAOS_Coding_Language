"""CHAOS executor for scripts with optional agent mode."""
import argparse
import json
from importlib.abc import Traversable
from pathlib import Path
from typing import Any, Dict, Union

from chaos_language import (
    ChaosAgent,
    generate_business_report,
    render_report_lines,
    run_chaos,
    validate_chaos,
)
from chaos_language.cli.packaged_scripts import resolve_packaged_script


def main():
    parser = argparse.ArgumentParser(description="CHAOS executor")
    parser.add_argument("file", nargs="?", help=".sn or .chaos file")
    parser.add_argument("--verbose", action="store_true")
    parser.add_argument("--agent", action="store_true", help="run in agent mode after loading file")
    parser.add_argument("--report", action="store_true", help="Generate business-facing summary")
    parser.add_argument(
        "--no-timestamp",
        action="store_true",
        help="Skip the generated_at field when producing reports",
    )
    parser.add_argument(
        "--emit",
        type=Path,
        help="Write the JSON environment (and report if requested) to this path",
    )
    args = parser.parse_args()

    if not args.file and not args.agent:
        parser.error("Provide a file or use --agent")

    agent = ChaosAgent("Concord") if args.agent else None

    if args.file:
        script_path = Path(args.file)
        resolved_path: Union[Path, Traversable] = script_path

        if not script_path.exists():
            packaged_script = resolve_packaged_script(script_path)
            if packaged_script is None:
                print("File not found.")
                return
            resolved_path = packaged_script

        with resolved_path.open("r", encoding="utf-8") as handle:  # type: ignore[arg-type]
            src = handle.read()
        validate_chaos(src)
        env = run_chaos(src, verbose=args.verbose)
        print(json.dumps(env, indent=2))
        payload: Dict[str, Any] = dict(env)
        if args.report:
            report = generate_business_report(env, include_timestamp=not args.no_timestamp)
            print()
            print("\n".join(render_report_lines(report)))
            payload = {"environment": env, "report": report}
        if args.emit:
            args.emit.parent.mkdir(parents=True, exist_ok=True)
            args.emit.write_text(json.dumps(payload, indent=2), encoding="utf-8")
            print(f"\nSaved output to {args.emit}")
        if agent:
            agent.step(sn=src)
            print("\n[agent] merged file into context.")

    if agent:
        print("\n[agent] type text; blank line to commit. /quit to exit.")
        buf: list[str] = []
        while True:
            line = input("agent> ").strip()
            if line == "/quit":
                break
            if not line:
                text = "\n".join(buf).strip()
                buf.clear()
                report = agent.step(text=text or None)
                print(f"action={report.action} emotions={report.emotions} dreams={report.dreams[:2]}")
            else:
                buf.append(line)


if __name__ == "__main__":
    main()
