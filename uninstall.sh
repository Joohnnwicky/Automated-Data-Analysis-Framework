#!/bin/bash
#
# Automated Data Analysis Framework - Uninstall Script
#
# Usage:
#   ./uninstall.sh
#   Or: curl -fsSL https://raw.githubusercontent.com/Joohnnwicky/Automated-Data-Analysis-Framework/main/uninstall.sh | sh
#

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

INSTALL_DIR="${HOME}/.automated-data-analysis"

echo ""
echo "${BLUE}╔══════════════════════════════════════════════════════════════╗${NC}"
echo "${BLUE}║  Automated Data Analysis Framework - Uninstaller             ║${NC}"
echo "${BLUE}╚══════════════════════════════════════════════════════════════╝${NC}"
echo ""

if [ ! -d "$INSTALL_DIR" ]; then
    echo "${YELLOW}Installation not found at $INSTALL_DIR${NC}"
    echo "Nothing to uninstall."
    exit 0
fi

echo "${YELLOW}This will remove:${NC}"
echo "  - $INSTALL_DIR"
echo "  - CLI command 'analyze'"
echo ""

# Ask for confirmation
read -p "Continue? (y/N) " -n 1 -r
echo ""

if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Cancelled."
    exit 0
fi

# Remove installation directory
echo "${YELLOW}Removing installation...${NC}"
rm -rf "$INSTALL_DIR"

echo "${GREEN}✓ Uninstallation complete${NC}"
echo ""
echo "Note: If you added $INSTALL_DIR/bin to your PATH in ~/.bashrc or ~/.zshrc,"
echo "      you may want to remove that line manually."
echo ""