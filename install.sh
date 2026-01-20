#!/usr/bin/env bash
# Nexus Programming Language - Local Installation Script
# Local installation script - runs from the repository
# For curl-based installation, see installer.sh

set -e

# Get the script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Disable colors on devices that don't support them
if [ "$TERM" = "dumb" ] || [ -z "$TERM" ]; then
    RED='' GREEN='' BLUE='' YELLOW='' NC=''
fi

print_success() {
    echo -e "${GREEN}✓${NC} $1"
}

print_error() {
    echo -e "${RED}✗${NC} $1"
}

print_info() {
    echo -e "${BLUE}ℹ${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}⚠${NC} $1"
}

echo ""
echo -e "${BLUE}╔═══════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║      Nexus (nxs) Programming Language     ║${NC}"
echo -e "${BLUE}║    Installing from local repository       ║${NC}"
echo -e "${BLUE}╚═══════════════════════════════════════════╝${NC}"
echo ""

# Detect OS and Architecture
OS="$(uname -s)"
ARCH="$(uname -m)"

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

# Detect if running on Termux
if [ -d "$HOME/.termux" ] || [ -n "$TERMUX_VERSION" ]; then
    PLATFORM="termux"
    print_success "Detected: Termux"
else
    print_success "Detected: $PLATFORM"
fi

# Detect architecture
case "$ARCH" in
    x86_64|amd64)
        ARCH_NAME="64-bit x86_64"
        ;;
    x86|i386|i686)
        ARCH_NAME="32-bit x86"
        ;;
    armv7l|armv7)
        ARCH_NAME="32-bit ARM (armv7)"
        ;;
    aarch64|arm64)
        ARCH_NAME="64-bit ARM (aarch64)"
        ;;
    *)
        ARCH_NAME="$ARCH"
        ;;
esac

print_success "Architecture: $ARCH_NAME"

# Auto-install Python if missing
install_python_if_needed() {
    if command -v python3 &> /dev/null; then
        PYTHON_CMD="python3"
        PYTHON_VERSION=$($PYTHON_CMD --version 2>&1 | cut -d' ' -f2)
        print_success "Python version: $PYTHON_VERSION"
        return 0
    fi
    
    if command -v python &> /dev/null; then
        PYTHON_CMD="python"
        PYTHON_VERSION=$($PYTHON_CMD --version 2>&1 | cut -d' ' -f2)
        print_success "Python version: $PYTHON_VERSION"
        return 0
    fi
    
    # Python is missing, try to install it
    print_warning "Python 3 not found, attempting to install..."
    
    DISTRO=$(detect_distro)
    
    # Determine if we need sudo
    SUDO=""
    if [ "$EUID" -ne 0 ] 2>/dev/null; then
        if command -v sudo &> /dev/null; then
            SUDO="sudo"
        fi
    fi
    
    if [ "$PLATFORM" = "termux" ]; then
        print_info "Installing Python via pkg (Termux)..."
        pkg install -y python 2>/dev/null && {
            print_success "Python installed successfully"
            if command -v python3 &> /dev/null; then
                PYTHON_CMD="python3"
            else
                PYTHON_CMD="python"
            fi
            PYTHON_VERSION=$($PYTHON_CMD --version 2>&1 | cut -d' ' -f2)
            print_success "Python version: $PYTHON_VERSION"
            return 0
        }
        print_error "Failed to install Python on Termux"
        return 1
    elif [ "$DISTRO" = "alpine" ]; then
        print_info "Installing Python via apk (Alpine)..."
        $SUDO apk add --no-cache python3 py3-pip 2>/dev/null && {
            print_success "Python installed successfully"
            PYTHON_CMD="python3"
            PYTHON_VERSION=$($PYTHON_CMD --version 2>&1 | cut -d' ' -f2)
            print_success "Python version: $PYTHON_VERSION"
            return 0
        }
        print_error "Failed to install Python on Alpine"
        return 1
    elif [ "$DISTRO" = "debian" ] || [ "$DISTRO" = "ubuntu" ]; then
        print_info "Installing Python via apt (Debian/Ubuntu)..."
        $SUDO apt-get update 2>/dev/null && $SUDO apt-get install -y python3 python3-pip 2>/dev/null && {
            print_success "Python installed successfully"
            PYTHON_CMD="python3"
            PYTHON_VERSION=$($PYTHON_CMD --version 2>&1 | cut -d' ' -f2)
            print_success "Python version: $PYTHON_VERSION"
            return 0
        }
        print_error "Failed to install Python on Debian/Ubuntu"
        return 1
    elif [ "$DISTRO" = "fedora" ] || [ "$DISTRO" = "rhel" ] || [ "$DISTRO" = "centos" ]; then
        print_info "Installing Python via dnf (Fedora/RHEL/CentOS)..."
        $SUDO dnf install -y python3 python3-pip 2>/dev/null && {
            print_success "Python installed successfully"
            PYTHON_CMD="python3"
            PYTHON_VERSION=$($PYTHON_CMD --version 2>&1 | cut -d' ' -f2)
            print_success "Python version: $PYTHON_VERSION"
            return 0
        }
        print_error "Failed to install Python on Fedora/RHEL/CentOS"
        return 1
    elif [ "$DISTRO" = "arch" ]; then
        print_info "Installing Python via pacman (Arch)..."
        $SUDO pacman -S --noconfirm python python-pip 2>/dev/null && {
            print_success "Python installed successfully"
            PYTHON_CMD="python3"
            PYTHON_VERSION=$($PYTHON_CMD --version 2>&1 | cut -d' ' -f2)
            print_success "Python version: $PYTHON_VERSION"
            return 0
        }
        print_error "Failed to install Python on Arch"
        return 1
    elif [ "$DISTRO" = "opensuse" ] || [ "$DISTRO" = "opensuse-leap" ]; then
        print_info "Installing Python via zypper (openSUSE)..."
        $SUDO zypper install -y python3 python3-pip 2>/dev/null && {
            print_success "Python installed successfully"
            PYTHON_CMD="python3"
            PYTHON_VERSION=$($PYTHON_CMD --version 2>&1 | cut -d' ' -f2)
            print_success "Python version: $PYTHON_VERSION"
            return 0
        }
        print_error "Failed to install Python on openSUSE"
        return 1
    else
        print_error "Could not detect your Linux distribution"
        echo "Please install Python 3.8 or higher manually and try again"
        return 1
    fi
}

