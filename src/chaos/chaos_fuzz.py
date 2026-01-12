"""
Run every .sn in chaos_corpus/ through the runtime.

Fuzz testing suite for CHAOS - systematically executes all example
programs to ensure the symbolic-emotional computation system remains
stable and true to its sacred architecture.
"""

import argparse
import glob
import json
import os
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from .chaos_runtime import run_chaos
from .chaos_validator import validate_chaos


def run_fuzz_test(file_path: str, verbose: bool = False) -> Tuple[bool, str, Dict[str, Any]]:
    """
    Execute a single CHAOS file and return results.
    
    Args:
        file_path: Path to the CHAOS file to test
        verbose: If True, print detailed execution information
        
    Returns:
        Tuple of (success, error_message, environment)
    """
    try:
        with open(file_path, "r", encoding="utf-8") as handle:
            source = handle.read()
        
        # Validation phase
        validate_chaos(source)
        
        # Execution phase
        environment = run_chaos(source, verbose=verbose)
        
        return True, "", environment
        
    except Exception as exc:
        return False, str(exc), {}


def run_corpus_tests(corpus_dir: str = "chaos_corpus", verbose: bool = False) -> Dict[str, any]:
    """
    Run all CHAOS files in the corpus directory.
    
    Args:
        corpus_dir: Directory containing test CHAOS files
        verbose: If True, print detailed execution information
        
    Returns:
        Dictionary with test results summary
    """
    results = {
        "total_files": 0,
        "passed": 0,
        "failed": 0,
        "failures": [],
        "environments": {}
    }
    
    # Find all .sn and .chaos files
    pattern_sn = os.path.join(corpus_dir, "*.sn")
    pattern_chaos = os.path.join(corpus_dir, "*.chaos")
    
    test_files = glob.glob(pattern_sn) + glob.glob(pattern_chaos)
    results["total_files"] = len(test_files)
    
    if not test_files:
        print(f"No test files found in {corpus_dir}/")
        return results
    
    print(f"🔍 Running fuzz tests on {len(test_files)} CHAOS files...\n")
    
    for file_path in sorted(test_files):
        file_name = os.path.basename(file_path)
        
        if verbose:
            print(f"Testing: {file_name}")
        
        success, error, environment = run_fuzz_test(file_path, verbose=False)
        
        if success:
            results["passed"] += 1
            results["environments"][file_name] = environment
            
            if verbose:
                print(f"  ✅ {file_name}")
                print(f"     Symbols: {len(environment.get('structured_core', {}))}")
                print(f"     Emotions: {len(environment.get('emotive_layer', []))}")
            else:
                print(f"✅ {file_name}")
        else:
            results["failed"] += 1
            results["failures"].append({
                "file": file_name,
                "error": error
            })
            
            print(f"❌ {file_name}: {error}")
    
    return results


def print_results_summary(results: Dict[str, any]) -> None:
    """Print a summary of fuzz test results."""
    print(f"\n📊 Fuzz Test Summary:")
    print(f"   Total Files: {results['total_files']}")
    print(f"   Passed: {results['passed']} ✅")
    print(f"   Failed: {results['failed']} ❌")
    
    if results['failed'] > 0:
        print(f"\n❌ Failures:")
        for failure in results['failures']:
            print(f"   {failure['file']}: {failure['error']}")
    
    # Calculate overall statistics
    if results['environments']:
        total_symbols = sum(len(env.get('structured_core', {})) 
                          for env in results['environments'].values())
        total_emotions = sum(len(env.get('emotive_layer', [])) 
                           for env in results['environments'].values())
        total_narrative = sum(len(env.get('chaosfield_layer', '')) 
                            for env in results['environments'].values())
        
        avg_symbols = total_symbols / len(results['environments'])
        avg_emotions = total_emotions / len(results['environments'])
        avg_narrative = total_narrative / len(results['environments'])
        
        print(f"\n📈 Execution Statistics:")
        print(f"   Average symbols per program: {avg_symbols:.1f}")
        print(f"   Average emotions per program: {avg_emotions:.1f}")
        print(f"   Average narrative length: {avg_narrative:.0f} characters")


def generate_test_report(results: Dict[str, any], output_file: Optional[str] = None) -> None:
    """Generate a detailed test report."""
    report = {
        "timestamp": __import__('datetime').datetime.now().isoformat(),
        "test_results": results,
        "summary": {
            "success_rate": results["passed"] / max(results["total_files"], 1),
            "total_executed": results["total_files"]
        }
    }
    
    if output_file:
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=2)
        print(f"📄 Detailed report saved to: {output_file}")
    else:
        print(f"\n📄 Detailed Test Report:")
        print(json.dumps(report, indent=2))


def main() -> None:
    """Main entry point for fuzz testing."""
    parser = argparse.ArgumentParser(
        description="CHAOS Fuzz Testing Suite",
        epilog="Examples:\n"
               "  chaos-fuzz                      # Test all files in chaos_corpus/\n"
               "  chaos-fuzz --verbose            # Show detailed execution\n"
               "  chaos-fuzz --corpus my_tests/   # Test files in custom directory\n"
               "  chaos-fuzz --report results.json # Generate detailed report\n",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument(
        "--corpus", 
        default="chaos_corpus",
        help="Directory containing CHAOS test files (default: chaos_corpus)"
    )
    parser.add_argument(
        "--verbose", 
        action="store_true",
        help="Show detailed execution information"
    )
    parser.add_argument(
        "--report",
        help="Save detailed results to JSON file"
    )
    parser.add_argument(
        "--exit-on-failure",
        action="store_true",
        help="Exit with error code if any tests fail"
    )
    
    args = parser.parse_args()
    
    # Check if corpus directory exists
    if not os.path.exists(args.corpus):
        print(f"❌ Corpus directory not found: {args.corpus}")
        print("   Create the directory and add .sn or .chaos files to run tests.")
        sys.exit(1)
    
    # Run the fuzz tests
    results = run_corpus_tests(args.corpus, args.verbose)
    
    # Print summary
    print_results_summary(results)
    
    # Generate report if requested
    if args.report:
        generate_test_report(results, args.report)
    
    # Exit with appropriate code
    if args.exit_on_failure and results["failed"] > 0:
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == "__main__":
    main()
