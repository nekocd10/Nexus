#!/usr/bin/env python3
"""
Nexus CLI - Unified command-line interface for the Nexus ecosystem
Manages: language, package manager, frontend, backend, building, and deployment
"""

import sys
import os
import json
import argparse
import subprocess
from pathlib import Path
from typing import Optional


class NexusCLI:
    def __init__(self):
        self.version = "1.0.0"
        self.commands = {
            "new": "Create a new Nexus project",
            "install": "Install Nexus package",
            "nxs": "NPM package manager commands",
            "run": "Run a Nexus file",
            "build": "Build the project",
            "dev": "Start development server",
            "deploy": "Deploy to production",
            "repl": "Interactive REPL",
            "version": "Show version",
            "help": "Show help"
        }
    
    def main(self):
        """Main entry point"""
        if len(sys.argv) < 2:
            self.show_help()
            return
        
        command = sys.argv[1]
        args = sys.argv[2:]
        
        if command == "new":
            self.cmd_new(args)
        elif command == "install":
            self.cmd_install(args)
        elif command == "nxs":
            self.cmd_nxs(args)
        elif command == "run":
            self.cmd_run(args)
        elif command == "build":
            self.cmd_build(args)
        elif command == "dev":
            self.cmd_dev(args)
        elif command == "deploy":
            self.cmd_deploy(args)
        elif command == "repl":
            self.cmd_repl()
        elif command == "version":
            print(f"Nexus v{self.version}")
        elif command == "help" or command == "-h" or command == "--help":
            self.show_help()
        else:
            print(f"❌ Unknown command: {command}")
            print("Try 'nexus help' for more information")
            sys.exit(1)
    
    def show_help(self):
        """Show help message"""
        print("╔═══════════════════════════════════════════╗")
        print("║         Nexus Command Line Interface       ║")
        print("║    A Complete Programming Ecosystem        ║")
        print("╚═══════════════════════════════════════════╝")
        print()
        print("USAGE: nexus <command> [options]")
        print()
        print("COMMANDS:")
        for cmd, desc in self.commands.items():
            print(f"  {cmd:<15} {desc}")
        print()
        print("EXAMPLES:")
        print("  nexus new myapp              # Create new project")
        print("  nexus install mylib          # Install Nexus package")
        print("  nexus nxs install react      # Install NPM package")
        print("  nexus run script.nexus       # Run Nexus file")
        print("  nexus build                  # Build project")
        print("  nexus dev                    # Start dev server")
        print()
    
    def cmd_new(self, args: list):
        """Create a new project"""
        if not args:
            print("Usage: nexus new <project-name>")
            sys.exit(1)
        
        project_name = args[0]
        project_path = Path(project_name)
        
        if project_path.exists():
            print(f"❌ Directory '{project_name}' already exists")
            sys.exit(1)
        
        print(f"🆕 Creating Nexus project: {project_name}")
        
        project_path.mkdir(parents=True)
        
        # Create directory structure
        (project_path / "src").mkdir()
        (project_path / "src" / "components").mkdir()
        (project_path / "public").mkdir()
        
        # Create nxs.json
        nxs_config = {
            "name": project_name,
            "version": "1.0.0",
            "description": "A Nexus project",
            "entry": {
                "frontend": "src/index.nxs",
                "backend": "src/api.nxsjs"
            },
            "output": {
                "frontend": "dist/index.html",
                "backend": "dist/app.py"
            },
            "dependencies": {},
            "devDependencies": {},
            "scripts": {
                "dev": "nexus dev",
                "build": "nexus build",
                "start": "nexus dev"
            }
        }
        
        with open(project_path / "nxs.json", 'w') as f:
            json.dump(nxs_config, f, indent=2)
        
        # Create sample files
        self._create_sample_frontend(project_path / "src" / "index.nxs")
        self._create_sample_backend(project_path / "src" / "api.nxsjs")
        self._create_sample_readme(project_path / "README.md")
        
        print()
        print("✅ Project created successfully!")
        print()
        print(f"  cd {project_name}")
        print("  nexus install <nexus-pkg>      # Install Nexus packages")
        print("  nexus nxs install <npm-pkg>    # Install NPM packages")
        print("  nexus dev                      # Start dev server")
        print()
    
    def cmd_install(self, args: list):
        """Install Nexus package"""
        if not args:
            print("Usage: nexus install <package> [version]")
            sys.exit(1)
        
        package_name = args[0]
        version = args[1] if len(args) > 1 else "latest"
        
        try:
            # use relative import so entrypoint "nexus" works both installed and
            # when running `python -m src.cli` during development
            from .package_manager import NxsPackageManager
            pm = NxsPackageManager()
            
            # Try custom registry first, then local
            if pm.try_install_custom(package_name, version):
                return
            if pm.try_install_local(package_name):
                return
            
            print(f"❌ Nexus package '{package_name}' not found")
        
        except ImportError:
            print("❌ Package manager not available")
            sys.exit(1)
    
    def cmd_nxs(self, args: list):
        """NPM package manager commands"""
        if not args:
            print("Usage: nexus nxs <command> [package]")
            print()
            print("Commands:")
            print("  install <pkg>   # Install NPM package")
            print("  remove <pkg>    # Remove package")
            print("  search <query>  # Search packages")
            print("  list            # List installed packages")
            print("  package <pkg> version  # Show package version")
            print("  publish         # Publish package")
            return
        
        command = args[0]
        
        try:
            from src.package_manager import NxsPackageManager
            pm = NxsPackageManager()
            
            if command == "install" and len(args) > 1:
                package = args[1]
                version = args[2] if len(args) > 2 else "latest"
                if not pm.try_install_npm(package, version):
                    print(f"❌ NPM package '{package}' not found")
            
            elif command == "remove" and len(args) > 1:
                package = args[1]
                pm.remove(package)
            
            elif command == "search" and len(args) > 1:
                query = args[1]
                pm.search(query)
            
            elif command == "list":
                pm.list_packages()
            
            elif command == "publish":
                pm.publish()
            
            elif command == "package" and len(args) >= 3 and args[2] == "version":
                package_name = args[1]
                version = pm.get_package_version(package_name)
                if version:
                    print(f"{package_name}@{version}")
                else:
                    print(f"Package '{package_name}' not found or version unknown")
            
            else:
                print(f"Unknown nxs command: {command}")
        
        except ImportError:
            print("❌ Package manager not available")
            sys.exit(1)
    
    def cmd_run(self, args: list):
        """Run a Nexus file"""
        if not args:
            print("Usage: nexus run <file.nexus>")
            sys.exit(1)
        
        file_path = args[0]
        
        if not Path(file_path).exists():
            print(f"❌ File not found: {file_path}")
            sys.exit(1)
        
        print(f"▶️  Running: {file_path}")
        
        try:
            # interpreter/lexer/parser modules are located in this package
            from .interpreter import NexusInterpreter
            from .lexer import NexusLexer
            from .parser import NexusParser
            
            with open(file_path, 'r') as f:
                source = f.read()
            
            lexer = NexusLexer(source)
            tokens = lexer.tokenize()
            
            parser = NexusParser(tokens)
            ast = parser.parse()
            
            interpreter = NexusInterpreter()
            interpreter.interpret(ast)
        
        except Exception as e:
            print(f"❌ Error: {e}")
            sys.exit(1)
    
    def cmd_build(self, args: list):
        """Build the project"""
        config_file = "nxs.json"
        
        if not Path(config_file).exists():
            print("❌ nxs.json not found. Are you in a Nexus project?")
            sys.exit(1)
        
        print("🏗️  Building project...")
        
        try:
            # builder module lives in this package; earlier versions imported
            # from a top‑level `nxs_build` package which isn't provided by
            # our setup.py. use relative import to ensure it resolves correctly
            from .build import NexusBuilder, NexusBuildConfig
            config = NexusBuildConfig(config_file)
            builder = NexusBuilder(config)
            builder.build()
        
        except ImportError:
            print("❌ Build system not available (missing `src.build`)")
            sys.exit(1)
    
    def cmd_dev(self, args: list):
        """Start development server"""
        config_file = "nxs.json"
        
        if not Path(config_file).exists():
            print("❌ nxs.json not found. Are you in a Nexus project?")
            sys.exit(1)
        
        port = int(args[0]) if args else 5000
        
        try:
            # same fix as build command above
            from .build import NexusBuilder, NexusBuildConfig, NexusDevServer
            config = NexusBuildConfig(config_file)
            builder = NexusBuilder(config)
            builder.build()
            
            server = NexusDevServer(config)
            server.start(port)
        
        except ImportError:
            print("❌ Build system not available (missing `src.build`)")
            sys.exit(1)
        except Exception as e:
            print(f"❌ Error: {e}")
            sys.exit(1)
    
    def cmd_deploy(self, args: list):
        """Deploy to production"""
        environment = args[0] if args else "production"
        
        print(f"🚀 Deploying to {environment}...")
        
        try:
            from nxs_build import NexusBuilder, NexusBuildConfig
            config = NexusBuildConfig("nxs.json")
            builder = NexusBuilder(config)
            builder.build()
            
            # Generate deployment artifacts
            dist_path = Path("dist")
            
            print(f"  📦 Build artifacts:")
            for file in dist_path.glob("**/*"):
                if file.is_file():
                    size = file.stat().st_size
                    print(f"     - {file.relative_to(dist_path)} ({size} bytes)")
            
            print()
            print("✅ Ready for deployment!")
            print(f"   Deploy the 'dist' directory to your {environment} server")
        
        except Exception as e:
            print(f"❌ Deployment failed: {e}")
            sys.exit(1)
    
    def cmd_repl(self):
        """Interactive REPL"""
        print("🎮 Nexus Interactive REPL")
        print("Type 'exit' to quit, 'help' for commands")
        print()
        
        try:
            from .interpreter import NexusInterpreter
            from .lexer import NexusLexer
            from .parser import NexusParser
            
            interpreter = NexusInterpreter()
            
            while True:
                try:
                    source = input("nexus> ").strip()
                    
                    if not source:
                        continue
                    
                    if source == "exit":
                        print("👋 Goodbye!")
                        break
                    
                    if source == "help":
                        print("Nexus REPL Commands:")
                        print("  exit     - Exit REPL")
                        print("  help     - Show this help")
                        print("  clear    - Clear environment")
                        continue
                    
                    if source == "clear":
                        interpreter = NexusInterpreter()
                        print("Cleared")
                        continue
                    
                    lexer = NexusLexer(source)
                    tokens = lexer.tokenize()
                    
                    parser = NexusParser(tokens)
                    ast = parser.parse()
                    
                    result = interpreter.interpret(ast)
                    if result is not None:
                        print(f"  => {result}")
                
                except KeyboardInterrupt:
                    print("\n^C")
                except Exception as e:
                    print(f"❌ Error: {e}")
        
        except ImportError:
            print("❌ Interpreter not available")
            sys.exit(1)
    
    def _create_sample_frontend(self, path: Path):
        """Create sample frontend file"""
        content = '''<view class="container">
    <h1>Welcome to Nexus</h1>
    
    <card class="hero">
        <h2>Build Modern Apps</h2>
        <p>A completely new programming language for full-stack development</p>
    </card>
    
    <card>
        <h3>Get Started</h3>
        <input type="text" placeholder="Enter your name" @bind="userName" />
        <input type="email" placeholder="Enter email" @bind="userEmail" />
        <btn @click="submitForm()">Submit</btn>
    </card>
    
    <card id="output" style="display:none;">
        <h3>Your Information</h3>
        <p>Name: <span id="display-name"></span></p>
        <p>Email: <span id="display-email"></span></p>
    </card>
</view>

<style>
.container { max-width: 800px; margin: 0 auto; padding: 20px; }
.hero { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; }
.card { border: 1px solid #ddd; border-radius: 8px; padding: 16px; margin: 16px 0; }
input { width: 100%; padding: 8px; margin: 8px 0; border: 1px solid #ddd; border-radius: 4px; }
btn { background: #667eea; color: white; padding: 10px 20px; border: none; border-radius: 4px; cursor: pointer; }
btn:hover { background: #764ba2; }
</style>

<script>
@state userName = ""
@state userEmail = ""

function submitForm() {
    document.getElementById("display-name").textContent = userName;
    document.getElementById("display-email").textContent = userEmail;
    document.getElementById("output").style.display = "block";
}
</script>
'''
        with open(path, 'w') as f:
            f.write(content)
    
    def _create_sample_backend(self, path: Path):
        """Create sample backend file"""
        content = '''@config {
    port: 5000,
    database: "nexus.db",
    cors: true
}

@model User {
    id: number,
    name: string,
    email: string,
    created_at: datetime
}

@route GET "/api/users" {
    SELECT * FROM users
}

@route GET "/api/users/:id" {
    SELECT * FROM users WHERE id = :id
}

@route POST "/api/users" @auth {
    INSERT INTO users (name, email) VALUES (?, ?)
}

@route PUT "/api/users/:id" @auth {
    UPDATE users SET name = ?, email = ? WHERE id = :id
}

@route DELETE "/api/users/:id" @admin {
    DELETE FROM users WHERE id = :id
}

@middleware auth {
    print("Checking authentication token")
}

@middleware admin {
    print("Checking admin privileges")
}
'''
        with open(path, 'w') as f:
            f.write(content)
    
    def _create_sample_readme(self, path: Path):
        """Create sample README file"""
        content = '''# Nexus Project

A modern full-stack application built with Nexus.

## Getting Started

```bash
# Install dependencies
nexus nxs install

# Start development server
nexus dev

# Build for production
nexus build
```

## Project Structure

```
src/
  ├── index.nxs          # Frontend entry point
  ├── api.nxsjs          # Backend entry point
  └── components/        # Reusable components
public/                  # Static assets
dist/                    # Built project
nxs.json                 # Project configuration
```

## Development

- **Frontend**: Write `.nxs` files with HTML and custom Nexus components
- **Backend**: Write `.nxsjs` files with decorators and routes
- **Dependencies**: Use `nexus nxs install` to add packages

## Resources

- [Nexus Documentation](https://nexus.dev/docs)
- [API Reference](https://nexus.dev/api)
- [Examples](https://nexus.dev/examples)

## License

MIT
'''
        with open(path, 'w') as f:
            f.write(content)


def main():
    cli = NexusCLI()
    cli.main()


if __name__ == "__main__":
    main()
