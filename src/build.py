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
                "frontend": "dist/index.nxs",
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
        """Copy .nxs frontend files to dist"""
        print("  📦 Bundling frontend...")
        
        entry = self.config.config.get("entry", {}).get("frontend")
        if not entry or not Path(entry).exists():
            print("    ℹ️  No frontend entry found")
            return
        
        try:
            # Copy .nxs files as-is (no conversion to HTML)
            output = self.config.config.get("output", {}).get("frontend", "dist/index.nxs")
            Path(output).parent.mkdir(parents=True, exist_ok=True)
            shutil.copy(entry, output)
            print(f"    ✓ Bundled {entry} -> {output}")
            
            # Also copy all other .nxs files in src/
            for nxs_file in Path("src").rglob("*.nxs"):
                if nxs_file.name != "index.nxs":
                    dest = self.dist_dir / "components" / nxs_file.name
                    dest.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy(nxs_file, dest)
                    print(f"    ✓ Bundled {nxs_file} -> {dest}")
        except Exception as e:
            print(f"    ❌ Frontend build failed: {e}")
    
    def build_backend(self):
        """Bundle .nxsjs backend files (pure Nexus format, not compiled)"""
        print("  🔧 Bundling backend...")
        
        entry = self.config.config.get("entry", {}).get("backend")
        if not entry or not Path(entry).exists():
            print("    ℹ️  No backend entry found")
            return
        
        try:
            # Copy main entry point as-is (pure Nexus format)
            output = self.config.config.get("output", {}).get("backend", "dist/api.nxsjs")
            Path(output).parent.mkdir(parents=True, exist_ok=True)
            shutil.copy(entry, output)
            print(f"    ✓ Bundled {entry} -> {output}")
            
            # Copy all other .nxsjs files in src/ as-is (pure Nexus backend format)
            for nxsjs_file in Path("src").rglob("*.nxsjs"):
                if nxsjs_file.name != Path(entry).name:
                    try:
                        # Copy .nxsjs files as-is to preserve pure Nexus backend syntax
                        dest = self.dist_dir / "api" / nxsjs_file.name
                        dest.parent.mkdir(parents=True, exist_ok=True)
                        shutil.copy(nxsjs_file, dest)
                        print(f"    ✓ Bundled {nxsjs_file} -> {dest}")
                    except Exception as e:
                        print(f"    ⚠️  Failed to bundle {nxsjs_file}: {e}")
        except Exception as e:
            print(f"    ❌ Backend build failed: {e}")
    
    def copy_assets(self):
        """Copy static assets and runtime files"""
        # Copy Nexus runtime
        print("  📋 Copying Nexus runtime...")
        
        # Try to find nexus-runtime.js from the Nexus installation
        import os
        nexus_package_dir = os.path.dirname(os.path.abspath(__file__))
        runtime_src = Path(nexus_package_dir) / "nexus-runtime.js"
        
        if not runtime_src.exists():
            # Fallback: look in src/ relative to current dir
            runtime_src = Path("src/nexus-runtime.js")
        
        if runtime_src.exists():
            shutil.copy(runtime_src, self.dist_dir / "nexus-runtime.js")
            print(f"    ✓ Copied nexus-runtime.js")
        else:
            print(f"    ⚠️  nexus-runtime.js not found at {runtime_src}")
        
        # Generate minimal index.html loader (stays in place)
        print("  📋 Generating HTML loader...")
        self.generate_loader_html()
        
        # Copy assets if present
        assets_dir = self.src_dir / "assets"
        if assets_dir.exists():
            print("  📋 Copying static assets...")
            shutil.copytree(assets_dir, self.dist_dir / "assets", dirs_exist_ok=True)
    
    def generate_loader_html(self):
        """Generate minimal HTML that loads and renders .nxs files"""
        loader_html = r"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Nexus Application</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: #f5f5f5;
            padding: 20px;
        }

        #app {
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 8px;
            padding: 20px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }

        .nxs-view { display: flex; flex-direction: column; gap: 10px; }
        .nxs-card { background: white; border-radius: 8px; padding: 16px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); margin: 8px 0; }
        .nxs-btn { background: #007AFF; color: white; border: none; border-radius: 6px; padding: 10px 20px; cursor: pointer; font-size: 16px; transition: background 0.2s; }
        .nxs-btn:hover { background: #0051D5; }
        .nxs-input { border: 1px solid #ddd; border-radius: 6px; padding: 8px 12px; font-size: 16px; width: 100%; }
        .nxs-input:focus { outline: none; border-color: #007AFF; box-shadow: 0 0 0 3px rgba(0,122,255,0.1); }
        .nxs-text { font-size: 16px; color: #333; line-height: 1.5; }
        .nxs-heading { font-size: 24px; font-weight: 600; color: #000; margin: 16px 0 8px 0; }
        .nxs-subheading { font-size: 18px; font-weight: 500; color: #333; margin: 12px 0 4px 0; }
        .nxs-error { background: #fee; color: #c33; padding: 12px; border-radius: 6px; margin: 10px 0; font-family: monospace; font-size: 12px; white-space: pre-wrap; word-break: break-word; max-height: 400px; overflow-y: auto; }
        .nxs-loading { text-align: center; padding: 40px 20px; color: #666; }
        .spinner { border: 3px solid #f3f3f3; border-top: 3px solid #007AFF; border-radius: 50%; width: 40px; height: 40px; animation: spin 1s linear infinite; margin: 0 auto 10px; }
        @keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }
        .debug-info { font-size: 12px; color: #666; margin-top: 20px; padding: 10px; background: #f9f9f9; border-radius: 4px; max-height: 200px; overflow-y: auto; white-space: pre-wrap; word-break: break-word; }
    </style>
</head>
<body>
    <div id="app">
        <div class="nxs-loading">
            <div class="spinner"></div>
            <p>Loading Nexus application...</p>
            <div class="debug-info" id="debug"></div>
        </div>
    </div>

    <script src="nexus-runtime.js"><\/script>
    <script>
        const debugEl = document.getElementById('debug');
        const log = (msg) => {
            console.log(msg);
            debugEl.innerHTML += msg + '\n';
        };

        (async function init() {
            try {
                log('[1/5] Checking if NexusRuntime is available...');
                if (typeof NexusRuntime === 'undefined') {
                    throw new Error('NexusRuntime class not loaded');
                }
                log('[1/5] ✓ NexusRuntime available');
                
                log('[2/5] Initializing Nexus runtime...');
                const runtime = new NexusRuntime();
                log('[2/5] ✓ Runtime initialized');
                
                log('[3/5] Loading index.nxs file...');
                await runtime.load('index.nxs');
                log('[3/5] ✓ Loaded ' + runtime.source.length + ' bytes');
                
                log('[4/5] Parsing Nexus code...');
                if (!runtime.ast) {
                    throw new Error('AST is null after parsing');
                }
                log('[4/5] ✓ Parsed ' + runtime.ast.body.length + ' statements');
                
                log('[5/5] Executing code and rendering...');
                runtime.execute();
                log('[5/5] ✓ Executed successfully');
                
                log('');
                log('✅ Application loaded and running!');
                log('State: ' + JSON.stringify(runtime.state, null, 2));
                log('Components: ' + runtime.components.length);
                log('Functions: ' + Object.keys(runtime.functions).join(', '));
                
                window.nexusRuntime = runtime;
                window.nxsDebug = {
                    state: () => runtime.state,
                    functions: () => Object.keys(runtime.functions),
                    components: () => runtime.components.length,
                    load: (file) => runtime.load(file),
                    execute: () => runtime.execute(),
                    reload: async () => { await runtime.load('index.nxs'); runtime.execute(); }
                };
                
                // Keep debug visible for inspection
            } catch (error) {
                console.error('ERROR:', error);
                console.error('Stack:', error.stack);
                log('');
                log('❌ ERROR: ' + error.message);
                log('');
                log('Stack Trace:');
                log(error.stack || 'No stack trace');
                
                const errorHtml = `
                    <div class="nxs-loading">
                        <div style="text-align: left; background: #fff3cd; padding: 20px; border-radius: 8px; margin: 20px 0; border: 1px solid #ffc107;">
                            <h2 style="color: #856404; margin-bottom: 10px;">⚠️ Application Error</h2>
                            <div class="nxs-error">${escapeHtml(error.message)}

Stack:
${escapeHtml(error.stack || 'No stack trace')}</div>
                        </div>
                    </div>
                `;
                document.getElementById('app').innerHTML = errorHtml;
            }
        })();
        
        function escapeHtml(text) {
            const div = document.createElement('div');
            div.textContent = text;
            return div.innerHTML;
        }
    <\/script>
</body>
</html>"""
        
        index_path = self.dist_dir / "index.html"
        with open(index_path, 'w') as f:
            f.write(loader_html)
        print(f"    ✓ Generated {index_path}")


class NexusDevServer:
    def __init__(self, config: NexusBuildConfig):
        self.config = config
        self.watch_dirs = ["src"]
    
    def start(self, port: int = 5000):
        """Start development server with .nxs/.nxsjs file interpretation"""
        print(f"🚀 Starting dev server on port {port}...")
        
        try:
            from http.server import HTTPServer, SimpleHTTPRequestHandler
            from src.interpreter import NexusInterpreter
            from src.backend import NxsjsInterpreter
            import json
            import threading
            
            os.chdir("dist")
            
            class NexusHandler(SimpleHTTPRequestHandler):
                def do_GET(self):
                    # Handle .nxs files (frontend)
                    if self.path.endswith('.nxs'):
                        try:
                            nxs_file = self.path.lstrip('/')
                            if Path(nxs_file).exists():
                                with open(nxs_file, 'r') as f:
                                    content = f.read()
                                
                                # Interpret .nxs file to get HTML/JS
                                from frontend import NxsParser
                                
                                parser = NxsParser(content)
                                result = parser.parse()
                                
                                self.send_response(200)
                                self.send_header("Content-type", "text/html")
                                self.end_headers()
                                self.wfile.write(str(result).encode())
                                return
                        except Exception as e:
                            print(f"Error interpreting .nxs: {e}")
                    
                    # Handle .nxsjs files (backend)
                    elif self.path.endswith('.nxsjs'):
                        try:
                            nxsjs_file = self.path.lstrip('/')
                            if Path(nxsjs_file).exists():
                                with open(nxsjs_file, 'r') as f:
                                    content = f.read()
                                
                                interpreter = NxsjsInterpreter()
                                result = interpreter.interpret(content)
                                
                                self.send_response(200)
                                self.send_header("Content-type", "application/json")
                                self.end_headers()
                                self.wfile.write(json.dumps(result).encode())
                                return
                        except Exception as e:
                            print(f"Error interpreting .nxsjs: {e}")
                    
                    # Default handling for other files
                    super().do_GET()
                
                def end_headers(self):
                    self.send_header("Cache-Control", "no-store, no-cache, must-revalidate")
                    super().end_headers()
            
            server = HTTPServer(('localhost', port), NexusHandler)
            print(f"  📍 http://localhost:{port}")
            print(f"  ⚡ Interpreting .nxs and .nxsjs files on request")
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
        print("Usage: nxs build <command>")
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
