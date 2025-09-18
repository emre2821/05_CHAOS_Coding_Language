"""CHAOS executor for scripts with optional agent mode."""
import argparse
import json
import os
from pathlib import Path
from typing import Any, Dict

from chaos_agent import ChaosAgent
from chaos_reports import generate_business_report, render_report_lines
from chaos_runtime import run_chaos
from chaos_validator import validate_chaos


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
        if not os.path.exists(args.file):
            print("File not found.")
            return
        with open(args.file, "r", encoding="utf-8") as handle:
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
