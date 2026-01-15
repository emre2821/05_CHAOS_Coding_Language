"""
CHAOS executor for scripts with optional agent mode.

Advanced execution interface that combines CHAOS program execution
with agent integration and business reporting capabilities.
"""

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Any, Dict, Optional

from .chaos_agent import ChaosAgent
from .chaos_runtime import run_chaos
from .chaos_validator import validate_chaos


def generate_business_report(environment: Dict[str, Any], 
                           include_timestamp: bool = True) -> Dict[str, Any]:
    """
    Generate a business-facing summary of CHAOS execution results.
    
    Args:
        environment: The CHAOS execution environment
        include_timestamp: Whether to include execution timestamp
        
    Returns:
        Business-friendly report dictionary
    """
    report = {
        "summary": {
            "symbols_defined": len(environment.get("structured_core", {})),
            "emotions_expressed": len(environment.get("emotive_layer", [])),
            "narrative_length": len(environment.get("chaosfield_layer", "")),
            "execution_success": True
        }
    }
    
    if include_timestamp:
        from datetime import datetime
        report["generated_at"] = datetime.now().isoformat()
    
    # Extract key insights
    if environment.get("structured_core"):
        report["structured_insights"] = {
            "primary_symbols": list(environment["structured_core"].keys())[:5],
            "symbol_count": len(environment["structured_core"])
        }
    
    if environment.get("emotive_layer"):
        emotions = environment["emotive_layer"]
        if emotions:
            dominant_emotion = max(emotions, key=lambda e: e.get("intensity", 0))
            report["emotional_insights"] = {
                "dominant_emotion": dominant_emotion["name"],
                "intensity": dominant_emotion["intensity"],
                "total_emotions": len(emotions)
            }
    
    if environment.get("chaosfield_layer"):
        narrative = environment["chaosfield_layer"]
        if narrative:
            word_count = len(narrative.split())
            report["narrative_insights"] = {
                "word_count": word_count,
                "preview": narrative[:100] + "..." if len(narrative) > 100 else narrative
            }
    
    return report


def render_report_lines(report: Dict[str, Any]) -> list[str]:
    """
    Render a business report as human-readable lines.
    
    Args:
        report: The business report dictionary
        
    Returns:
        List of formatted report lines
    """
    lines = []
    lines.append("=" * 50)
    lines.append("CHAOS Execution Report")
    lines.append("=" * 50)
    
    # Summary
    summary = report["summary"]
    lines.append(f"Symbols Defined: {summary['symbols_defined']}")
    lines.append(f"Emotions Expressed: {summary['emotions_expressed']}")
    lines.append(f"Narrative Length: {summary['narrative_length']} characters")
    lines.append("")
    
    # Structured insights
    if "structured_insights" in report:
        insights = report["structured_insights"]
        lines.append("🔍 Symbolic Insights:")
        lines.append(f"  Primary Symbols: {', '.join(insights['primary_symbols'])}")
        lines.append("")
    
    # Emotional insights
    if "emotional_insights" in report:
        insights = report["emotional_insights"]
        lines.append("💝 Emotional Insights:")
        lines.append(f"  Dominant Emotion: {insights['dominant_emotion']} ({insights['intensity']}/10)")
        lines.append("")
    
    # Narrative insights
    if "narrative_insights" in report:
        insights = report["narrative_insights"]
        lines.append("📖 Narrative Insights:")
        lines.append(f"  Word Count: {insights['word_count']}")
        lines.append(f"  Preview: {insights['preview']}")
        lines.append("")
    
    if "generated_at" in report:
        lines.append(f"Generated: {report['generated_at']}")
    
    lines.append("=" * 50)
    return lines


def main() -> None:
    """Main execution entry point."""
    parser = argparse.ArgumentParser(
        description="CHAOS Executor - Run symbolic-emotional programs",
        epilog="Examples:\n"
               "  chaos-exec script.sn                    # Execute CHAOS script\n"
               "  chaos-exec script.sn --agent            # Execute then enter agent mode\n"
               "  chaos-exec script.sn --report           # Generate business report\n"
               "  chaos-exec script.sn --emit output.json # Save results to file\n",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument("file", nargs="?", help=".sn or .chaos file to execute")
    parser.add_argument("--verbose", action="store_true", help="Verbose execution output")
    parser.add_argument("--agent", action="store_true", help="Run in agent mode after loading file")
    parser.add_argument("--report", action="store_true", help="Generate business-facing summary")
    parser.add_argument(
        "--no-timestamp",
        action="store_true",
        help="Skip the generated_at field when producing reports"
    )
    parser.add_argument(
        "--emit",
        type=Path,
        help="Write the JSON environment (and report if requested) to this path"
    )
    parser.add_argument("--validate-only", action="store_true", help="Only validate, don't execute")
    
    args = parser.parse_args()
    
    # Validation
    if not args.file and not args.agent:
        parser.error("Provide a file or use --agent mode")
    
    # Initialize agent if needed
    agent = ChaosAgent("Concord") if args.agent else None
    
    # File execution
    if args.file:
        if not os.path.exists(args.file):
            print("File not found.", file=sys.stderr)
            sys.exit(1)
        
        try:
            with open(args.file, "r", encoding="utf-8") as handle:
                source = handle.read()
        except OSError as err:
            print(f"Could not read {args.file}: {err}", file=sys.stderr)
            sys.exit(1)
        
        # Validation phase
        try:
            validate_chaos(source)
        except Exception as e:
            print(f"Validation failed: {e}", file=sys.stderr)
            sys.exit(1)
        
        if args.validate_only:
            print("✓ CHAOS program is valid")
            sys.exit(0)
        
        # Execution phase
        try:
            environment = run_chaos(source, verbose=args.verbose)
        except Exception as e:
            print(f"Execution failed: {e}", file=sys.stderr)
            sys.exit(1)
        
        # Output results
        if not args.emit and not args.report:
            print(json.dumps(environment, indent=2))
        
        # Prepare output payload
        payload: Dict[str, Any] = {"environment": environment}
        
        # Generate report if requested
        if args.report:
            report = generate_business_report(
                environment, 
                include_timestamp=not args.no_timestamp
            )
            
            if not args.emit:
                print()  # Blank line before report
                print("\n".join(render_report_lines(report)))
            
            payload["report"] = report
        
        # Emit to file if requested
        if args.emit:
            args.emit.parent.mkdir(parents=True, exist_ok=True)
            args.emit.write_text(json.dumps(payload, indent=2), encoding="utf-8")
            print(f"\nSaved output to {args.emit}")
        
        # Agent integration
        if agent:
            agent.step(sn=source)
            print("\n[agent] Merged file into symbolic consciousness")
    
    # Agent mode
    if agent:
        print("\n[agent] Type text; blank line to commit. Type '/quit' to exit.")
        buffer = []
        
        while True:
            try:
                line = input("agent> ").strip()
                if line == "/quit":
                    break
                
                if not line:
                    text = "\n".join(buffer).strip()
                    buffer.clear()
                    report = agent.step(text=text or None)
                    
                    emotion_summary = f"{len(report.emotions)} emotions" if report.emotions else "no emotions"
                    action_name = report.action.kind if report.action else "idle"
                    dream_summary = f"{len(report.dreams)} dreams" if report.dreams else "no dreams"
                    
                    print(f"action={action_name} emotions={emotion_summary} dreams={dream_summary}")
                else:
                    buffer.append(line)
            except KeyboardInterrupt:
                print("\nAgent session ended.")
                break
            except Exception as e:
                print(f"Agent error: {e}")
                buffer.clear()


if __name__ == "__main__":
    main()