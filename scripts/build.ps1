$ErrorActionPreference = 'Stop'
Set-Location (Split-Path $PSScriptRoot -Parent)
& ./.venv/Scripts/python.exe -m PyInstaller --noconfirm --windowed --name 'Ocal Media Player' --icon 'assets/app-icon.ico' --add-data 'assets;assets' --add-data 'runtime/vlc-4.0.0-dev;runtime/vlc-4.0.0-dev' --add-data 'THIRD-PARTY-NOTICES.md;.' --add-data 'LICENSE;.' --exclude-module PySide6.QtWebEngineCore --exclude-module PySide6.QtWebEngineWidgets --exclude-module PySide6.QtQml --exclude-module PySide6.QtQuick run.py
if ($LASTEXITCODE -ne 0) { throw 'Packaging failed' }
Write-Host 'Portable app: dist\Ocal Media Player\Ocal Media Player.exe (keep the _internal folder beside it)'
