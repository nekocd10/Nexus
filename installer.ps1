<#
Native Windows PowerShell installer for Nexus

Usage:
  Open PowerShell (Admin not required) and run:
    powershell -NoProfile -ExecutionPolicy Bypass -Command "& { iwr https://raw.githubusercontent.com/nekocd10/Nexus/main/installer.ps1 -OutFile $env:TEMP\nexus_installer.ps1; & $env:TEMP\nexus_installer.ps1 }"

This script:
- Verifies Python is available
- Downloads the repository zip from GitHub
- Installs the package via `python -m pip install --user .`
- Prints path hints if the `nexus` command is not immediately on PATH
#>

param()

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

Write-Host "Nexus native Windows installer (PowerShell)"

# Find Python
$pyCmd = Get-Command python -ErrorAction SilentlyContinue
if (-not $pyCmd) { $pyCmd = Get-Command python3 -ErrorAction SilentlyContinue }
if (-not $pyCmd) {
    Write-Error "Python not found. Install Python 3.8+ and ensure 'python' is on PATH: https://www.python.org/downloads/"
    exit 1
}

$tempDir = Join-Path $env:TEMP ("nexus_install_" + [guid]::NewGuid().ToString())
New-Item -ItemType Directory -Path $tempDir | Out-Null
$zipPath = Join-Path $tempDir 'nexus.zip'
$repoZip = 'https://github.com/nekocd10/Nexus/archive/refs/heads/main.zip'

Write-Host "Downloading Nexus..."
Invoke-WebRequest -Uri $repoZip -OutFile $zipPath -UseBasicParsing

Write-Host "Extracting..."
Expand-Archive -Path $zipPath -DestinationPath $tempDir

# Locate extracted folder
$extracted = Get-ChildItem -Path $tempDir | Where-Object { $_.PSIsContainer } | Select-Object -First 1
if (-not $extracted) { Write-Error "Failed to extract repository."; exit 1 }

Push-Location $extracted.FullName

Write-Host "Installing Nexus via pip (user install)..."
& $pyCmd.Source -m pip install --user .

# Show user-base scripts path hint
try {
    $userBase = & $pyCmd.Source -c "import site,sys;print(site.USER_BASE)"
    $scriptsPath = Join-Path $userBase 'Scripts'
    Write-Host "If 'nexus' is not found after install, add this to your PATH:"
    Write-Host "  $scriptsPath"
} catch {
    Write-Host "Installed; if 'nexus' is not on PATH, ensure your Python user Scripts directory is in PATH."
}

Pop-Location

Write-Host "Cleaning up temporary files..."
Remove-Item -Recurse -Force $tempDir

Write-Host "Done. Restart your terminal or run `hash -r` (Git Bash) / open a new PowerShell session to use 'nexus'."
