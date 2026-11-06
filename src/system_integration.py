"""Windows 11 Default Apps registration and file association system integration.

Registers Ocal Media Player as a native Windows 11 Media Client in:
  - HKCU\\Software\\RegisteredApplications (appears in Windows Default Apps)
  - HKCU\\Software\\Clients\\Media\\Ocal Media Player\\Capabilities
  - HKCU\\Software\\Classes\\Applications\\Ocal Media Player.exe
  - HKCU\\Software\\Classes\\OcalMediaPlayer.<ext> (audio & video ProgIDs)

Maintains Windows Shell Property Thumbnail Handler for video previews with
Ocal Media Player badge overlay, and native player icon for audio files.
"""
import os
import sys
import subprocess
from pathlib import Path

# Supported Media Extensions
AUDIO_EXTENSIONS = {
    '.mp3': ('MP3 Audio File', 'audio/mpeg'),
    '.flac': ('FLAC Audio File', 'audio/flac'),
    '.wav': ('WAV Audio File', 'audio/wav'),
    '.m4a': ('M4A Audio File', 'audio/mp4'),
    '.aac': ('AAC Audio File', 'audio/aac'),
    '.ogg': ('OGG Audio File', 'audio/ogg'),
    '.opus': ('Opus Audio File', 'audio/opus'),
    '.wma': ('WMA Audio File', 'audio/x-ms-wma'),
}

VIDEO_EXTENSIONS = {
    '.mp4': ('MP4 Video File', 'video/mp4'),
    '.mkv': ('MKV Video File', 'video/x-matroska'),
    '.avi': ('AVI Video File', 'video/avi'),
    '.mov': ('QuickTime Video File', 'video/quicktime'),
    '.wmv': ('WMV Video File', 'video/x-ms-wmv'),
    '.webm': ('WebM Video File', 'video/webm'),
}

ALL_EXTENSIONS = {**AUDIO_EXTENSIONS, **VIDEO_EXTENSIONS}

# Windows Shell Thumbnail Handler GUIDs
SHELL_THUMBNAIL_PROVIDER = '{9DBD2C50-62AD-11D0-B806-00C04FD706EC}'
IEXTRACT_IMAGE_ID = '{BB2E617C-0920-11D1-9A0B-00C04FC2D6C1}'
ITHUMBNAIL_PROVIDER_ID = '{e357fccd-a995-4576-b01f-234630154e96}'


def get_installed_exe_path() -> Path:
    """Return the absolute path to Ocal Media Player executable."""
    if getattr(sys, 'frozen', False):
        return Path(sys.executable).resolve()
    
    # Check if compiled binary exists in dist
    base_dir = Path(__file__).resolve().parent.parent
    dist_exe = base_dir / 'dist' / 'Ocal Media Player' / 'Ocal Media Player.exe'
    if dist_exe.is_file():
        return dist_exe
    
    # Fallback to pythonw/python running run.py
    return Path(sys.executable).resolve()


def get_app_icon_path() -> Path:
    """Return the absolute path to the application icon."""
    base_dir = Path(__file__).resolve().parent.parent
    if getattr(sys, 'frozen', False):
        app_dir = Path(sys.executable).resolve().parent
        ico = app_dir / 'assets' / 'app-icon.ico'
        if ico.is_file():
            return ico
    ico = base_dir / 'assets' / 'app-icon.ico'
    return ico.resolve()


def notify_shell_associations_changed():
    """Notify Windows Explorer that file associations and icons have changed."""
    if sys.platform == 'win32':
        try:
            import ctypes
            # SHCNE_ASSOCCHANGED = 0x08000000, SHCNF_IDLIST = 0
            ctypes.windll.shell32.SHChangeNotify(0x08000000, 0, 0, 0)
        except Exception:
            pass