# Check and install Python if needed
install_python_if_needed || exit 1

PYTHON_VERSION=$($PYTHON_CMD --version 2>&1 | cut -d' ' -f2)
print_success "Python version: $PYTHON_VERSION"

# Delete all markdown files to reduce size and clutter
print_info "Cleaning up documentation files..."
find "$SCRIPT_DIR" -maxdepth 1 -name "*.md" -type f -delete 2>/dev/null || true
rm -f "$SCRIPT_DIR/SHOWCASE.md" "$SCRIPT_DIR/pormt-for-later.txt" 2>/dev/null || true
print_success "Removed markdown files"

# Install Python package
echo ""
echo "Installing Nexus package in development mode..."
cd "$SCRIPT_DIR"

# Verify pip is available
if ! $PYTHON_CMD -m pip --version &> /dev/null; then
    print_warning "pip not found, attempting to install it..."
    SUDO=""
    if [ "$EUID" -ne 0 ] 2>/dev/null; then
        if command -v sudo &> /dev/null; then
            SUDO="sudo"
        fi
    fi
    
    if command -v apt-get &> /dev/null; then
        $SUDO apt-get install -y python3-pip 2>/dev/null || true
    elif command -v dnf &> /dev/null; then
        $SUDO dnf install -y python3-pip 2>/dev/null || true
    elif command -v pacman &> /dev/null; then
        $SUDO pacman -S --noconfirm python-pip 2>/dev/null || true
    elif command -v apk &> /dev/null; then
        $SUDO apk add --no-cache py3-pip 2>/dev/null || true
    elif command -v zypper &> /dev/null; then
        $SUDO zypper install -y python3-pip 2>/dev/null || true
    fi
    
    if ! $PYTHON_CMD -m pip --version &> /dev/null; then
        print_error "pip is not available. Try installing it manually first."
        exit 1
    fi
fi

print_info "Attempting installation method 1: standard install..."
INSTALL_OUTPUT=$($PYTHON_CMD -m pip install -e . 2>&1)
if echo "$INSTALL_OUTPUT" | grep -q "Successfully installed\|Requirement already satisfied"; then
    print_success "Package installed successfully"
else
    print_info "Method 1 failed, trying method 2: --user flag..."
    INSTALL_OUTPUT=$($PYTHON_CMD -m pip install --user -e . 2>&1)
    if echo "$INSTALL_OUTPUT" | grep -q "Successfully installed\|Requirement already satisfied"; then
        print_success "Package installed successfully (--user)"
    else
        print_info "Method 2 failed, trying method 3: non-editable install..."
        INSTALL_OUTPUT=$($PYTHON_CMD -m pip install --user . 2>&1)
        if echo "$INSTALL_OUTPUT" | grep -q "Successfully installed\|Requirement already satisfied"; then
            print_success "Package installed successfully"
        else
            print_error "Failed to install package"
            echo ""
            echo "Error details:"
            echo "$INSTALL_OUTPUT"
            exit 1
        fi
    fi
fi

# Verify installation
echo ""
print_info "Verifying installation..."

# Get Python's bin directory
PYTHON_BIN=$($PYTHON_CMD -c "import site; print(site.getusersitepackages().replace('site-packages', 'bin'))" 2>/dev/null)
if [ -z "$PYTHON_BIN" ]; then
    PYTHON_BIN=$($PYTHON_CMD -m site --user-base 2>/dev/null)/bin
fi

# Check if nexus is in PATH
if command -v nexus &> /dev/null; then
    print_success "✓ Nexus CLI is available in PATH"
    NEXUS_PATH=$(which nexus)
    print_info "Location: $NEXUS_PATH"
else
    print_warning "⚠ Nexus not found in PATH"
    if [ -f "$PYTHON_BIN/nexus" ]; then
        print_info "But it's installed at: $PYTHON_BIN/nexus"
        echo ""
        echo "Add this to your shell profile (~/.bashrc, ~/.zshrc, etc):"
        echo "  export PATH=\"\$PATH:$PYTHON_BIN\""
        echo ""
        echo "Then restart terminal or run:"
        echo "  source ~/.bashrc"
    fi
fi

echo ""
echo -e "${GREEN}╔════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║     Installation Complete! 🎉           ║${NC}"
echo -e "${GREEN}╚════════════════════════════════════════╝${NC}"
echo ""
echo "Quick start:"
echo "  1. Try a command: nexus --version"
echo "  2. Create a program: echo 'println \"Hello!\"' > hello.nexus"
echo "  3. Run it: nexus hello.nexus"
echo ""
echo "Commands:"
echo "  nexus script.nexus      # Run a Nexus program"
echo "  nexus --help            # Show help"
echo "  nxs script.nexus        # Alias for nexus"
echo ""
print_success "Enjoy Nexus (nxs)!"
echo ""
