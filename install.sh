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
    # Determine installation prefix
    INSTALL_PREFIX="/usr/local"
    
    # Check if we have write permissions
    if [ ! -w "$INSTALL_PREFIX/bin" ]; then
        echo "⚠️  No write access to $INSTALL_PREFIX/bin (trying with sudo)..."
        SUDO="sudo"
    else
        SUDO=""
    fi
    
    # Create nexus command wrapper
    cat > /tmp/nexus << 'EOF'
#!/usr/bin/env python3
"""
Nexus Programming Language CLI
Global entry point - installed via setuptools
"""

import sys
import os

try:
    from nexus_cli import main
    main()
except ImportError as e:
    print(f"Error: Nexus CLI not found. Please reinstall: pip install -e .", file=sys.stderr)
    sys.exit(1)
EOF
    
    $SUDO install -m 755 /tmp/nexus "$INSTALL_PREFIX/bin/nexus"
    echo "✓ Created $INSTALL_PREFIX/bin/nexus"
    
    # Create nxs command wrapper
    cat > /tmp/nxs << 'EOF'
#!/usr/bin/env python3
"""
Nexus Package Manager CLI
Global entry point - installed via setuptools
"""

import sys
import os

try:
    from nxs_pm import main
    main()
except ImportError as e:
    print(f"Error: Nexus PM not found. Please reinstall: pip install -e .", file=sys.stderr)
    sys.exit(1)
EOF
    
    $SUDO install -m 755 /tmp/nxs "$INSTALL_PREFIX/bin/nxs"
    echo "✓ Created $INSTALL_PREFIX/bin/nxs"
    
    # Verify installation
    if command -v nexus &> /dev/null; then
        echo "✓ Verified: nexus command is available in PATH"
    else
        echo "⚠️  Warning: nexus command not found in PATH"
        echo "   Make sure $INSTALL_PREFIX/bin is in your PATH"
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
