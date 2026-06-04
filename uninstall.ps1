# Automated Data Analysis Framework - Windows Uninstall Script
#
# Usage:
#   .\uninstall.ps1
#   Or: iwr -useb https://raw.githubusercontent.com/Joohnnwicky/Automated-Data-Analysis-Framework/main/uninstall.ps1 | iex
#

param(
    [string]$InstallDir = "$env:USERPROFILE\.automated-data-analysis"
)

function Write-ColorOutput {
    param([string]$Message, [string]$Color = "White")
    Write-Host $Message -ForegroundColor $Color
}

Write-Host ""
Write-ColorOutput "╔══════════════════════════════════════════════════════════════╗" "Cyan"
Write-ColorOutput "║  Automated Data Analysis Framework - Windows Uninstaller     ║" "Cyan"
Write-ColorOutput "╚══════════════════════════════════════════════════════════════╝" "Cyan"
Write-Host ""

if (-not (Test-Path $InstallDir)) {
    Write-ColorOutput "Installation not found at $InstallDir" "Yellow"
    Write-Host "Nothing to uninstall."
    exit 0
}

Write-ColorOutput "This will remove:" "Yellow"
Write-Host "  - $InstallDir"
Write-Host "  - CLI command 'analyze.ps1'"
Write-Host ""

# Ask for confirmation
$confirmation = Read-Host "Continue? (y/N)"
if ($confirmation -ne "y" -and $confirmation -ne "Y") {
    Write-Host "Cancelled."
    exit 0
}

# Remove installation directory
Write-ColorOutput "Removing installation..." "Yellow"
Remove-Item -Recurse -Force $InstallDir

Write-ColorOutput "✓ Uninstallation complete" "Green"
Write-Host ""
Write-Host "Note: If you added $InstallDir\bin to your PATH in PowerShell profile,"
Write-Host "      you may want to remove that line manually from `$PROFILE"
Write-Host ""