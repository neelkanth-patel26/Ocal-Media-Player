"""Atomic local library storage; never modifies users' media files."""
import json
import os
import math
from pathlib import Path
from urllib.parse import urlparse

from .metadata import extract_media_metadata

AUDIO = {
    '.mp3', '.flac', '.wav', '.aac', '.m4a', '.ogg', '.opus',
    '.wma', '.aiff', '.alac', '.mid', '.midi', '.ac3', '.dts',
    '.ape', '.mp2', '.mka', '.ra', '.voc', '.amr'
}
VIDEO = {
    '.mp4', '.mkv', '.mov', '.avi', '.webm', '.m4v', '.wmv',
    '.mpeg', '.mpg', '.ts', '.m2ts', '.flv', '.3gp', '.vob',
    '.ogv', '.divx', '.asf', '.rm', '.rmvb', '.f4v', '.mts'
}


def clock(ms):
    seconds = max(0, int(ms)) // 1000
    hours, seconds = divmod(seconds, 3600)
    minutes, seconds = divmod(seconds, 60)
    return f'{hours}:{minutes:02}:{seconds:02}' if hours else f'{minutes}:{seconds:02}'


class Library:
    def __init__(self, directory=None):
        self.is_custom = bool(directory or os.environ.get('OCAL_DATA_DIR') or os.environ.get('GNS_DATA_DIR'))
        local_app = Path(os.environ.get('LOCALAPPDATA', Path.home()))
        default_dir = local_app / 'Ocal Media Player'
        legacy_dir = local_app / 'GNS Player'
        if not directory and not os.environ.get('OCAL_DATA_DIR') and not default_dir.exists() and legacy_dir.exists():
            try:
                import shutil
                shutil.copytree(legacy_dir, default_dir)
            except Exception:
                pass
        target_dir = Path(directory or os.environ.get('OCAL_DATA_DIR') or os.environ.get('GNS_DATA_DIR') or default_dir)
        try:
            target_dir.mkdir(parents=True, exist_ok=True)
            self.directory = target_dir
        except (PermissionError, OSError):
            fallback_dir = Path(__file__).resolve().parent.parent / '.data'
            fallback_dir.mkdir(parents=True, exist_ok=True)
            self.directory = fallback_dir
        self.path = self.directory / 'library.json'
        self.items = []
        self.settings = {
            'volume': 70,
            'watch_folders': [],
            'theme_mode': 'system',
            'accent_color': 'system',
            'audio_profile': 'Flat',
            'video_aspect': 'Auto',
            'auto_check_updates': True,
            'auto_resume': True,
            'hardware_decoding': True,
        }
        self.warning = ''
        if self.path.exists():
            try:
                data = json.loads(self.path.read_text(encoding='utf-8'))
                if not isinstance(data, dict) or not isinstance(data.get('items'), list):
                    raise ValueError('Invalid library structure')
                for item in data['items']:
                    if not isinstance(item, dict) or not isinstance(item.get('path'), str) or not isinstance(item.get('title'), str):
                        raise ValueError('Invalid library item')
                    item.setdefault('kind', 'Video')
                    item.setdefault('favorite', False)
                    item.setdefault('artist', '')
                    item.setdefault('album', '')
                    for key in ('position', 'duration', 'played'):
                        item[key] = max(0, float(item.get(key, 0)))
                        if not math.isfinite(item[key]):
                            raise ValueError('Invalid timestamp')
                    if not isinstance(item.get('bookmarks', []), list):
                        raise ValueError('Invalid bookmarks')
                    item.setdefault('bookmarks', [])
                    for mark in item['bookmarks']:
                        if not isinstance(mark, dict) or not isinstance(mark.get('name'), str):
                            raise ValueError('Invalid bookmark')
                        mark['time'] = float(mark['time'])
                        if not math.isfinite(mark['time']) or mark['time'] < 0:
                            raise ValueError('Invalid bookmark timestamp')
                self.items = data['items']
                if isinstance(data.get('settings'), dict):
                    self.settings.update(data['settings'])
                self.settings['volume'] = min(100, max(0, int(self.settings['volume'])))
            except (ValueError, TypeError, KeyError, OverflowError, OSError):
                # Keep the damaged file for recovery before the next save.
                backup = self.directory / 'library.recovery.json'
                backup.write_bytes(self.path.read_bytes())
                self.items = []
                self.settings = {'volume': 70}
                self.warning = f'Your library could not be read. A recovery copy is saved at {backup}.'

    def save(self):
        try:
            self.directory.mkdir(parents=True, exist_ok=True)
            temp = self.path.with_suffix('.tmp')
            temp.write_text(json.dumps({'version': 1, 'items': self.items, 'settings': self.settings}, indent=2), encoding='utf-8')
            temp.replace(self.path)
        except Exception:
            pass

    def add(self, locations):
        added = []
        known = {x['path'].casefold(): x for x in self.items}
        for location in locations:
            remote = '://' in str(location)
            path = str(location) if remote else str(Path(location).resolve())
            if remote:
                if urlparse(path).scheme.lower() not in {'http', 'https', 'rtsp', 'rtmp', 'udp', 'rtp'}:
                    continue
            elif not Path(path).is_file() or Path(path).suffix.lower() not in AUDIO | VIDEO:
                continue
            if path.casefold() in known:
                added.append(known[path.casefold()])
                continue
            dur = 0
            artist = ''
            album = ''
            title = path if remote else Path(path).stem
            if not remote:
                dur, tags = extract_media_metadata(path)
                if tags.get('title'):
                    title = tags['title']
                artist = tags.get('artist', '')
                album = tags.get('album', '')
            item = {
                'path': path,
                'title': title,
                'artist': artist,
                'album': album,
                'kind': 'Stream' if remote else ('Music' if Path(path).suffix.lower() in AUDIO else 'Video'),
                'favorite': False,
                'position': 0,
                'duration': dur,
                'played': 0,
                'bookmarks': []
            }
            self.items.append(item)
            known[path.casefold()] = item
            added.append(item)
        self.save()
        return added
