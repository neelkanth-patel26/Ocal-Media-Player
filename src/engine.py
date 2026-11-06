"""Small, explicitly typed LibVLC 4 ABI adapter. All public times are milliseconds."""
import ctypes as C
import os
import sys
from pathlib import Path

ROOT = Path(getattr(sys, '_MEIPASS', Path(__file__).resolve().parent.parent))


class Engine:
    def __init__(self, hwnd=0):
        self.instance = self.player = None
        self.paused_seek = None
        self.desired_media = None
        directory = Path(os.environ.get('OCAL_VLC_DIR', os.environ.get('GNS_VLC_DIR', ROOT / 'runtime' / 'vlc-4.0.0-dev')))
        if not (directory / 'libvlc.dll').is_file():
            raise RuntimeError('VLC 4 runtime is missing. Run scripts/setup.ps1 first.')
        self.dll_directory = os.add_dll_directory(str(directory))
        os.environ['VLC_PLUGIN_PATH'] = str(directory / 'plugins')
        self.core = C.CDLL(str(directory / 'libvlccore.dll'))
        self.lib = C.CDLL(str(directory / 'libvlc.dll'))
        signatures = {
            'get_version': (C.c_char_p, []),
            'new': (C.c_void_p, [C.c_int, C.POINTER(C.c_char_p)]),
            'release': (None, [C.c_void_p]),
            'media_player_new': (C.c_void_p, [C.c_void_p, C.c_void_p, C.c_void_p]),
            'media_player_release': (None, [C.c_void_p]),
            'media_new_path': (C.c_void_p, [C.c_char_p]),
            'media_new_location': (C.c_void_p, [C.c_char_p]),
            'media_release': (None, [C.c_void_p]),
            'media_player_set_media': (None, [C.c_void_p, C.c_void_p]),
            'media_player_get_media': (C.c_void_p, [C.c_void_p]),
            'media_player_set_hwnd': (None, [C.c_void_p, C.c_void_p]),
            'media_player_play': (C.c_int, [C.c_void_p]),
            'media_player_set_pause': (None, [C.c_void_p, C.c_int]),
            'media_player_stop_async': (C.c_int, [C.c_void_p]),
            'media_player_get_state': (C.c_int, [C.c_void_p]),
            'media_player_get_time': (C.c_int64, [C.c_void_p]),
            'media_player_get_length': (C.c_int64, [C.c_void_p]),
            'media_player_is_seekable': (C.c_int, [C.c_void_p]),
            'media_player_set_time': (C.c_int, [C.c_void_p, C.c_int64, C.c_bool]),
            'media_player_set_rate': (C.c_int, [C.c_void_p, C.c_float]),
            'audio_set_volume': (C.c_int, [C.c_void_p, C.c_int]),
            'media_player_add_slave': (C.c_int, [C.c_void_p, C.c_int, C.c_char_p, C.c_bool]),
            'video_take_snapshot': (C.c_int, [C.c_void_p, C.c_uint, C.c_char_p, C.c_uint, C.c_uint]),
            'video_set_mouse_input': (None, [C.c_void_p, C.c_uint]),
            'video_set_key_input': (None, [C.c_void_p, C.c_uint]),
            'audio_equalizer_get_preset_count': (C.c_uint, []),
            'audio_equalizer_get_preset_name': (C.c_char_p, [C.c_uint]),
            'audio_equalizer_new_from_preset': (C.c_void_p, [C.c_uint]),
            'audio_equalizer_release': (None, [C.c_void_p]),
            'media_player_set_equalizer': (C.c_int, [C.c_void_p, C.c_void_p]),
            'video_set_aspect_ratio': (None, [C.c_void_p, C.c_char_p]),
            'video_get_aspect_ratio': (C.c_char_p, [C.c_void_p]),
        }
        for name, (result, args) in signatures.items():
            fn = getattr(self.lib, 'libvlc_' + name)
            fn.restype, fn.argtypes = result, args
            setattr(self, '_' + name, fn)
        self.version = self._get_version().decode()
        if not self.version.startswith('4.'):
            raise RuntimeError(f'Ocal Media Player requires LibVLC 4; found {self.version}')
        self.instance = self._new(0, None)
        if not self.instance:
            raise RuntimeError('Could not initialize LibVLC 4.')
        self.player = self._media_player_new(self.instance, None, None)
        if not self.player:
            self._release(self.instance)
            raise RuntimeError('Could not create the media player.')
        self._media_player_set_hwnd(self.player, hwnd)
        self._video_set_mouse_input(self.player, 0)
        self._video_set_key_input(self.player, 0)

    def play(self, location):
        self.paused_seek = None
        remote = '://' in location
        media = (self._media_new_location if remote else self._media_new_path)(location.encode('utf-8'))
        if not media:
            raise RuntimeError('VLC could not open this media.')
        try:
            self._media_player_set_media(self.player, media)
            self.desired_media = media
        finally:
            self._media_release(media)
        if self._media_player_play(self.player) == -1:
            raise RuntimeError('VLC could not start playback.')

    @property
    def media_ready(self):
        media = self._media_player_get_media(self.player)
        if not media:
            return False
        try:
            return media == self.desired_media
        finally:
            self._media_release(media)

    @property
    def state(self):
        if not getattr(self, 'player', None):
            return 0
        try:
            return self._media_player_get_state(self.player)
        except Exception:
            return 0

    @property
    def time(self):
        # VLC's clock may not publish an audio seek until playback resumes.
        if self.paused_seek is not None and self.state == 3:
            return self.paused_seek
        self.paused_seek = None
        return max(0, self._media_player_get_time(self.player) // 1000)

    @property
    def length(self):
        return max(0, self._media_player_get_length(self.player) // 1000)

    @property
    def seekable(self):
        return bool(self._media_player_is_seekable(self.player))

    def seek(self, milliseconds):
        milliseconds = max(0, int(milliseconds))
        result = self._media_player_set_time(self.player, milliseconds * 1000, False)
        if result == 0 and self.state == 3:
            self.paused_seek = milliseconds
        return result

    def pause(self, paused=True):
        self._media_player_set_pause(self.player, int(paused))

    def volume(self, value):
        self._audio_set_volume(self.player, int(value))

    def rate(self, value):
        return self._media_player_set_rate(self.player, value)

    def subtitle(self, path):
        return self._media_player_add_slave(self.player, 0, Path(path).resolve().as_uri().encode(), True)

    def snapshot(self, path):
        return self._video_take_snapshot(self.player, 0, str(path).encode('utf-8'), 0, 0)

    def get_equalizer_presets(self):
        try:
            count = self._audio_equalizer_get_preset_count()
            return [self._audio_equalizer_get_preset_name(i).decode() for i in range(count)]
        except Exception:
            return []

    def set_equalizer_preset(self, preset_name):
        if not preset_name or preset_name.lower() in ('off', 'flat'):
            # Setting None clears equalizer back to standard
            if preset_name and preset_name.lower() == 'flat':
                presets = self.get_equalizer_presets()
                if 'Flat' in presets:
                    idx = presets.index('Flat')
                    eq = self._audio_equalizer_new_from_preset(idx)
                    if eq:
                        try:
                            self._media_player_set_equalizer(self.player, eq)
                        finally:
                            self._audio_equalizer_release(eq)
                        return True
            self._media_player_set_equalizer(self.player, None)
            return True
        presets = self.get_equalizer_presets()
        for idx, name in enumerate(presets):
            if name.lower() == preset_name.lower():
                eq = self._audio_equalizer_new_from_preset(idx)
                if eq:
                    try:
                        self._media_player_set_equalizer(self.player, eq)
                    finally:
                        self._audio_equalizer_release(eq)
                    return True
        return False

    def set_aspect_ratio(self, ratio_str):
        if not ratio_str or ratio_str.lower() in ('auto', 'default'):
            self._video_set_aspect_ratio(self.player, None)
        else:
            self._video_set_aspect_ratio(self.player, ratio_str.encode('utf-8'))

    def close(self):
        if self.player:
            self._media_player_stop_async(self.player)
            self._media_player_release(self.player)
            self.player = None
        if self.instance:
            self._release(self.instance)
            self.instance = None
