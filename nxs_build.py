"""
Nexus Build System
Bundles and compiles .nxs and .nxsjs files
"""

import os
import json
import shutil
import subprocess
from pathlib import Path
from typing import Dict, List, Any

class NexusBuildConfig:
    def __init__(self, config_file: str = "nxs.json"):
        self.config_file = config_file
        self.config = self.load_config()
    
    def load_config(self) -> Dict[str, Any]:
        """Load build configuration"""
        if Path(self.config_file).exists():
            with open(self.config_file, 'r') as f:
                return json.load(f)
        
        return {
            "name": "nexus-app",
            "version": "1.0.0",
            "entry": {
                "frontend": "src/index.nxs",
                "backend": "src/api.nxsjs"
            },
            "output": {
                "frontend": "dist/index.html",
                "backend": "dist/app.py"
            },
            "dependencies": {},
            "devDependencies": {}
        }
    
    def save_config(self):
        """Save configuration"""
        with open(self.config_file, 'w') as f:
            json.dump(self.config, f, indent=2)


class NexusBuilder:
    def __init__(self, config: NexusBuildConfig):
        self.config = config
        self.dist_dir = Path("dist")
        self.src_dir = Path("src")
    
    def build(self):
        """Build the project"""
        print("🏗️  Building Nexus project...")
        
        # Clean dist
        if self.dist_dir.exists():
            shutil.rmtree(self.dist_dir)
        self.dist_dir.mkdir(parents=True)
        
        # Build frontend
        self.build_frontend()
        
        # Build backend
        self.build_backend()
        
        # Copy assets
        self.copy_assets()
        
        print("✅ Build complete!")
    
    def build_frontend(self):
        """Compile .nxs frontend files"""
        print("  📦 Compiling frontend...")
        
        entry = self.config.config.get("entry", {}).get("frontend")
        if not entry or not Path(entry).exists():
            print("    ℹ️  No frontend entry found")
            return
        
        try:
            from nxs_frontend import NxsCompiler
            compiler = NxsCompiler(entry)
            output = self.config.config.get("output", {}).get("frontend", "dist/index.html")
            compiler.write_output(output)
        except Exception as e:
            print(f"    ❌ Frontend build failed: {e}")
    
    def build_backend(self):
        """Compile .nxsjs backend files"""
        print("  🔧 Compiling backend...")
        
        entry = self.config.config.get("entry", {}).get("backend")
        if not entry or not Path(entry).exists():
            print("    ℹ️  No backend entry found")
            return
        
        try:
            from nxs_backend import NxsjsCompiler
            compiler = NxsjsCompiler(entry)
            python_code = compiler.compile()
            output = self.config.config.get("output", {}).get("backend", "dist/app.py")
            Path(output).parent.mkdir(parents=True, exist_ok=True)
            with open(output, 'w') as f:
                f.write(python_code)
            print(f"    ✓ Compiled {entry} -> {output}")
        except Exception as e:
            print(f"    ❌ Backend build failed: {e}")
    
    def copy_assets(self):
        """Copy static assets"""
        assets_dir = self.src_dir / "assets"
        if assets_dir.exists():
            print("  📋 Copying assets...")
            shutil.copytree(assets_dir, self.dist_dir / "assets", dirs_exist_ok=True)


class NexusDevServer:
    def __init__(self, config: NexusBuildConfig):
        self.config = config
        self.watch_dirs = ["src"]
    
    def start(self, port: int = 5000):
        """Start development server"""
        print(f"🚀 Starting dev server on port {port}...")
        
        try:
            from http.server import HTTPServer, SimpleHTTPRequestHandler
            import threading
            
            os.chdir("dist")
            
            class Handler(SimpleHTTPRequestHandler):
                def end_headers(self):
                    self.send_header("Cache-Control", "no-store, no-cache, must-revalidate")
                    super().end_headers()
            
            server = HTTPServer(('localhost', port), Handler)
            print(f"  📍 http://localhost:{port}")
            server.serve_forever()
        
        except Exception as e:
            print(f"❌ Server failed: {e}")


