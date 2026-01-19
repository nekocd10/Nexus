#!/usr/bin/env bash
# Nexus Programming Language - Curl-based Installer
# Usage: bash <(curl -sL https://github.com/nekocd10/maybe-a-custom-language/raw/main/installer.sh)
# Or:    bash <(wget -qO- https://github.com/nekocd10/maybe-a-custom-language/raw/main/installer.sh)

set -e

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

print_header() {
    echo ""
    echo -e "${BLUE}╔═══════════════════════════════════════════╗${NC}"
    echo -e "${BLUE}║     Nexus Programming Language Setup       ║${NC}"
    echo -e "${BLUE}║    Installing global CLI commands...       ║${NC}"
    echo -e "${BLUE}╚═══════════════════════════════════════════╝${NC}"
    echo ""
}

print_success() {
    echo -e "${GREEN}✓${NC} $1"
}

print_error() {
    echo -e "${RED}✗${NC} $1"
}

print_info() {
    echo -e "${BLUE}ℹ${NC} $1"
}

print_header

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

print_success "Detected platform: $PLATFORM"

# Check Python installation
if ! command -v python3 &> /dev/null; then
    print_error "Python 3 is required but not installed"
    echo "Please install Python 3.8 or higher"
    exit 1
fi

PYTHON_VERSION=$(python3 --version 2>&1 | cut -d' ' -f2)
print_success "Python version: $PYTHON_VERSION"

# Create temporary directory for download
TEMP_DIR=$(mktemp -d)
trap "rm -rf $TEMP_DIR" EXIT

print_info "Creating temporary directory: $TEMP_DIR"

# Download the repository
print_info "Downloading Nexus from GitHub..."
cd "$TEMP_DIR"

if command -v git &> /dev/null; then
    git clone --depth 1 https://github.com/nekocd10/maybe-a-custom-language.git nexus-repo 2>/dev/null || {
        print_error "Failed to clone repository with git, trying wget..."
        if command -v wget &> /dev/null; then
            wget -q https://github.com/nekocd10/maybe-a-custom-language/archive/refs/heads/main.zip
            unzip -q main.zip
            mv maybe-a-custom-language-main nexus-repo
        elif command -v curl &> /dev/null; then
            curl -sL https://github.com/nekocd10/maybe-a-custom-language/archive/refs/heads/main.zip -o main.zip
            unzip -q main.zip
            mv maybe-a-custom-language-main nexus-repo
        else
            print_error "Neither git, wget, nor curl found. Please install one of them."
            exit 1
        fi
    }
else
    print_info "Git not found, using wget/curl fallback..."
    if command -v wget &> /dev/null; then
        wget -q https://github.com/nekocd10/maybe-a-custom-language/archive/refs/heads/main.zip
        unzip -q main.zip
        mv maybe-a-custom-language-main nexus-repo
    elif command -v curl &> /dev/null; then
        curl -sL https://github.com/nekocd10/maybe-a-custom-language/archive/refs/heads/main.zip -o main.zip
        unzip -q main.zip
        mv maybe-a-custom-language-main nexus-repo
    else
        print_error "Neither git, wget, nor curl found. Please install one of them."
        exit 1
    fi
fi

cd nexus-repo
print_success "Repository downloaded successfully"

# Install Python package
print_info "Installing Nexus package..."
pip install -e . > /dev/null 2>&1

if [ $? -eq 0 ]; then
    print_success "Package installed successfully"
else
    print_error "Failed to install package"
    print_info "Trying with --user flag..."
    pip install --user -e . > /dev/null 2>&1
    
    if [ $? -ne 0 ]; then
        print_error "Installation failed. Please check your Python/pip installation."
        exit 1
    fi
fi

# Verify installation
print_info "Verifying installation..."
if nexus --version &> /dev/null; then
    print_success "Nexus CLI is available"
    nexus --version
else
    print_error "Nexus CLI not found in PATH"
    print_info "You may need to add Python's bin directory to your PATH"
    echo ""
    echo "Try adding this to your shell profile (~/.bashrc, ~/.zshrc, etc.):"
    echo "export PATH=\"\$PATH:$(python3 -m site --user-base)/bin\""
fi

# Print completion message
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
echo "   nexus --help"
echo ""
echo "3. Explore examples:"
echo "   ls examples/"
echo ""
print_success "Enjoy Nexus!"
echo ""
