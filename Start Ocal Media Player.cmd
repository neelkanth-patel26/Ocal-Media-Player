@echo off
cd /d "%~dp0"
if exist "dist\Ocal Media Player\Ocal Media Player.exe" (
    start "" "dist\Ocal Media Player\Ocal Media Player.exe"
) else (
    start "" ".venv\Scripts\pythonw.exe" "run.py"
)
