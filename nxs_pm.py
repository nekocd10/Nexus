"""
Nexus Package Manager (nxs)
Manages Nexus packages with npm compatibility and custom packages
"""

import json
import os
import sys
import subprocess
import shutil
from pathlib import Path
from typing import Dict, List, Any
import urllib.request
import urllib.error

class NxsPackageManager:
    def __init__(self):
        self.nxs_home = Path.home() / ".nexus"
        self.nxs_home.mkdir(exist_ok=True)
        
        self.registry_file = self.nxs_home / "registry.json"
        self.packages_dir = self.nxs_home / "packages"
        self.packages_dir.mkdir(exist_ok=True)
        
        self.project_packages = Path.cwd() / "nxs_modules"
        self.project_package_json = Path.cwd() / "nxs.json"
        
        self.load_registry()
    
    def load_registry(self):
        """Load or create the package registry"""
        if self.registry_file.exists():
            with open(self.registry_file, 'r') as f:
                self.registry = json.load(f)
        else:
            self.registry = {
                "packages": {},
                "local": {},
                "npm_packages": {}
            }
            self.save_registry()
    
    def save_registry(self):
        """Save registry to file"""
        with open(self.registry_file, 'w') as f:
            json.dump(self.registry, f, indent=2)
    
    def install(self, package_name: str, version: str = "latest"):
        """Install a package"""
        print(f"Installing {package_name}@{version}...")
        
        # Try npm first
        if self.try_install_npm(package_name, version):
            return
        
        # Try custom registry
        if self.try_install_custom(package_name, version):
            return
        
        # Try local
        if self.try_install_local(package_name):
            return
        
        print(f"Error: Package {package_name} not found")
    
    def try_install_npm(self, package_name: str, version: str) -> bool:
        """Try to install from npm"""
        try:
            print(f"  Searching npm registry...")
            result = subprocess.run(
                ["npm", "info", package_name, "version"],
                capture_output=True,
                text=True,
                timeout=5
            )
            
            if result.returncode == 0:
                npm_version = result.stdout.strip()
                print(f"  Found npm package version {npm_version}")
                
                # Create npm package wrapper
                pkg_dir = self.packages_dir / f"{package_name}@{npm_version}"
                pkg_dir.mkdir(parents=True, exist_ok=True)
                
                # Store npm reference
                self.registry["npm_packages"][package_name] = {
                    "version": npm_version,
                    "type": "npm",
                    "installed": True
                }
                self.save_registry()
                
                # Link to project
                self.link_package(package_name, str(pkg_dir))
                print(f"  ✓ Installed {package_name}@{npm_version}")
                return True
        except Exception as e:
            pass
        
        return False
    
    def try_install_custom(self, package_name: str, version: str) -> bool:
        """Try to install from custom registry"""
        if package_name in self.registry["packages"]:
            pkg_info = self.registry["packages"][package_name]
            
            # Create package directory
            pkg_dir = self.packages_dir / f"{package_name}@{version}"
            pkg_dir.mkdir(parents=True, exist_ok=True)
            
            # Copy package files
            if "path" in pkg_info:
                src = Path(pkg_info["path"])
                if src.exists():
                    shutil.copytree(src, pkg_dir, dirs_exist_ok=True)
                    self.link_package(package_name, str(pkg_dir))
                    print(f"  ✓ Installed {package_name}@{version}")
                    return True
        
        return False
    
    def try_install_local(self, package_name: str) -> bool:
        """Try to install from local directory"""
        local_path = Path.cwd() / package_name
        if local_path.exists() and local_path.is_dir():
            pkg_dir = self.packages_dir / package_name
            shutil.copytree(local_path, pkg_dir, dirs_exist_ok=True)
            self.link_package(package_name, str(pkg_dir))
            print(f"  ✓ Installed {package_name} from local")
            return True
        
        return False
    
    def link_package(self, name: str, path: str):
        """Link package to project"""
        self.project_packages.mkdir(exist_ok=True)
        link_path = self.project_packages / name
        
        # Create symlink or copy
        if link_path.exists():
            shutil.rmtree(link_path)
        
        try:
            os.symlink(path, link_path)
        except (OSError, NotImplementedError):
            shutil.copytree(path, link_path)
        
        # Update nxs.json
        self.update_package_json(name)
    
    def update_package_json(self, package_name: str):
        """Update nxs.json with installed package"""
        if self.project_package_json.exists():
            with open(self.project_package_json, 'r') as f:
                pkg_json = json.load(f)
        else:
            pkg_json = {"dependencies": {}, "devDependencies": {}}
        
        if "dependencies" not in pkg_json:
            pkg_json["dependencies"] = {}
        
        pkg_json["dependencies"][package_name] = "*"
        
        with open(self.project_package_json, 'w') as f:
            json.dump(pkg_json, f, indent=2)
    
    def remove(self, package_name: str):
        """Remove a package"""
        print(f"Removing {package_name}...")
        
        link_path = self.project_packages / package_name
        if link_path.exists():
            shutil.rmtree(link_path)
        
        # Remove from nxs.json
        if self.project_package_json.exists():
            with open(self.project_package_json, 'r') as f:
                pkg_json = json.load(f)
            
            if "dependencies" in pkg_json and package_name in pkg_json["dependencies"]:
                del pkg_json["dependencies"][package_name]
            
            with open(self.project_package_json, 'w') as f:
                json.dump(pkg_json, f, indent=2)
        
        print(f"  ✓ Removed {package_name}")
    
    def search(self, query: str):
        """Search for packages"""
        print(f"Searching for '{query}'...")
        
        results = []
        
        # Search custom registry
        for name in self.registry["packages"]:
            if query.lower() in name.lower():
                results.append((name, "custom"))
        
        # Search npm
        try:
            result = subprocess.run(
                ["npm", "search", query, "--json"],
                capture_output=True,
                text=True,
                timeout=10
            )
            if result.returncode == 0:
                npm_results = json.loads(result.stdout)
                for pkg in npm_results[:5]:  # Limit to 5 results
                    results.append((pkg["name"], "npm"))
        except:
            pass
        
        if results:
            print(f"\nFound {len(results)} package(s):\n")
            for name, source in results[:10]:
                print(f"  {name:40} ({source})")
        else:
            print("  No packages found")
    
    def publish(self, package_name: str, version: str, description: str = ""):
        """Publish a custom package"""
        pkg_info = {
            "name": package_name,
            "version": version,
            "description": description,
            "path": str(Path.cwd()),
            "type": "custom"
        }
        
        self.registry["packages"][package_name] = pkg_info
        self.save_registry()
        print(f"  ✓ Published {package_name}@{version}")
    
    def list_packages(self):
        """List installed packages"""
        if not self.project_packages.exists():
            print("No packages installed")
            return
        
        packages = list(self.project_packages.iterdir())
        if not packages:
            print("No packages installed")
            return
        
        print(f"Installed packages ({len(packages)}):\n")
        for pkg in sorted(packages):
            size = sum(f.stat().st_size for f in pkg.rglob('*') if f.is_file())
            size_mb = size / (1024 * 1024)
            print(f"  {pkg.name:30} {size_mb:.2f}MB")
    
    def get_version(self):
        """Get nxs version"""
        return "1.0.0"
    
    def run_script(self, script_name: str):
        """Run a script defined in nxs.json"""
        if not self.project_package_json.exists():
            print("❌ nxs.json not found")
            sys.exit(1)
        
        with open(self.project_package_json, 'r') as f:
            pkg_json = json.load(f)
        
        if "scripts" not in pkg_json or script_name not in pkg_json["scripts"]:
            print(f"❌ Script '{script_name}' not found in nxs.json")
            sys.exit(1)
        
        script = pkg_json["scripts"][script_name]
        print(f"▶️  Running script: {script}")
        
        result = subprocess.run(script, shell=True)
        sys.exit(result.returncode)
    
    def add_dependencies(self, packages: List[str], dev: bool = False):
        """Add multiple dependencies at once"""
        for pkg in packages:
            version = "latest"
            if "@" in pkg:
                pkg, version = pkg.rsplit("@", 1)
            self.install(pkg, version)
    
    def update_all(self):
        """Update all packages"""
        if not self.project_package_json.exists():
            print("❌ nxs.json not found")
            return
        
        with open(self.project_package_json, 'r') as f:
            pkg_json = json.load(f)
        
        if "dependencies" in pkg_json:
            print("🔄 Updating all packages...")
            for pkg_name in pkg_json["dependencies"]:
                print(f"  Updating {pkg_name}...")
                self.install(pkg_name, "latest")
        
        print("✅ All packages updated")


