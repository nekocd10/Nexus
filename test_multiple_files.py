#!/usr/bin/env python3
"""
Test multiple .nxs and .nxsjs files in a project
"""

import subprocess
import sys
from pathlib import Path
import shutil

def test_multiple_files():
    """Test project with multiple .nxs and .nxsjs files"""
    
    print("╔" + "="*58 + "╗")
    print("║" + " "*58 + "║")
    print("║" + "  Multiple Files Test Suite".center(58) + "║")
    print("║" + " "*58 + "║")
    print("╚" + "="*58 + "╝")
    
    # Create test project
    test_dir = Path("/tmp/nexus-multi-test")
    if test_dir.exists():
        shutil.rmtree(test_dir)
    
    print("\n[1] Creating project with multiple files...")
    subprocess.run(f"cd /tmp && nexus new nexus-multi-test", shell=True, capture_output=True)
    
    # Add multiple .nxs files
    print("[2] Adding multiple .nxs component files...")
    (test_dir / "src" / "components").mkdir(exist_ok=True)
    
    (test_dir / "src" / "components" / "navbar.nxs").write_text("""<card class="navbar">
    <h2>Navigation Bar Component</h2>
    <btn @click="goHome()">Home</btn>
    <btn @click="goAbout()">About</btn>
</card>""")
    
    (test_dir / "src" / "components" / "sidebar.nxs").write_text("""<card class="sidebar">
    <h3>Sidebar Menu</h3>
    <btn @click="menu1()">Menu 1</btn>
    <btn @click="menu2()">Menu 2</btn>
</card>""")
    
    (test_dir / "src" / "components" / "footer.nxs").write_text("""<card class="footer">
    <p>Footer Component - Copyright 2024</p>
</card>""")
    
    # Add multiple .nxsjs files
    print("[3] Adding multiple .nxsjs backend files...")
    
    (test_dir / "src" / "api" / "users.nxsjs").parent.mkdir(exist_ok=True)
    (test_dir / "src" / "api" / "users.nxsjs").write_text("""@route GET "/api/users" {
    return "SELECT * FROM users"
}

@route POST "/api/users" {
    return "INSERT INTO users"
}""")
    
    (test_dir / "src" / "api" / "posts.nxsjs").write_text("""@route GET "/api/posts" {
    return "SELECT * FROM posts"
}

@route DELETE "/api/posts/:id" {
    return "DELETE FROM posts WHERE id = ?"
}""")
    
    (test_dir / "src" / "api" / "auth.nxsjs").write_text("""@route POST "/api/login" {
    return "authenticate user"
}

@route POST "/api/logout" {
    return "clear session"
}""")
    
    # List all files before build
    print("\n[4] Source files before build:")
    all_nxs = list(test_dir.rglob("*.nxs"))
    all_nxsjs = list(test_dir.rglob("*.nxsjs"))
    
    print(f"    .nxs files ({len(all_nxs)}):")
    for f in sorted(all_nxs):
        print(f"      - {f.relative_to(test_dir)}")
    
    print(f"    .nxsjs files ({len(all_nxsjs)}):")
    for f in sorted(all_nxsjs):
        print(f"      - {f.relative_to(test_dir)}")
    
    # Build project
    print("\n[5] Building project...")
    result = subprocess.run(f"cd {test_dir} && nexus build", shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"    ❌ Build failed: {result.stderr}")
        return False
    print(result.stdout)
    
    # Verify dist structure
    print("[6] Verifying dist/ structure:")
    dist_nxs = list((test_dir / "dist").rglob("*.nxs"))
    dist_nxsjs = list((test_dir / "dist").rglob("*.nxsjs"))
    
    print(f"    ✓ .nxs files in dist/ ({len(dist_nxs)}):")
    for f in sorted(dist_nxs):
        rel_path = f.relative_to(test_dir / "dist")
        content = f.read_text()
        is_nexus = "<view" in content or "<card" in content or "<btn" in content
        status = "✓ Nexus format" if is_nexus else "⚠️  HTML format"
        print(f"      - {rel_path} ({status})")
    
    print(f"    ✓ .nxsjs files in dist/ ({len(dist_nxsjs)}):")
    for f in sorted(dist_nxsjs):
        rel_path = f.relative_to(test_dir / "dist")
        print(f"      - {rel_path}")
    
    # Verify no HTML conversion
    print("\n[7] Verifying format preservation (NO HTML conversion):")
    all_correct = True
    for nxs_file in dist_nxs:
        content = nxs_file.read_text()
        has_nexus_tags = "<view" in content or "<card" in content or "<btn" in content
        has_html_tags = "<button" in content or "<div class=\"nxs" in content
        
        if has_nexus_tags and not has_html_tags:
            print(f"    ✓ {nxs_file.relative_to(test_dir / 'dist')}: Nexus format preserved")
        else:
            print(f"    ❌ {nxs_file.relative_to(test_dir / 'dist')}: Format issue detected")
            all_correct = False
    
    # Summary
    print("\n" + "="*60)
    print("MULTI-FILE TEST SUMMARY")
    print("="*60)
    print(f"Source .nxs files:    {len(all_nxs)}")
    print(f"Source .nxsjs files:  {len(all_nxsjs)}")
    print(f"Bundled .nxs files:   {len(dist_nxs)}")
    print(f"Bundled .nxsjs files: {len(dist_nxsjs)}")
    print(f"Format preserved:     {'✓ YES' if all_correct else '❌ NO'}")
    
    print("\nDist structure:")
    for item in sorted((test_dir / "dist").rglob("*")):
        if item.is_file():
            level = len(item.relative_to(test_dir / "dist").parts)
            indent = "  " * level
            print(f"{indent}- {item.name}")
    
    return all_correct and len(dist_nxs) > 1 and len(dist_nxsjs) > 0

if __name__ == "__main__":
    success = test_multiple_files()
    
    print("\n" + "="*60)
    if success:
        print("🎉 MULTI-FILE SUPPORT VERIFIED!")
        print("✅ Multiple .nxs files bundled correctly")
        print("✅ Multiple .nxsjs files compiled correctly")
        print("✅ Nexus format preserved (no HTML conversion)")
        sys.exit(0)
    else:
        print("❌ Multi-file test failed")
        sys.exit(1)
