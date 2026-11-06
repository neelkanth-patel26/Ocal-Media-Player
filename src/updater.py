"""Ocal Media Player auto-updater using GitHub Releases API."""
import os
import sys
import json
import tempfile
import subprocess
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError
from PySide6.QtCore import QThread, Signal

CURRENT_VERSION = "1.0.0"
REPO_OWNER = "neelkanth-patel26"
REPO_NAME = "Ocal-Media-Player"
LATEST_RELEASE_URL = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/releases/latest"


def parse_version(ver_str):
    """Parse 'v1.2.3' or '1.2.3' into a comparable tuple of ints."""
    clean = ver_str.strip().lstrip('vV')
    parts = []
    for part in clean.split('.'):
        digits = ''
        for ch in part:
            if ch.isdigit():
                digits += ch
            else:
                break
        parts.append(int(digits) if digits else 0)
    return tuple(parts)


def is_newer_version(latest_str, current_str=CURRENT_VERSION):
    try:
        return parse_version(latest_str) > parse_version(current_str)
    except Exception:
        return False


class UpdateCheckerThread(QThread):
    """Checks for latest release from GitHub API in background."""
    update_available = Signal(str, str, str, str)  # version, notes, download_url, asset_name
    up_to_date = Signal(str)
    error = Signal(str)

    def __init__(self, parent=None, current_version=CURRENT_VERSION):
        super().__init__(parent)
        self.current_version = current_version

    def run(self):
        req = Request(LATEST_RELEASE_URL, headers={
            'User-Agent': 'Ocal-Media-Player',
            'Accept': 'application/vnd.github.v3+json'
        })
        try:
            with urlopen(req, timeout=10) as resp:
                if resp.status == 200:
                    data = json.loads(resp.read().decode('utf-8'))
                    tag = data.get('tag_name', '').lstrip('vV')
                    notes = data.get('body', '') or 'No release notes provided.'
                    assets = data.get('assets', [])

                    installer_asset = None
                    for asset in assets:
                        name = asset.get('name', '').lower()
                        if name.endswith('.exe'):
                            installer_asset = asset
                            if 'setup' in name:
                                break

                    if is_newer_version(tag, self.current_version):
                        url = installer_asset.get('browser_download_url', '') if installer_asset else ''
                        name = installer_asset.get('name', f'Ocal-Media-Player-{tag}-Setup.exe') if installer_asset else ''
                        self.update_available.emit(tag, notes, url, name)
                    else:
                        self.up_to_date.emit(self.current_version)
                else:
                    self.error.emit(f"HTTP {resp.status}")
        except HTTPError as e:
            if e.code == 404:
                # No release published yet on repository; current version is up to date
                self.up_to_date.emit(self.current_version)
            else:
                self.error.emit(f"GitHub API Error: {e.reason} ({e.code})")
        except URLError as e:
            self.error.emit(f"Network error: {e.reason}")
        except Exception as e:
            self.error.emit(str(e))


class UpdateDownloaderThread(QThread):
    """Downloads installer asset in background with progress."""
    progress = Signal(int)  # 0 to 100
    finished = Signal(str)  # target file path
    error = Signal(str)

    def __init__(self, download_url, asset_name, parent=None):
        super().__init__(parent)
        self.download_url = download_url
        self.asset_name = asset_name
        self._is_cancelled = False

    def cancel(self):
        self._is_cancelled = True

    def run(self):
        if not self.download_url:
            self.error.emit("No download URL provided for installer.")
            return

        target_dir = Path(tempfile.gettempdir()) / 'OcalMediaPlayerUpdate'
        try:
            target_dir.mkdir(parents=True, exist_ok=True)
            target_file = target_dir / self.asset_name

            req = Request(self.download_url, headers={'User-Agent': 'Ocal-Media-Player'})
            with urlopen(req, timeout=30) as resp:
                total_size = int(resp.headers.get('content-length', 0))
                downloaded = 0
                chunk_size = 65536

                with open(target_file, 'wb') as f:
                    while True:
                        if self._is_cancelled:
                            return
                        chunk = resp.read(chunk_size)
                        if not chunk:
                            break
                        f.write(chunk)
                        downloaded += len(chunk)
                        if total_size > 0:
                            pct = min(100, int((downloaded / total_size) * 100))
                            self.progress.emit(pct)

            self.finished.emit(str(target_file))
        except Exception as e:
            self.error.emit(str(e))


def launch_installer_and_exit(installer_path, silent=False):
    """Launch the downloaded Inno Setup installer and terminate current application."""
    if not os.path.exists(installer_path):
        return False
    args = [str(installer_path)]
    if silent:
        args.extend(['/SILENT', '/SUPPRESSMSGBOXES', '/NORESTART'])
    try:
        subprocess.Popen(args, close_fds=True)
        from PySide6.QtWidgets import QApplication
        app = QApplication.instance()
        if app:
            app.quit()
        else:
            sys.exit(0)
        return True
    except Exception:
        return False
