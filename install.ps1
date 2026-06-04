# Automated Data Analysis Framework - Windows Installation Script
#
# Usage:
#   PowerShell:
#     Invoke-WebRequest -Uri "https://raw.githubusercontent.com/Joohnnwicky/Automated-Data-Analysis-Framework/main/install.ps1" -OutFile "install.ps1"
#     .\install.ps1
#
#   Or one-liner:
#     iwr -useb https://raw.githubusercontent.com/Joohnnwicky/Automated-Data-Analysis-Framework/main/install.ps1 | iex
#

param(
    [string]$InstallDir = "$env:USERPROFILE\.automated-data-analysis",
    [string]$RepoUrl = "https://github.com/Joohnnwicky/Automated-Data-Analysis-Framework.git"
)

# Colors
function Write-ColorOutput {
    param([string]$Message, [string]$Color = "White")
    Write-Host $Message -ForegroundColor $Color
}

Write-ColorOutput "`n╔══════════════════════════════════════════════════════════════╗" "Cyan"
Write-ColorOutput "║  Automated Data Analysis Framework - Windows Installer       ║" "Cyan"
Write-ColorOutput "╚══════════════════════════════════════════════════════════════╝" "Cyan"
Write-Host ""

# Step 1: Check Python
Write-ColorOutput "[1/5] Checking Python version..." "Yellow"

$pythonCmd = $null
if (Get-Command python -ErrorAction SilentlyContinue) {
    $pythonCmd = "python"
} elseif (Get-Command python3 -ErrorAction SilentlyContinue) {
    $pythonCmd = "python3"
} else {
    Write-ColorOutput "Error: Python not found. Please install Python 3.10+ first." "Red"
    Write-Host "Download from: https://www.python.org/downloads/"
    exit 1
}

$pythonVersion = (& $pythonCmd --version 2>&1).Split()[1]
$versionParts = $pythonVersion.Split('.')
$major = [int]$versionParts[0]
$minor = [int]$versionParts[1]

if ($major -lt 3 -or ($major -eq 3 -and $minor -lt 10)) {
    Write-ColorOutput "Error: Python version $pythonVersion is too old. Need Python 3.10+" "Red"
    exit 1
}

Write-ColorOutput "✓ Python $pythonVersion found" "Green"

# Step 2: Check pip
Write-ColorOutput "[2/5] Checking pip..." "Yellow"

try {
    & $pythonCmd -m pip --version | Out-Null
    Write-ColorOutput "✓ pip found" "Green"
} catch {
    Write-ColorOutput "Error: pip not found. Please install pip first." "Red"
    exit 1
}

# Step 3: Check git
Write-ColorOutput "[3/5] Checking git..." "Yellow"

if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
    Write-ColorOutput "Error: git not found. Please install git first." "Red"
    Write-Host "Download from: https://git-scm.com/downloads"
    exit 1
}

Write-ColorOutput "✓ git found" "Green"

# Step 4: Install source
Write-ColorOutput "[4/5] Installing source code..." "Yellow"

if (Test-Path $InstallDir) {
    Write-Host "  Existing installation found at $InstallDir"
    Write-Host "  Updating..."
    Push-Location $InstallDir
    git pull origin master 2>&1 | Out-Null
    Pop-Location
} else {
    Write-Host "  Cloning to $InstallDir..."
    git clone $RepoUrl $InstallDir 2>&1 | Out-Null
}

Write-ColorOutput "✓ Source code installed" "Green"

# Step 5: Install dependencies
Write-ColorOutput "[5/5] Installing Python dependencies..." "Yellow"

Push-Location $InstallDir
& $pythonCmd -m pip install -r requirements.txt --quiet 2>&1 | Out-Null
Pop-Location

Write-ColorOutput "✓ Dependencies installed" "Green"

# Create CLI wrapper
Write-ColorOutput "Creating CLI command..." "Yellow"

$binDir = "$InstallDir\bin"
$cliScript = "$binDir\analyze.ps1"

if (-not (Test-Path $binDir)) {
    New-Item -ItemType Directory -Path $binDir -Force | Out-Null
}

# Create PowerShell wrapper
$wrapperContent = @"
# Automated Data Analysis Framework CLI Wrapper
`$ProjectDir = "$InstallDir"

# Determine Python command
if (Get-Command python -ErrorAction SilentlyContinue) {
    `$PythonCmd = "python"
} elseif (Get-Command python3 -ErrorAction SilentlyContinue) {
    `$PythonCmd = "python3"
} else {
    Write-Host "Error: Python not found"
    exit 1
}

# Run the CLI
Push-Location `$ProjectDir
`$env:PYTHONPATH = `$ProjectDir
& `$PythonCmd -m src.workflow.cli @args
Pop-Location
"@

Set-Content -Path $cliScript -Value $wrapperContent -Encoding UTF8

Write-ColorOutput "✓ CLI command created at $cliScript" "Green"

# Success message
Write-Host ""
Write-ColorOutput "╔══════════════════════════════════════════════════════════════╗" "Green"
Write-ColorOutput "║  Installation Complete!                                       ║" "Green"
Write-ColorOutput "╚══════════════════════════════════════════════════════════════╝" "Green"
Write-Host ""
Write-Host "Installation directory: $InstallDir"
Write-Host ""
Write-ColorOutput "Quick Start:" "Yellow"
Write-Host ""
Write-Host "  1. Add to PATH (PowerShell):"
Write-Host "     `$env:PATH += `";$binDir`""
Write-Host ""
Write-Host "  Or permanently (add to PowerShell profile):"
Write-Host "     Add-Content `$PROFILE `"`$env:PATH += `";$binDir`"`""
Write-Host ""
Write-Host "  2. Run analysis:"
Write-Host "     analyze.ps1 data\sales.xlsx"
Write-Host ""
Write-Host "  3. Or use directly:"
Write-Host "     $cliScript data\sales.xlsx"
Write-Host ""
Write-ColorOutput "Uninstall:" "Yellow"
Write-Host "     Remove-Item -Recurse -Force $InstallDir"
Write-Host ""