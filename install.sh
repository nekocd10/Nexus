#!/usr/bin/env bash
# Nexus Programming Language - Installation Script
# This script sets up the Nexus CLI for global use
# Usage: bash install.sh

set -e

echo "╔═══════════════════════════════════════════╗"
echo "║     Nexus Programming Language Setup       ║"
echo "║    Installing global CLI commands...       ║"
echo "╚═══════════════════════════════════════════╝"
echo ""

# Detect OS
OS="$(uname -s)"
case "$OS" in
    Linux*)
        PLATFORM="linux"
        ;;
    Darwin*)
        PLATFORM="macos"
        ;;
    MINGW*|MSYS*|CYGWIN*)
        PLATFORM="windows"
        ;;
    *)
        PLATFORM="unknown"
        ;;
esac

echo "✓ Detected platform: $PLATFORM"
echo ""

# Get the script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
echo "✓ Installation directory: $SCRIPT_DIR"
echo ""

# Check Python installation
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not installed"
    echo "   Please install Python 3.8 or higher"
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
echo "✓ Python version: $PYTHON_VERSION"
echo ""

# Install Python package
echo "📦 Installing Python package..."
cd "$SCRIPT_DIR"
python3 -m pip install -e . --quiet

if [ $? -eq 0 ]; then
    echo "✓ Python package installed"
else
    echo "⚠️  Failed to install Python package, continuing anyway..."
fi
echo ""

# Create CLI entry points
echo "🔗 Creating CLI entry points..."

# For Linux/macOS
if [ "$PLATFORM" != "windows" ]; then
    # Create nexus command wrapper
    if [ -d "/usr/local/bin" ] && [ -w "/usr/local/bin" ]; then
        cat > /usr/local/bin/nexus << 'EOF'
#!/usr/bin/env python3
"""
Nexus Programming Language CLI
Global entry point
"""

import sys
import os

# Add the nexus directory to Python path
nexus_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if os.path.exists(os.path.join(nexus_dir, "nexus_cli.py")):
    sys.path.insert(0, nexus_dir)

try:
    from nexus_cli import main
    main()
except ImportError:
    # Fallback to installed package
    from nexus_cli import main
    main()
EOF
        chmod +x /usr/local/bin/nexus
        echo "✓ Created /usr/local/bin/nexus"
    else
        echo "⚠️  Cannot write to /usr/local/bin (needs sudo)"
    fi
    
    # Create nxs command wrapper
    if [ -d "/usr/local/bin" ] && [ -w "/usr/local/bin" ]; then
        cat > /usr/local/bin/nxs << 'EOF'
#!/usr/bin/env python3
"""
Nexus Package Manager CLI
Global entry point
"""

import sys
import os

# Add the nexus directory to Python path
nexus_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if os.path.exists(os.path.join(nexus_dir, "nxs_pm.py")):
    sys.path.insert(0, nexus_dir)

try:
    from nxs_pm import main
    main()
except ImportError:
    # Fallback to installed package
    from nxs_pm import main
    main()
EOF
        chmod +x /usr/local/bin/nxs
        echo "✓ Created /usr/local/bin/nxs"
    fi
fi

echo ""
echo "╔═══════════════════════════════════════════╗"
echo "║         Installation Complete!             ║"
echo "╚═══════════════════════════════════════════╝"
echo ""
echo "You can now use:"
echo "  • nexus <command>      - Nexus CLI"
echo "  • nxs <command>        - Package manager"
echo ""
echo "Try these commands:"
echo "  nexus help             - Show help"
echo "  nexus new myapp        - Create a new project"
echo "  nxs search react       - Search for packages"
echo ""
echo "For more information:"
echo "  https://github.com/nekocd10/maybe-a-custom-language"
echo ""
