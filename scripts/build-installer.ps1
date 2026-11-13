# Ocal Media Player - Build & Inno Setup Packaging Script
# Automates PyInstaller portable build and Inno Setup 6 installer creation
[CmdletBinding()]
param()

$ErrorActionPreference = 'Stop'
$ProgressPreference = 'SilentlyContinue'
$projectRoot = Split-Path $PSScriptRoot -Parent
Set-Location $projectRoot

Write-Host "============================================================" -ForegroundColor Cyan
Write-Host " Ocal Media Player - Automated Build & Setup Generator" -ForegroundColor Cyan
Write-Host " Developer: Ocal Software under Gaming Network Studio" -ForegroundColor Gray
Write-Host "============================================================" -ForegroundColor Cyan

# 1. Clean previous build folders and terminate running player
Write-Host "[1/3] Terminating any running player processes and cleaning build directories..." -ForegroundColor Yellow
Get-Process -Name "*Ocal Media Player*" -ErrorAction SilentlyContinue | Stop-Process -Force -ErrorAction SilentlyContinue
Start-Sleep -Milliseconds 500

@("dist-installer", "build", "dist") | ForEach-Object {
    if (Test-Path $_) {
        Remove-Item -Recurse -Force $_ -ErrorAction SilentlyContinue
    }
}
New-Item -ItemType Directory -Path "dist-installer" -Force | Out-Null

# 2. Build PyInstaller distribution
Write-Host "[2/3] Building executable with PyInstaller..." -ForegroundColor Yellow
& ./.venv/Scripts/python.exe -m PyInstaller --noconfirm --windowed `
    --name 'Ocal Media Player' `
    --icon 'assets/app-icon.ico' `
    --add-data 'assets;assets' `
    --add-data 'runtime/vlc-4.0.0-dev;runtime/vlc-4.0.0-dev' `
    --add-data 'THIRD-PARTY-NOTICES.md;.' `
    --add-data 'LICENSE;.' `
    --exclude-module PySide6.QtWebEngineCore `
    --exclude-module PySide6.QtWebEngineWidgets `
    --exclude-module PySide6.QtQml `
    --exclude-module PySide6.QtQuick `
    run.py

if ($LASTEXITCODE -ne 0) {
    throw "PyInstaller packaging failed with exit code $LASTEXITCODE."
}

$exePath = "dist\Ocal Media Player\Ocal Media Player.exe"
if (-not (Test-Path $exePath)) {
    throw "PyInstaller did not generate expected binary at: $exePath"
}
Write-Host "PyInstaller packaging complete and verified at: $exePath" -ForegroundColor Green

# 3. Locate Inno Setup 6 Compiler (ISCC.exe)
Write-Host "[3/3] Locating Inno Setup 6 and compiling installer..." -ForegroundColor Yellow
$isccCandidates = @(
    "ISCC.exe",
    "$env:USERPROFILE\AppData\Local\Programs\Inno Setup 6\ISCC.exe",
    "C:\Program Files (x86)\Inno Setup 6\ISCC.exe",
    "C:\Program Files\Inno Setup 6\ISCC.exe"
)

$isccPath = $null
foreach ($candidate in $isccCandidates) {
    if (Get-Command $candidate -ErrorAction SilentlyContinue) {
        $isccPath = (Get-Command $candidate).Source
        break
    }
    if (Test-Path $candidate) {
        $isccPath = $candidate
        break
    }
}

if (-not $isccPath) {
    throw "ISCC.exe (Inno Setup 6) was not found. Please install Inno Setup 6."
}

Write-Host "Found ISCC compiler at: $isccPath" -ForegroundColor Green
& $isccPath "installer.iss"
if ($LASTEXITCODE -ne 0) {
    throw "Inno Setup compilation failed with exit code $LASTEXITCODE."
}

$version = ((Get-Content src/updater.py | Select-String 'CURRENT_VERSION\s*=\s*"([^"]+)"').Matches.Groups[1].Value)
if (-not $version) { $version = "1.0.2" }
$setupExe = Get-ChildItem "dist-installer\Ocal-Media-Player-*-Setup.exe" | Select-Object -First 1

Write-Host "Creating portable zip package..." -ForegroundColor Yellow
$portableZip = "dist-installer\Ocal-Media-Player-$version-Portable-x64.zip"
if (Test-Path $portableZip) { Remove-Item -Force $portableZip }
& ./.venv/Scripts/python.exe -c "import shutil; shutil.make_archive('dist-installer/Ocal-Media-Player-$version-Portable-x64', 'zip', root_dir='dist/Ocal Media Player')"
Write-Host "Portable package created at: $portableZip" -ForegroundColor Green

Write-Host ""
Write-Host "============================================================" -ForegroundColor Green
Write-Host " BUILD SUCCESSFUL!" -ForegroundColor Green
Write-Host " Portable binary: dist\Ocal Media Player\Ocal Media Player.exe" -ForegroundColor White
if ($setupExe) {
    Write-Host " Installer package: $($setupExe.FullName)" -ForegroundColor Cyan
    Write-Host " Installer size: $([math]::Round($setupExe.Length / 1MB, 2)) MB" -ForegroundColor Gray
}
if (Test-Path $portableZip) {
    $zipItem = Get-Item $portableZip
    Write-Host " Portable zip: $($zipItem.FullName)" -ForegroundColor Cyan
    Write-Host " Portable zip size: $([math]::Round($zipItem.Length / 1MB, 2)) MB" -ForegroundColor Gray
}
Write-Host "============================================================" -ForegroundColor Green

