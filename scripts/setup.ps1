$ErrorActionPreference = 'Stop'
Set-Location (Split-Path $PSScriptRoot -Parent)
if (!(Test-Path '.venv/Scripts/python.exe')) { python -m venv .venv }
& ./.venv/Scripts/python.exe -m pip install -r requirements.txt
if ($LASTEXITCODE -ne 0) { throw 'Dependency installation failed' }
New-Item -ItemType Directory -Force downloads,runtime,upstream | Out-Null
$base = 'https://artifacts.videolan.org/vlc/nightly-win64/20261104-0427/'
$archive = 'vlc-4.0.0-dev-win64-c6d1df39.zip'
$expected = '6822f0b42b7f392989fd8420d70f62cba15bf2b594b9b55b4f6bb7cdeaa15b8ee3c84842f46543abec0058ac39e34c17b910a2232787b4782621b8b3eb2d6ed3'
if (!(Test-Path 'downloads/vlc-4.zip')) { Invoke-WebRequest ($base + $archive) -OutFile downloads/vlc-4.zip }
if ((Get-FileHash downloads/vlc-4.zip -Algorithm SHA512).Hash.ToLower() -ne $expected) { throw 'VLC archive SHA512 does not match the pinned build' }
if (!(Test-Path 'runtime/vlc-4.0.0-dev/libvlc.dll')) { Expand-Archive downloads/vlc-4.zip -DestinationPath runtime }
if (!(Test-Path 'upstream/vlc/.git')) {
    git clone --depth 1 https://code.videolan.org/videolan/vlc.git upstream/vlc
    if ($LASTEXITCODE -ne 0) { throw 'VLC source clone failed' }
}
Write-Host 'Ready. Run: .\.venv\Scripts\python.exe run.py'
