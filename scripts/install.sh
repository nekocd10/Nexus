#!/usr/bin/env bash
# Nexus Programming Language - Installation Script
# Local installation script - runs from the repository
# For curl-based installation, see installer.sh

set -e

# Get the script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

print_success() {
    echo -e "${GREEN}✓${NC} $1"
}

print_error() {
    echo -e "${RED}✗${NC} $1"
}

echo ""
echo -e "${BLUE}╔═══════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║     Nexus Programming Language Setup       ║${NC}"
echo -e "${BLUE}║    Installing from local repository        ║${NC}"
echo -e "${BLUE}╚═══════════════════════════════════════════╝${NC}"
echo ""

# Check Python installation
if ! command -v python3 &> /dev/null; then
    print_error "Python 3 is required but not installed"
    echo "   Please install Python 3.8 or higher"
    exit 1
fi

PYTHON_VERSION=$(python3 --version 2>&1 | cut -d' ' -f2)
print_success "Python version: $PYTHON_VERSION"

# Install Python package
echo ""
echo "Installing Nexus package in development mode..."
cd "$SCRIPT_DIR"
python3 -m pip install -e . 

if [ $? -eq 0 ]; then
    print_success "Package installed successfully"
else
    print_error "Failed to install package"
    exit 1
fi

# Verify installation
echo ""
echo "Verifying installation..."
if nexus --version &> /dev/null; then
    print_success "Nexus CLI is available"
    nexus --version
else
    print_error "Nexus CLI not found in PATH"
    echo "You may need to restart your terminal or add Python's bin to PATH"
fi

echo ""
echo -e "${GREEN}╔════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║     Installation Complete!              ║${NC}"
echo -e "${GREEN}╚════════════════════════════════════════╝${NC}"
echo ""
echo "Next steps:"
echo "1. Try your first program:"
echo "   echo 'println \"Hello, Nexus!\"' > hello.nexus"
echo "   nexus hello.nexus"
echo ""
echo "2. View documentation:"
echo "   cat docs/DOCUMENTATION.md"
echo ""
echo "3. Explore examples:"
echo "   ls examples/"
echo ""