def is_registered_in_default_apps() -> bool:
    """Check if Ocal Media Player is registered in Windows RegisteredApplications."""
    if sys.platform != 'win32':
        return False
    try:
        import winreg
        with winreg.OpenKey(
            winreg.HKEY_CURRENT_USER,
            r'Software\RegisteredApplications'
        ) as key:
            winreg.QueryValueEx(key, 'Ocal Media Player')
            return True
    except Exception:
        return False


def register_default_media_player(exe_path: Path = None, icon_path: Path = None) -> bool:
    """
    Register Ocal Media Player into Windows 11 Registry under HKCU (no admin required).
    Registers:
      1. RegisteredApplications & Media Client Capabilities (for Windows Default Apps)
      2. Applications\\Ocal Media Player.exe
      3. File associations with dedicated ProgIDs for audio and video
      4. Shell thumbnail extraction for video files with app icon badge
    """
    if sys.platform != 'win32':
        return False

    import winreg

    if exe_path is None:
        exe_path = get_installed_exe_path()
    if icon_path is None:
        icon_path = get_app_icon_path()

    exe_str = str(exe_path)
    icon_str = f'"{icon_path}",0'
    open_cmd = f'"{exe_str}" "%1"'

    try:
        # 1. RegisteredApplications (HKCU)
        with winreg.CreateKey(winreg.HKEY_CURRENT_USER, r'Software\RegisteredApplications') as reg_apps:
            winreg.SetValueEx(reg_apps, 'Ocal Media Player', 0, winreg.REG_SZ,
                              r'Software\Clients\Media\Ocal Media Player\Capabilities')

        # 2. Software\Clients\Media\Ocal Media Player
        client_key_path = r'Software\Clients\Media\Ocal Media Player'
        with winreg.CreateKey(winreg.HKEY_CURRENT_USER, client_key_path) as client_key:
            winreg.SetValueEx(client_key, '', 0, winreg.REG_SZ, 'Ocal Media Player')

        with winreg.CreateKey(winreg.HKEY_CURRENT_USER, f'{client_key_path}\\DefaultIcon') as def_icon:
            winreg.SetValueEx(def_icon, '', 0, winreg.REG_SZ, icon_str)

        with winreg.CreateKey(winreg.HKEY_CURRENT_USER, f'{client_key_path}\\shell\\open\\command') as open_k:
            winreg.SetValueEx(open_k, '', 0, winreg.REG_SZ, f'"{exe_str}"')

        # Capabilities
        cap_path = f'{client_key_path}\\Capabilities'
        with winreg.CreateKey(winreg.HKEY_CURRENT_USER, cap_path) as cap_key:
            winreg.SetValueEx(cap_key, 'ApplicationName', 0, winreg.REG_SZ, 'Ocal Media Player')
            winreg.SetValueEx(cap_key, 'ApplicationDescription', 0, winreg.REG_SZ,
                              'Fluent Design Audio & Video Media Player for Windows 11')
            winreg.SetValueEx(cap_key, 'ApplicationIcon', 0, winreg.REG_SZ, icon_str)

        with winreg.CreateKey(winreg.HKEY_CURRENT_USER, f'{cap_path}\\FileAssociations') as fa_key:
            for ext in ALL_EXTENSIONS:
                progid = f'OcalMediaPlayer{ext}'
                winreg.SetValueEx(fa_key, ext, 0, winreg.REG_SZ, progid)

        # 3. Software\Classes\Applications\Ocal Media Player.exe
        app_class_path = r'Software\Classes\Applications\Ocal Media Player.exe'
        with winreg.CreateKey(winreg.HKEY_CURRENT_USER, app_class_path) as app_key:
            winreg.SetValueEx(app_key, 'FriendlyAppName', 0, winreg.REG_SZ, 'Ocal Media Player')
            winreg.SetValueEx(app_key, 'ApplicationCompany', 0, winreg.REG_SZ,
                              'Ocal Software under Gaming Network Studio')

        with winreg.CreateKey(winreg.HKEY_CURRENT_USER, f'{app_class_path}\\DefaultIcon') as a_icon:
            winreg.SetValueEx(a_icon, '', 0, winreg.REG_SZ, icon_str)

        with winreg.CreateKey(winreg.HKEY_CURRENT_USER, f'{app_class_path}\\shell\\open\\command') as a_cmd:
            winreg.SetValueEx(a_cmd, '', 0, winreg.REG_SZ, open_cmd)

        with winreg.CreateKey(winreg.HKEY_CURRENT_USER, f'{app_class_path}\\SupportedTypes') as a_supp:
            for ext in ALL_EXTENSIONS:
                winreg.SetValueEx(a_supp, ext, 0, winreg.REG_SZ, '')

        # 4. ProgIDs for Audio Extensions
        for ext, (desc, mime) in AUDIO_EXTENSIONS.items():
            progid = f'OcalMediaPlayer{ext}'
            p_path = f'Software\\Classes\\{progid}'
            with winreg.CreateKey(winreg.HKEY_CURRENT_USER, p_path) as pk:
                winreg.SetValueEx(pk, '', 0, winreg.REG_SZ, f'{desc} (Ocal Media Player)')
                winreg.SetValueEx(pk, 'FriendlyTypeName', 0, winreg.REG_SZ, f'{desc} (Ocal Media Player)')
                winreg.SetValueEx(pk, 'PerceivedType', 0, winreg.REG_SZ, 'audio')

            with winreg.CreateKey(winreg.HKEY_CURRENT_USER, f'{p_path}\\DefaultIcon') as di:
                winreg.SetValueEx(di, '', 0, winreg.REG_SZ, icon_str)

            with winreg.CreateKey(winreg.HKEY_CURRENT_USER, f'{p_path}\\shell\\open\\command') as sc:
                winreg.SetValueEx(sc, '', 0, winreg.REG_SZ, open_cmd)

            with winreg.CreateKey(winreg.HKEY_CURRENT_USER, f'{p_path}\\shell\\Play') as sp:
                winreg.SetValueEx(sp, '', 0, winreg.REG_SZ, 'Play with Ocal Media Player')
                winreg.SetValueEx(sp, 'Icon', 0, winreg.REG_SZ, f'"{icon_path}"')
            with winreg.CreateKey(winreg.HKEY_CURRENT_USER, f'{p_path}\\shell\\Play\\command') as spc:
                winreg.SetValueEx(spc, '', 0, winreg.REG_SZ, open_cmd)

            # Extension OpenWithProgids
            ext_path = f'Software\\Classes\\{ext}'
            with winreg.CreateKey(winreg.HKEY_CURRENT_USER, ext_path) as ek:
                winreg.SetValueEx(ek, 'PerceivedType', 0, winreg.REG_SZ, 'audio')
                winreg.SetValueEx(ek, 'Content Type', 0, winreg.REG_SZ, mime)
            with winreg.CreateKey(winreg.HKEY_CURRENT_USER, f'{ext_path}\\OpenWithProgids') as ow:
                winreg.SetValueEx(ow, progid, 0, winreg.REG_SZ, '')

        # 5. ProgIDs for Video Extensions (Preserves Windows Video Thumbnail Extraction with app overlay)
        for ext, (desc, mime) in VIDEO_EXTENSIONS.items():
            progid = f'OcalMediaPlayer{ext}'
            p_path = f'Software\\Classes\\{progid}'
            with winreg.CreateKey(winreg.HKEY_CURRENT_USER, p_path) as pk:
                winreg.SetValueEx(pk, '', 0, winreg.REG_SZ, f'{desc} (Ocal Media Player)')
                winreg.SetValueEx(pk, 'FriendlyTypeName', 0, winreg.REG_SZ, f'{desc} (Ocal Media Player)')
                winreg.SetValueEx(pk, 'PerceivedType', 0, winreg.REG_SZ, 'video')
                # Treatment = 3 instructs Windows Explorer to render video thumbnail previews
                winreg.SetValueEx(pk, 'Treatment', 0, winreg.REG_DWORD, 3)
                winreg.SetValueEx(pk, 'ThumbnailCutoff', 0, winreg.REG_DWORD, 1)

            with winreg.CreateKey(winreg.HKEY_CURRENT_USER, f'{p_path}\\DefaultIcon') as di:
                winreg.SetValueEx(di, '', 0, winreg.REG_SZ, icon_str)

            with winreg.CreateKey(winreg.HKEY_CURRENT_USER, f'{p_path}\\shell\\open\\command') as sc:
                winreg.SetValueEx(sc, '', 0, winreg.REG_SZ, open_cmd)

            with winreg.CreateKey(winreg.HKEY_CURRENT_USER, f'{p_path}\\shell\\Play') as sp:
                winreg.SetValueEx(sp, '', 0, winreg.REG_SZ, 'Play with Ocal Media Player')
                winreg.SetValueEx(sp, 'Icon', 0, winreg.REG_SZ, f'"{icon_path}"')
            with winreg.CreateKey(winreg.HKEY_CURRENT_USER, f'{p_path}\\shell\\Play\\command') as spc:
                winreg.SetValueEx(spc, '', 0, winreg.REG_SZ, open_cmd)

            # Explicitly wire Windows Shell Property Thumbnail Handler to ProgID
            shellex_base = f'{p_path}\\ShellEx'
            with winreg.CreateKey(winreg.HKEY_CURRENT_USER, f'{shellex_base}\\{IEXTRACT_IMAGE_ID}') as th1:
                winreg.SetValueEx(th1, '', 0, winreg.REG_SZ, SHELL_THUMBNAIL_PROVIDER)
            with winreg.CreateKey(winreg.HKEY_CURRENT_USER, f'{shellex_base}\\{ITHUMBNAIL_PROVIDER_ID}') as th2:
                winreg.SetValueEx(th2, '', 0, winreg.REG_SZ, SHELL_THUMBNAIL_PROVIDER)

            # Extension OpenWithProgids & ShellEx
            ext_path = f'Software\\Classes\\{ext}'
            with winreg.CreateKey(winreg.HKEY_CURRENT_USER, ext_path) as ek:
                winreg.SetValueEx(ek, 'PerceivedType', 0, winreg.REG_SZ, 'video')
                winreg.SetValueEx(ek, 'Content Type', 0, winreg.REG_SZ, mime)
            with winreg.CreateKey(winreg.HKEY_CURRENT_USER, f'{ext_path}\\OpenWithProgids') as ow:
                winreg.SetValueEx(ow, progid, 0, winreg.REG_SZ, '')

            # Ensure extension has video thumbnail handler configured
            with winreg.CreateKey(winreg.HKEY_CURRENT_USER, f'{ext_path}\\ShellEx\\{IEXTRACT_IMAGE_ID}') as eth1:
                winreg.SetValueEx(eth1, '', 0, winreg.REG_SZ, SHELL_THUMBNAIL_PROVIDER)
            with winreg.CreateKey(winreg.HKEY_CURRENT_USER, f'{ext_path}\\ShellEx\\{ITHUMBNAIL_PROVIDER_ID}') as eth2:
                winreg.SetValueEx(eth2, '', 0, winreg.REG_SZ, SHELL_THUMBNAIL_PROVIDER)

        notify_shell_associations_changed()
        return True
    except Exception as exc:
        print(f'Failed to register default player: {exc}', file=sys.stderr)
        return False


def open_windows_default_apps_settings():
    """Launch Windows 11 Settings to the Default Apps page."""
    if sys.platform == 'win32':
        try:
            os.startfile('ms-settings:defaultapps')
        except Exception:
            subprocess.Popen(['explorer', 'ms-settings:defaultapps'])

