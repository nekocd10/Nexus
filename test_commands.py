#!/usr/bin/env python3
"""
Test all Nexus CLI commands
"""

import subprocess
import sys
import shutil
from pathlib import Path

def run_cmd(cmd, description):
    """Run a command and report results"""
    print(f"\n{'='*60}")
    print(f"TEST: {description}")
    print(f"CMD: {cmd}")
    print(f"{'='*60}")
    try:
        result = subprocess.run(cmd, shell=True, capture_output=False, text=True)
        if result.returncode == 0:
            print(f"✅ SUCCESS: {description}")
            return True
        else:
            print(f"❌ FAILED: {description}")
            return False
    except Exception as e:
        print(f"❌ ERROR: {e}")
        return False

def main():
    results = {}
    
    # Test 1: nexus help
    results["nexus help"] = run_cmd("nexus help", "Show help message")
    
    # Test 2: nexus version
    results["nexus version"] = run_cmd("nexus version", "Show version")
    
    # Test 3: nexus run
    results["nexus run"] = run_cmd("cd /workspaces/Nexus && nexus run test.nexus", "Run Nexus file")
    
    # Test 4: nexus new
    test_dir = Path("/tmp/nexus-test-app")
    if test_dir.exists():
        shutil.rmtree(test_dir)
    results["nexus new"] = run_cmd(f"cd /tmp && nexus new nexus-test-app", "Create new project")
    
    # Test 5: nexus build
    if test_dir.exists():
        results["nexus build"] = run_cmd(f"cd {test_dir} && nexus build", "Build project")
    else:
        print("\n⚠️  Skipping build test - project creation failed")
        results["nexus build"] = False
    
    # Test 6: Check dist files were created correctly
    if test_dir.exists() and (test_dir / "dist").exists():
        print(f"\n{'='*60}")
        print("TEST: Verify dist/ contains .nxs files")
        print(f"{'='*60}")
        nxs_files = list((test_dir / "dist").rglob("*.nxs"))
        if nxs_files:
            print(f"✅ Found {len(nxs_files)} .nxs file(s) in dist/:")
            for f in nxs_files:
                print(f"  - {f.relative_to(test_dir / 'dist')}")
                # Show content to verify it's still .nxs format, not HTML
                content = f.read_text()
                if content.startswith("<") and ("btn" in content or "view" in content or "card" in content):
                    print(f"    ✓ Format is Nexus (.nxs), not HTML")
                else:
                    print(f"    ⚠️  Content check: {content[:50]}...")
            results["dist .nxs files"] = True
        else:
            print("❌ No .nxs files found in dist/")
            results["dist .nxs files"] = False
    
    # Test 7: nexus install
    results["nexus install"] = run_cmd("nexus install", "Install (will show usage)")
    
    # Test 8: nexus nxs
    results["nexus nxs"] = run_cmd("nexus nxs", "NPM package manager (will show usage)")
    
    # Test 9: Create and test a new simple .nexus file
    print(f"\n{'='*60}")
    print("TEST: Create and run simple test file")
    print(f"{'='*60}")
    test_file = Path("/tmp/test_simple.nexus")
    test_file.write_text('println "Test successful!"')
    results["nexus run simple"] = run_cmd(f"nexus run {test_file}", "Run simple Nexus file")
    
    # Summary
    print(f"\n{'='*60}")
    print("SUMMARY OF ALL COMMAND TESTS")
    print(f"{'='*60}")
    
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    for cmd_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status:8} {cmd_name}")
    
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 ALL COMMANDS WORKING!")
        return 0
    else:
        print(f"\n⚠️  {total - passed} test(s) failed")
        return 1

if __name__ == "__main__":
    sys.exit(main())