def main():
    if len(sys.argv) < 2:
        print("╔═══════════════════════════════════════════╗")
        print("║   Nexus Package Manager (nxs) v1.0.0      ║")
        print("║   npm-compatible package management       ║")
        print("╚═══════════════════════════════════════════╝")
        print()
        print("Usage: nxs <command> [args]")
        print()
        print("Commands:")
        print("  install <package>         Install a package")
        print("  install <pkg1> <pkg2>...  Install multiple packages")
        print("  remove package <package>  Remove a package")
        print("  search <query>            Search for packages")
        print("  list                      List installed packages")
        print("  update                    Update all packages")
        print("  run <script>              Run a script from nxs.json")
        print("  publish <name> <version>  Publish a package")
        print("  version                   Show nxs version")
        print()
        print("Examples:")
        print("  nxs install react vue express")
        print("  nxs install @types/node")
        print("  nxs search database")
        print("  nxs run build")
        sys.exit(1)
    
    pm = NxsPackageManager()
    command = sys.argv[1]
    
    if command == "install":
        if len(sys.argv) < 3:
            print("Usage: nxs install <package> [package2] [package3]...")
            sys.exit(1)
        packages = sys.argv[2:]
        pm.add_dependencies(packages)
    
    elif command == "remove":
        if len(sys.argv) < 4 or sys.argv[2] != "package":
            print("Usage: nxs remove package <package>")
            sys.exit(1)
        pm.remove(sys.argv[3])
    
    elif command == "search":
        if len(sys.argv) < 3:
            print("Usage: nxs search <query>")
            sys.exit(1)
        pm.search(sys.argv[2])
    
    elif command == "list":
        pm.list_packages()
    
    elif command == "update":
        pm.update_all()
    
    elif command == "run":
        if len(sys.argv) < 3:
            print("Usage: nxs run <script>")
            sys.exit(1)
        pm.run_script(sys.argv[2])
    
    elif command == "publish":
        if len(sys.argv) < 4:
            print("Usage: nxs publish <name> <version> [description]")
            sys.exit(1)
        desc = sys.argv[4] if len(sys.argv) > 4 else ""
        pm.publish(sys.argv[2], sys.argv[3], desc)
    
    elif command == "version":
        print(f"nxs {pm.get_version()}")
    
    else:
        print(f"❌ Unknown command: {command}")
        print("Try 'nxs' for help")
        sys.exit(1)


if __name__ == "__main__":
    main()
