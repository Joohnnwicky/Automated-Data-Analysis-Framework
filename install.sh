#!/bin/bash
#
# Automated Data Analysis Framework - Installation Script
#
# Usage:
#   curl -fsSL https://raw.githubusercontent.com/Joohnnwicky/Automated-Data-Analysis-Framework/main/install.sh | sh
#
# Or:
#   git clone https://github.com/Joohnnwicky/Automated-Data-Analysis-Framework.git
#   cd Automated-Data-Analysis-Framework && ./install.sh
#

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Default installation directory
INSTALL_DIR="${HOME}/.automated-data-analysis"
REPO_URL="https://github.com/Joohnnwicky/Automated-Data-Analysis-Framework.git"

echo ""
echo "${BLUE}╔══════════════════════════════════════════════════════════════╗${NC}"
echo "${BLUE}║  Automated Data Analysis Framework - Installer               ║${NC}"
echo "${BLUE}╚══════════════════════════════════════════════════════════════╝${NC}"
echo ""

# Check Python version
check_python() {
    echo "${YELLOW}[1/5] Checking Python version...${NC}"

    if command -v python3 &> /dev/null; then
        PYTHON_CMD="python3"
    elif command -v python &> /dev/null; then
        PYTHON_CMD="python"
    else
        echo "${RED}Error: Python not found. Please install Python 3.10+ first.${NC}"
        exit 1
    fi

    PYTHON_VERSION=$($PYTHON_CMD --version 2>&1 | cut -d' ' -f2)
    PYTHON_MAJOR=$(echo $PYTHON_VERSION | cut -d'.' -f1)
    PYTHON_MINOR=$(echo $PYTHON_VERSION | cut -d'.' -f2)

    if [ "$PYTHON_MAJOR" -lt 3 ] || ([ "$PYTHON_MAJOR" -eq 3 ] && [ "$PYTHON_MINOR" -lt 10 ]); then
        echo "${RED}Error: Python version $PYTHON_VERSION is too old. Need Python 3.10+${NC}"
        exit 1
    fi

    echo "${GREEN}✓ Python $PYTHON_VERSION found${NC}"
}

# Check pip
check_pip() {
    echo "${YELLOW}[2/5] Checking pip...${NC}"

    if ! $PYTHON_CMD -m pip --version &> /dev/null; then
        echo "${RED}Error: pip not found. Please install pip first.${NC}"
        exit 1
    fi

    echo "${GREEN}✓ pip found${NC}"
}

# Clone or update repository
install_source() {
    echo "${YELLOW}[3/5] Installing source code...${NC}"

    if [ -d "$INSTALL_DIR" ]; then
        echo "  Existing installation found at $INSTALL_DIR"
        echo "  Updating..."
        cd "$INSTALL_DIR"
        git pull origin master || true
    else
        echo "  Cloning to $INSTALL_DIR..."
        git clone "$REPO_URL" "$INSTALL_DIR"
    fi

    echo "${GREEN}✓ Source code installed${NC}"
}

# Install dependencies
install_dependencies() {
    echo "${YELLOW}[4/5] Installing Python dependencies...${NC}"

    cd "$INSTALL_DIR"
    $PYTHON_CMD -m pip install -r requirements.txt --quiet

    echo "${GREEN}✓ Dependencies installed${NC}"
}

# Setup CLI command
setup_cli() {
    echo "${YELLOW}[5/5] Setting up CLI command...${NC}"

    # Create wrapper script
    CLI_SCRIPT="$INSTALL_DIR/bin/analyze"
    mkdir -p "$INSTALL_DIR/bin"

    cat > "$CLI_SCRIPT" << 'CLI_EOF'
#!/bin/bash
# Automated Data Analysis Framework CLI Wrapper

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

# Determine Python command
if command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
else
    PYTHON_CMD="python"
fi

# Run the CLI
cd "$PROJECT_DIR"
$PYTHON_CMD -c "
import sys
sys.path.insert(0, '$PROJECT_DIR')

from src.workflow.cli import main
main()
" "$@"
CLI_EOF

    chmod +x "$CLI_SCRIPT"

    # Add to PATH (for current session)
    if ! echo $PATH | grep -q "$INSTALL_DIR/bin"; then
        echo ""
        echo "${BLUE}To use 'analyze' command, add to your PATH:${NC}"
        echo ""
        echo "  Add this line to your ~/.bashrc or ~/.zshrc:"
        echo ""
        echo "    export PATH=\"\$PATH:$INSTALL_DIR/bin\""
        echo ""
        echo "  Or run once for current session:"
        echo ""
        echo "    export PATH=\"\$PATH:$INSTALL_DIR/bin\""
        echo ""
    fi

    echo "${GREEN}✓ CLI command installed at $CLI_SCRIPT${NC}"
}

# Print success message
print_success() {
    echo ""
    echo "${GREEN}╔══════════════════════════════════════════════════════════════╗${NC}"
    echo "${GREEN}║  Installation Complete!                                       ║${NC}"
    echo "${GREEN}╚══════════════════════════════════════════════════════════════╝${NC}"
    echo ""
    echo "Installation directory: $INSTALL_DIR"
    echo ""
    echo "${YELLOW}Quick Start:${NC}"
    echo ""
    echo "  1. Add to PATH:"
    echo "     export PATH=\"\$PATH:$INSTALL_DIR/bin\""
    echo ""
    echo "  2. Run analysis:"
    echo "     analyze data/sales.xlsx"
    echo ""
    echo "  3. Or use in Claude Code:"
    echo "     cd $INSTALL_DIR"
    echo "     claude"
    echo "     > 分析这份销售数据"
    echo ""
    echo "${YELLOW}Uninstall:${NC}"
    echo "     rm -rf $INSTALL_DIR"
    echo ""
}

# Run installation
main() {
    check_python
    check_pip
    install_source
    install_dependencies
    setup_cli
    print_success
}

main