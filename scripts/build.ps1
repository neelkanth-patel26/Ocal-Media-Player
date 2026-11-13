$ErrorActionPreference = 'Stop'
Set-Location (Split-Path $PSScriptRoot -Parent)
# Avoid collecting unrelated DLLs from tools on the caller's PATH. In particular,
# Poppler's ICU DLL shadows the Windows ICU API required by Qt 6.12.
$originalBuildPath = $env:PATH
$pythonBase = & ./.venv/Scripts/python.exe -c 'import sys; print(sys.base_prefix)'
if ($LASTEXITCODE -ne 0) { throw 'Could not locate the Python runtime' }
try {
    $env:PATH = @((Join-Path (Get-Location) '.venv/Scripts'), $pythonBase, (Join-Path $env:SystemRoot 'System32'), $env:SystemRoot) -join ';'
    & ./.venv/Scripts/python.exe -m PyInstaller --clean --noconfirm --windowed --name 'Ocal Media Player' --icon 'assets/app-icon.ico' --add-data 'assets;assets' --add-data 'runtime/vlc-4.0.0-dev;runtime/vlc-4.0.0-dev' --add-data 'THIRD-PARTY-NOTICES.md;.' --add-data 'LICENSE;.' --exclude-module PySide6.QtWebEngineCore --exclude-module PySide6.QtWebEngineWidgets --exclude-module PySide6.QtQml --exclude-module PySide6.QtQuick run.py
    if ($LASTEXITCODE -ne 0) { throw 'Packaging failed' }
} finally {
    $env:PATH = $originalBuildPath
}
Write-Host 'Portable app: dist\Ocal Media Player\Ocal Media Player.exe (keep the _internal folder beside it)'
