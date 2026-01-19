# Nexus Installation Guide

Complete guide to install and set up Nexus Programming Language with global CLI support.

## Quick Start

### Option 1: Automatic Installation (Recommended)

```bash
# Clone the repository
git clone https://github.com/nekocd10/maybe-a-custom-language.git
cd maybe-a-custom-language

# Run installation script
bash install.sh
```

After installation, you can use `nexus` and `nxs` commands globally from any directory:

```bash
nexus new myapp              # Create a new project
nexus dev                    # Start development server
nxs install react express    # Install packages
nxs remove package react     # Remove a package
```

### Option 2: Manual Installation

#### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Node.js 12+ (optional, for JavaScript interop)
- npm (optional, for npm package support)

#### Step 1: Clone Repository

```bash
git clone https://github.com/nekocd10/maybe-a-custom-language.git
cd maybe-a-custom-language
```

#### Step 2: Install Python Package

```bash
# Install in development mode
python3 -m pip install -e .

# Or install normally
python3 setup.py install
```

#### Step 3: Verify Installation

```bash
# Test nexus command
nexus --version

# Test nxs command
nxs --version
```

## Setting Up CLI Manually

If the installation script doesn't work, you can set up the CLI manually:

### Linux/macOS

Create wrapper scripts:

```bash
# Create /usr/local/bin/nexus
sudo nano /usr/local/bin/nexus
```

Add this content:

```bash
#!/usr/bin/env python3
import sys
from nexus_cli import main
main()
```

Make it executable:

```bash
sudo chmod +x /usr/local/bin/nexus
sudo chmod +x /usr/local/bin/nxs
```

### Windows

Create batch files in a directory on your PATH:

**nexus.bat:**
```batch
@echo off
python -m nexus_cli %*
```

**nxs.bat:**
```batch
@echo off
python -m nxs_pm %*
```

## Project Structure

After installation, the following structure is created:

```
maybe-a-custom-language/
├── nexus                    # Main entry point
├── nexus_cli.py            # CLI interface
├── nexus_interpreter.py    # Language interpreter
├── nexus_lexer.py          # Tokenizer
├── nexus_parser.py         # Parser
├── nxs_pm.py               # Package manager
├── nxs_frontend.py         # Frontend compiler (.nxs)
├── nxs_backend.py          # Backend compiler (.nxsjs)
├── nxs_build.py            # Build system
├── nxs_bundler.py          # Bundler
├── nxs_interop.py          # Interoperability layer
├── setup.py                # Python package setup
├── install.sh              # Installation script
└── nexus_examples/         # Example programs
```

## First Steps

### 1. Create a New Project

```bash
nexus new myapp
cd myapp
```

This creates a new Nexus project with:
- `src/index.nxs` - Frontend entry point
- `src/api.nxsjs` - Backend entry point
- `nxs.json` - Project configuration

### 2. Install Dependencies

```bash
nxs install react express  # Install multiple packages at once
```

### 3. Start Development

```bash
nexus dev                   # Start dev server on port 5000
```

Open http://localhost:5000 in your browser.

### 4. Build for Production

```bash
nexus build
```

Output files are in the `dist/` directory.

## Common Commands

### Nexus CLI

```bash
# Create new project
nexus new <project-name>

# Run a file
nexus run script.nexus

# Start development server
nexus dev [port]

# Build project
nexus build

# Interactive REPL
nexus repl

# Show version
nexus --version

# Get help
nexus help
```

### Package Manager (nxs)

```bash
# Install packages
nxs install package1 package2 package3

# Remove package
nxs remove package

# Search packages
nxs search query

# List installed packages
nxs list

# Run scripts from nxs.json
nxs run build

# Update all packages
nxs update

# Publish package
nxs publish name version

# Show version
nxs version
```

## Environment Setup

### Windows PATH Setup

1. Open Environment Variables:
   - Press `Win + X`, select "System"
   - Click "Advanced system settings"
   - Click "Environment Variables"

2. Add Python Scripts directory to PATH:
   - Find "Path" in System variables
   - Click "Edit"
   - Add: `C:\Python\Scripts\` (adjust for your Python installation)

### macOS/Linux PATH Setup

If `/usr/local/bin` is not in your PATH, add it:

```bash
# Add to ~/.bashrc or ~/.zshrc
export PATH="/usr/local/bin:$PATH"

# Reload
source ~/.bashrc
# or
source ~/.zshrc
```

## Troubleshooting

### Command Not Found

```bash
# Check if Python package is installed
python3 -m pip show nexus-lang

# Reinstall if needed
python3 -m pip install -e .
```

### Python Version Issues

```bash
# Verify Python 3.8+
python3 --version

# Try with specific version if multiple installed
python3.10 -m pip install -e .
```

### Permission Denied

```bash
# On Linux/macOS, if you get permission errors:
# Option 1: Use sudo (not recommended)
sudo bash install.sh

# Option 2: Install for current user only
python3 -m pip install --user -e .

# Then add to PATH:
export PATH="$HOME/.local/bin:$PATH"
```

### Node.js Not Found

For full functionality with JavaScript interop:

```bash
# Install Node.js (macOS with Homebrew)
brew install node

# Or from nodejs.org
# Then verify:
node --version
npm --version
```

## Uninstallation

### Remove Global Commands

```bash
# Linux/macOS
sudo rm /usr/local/bin/nexus
sudo rm /usr/local/bin/nxs
```

### Remove Python Package

```bash
python3 -m pip uninstall nexus-lang
```

## Next Steps

- [Create your first Nexus project](GETTING_STARTED.md)
- [Learn Nexus syntax](NEXUS_SPEC.md)
- [Explore examples](nexus_examples/)
- [Build full-stack apps](IMPLEMENTATION_GUIDE.md)

## Support

- Documentation: [README.md](README.md)
- Implementation Guide: [IMPLEMENTATION_GUIDE.md](IMPLEMENTATION_GUIDE.md)
- Examples: [nexus_examples/](nexus_examples/)
- Issues: [GitHub Issues](https://github.com/nekocd10/maybe-a-custom-language/issues)

## License

MIT - See LICENSE file for details
