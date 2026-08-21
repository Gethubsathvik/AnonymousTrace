# AnonymousTrace - Windows Setup
# Run this once to install the package and ensure AnonymousTrace works.

param(
    [switch]$Uninstall
)

$ErrorActionPreference = 'Stop'

function Get-PythonScriptsPaths {
    param([string]$PythonExe)

    $paths = @()

    $scriptsPath = & $pythonExe -c "import sys, os; print(os.path.join(os.path.dirname(sys.executable), 'Scripts'))" 2>$null
    if ($LASTEXITCODE -eq 0 -and $scriptsPath -and (Test-Path $scriptsPath)) {
        $paths += $scriptsPath
    }

    $userScripts = & $pythonExe -c "import site, os; print(os.path.join(site.getusersitepackages().replace('site-packages', 'Scripts')))" 2>$null
    if ($LASTEXITCODE -eq 0 -and $userScripts -and (Test-Path $userScripts) -and $paths -notcontains $userScripts) {
        $paths += $userScripts
    }

    $scriptsPath = & $pythonExe -c "import sysconfig; print(sysconfig.get_path('scripts'))" 2>$null
    if ($LASTEXITCODE -eq 0 -and $scriptsPath -and (Test-Path $scriptsPath) -and $paths -notcontains $scriptsPath) {
        $paths += $scriptsPath
    }

    return $paths | Select-Object -Unique
}

function Test-CommandAvailable {
    param([string]$Command)
    try {
        $null = Get-Command $Command -ErrorAction Stop
        return $true
    } catch {
        return $false
    }
}

function Reload-PathInCurrentSession {
    param([string[]]$ScriptsPaths)
    foreach ($scriptsPath in $ScriptsPaths) {
        if ($env:Path -notlike "*$scriptsPath*") {
            $env:Path = $env:Path + ';' + $scriptsPath
        }
    }
}

if ($Uninstall) {
    $pythonExe = (Get-Command python -ErrorAction SilentlyContinue).Source
    if (-not $pythonExe) {
        Write-Host "Python not found." -ForegroundColor Yellow
        exit 1
    }

    $scriptsPaths = Get-PythonScriptsPaths -PythonExe $pythonExe
    foreach ($scriptsPath in $scriptsPaths) {
        $currentPath = [Environment]::GetEnvironmentVariable("Path", "User") -split ';' | Where-Object { $_ -ne $scriptsPath }
        [Environment]::SetEnvironmentVariable("Path", ($currentPath -join ';'), "User")
        Write-Host "Removed from PATH: $scriptsPath" -ForegroundColor Green
    }

    & $pythonExe -m pip uninstall -y AnonymousTrace 2>$null | Out-Null
    Write-Host "Uninstalled AnonymousTrace." -ForegroundColor Green
    exit 0
}

Write-Host "=== AnonymousTrace Setup ===" -ForegroundColor Cyan
Write-Host ""

$pythonExe = (Get-Command python -ErrorAction SilentlyContinue).Source
if (-not $pythonExe) {
    Write-Host "Python not found. Install Python 3.10+ first." -ForegroundColor Red
    exit 1
}

$scriptsPaths = Get-PythonScriptsPaths -PythonExe $pythonExe
if (-not $scriptsPaths -or $scriptsPaths.Count -eq 0) {
    Write-Host "Could not detect Python Scripts path." -ForegroundColor Red
    exit 1
}

$currentPath = [Environment]::GetEnvironmentVariable("Path", "User") -split ';'
foreach ($scriptsPath in $scriptsPaths) {
    if ($currentPath -contains $scriptsPath) {
        Write-Host "Already in user PATH: $scriptsPath" -ForegroundColor Yellow
    } else {
        [Environment]::SetEnvironmentVariable("Path", ($env:Path + ';' + $scriptsPath), "User")
        Write-Host "Added to user PATH: $scriptsPath" -ForegroundColor Green
    }
}

Reload-PathInCurrentSession -ScriptsPaths $scriptsPaths

Write-Host ""
Write-Host "Installing AnonymousTrace..." -ForegroundColor Cyan
Push-Location $PSScriptRoot
& $pythonExe -m pip install -e .
if ($LASTEXITCODE -ne 0) {
    Write-Host "Installation failed." -ForegroundColor Red
    exit 1
}
Pop-Location

Write-Host ""
Write-Host "Verifying AnonymousTrace command..." -ForegroundColor Cyan
if (Test-CommandAvailable "AnonymousTrace") {
    Write-Host "AnonymousTrace is ready!" -ForegroundColor Green
    Write-Host ""
    Write-Host "Try it now:" -ForegroundColor Yellow
    Write-Host "  AnonymousTrace -h"
    Write-Host "  AnonymousTrace user123"
} else {
    Write-Host ""
    Write-Host "WARNING: AnonymousTrace command not found in current session." -ForegroundColor Red
    Write-Host ""
    Write-Host "This usually means PowerShell didn't reload PATH." -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Fix options (choose one):" -ForegroundColor Cyan
    Write-Host "  1. Close this window and open a NEW PowerShell window" -ForegroundColor White
    Write-Host "  2. Reload PATH now and retry:" -ForegroundColor White
    Write-Host "     `$env:Path = [Environment]::GetEnvironmentVariable('Path', 'User')" -ForegroundColor Gray
    Write-Host "     AnonymousTrace -h" -ForegroundColor Gray
}
