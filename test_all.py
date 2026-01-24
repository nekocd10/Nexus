#!/usr/bin/env python3
"""
Comprehensive test suite for Nexus
Tests all components: CLI, .nxs files, .nxsjs files, and rendering
"""

import os
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

def test_cli_commands():
    """Test CLI command availability"""
    print("\n" + "="*60)
    print("TEST 1: CLI Commands")
    print("="*60)
    
    try:
        from src.cli import NexusCLI
        cli = NexusCLI()
        print("✓ NexusCLI loaded successfully")
        print(f"  Available commands: {', '.join(cli.commands.keys())}")
        return True
    except Exception as e:
        print(f"✗ Failed to load CLI: {e}")
        return False

def test_nexus_files():
    """Test discovering and listing all .nxs files"""
    print("\n" + "="*60)
    print("TEST 2: Discovery of .nxs Files")
    print("="*60)
    
    nxs_files = list(Path("/workspaces/Nexus").rglob("*.nxs"))
    print(f"Found {len(nxs_files)} .nxs files:")
    for f in nxs_files:
        print(f"  ✓ {f.relative_to(Path('/workspaces/Nexus'))}")
    
    return len(nxs_files) > 0

def test_nxsjs_files():
    """Test discovering and listing all .nxsjs files"""
    print("\n" + "="*60)
    print("TEST 3: Discovery of .nxsjs Files")
    print("="*60)
    
    nxsjs_files = list(Path("/workspaces/Nexus").rglob("*.nxsjs"))
    print(f"Found {len(nxsjs_files)} .nxsjs files:")
    for f in nxsjs_files:
        print(f"  ✓ {f.relative_to(Path('/workspaces/Nexus'))}")
    
    return len(nxsjs_files) > 0

def test_interpreter():
    """Test Nexus interpreter loads and runs"""
    print("\n" + "="*60)
    print("TEST 4: Nexus Interpreter")
    print("="*60)
    
    try:
        from src.lexer import NexusLexer
        from src.parser import NexusParser
        from src.interpreter import NexusInterpreter
        
        code = 'println "Hello from Nexus!"'
        print(f"Code: {code}")
        
        lexer = NexusLexer(code)
        tokens = lexer.tokenize()
        print(f"  ✓ Tokenized: {len(tokens)} tokens")
        
        parser = NexusParser(tokens)
        ast = parser.parse()
        print(f"  ✓ Parsed: {ast}")
        
        interpreter = NexusInterpreter()
        result = interpreter.interpret(ast)
        print(f"  ✓ Executed: {result}")
        
        return True
    except Exception as e:
        print(f"✗ Interpreter test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_frontend_parser():
    """Test .nxs frontend file parsing and rendering"""
    print("\n" + "="*60)
    print("TEST 5: Frontend Parser (.nxs Rendering)")
    print("="*60)
    
    try:
        from src.frontend import NxsParser
        
        nxs_file = Path("/workspaces/Nexus/src/index.nxs")
        if not nxs_file.exists():
            print(f"✗ File not found: {nxs_file}")
            return False
        
        with open(nxs_file, 'r') as f:
            source = f.read()
        
        print(f"Source code ({len(source)} bytes):")
        print(source[:200] + "...")
        
        parser = NxsParser(source)
        html = parser.parse()
        print(f"\n  ✓ Parsed successfully")
        print(f"  Generated HTML: {len(html)} bytes")
        
        # Check for button rendering
        if 'class="nxs-btn"' in html or '<button' in html:
            print("  ✓ Button elements found in output")
        else:
            print("  ✗ Button elements NOT found in output")
            return False
        
        # Check for view/card elements
        if 'nxs-view' in html and 'nxs-card' in html:
            print("  ✓ Custom view and card components rendered")
        else:
            print("  ✗ Custom components NOT rendered properly")
        
        # Check for event bindings
        if 'onclick' in html:
            print("  ✓ Event bindings found (@click → onclick)")
        else:
            print("  ! Warning: No onclick events found")
        
        # Show sample of HTML
        print("\nGenerated HTML (first 500 chars):")
        print(html[:500] + "...")
        
        return True
    except Exception as e:
        print(f"✗ Frontend parser test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_backend_parser():
    """Test .nxsjs backend file parsing"""
    print("\n" + "="*60)
    print("TEST 6: Backend Parser (.nxsjs)")
    print("="*60)
    
    try:
        from src.backend import NxsjsParser, NxsjsInterpreter
        
        nxsjs_file = Path("/workspaces/Nexus/src/api.nxsjs")
        if not nxsjs_file.exists():
            print(f"✗ File not found: {nxsjs_file}")
            return False
        
        with open(nxsjs_file, 'r') as f:
            source = f.read()
        
        print(f"Source code ({len(source)} bytes):")
        print(source[:200] + "...")
        
        parser = NxsjsParser(source)
        ast = parser.parse()
        print(f"\n  ✓ Parsed successfully")
        print(f"  Config: {ast.get('config', {})}")
        print(f"  Models: {list(ast.get('models', {}).keys())}")
        print(f"  Routes: {len(ast.get('routes', []))} route(s)")
        print(f"  Middleware: {list(ast.get('middleware', {}).keys())}")
        
        # Show routes
        if ast.get('routes'):
            for route in ast['routes']:
                print(f"    - {route['method']} {route['path']}")
        
        return True
    except Exception as e:
        print(f"✗ Backend parser test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_all_imports():
    """Test that all module imports work correctly"""
    print("\n" + "="*60)
    print("TEST 7: Module Imports")
    print("="*60)
    
    modules = [
        ('src.lexer', 'NexusLexer'),
        ('src.parser', 'NexusParser'),
        ('src.interpreter', 'NexusInterpreter'),
        ('src.frontend', 'NxsParser'),
        ('src.backend', 'NxsjsParser'),
        ('src.cli', 'NexusCLI'),
    ]
    
    all_ok = True
    for module_name, class_name in modules:
        try:
            module = __import__(module_name, fromlist=[class_name])
            cls = getattr(module, class_name)
            print(f"  ✓ {module_name}.{class_name}")
        except Exception as e:
            print(f"  ✗ {module_name}.{class_name}: {e}")
            all_ok = False
    
    return all_ok

def main():
    """Run all tests"""
    print("\n")
    print("╔" + "="*58 + "╗")
    print("║" + " "*58 + "║")
    print("║" + "  Nexus Comprehensive Test Suite".center(58) + "║")
    print("║" + " "*58 + "║")
    print("╚" + "="*58 + "╝")
    
    results = {
        "CLI Commands": test_cli_commands(),
        ".nxs Files": test_nexus_files(),
        ".nxsjs Files": test_nxsjs_files(),
        "Module Imports": test_all_imports(),
        "Interpreter": test_interpreter(),
        "Frontend Parser": test_frontend_parser(),
        "Backend Parser": test_backend_parser(),
    }
    
    # Summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    for test_name, result in results.items():
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"  {status:8} {test_name}")
    
    print()
    print(f"Results: {passed}/{total} tests passed")
    print()
    
    if passed == total:
        print("╔" + "="*58 + "╗")
        print("║" + "  ALL TESTS PASSED! 🎉".center(58) + "║")
        print("╚" + "="*58 + "╝")
        return 0
    else:
        print("Some tests failed. Please review the output above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
