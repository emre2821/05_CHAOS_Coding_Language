#!/usr/bin/env python3
"""
Validation script for CHAOS language modernization.

This script verifies that the modernization preserves the sacred architecture
and philosophical identity of CHAOS while providing modern Python standards.
"""

import sys
import os
from pathlib import Path

# Add the source directory to Python path
sys.path.insert(0, str(Path(__file__).parent / "src"))

def validate_package_structure():
    """Validate the new repository structure."""
    print("🔍 Validating package structure...")
    
    required_dirs = [
        "src/chaos_legacy",
        "tests", 
        "examples",
        "docs",
        "experiments"
    ]
    
    required_files = [
        "src/chaos_legacy/__init__.py",
        "src/chaos_legacy/chaos_lexer.py",
        "src/chaos_legacy/chaos_parser.py", 
        "src/chaos_legacy/chaos_interpreter.py",
        "src/chaos_legacy/chaos_runtime.py",
        "src/chaos_legacy/chaos_emotion.py",
        "src/chaos_legacy/chaos_agent.py",
        "pyproject.toml",
        "setup.cfg",
        "README.md"
    ]
    
    missing_dirs = []
    missing_files = []
    
    for dir_path in required_dirs:
        if not os.path.isdir(dir_path):
            missing_dirs.append(dir_path)
    
    for file_path in required_files:
        if not os.path.isfile(file_path):
            missing_files.append(file_path)
    
    if missing_dirs or missing_files:
        print("❌ Missing components:")
        for d in missing_dirs:
            print(f"  Directory: {d}")
        for f in missing_files:
            print(f"  File: {f}")
        return False
    
    print("✅ Package structure is complete")
    return True

def validate_imports():
    """Validate that all modules can be imported."""
    print("🔍 Validating imports...")
    
    try:
        from chaos_legacy import (
            run_chaos, ChaosInterpreter, ChaosLexer, ChaosParser,
            ChaosError, ChaosSyntaxError, ChaosRuntimeError,
            ChaosAgent
        )
        print("✅ Core imports successful")
        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

def validate_basic_execution():
    """Test basic CHAOS program execution."""
    print("🔍 Validating basic execution...")
    
    try:
        from chaos_legacy import run_chaos
        
        # Test simple program
        program = """
        [NAME]: "test"
        [EMOTION:JOY:5]
        {
        Hello CHAOS!
        }
        """
        
        result = run_chaos(program)
        
        # Validate three-layer structure
        assert "structured_core" in result
        assert "emotive_layer" in result  
        assert "chaosfield_layer" in result
        assert result["structured_core"]["NAME"] == "test"
        assert len(result["emotive_layer"]) == 1
        assert result["emotive_layer"][0]["name"] == "JOY"
        assert "Hello CHAOS" in result["chaosfield_layer"]
        
        print("✅ Basic execution successful")
        return True
        
    except Exception as e:
        print(f"❌ Execution error: {e}")
        return False

def validate_example_programs():
    """Validate that example programs execute correctly."""
    print("🔍 Validating example programs...")
    
    try:
        from chaos_legacy import run_chaos
        
        examples_dir = Path("examples")
        if not examples_dir.exists():
            print("⚠️  Examples directory not found")
            return True
        
        example_files = list(examples_dir.glob("*.sn"))
        if not example_files:
            print("⚠️  No example files found")
            return True
        
        success_count = 0
        for example_file in example_files:
            try:
                with open(example_file, 'r', encoding='utf-8') as f:
                    source = f.read()
                
                result = run_chaos(source)
                
                # Validate three-layer structure
                assert "structured_core" in result
                assert "emotive_layer" in result
                assert "chaosfield_layer" in result
                
                success_count += 1
                print(f"  ✅ {example_file.name}")
                
            except Exception as e:
                print(f"  ❌ {example_file.name}: {e}")
        
        print(f"✅ {success_count}/{len(example_files)} examples executed successfully")
        return success_count == len(example_files)
        
    except Exception as e:
        print(f"❌ Example validation error: {e}")
        return False

def validate_agent_functionality():
    """Test CHAOS agent functionality."""
    print("🔍 Validating agent functionality...")
    
    try:
        from chaos_legacy import ChaosAgent
        
        agent = ChaosAgent("TestAgent")
        
        # Test agent cycle
        report = agent.step(text="Hello, agent!")
        
        # Validate report structure
        assert hasattr(report, 'emotions')
        assert hasattr(report, 'symbols')
        assert hasattr(report, 'narrative')
        assert hasattr(report, 'action')
        assert hasattr(report, 'dreams')
        assert hasattr(report, 'log')
        
        # Test with CHAOS program
        program = """
        [SYMBOL:TEST:VALUE]
        [EMOTION:KINDNESS:8]
        {
        Agent test program
        }
        """
        
        report = agent.step(sn=program)
        assert len(report.symbols) > 0
        assert len(report.emotions) > 0
        
        print("✅ Agent functionality validated")
        return True
        
    except Exception as e:
        print(f"❌ Agent validation error: {e}")
        return False

