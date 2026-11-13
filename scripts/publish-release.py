"""Publish Ocal Media Player release and upload build assets to GitHub Releases."""
import os
import sys
import json
import urllib.request
import urllib.error
import subprocess
from pathlib import Path


REPO_OWNER = 'neelkanth-patel26'
REPO_NAME = 'Ocal Media Player'
GITHUB_REPO = 'neelkanth-patel26/Ocal-Media-Player'
TAG_NAME = 'v1.0.2'
RELEASE_NAME = 'Ocal Media Player v1.0.2'

RELEASE_BODY = """## Ocal Media Player v1.0.2

Developer: **Ocal Software under Gaming Network Studio**  
Repository: [neelkanth-patel26/Ocal-Media-Player](https://github.com/neelkanth-patel26/Ocal-Media-Player)

### What's New in v1.0.2
- **Dynamic Theme Accent Updates**: Fallback media thumbnails in the main collection table, play queue, and bottom transport bar now instantly adapt whenever custom accents or system themes are toggled without caching stale colors.
- **Instantaneous Timeline Click-to-Seek**: Direct single-click seeking on the timeline seek bar jumps immediately to the exact track or video position without requiring scrubbing or dragging.
- **Multi-Ratio & Portrait Video Support**: Full support for landscape, portrait, and square aspect ratios: `Auto`, `16:9`, `9:16` (Vertical / Shorts / Reels), `4:3`, `3:4`, `1:1`, `4:5`, `21:9`, `16:10`, `Fit to Window`, and `Fill Window`.
- **Automatic Orientation & Anti-Stretch Detection**: Phone-recorded portrait videos and vertical content are automatically detected and pillarboxed cleanly without horizontal stretching or distortion.
- **Modern Fluent Installer & Updater Experience**: Distinct custom installer styles for fresh installation vs. seamless in-app upgrades.

### Included Downloads
- `Ocal-Media-Player-1.0.2-Setup.exe`: Complete Windows 11 installer with Start Menu shortcuts, desktop icon, and automated file associations.
- `Ocal-Media-Player-1.0.2-Portable-x64.zip`: Standalone portable package (extract and run anywhere).
"""


def get_github_token() -> str:
    """Retrieve GitHub token from environment or Git Credential Manager."""
    token = os.environ.get('GITHUB_TOKEN')
    if token:
        return token.strip()
    try:
        p = subprocess.Popen(['git', 'credential', 'fill'],
                             stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE, text=True)
        out, _ = p.communicate('protocol=https\nhost=github.com\n\n')
        for line in out.splitlines():
            if line.startswith('password='):
                return line.split('=', 1)[1].strip()
    except Exception as e:
        print(f'Warning: Could not query git credentials: {e}', file=sys.stderr)
    return None


def push_git_tag(tag: str):
    """Ensure the git tag is created and pushed to origin."""
    print(f'--> Checking git tag: {tag}')
    try:
        subprocess.run(['git', 'tag', '-a', tag, '-m', f'Release {tag}'],
                       check=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        res = subprocess.run(['git', 'push', 'origin', tag],
                             capture_output=True, text=True)
        if res.returncode == 0:
            print(f'Successfully pushed tag {tag} to origin.')
        else:
            print(f'Tag push note: {res.stderr.strip() or res.stdout.strip()}')
    except Exception as exc:
        print(f'Tag push exception: {exc}')


def create_or_get_release(token: str) -> dict:
    """Create GitHub release via REST API or fetch if already exists."""
    headers = {
        'Authorization': f'Bearer {token}',
        'Accept': 'application/vnd.github+json',
        'User-Agent': 'Ocal-Release-Publisher',
        'Content-Type': 'application/json',
    }

    # First check if release with this tag already exists
    get_url = f'https://api.github.com/repos/{GITHUB_REPO}/releases/tags/{TAG_NAME}'
    req = urllib.request.Request(get_url, headers=headers, method='GET')
    try:
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            print(f'Found existing release for tag {TAG_NAME} (ID: {data.get("id")})')
            return data
    except urllib.error.HTTPError as e:
        if e.code != 404:
            raise

    # Create new release
    print(f'Creating new release: {RELEASE_NAME} ({TAG_NAME})...')
    post_url = f'https://api.github.com/repos/{GITHUB_REPO}/releases'
    payload = json.dumps({
        'tag_name': TAG_NAME,
        'target_commitish': 'main',
        'name': RELEASE_NAME,
        'body': RELEASE_BODY,
        'draft': False,
        'prerelease': False
    }).encode('utf-8')

    req = urllib.request.Request(post_url, data=payload, headers=headers, method='POST')
    with urllib.request.urlopen(req) as resp:
        data = json.loads(resp.read().decode('utf-8'))
        print(f'Created release {RELEASE_NAME} successfully! ID: {data.get("id")}')
        return data


def upload_asset(token: str, release_id: int, file_path: Path):
    """Upload a binary asset file to the specified GitHub release."""
    file_path = file_path.resolve()
    if not file_path.is_file():
        raise FileNotFoundError(f'File not found: {file_path}')

    filename = file_path.name
    filesize = file_path.stat().st_size
    print(f'--> Uploading {filename} ({filesize / (1024*1024):.2f} MB)...')

    upload_url = f'https://uploads.github.com/repos/{GITHUB_REPO}/releases/{release_id}/assets?name={urllib.parse.quote(filename)}'

    headers = {
        'Authorization': f'Bearer {token}',
        'Accept': 'application/vnd.github+json',
        'User-Agent': 'Ocal-Release-Publisher',
        'Content-Type': 'application/octet-stream',
        'Content-Length': str(filesize),
    }

    with open(file_path, 'rb') as f:
        req = urllib.request.Request(upload_url, data=f, headers=headers, method='POST')
        with urllib.request.urlopen(req) as resp:
            result = json.loads(resp.read().decode('utf-8'))
            download_url = result.get('browser_download_url')
            print(f'Successfully uploaded {filename}!')
            print(f'    Download URL: {download_url}')
            return result


def main():
    token = get_github_token()
    if not token:
        print('Error: Could not obtain GitHub authorization token.', file=sys.stderr)
        return 1

    push_git_tag(TAG_NAME)
    release = create_or_get_release(token)
    release_id = release['id']
    html_url = release.get('html_url')

    base_dir = Path(__file__).resolve().parent.parent
    dist_installer = base_dir / 'dist-installer'

    assets_to_upload = [
        dist_installer / 'Ocal-Media-Player-1.0.2-Setup.exe',
        dist_installer / 'Ocal-Media-Player-1.0.2-Portable-x64.zip',
    ]

    # Delete existing asset if present so we can upload the updated build
    for a in release.get('assets', []):
        if a.get('name') in {p.name for p in assets_to_upload}:
            aid = a['id']
            print(f'Deleting previous asset {a["name"]} (id {aid}) to upload updated build...')
            del_req = urllib.request.Request(
                f'https://api.github.com/repos/{GITHUB_REPO}/releases/assets/{aid}',
                headers={'Authorization': f'Bearer {token}', 'Accept': 'application/vnd.github+json'},
                method='DELETE'
            )
            try:
                with urllib.request.urlopen(del_req) as del_resp:
                    pass
            except Exception as e:
                print(f'Note: Asset delete response: {e}')

    for asset_path in assets_to_upload:
        if asset_path.is_file():
            upload_asset(token, release_id, asset_path)
        else:
            print(f'Warning: Asset file not found: {asset_path}', file=sys.stderr)

    print('\n============================================================')
    print(' RELEASE PUBLISHED SUCCESSFULLY!')
    print(f' Release URL: {html_url}')
    print('============================================================\n')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())