class NexusWatcher:
    """Watch for file changes and rebuild"""
    
    def __init__(self, config: NexusBuildConfig):
        self.config = config
        self.builder = NexusBuilder(config)
        self.last_build = {}
    
    def watch(self):
        """Watch for changes"""
        import time
        print("👀 Watching for changes...")
        
        try:
            while True:
                changed = False
                
                for file in Path("src").rglob("*"):
                    if file.is_file():
                        mtime = file.stat().st_mtime
                        if str(file) not in self.last_build or self.last_build[str(file)] < mtime:
                            changed = True
                            self.last_build[str(file)] = mtime
                
                if changed:
                    print("\n📝 Changes detected, rebuilding...")
                    self.builder.build()
                
                time.sleep(1)
        
        except KeyboardInterrupt:
            print("\n\n👋 Stopped watching")


def main():
    import sys
    
    if len(sys.argv) < 2:
        print("Nexus Build System")
        print()
        print("Usage: nexus build <command>")
        print()
        print("Commands:")
        print("  build              Build the project")
        print("  dev                Start development server")
        print("  watch              Watch for changes and rebuild")
        print("  init               Initialize a new project")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "init":
        init_project()
    
    else:
        config = NexusBuildConfig()
        
        if command == "build":
            builder = NexusBuilder(config)
            builder.build()
        
        elif command == "dev":
            port = int(sys.argv[2]) if len(sys.argv) > 2 else 5000
            builder = NexusBuilder(config)
            builder.build()
            dev_server = NexusDevServer(config)
            dev_server.start(port)
        
        elif command == "watch":
            watcher = NexusWatcher(config)
            watcher.watch()
        
        else:
            print(f"Unknown command: {command}")
            sys.exit(1)


def init_project():
    """Initialize a new Nexus project"""
    print("🆕 Initializing Nexus project...")
    
    # Create directories
    Path("src").mkdir(exist_ok=True)
    Path("src/assets").mkdir(exist_ok=True)
    
    # Create nxs.json
    config = {
        "name": "nexus-app",
        "version": "1.0.0",
        "entry": {
            "frontend": "src/index.nxs",
            "backend": "src/api.nxsjs"
        },
        "output": {
            "frontend": "dist/index.html",
            "backend": "dist/app.py"
        },
        "dependencies": {},
        "devDependencies": {}
    }
    
    with open("nxs.json", 'w') as f:
        json.dump(config, f, indent=2)
    
    # Create sample frontend
    with open("src/index.nxs", 'w') as f:
        f.write("""<view class="app">
    <h1>Welcome to Nexus</h1>
    
    <card>
        <h2>Hello World</h2>
        <input type="text" placeholder="Enter your name" @bind="name" />
        <btn @click="handleClick()">Click Me</btn>
    </card>
</view>

<script>
function handleClick() {
    alert('Hello from Nexus!');
}
</script>
""")
    
    # Create sample backend
    with open("src/api.nxsjs", 'w') as f:
        f.write("""@config {
    port: 5000,
    database: 'nexus.db'
}

@model User {
    name: string,
    email: string,
    created: datetime
}

@route GET "/api/users" {
    return "SELECT * FROM users"
}

@route POST "/api/users" @auth {
    return "INSERT INTO users (name, email) VALUES (?, ?)"
}

@middleware auth {
    print("Checking authentication")
}
""")
    
    print("✅ Project initialized!")
    print("   - nxs.json created")
    print("   - src/index.nxs (frontend)")
    print("   - src/api.nxsjs (backend)")
    print()
    print("Next steps:")
    print("  nexus build build      # Build the project")
    print("  nexus build dev        # Start dev server")
    print("  nexus build watch      # Watch for changes")


if __name__ == "__main__":
    main()