def validate_emotional_computation():
    """Validate that emotional computation works correctly."""
    print("🔍 Validating emotional computation...")
    
    try:
        from chaos_legacy import run_chaos
        
        # Test emotional triggers
        program = """
        [EMOTION:FEAR:8]
        [EMOTION:HOPE:3]
        {
        The darkness surrounds us, but there is light ahead.
        }
        """
        
        result = run_chaos(program)
        
        # Validate emotions
        emotions = result["emotive_layer"]
        assert len(emotions) == 2
        
        fear_emotion = next(e for e in emotions if e["name"] == "FEAR")
        hope_emotion = next(e for e in emotions if e["name"] == "HOPE")
        
        assert fear_emotion["intensity"] == 8
        assert hope_emotion["intensity"] == 3
        
        # Test intensity clamping
        program_clamp = """
        [EMOTION:JOY:15]
        [EMOTION:SADNESS:-5]
        """
        
        result_clamp = run_chaos(program_clamp)
        emotions_clamp = result_clamp["emotive_layer"]
        
        joy_emotion = next(e for e in emotions_clamp if e["name"] == "JOY")
        sadness_emotion = next(e for e in emotions_clamp if e["name"] == "SADNESS")
        
        assert joy_emotion["intensity"] == 10  # Clamped to max
        assert sadness_emotion["intensity"] == 0  # Clamped to min
        
        print("✅ Emotional computation validated")
        return True
        
    except Exception as e:
        print(f"❌ Emotional computation error: {e}")
        return False

def validate_symbolic_processing():
    """Validate symbolic processing and relationships."""
    print("🔍 Validating symbolic processing...")
    
    try:
        from chaos_legacy import run_chaos
        
        # Test symbolic relationships
        program = """
        [SYMBOL:PERSONA:ALLY]
        [SYMBOL:PERSONA:TRUST]
        [RELATIONSHIP:ALLY:TRUST:8]
        """
        
        result = run_chaos(program)
        symbols = result["structured_core"]
        
        assert "PERSONA:ALLY" in symbols
        assert "PERSONA:TRUST" in symbols
        assert "RELATIONSHIP:ALLY:TRUST" in symbols
        
        print("✅ Symbolic processing validated")
        return True
        
    except Exception as e:
        print(f"❌ Symbolic processing error: {e}")
        return False

def validate_preservation_of_essence():
    """Validate that the soul of CHAOS has been preserved."""
    print("🔍 Validating preservation of CHAOS essence...")
    
    checks = [
        ("Three-layer architecture", validate_three_layer_architecture),
        ("Symbolic tags", validate_symbolic_tags),
        ("Emotional system", validate_emotional_system),
        ("Sacred protocols", validate_sacred_protocols),
        ("Mythic language", validate_mythic_language),
        ("EdenOS integration", validate_edenos_integration),
    ]
    
    all_passed = True
    for check_name, check_func in checks:
        try:
            if check_func():
                print(f"  ✅ {check_name}")
            else:
                print(f"  ❌ {check_name}")
                all_passed = False
        except Exception as e:
            print(f"  ❌ {check_name}: {e}")
            all_passed = False
    
    return all_passed

def validate_three_layer_architecture():
    """Check that three-layer architecture is preserved."""
    from chaos_legacy import run_chaos
    result = run_chaos("[TEST]: value\n[EMOTION:JOY:5]\n{test}")
    return ("structured_core" in result and 
            "emotive_layer" in result and 
            "chaosfield_layer" in result)

def validate_symbolic_tags():
    """Check that symbolic tags work correctly."""
    from chaos_legacy import run_chaos
    result = run_chaos("[EVENT]: test\n[SYMBOL:TEST:VALUE]")
    return (result["structured_core"]["EVENT"] == "test" and
            result["structured_core"]["SYMBOL:TEST"] == "VALUE")

def validate_emotional_system():
    """Check that emotional system works correctly."""
    from chaos_legacy import run_chaos
    result = run_chaos("[EMOTION:JOY:7]")
    return (len(result["emotive_layer"]) == 1 and
            result["emotive_layer"][0]["name"] == "JOY" and
            result["emotive_layer"][0]["intensity"] == 7)

def validate_sacred_protocols():
    """Check that sacred protocols are available."""
    from chaos_legacy.chaos_protocols import ProtocolRegistry
    registry = ProtocolRegistry()
    protocols = registry.list_protocols()
    return len(protocols) >= 4  # Should have at least the 4 standard protocols

def validate_mythic_language():
    """Check that mythic language is preserved in documentation."""
    with open("README.md", "r", encoding="utf-8") as f:
        content = f.read()
    
    mythic_terms = ["sacred", "ritual", "mythic", "symbolic", "emotional", "resonance"]
    return any(term in content.lower() for term in mythic_terms)

def validate_edenos_integration():
    """Check that EdenOS integration is preserved."""
    from chaos_legacy import ChaosAgent
    agent = ChaosAgent("Test")
    return hasattr(agent, 'ctx') and hasattr(agent, 'emotions')

def main():
    """Run all validation checks."""
    print("🌌 CHAOS Language Modernization Validation")
    print("=" * 50)
    
    validations = [
        ("Package Structure", validate_package_structure),
        ("Import System", validate_imports),
        ("Basic Execution", validate_basic_execution),
        ("Example Programs", validate_example_programs),
        ("Agent Functionality", validate_agent_functionality),
        ("Emotional Computation", validate_emotional_computation),
        ("Symbolic Processing", validate_symbolic_processing),
        ("Essence Preservation", validate_preservation_of_essence),
    ]
    
    results = []
    for name, validator in validations:
        try:
            success = validator()
            results.append((name, success))
            status = "✅ PASS" if success else "❌ FAIL"
            print(f"{status} {name}")
        except Exception as e:
            results.append((name, False))
            print(f"❌ FAIL {name}: {e}")
    
    print("\n" + "=" * 50)
    print("📊 Validation Summary:")
    
    passed = sum(1 for _, success in results if success)
    total = len(results)
    
    print(f"Passed: {passed}/{total}")
    
    if passed == total:
        print("\n🎉 All validations passed! The modernization is complete.")
        print("✨ CHAOS has been successfully modernized while preserving its sacred essence.")
        sys.exit(0)
    else:
        print("\n💥 Some validations failed. Please review the errors above.")
        failed_validations = [name for name, success in results if not success]
        print(f"Failed validations: {', '.join(failed_validations)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
