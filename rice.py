#!/usr/bin/env python3
"""Apply machine-local wallpaper paths and Firefox links, keeping private state outside Git."""
import argparse
import configparser
from datetime import datetime
import hashlib
import json
import os
from pathlib import Path
import shutil
import urllib.request

REPO = Path(__file__).resolve().parent
HOME = Path.home()
STATE = HOME / '.local/state/dotfiles'
WALL = HOME / '.local/share/wallpapers/tokyo-night.png'
# Source reviewed through GitHub; download is optional and never executes remote code.
GITHUB_WALL = 'https://raw.githubusercontent.com/tokyo-night/wallpapers/main/night/abstract/lockscreen_00_3840x2160.png'

def preserve(path, backup):
    if os.path.lexists(path):
        dest = backup / path.relative_to(HOME)
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(path, dest, follow_symlinks=False)

def link(source, target, backup):
    if target.is_symlink() and target.resolve() == source.resolve():
        temporary = target.with_name(target.name + '.dotfiles-link')
        if os.path.lexists(temporary):
            raise SystemExit(f'Temporary link already exists: {temporary}')
        temporary.symlink_to(os.path.relpath(source, target.parent))
        os.replace(temporary, target)
        return
    if target.is_dir():
        raise SystemExit(f'Refusing to replace directory: {target}')
    target.parent.mkdir(parents=True, exist_ok=True)
    preserve(target, backup)
    if os.path.lexists(target):
        target.unlink()
    target.symlink_to(os.path.relpath(source, target.parent))

def apply(fetch=False):
    backup = STATE / 'backups' / ('rice-' + datetime.now().strftime('%Y%m%d-%H%M%S-%f'))
    import gi
    gi.require_version('GdkPixbuf', '2.0')
    from gi.repository import GdkPixbuf
    WALL.parent.mkdir(parents=True, exist_ok=True)
    STATE.mkdir(parents=True, exist_ok=True)
    svg = HOME / '.local/share/wallpapers/tokyo-night.svg'
    if fetch:
        # Validate the image before replacing the current wallpaper. A network error
        # leaves the existing theme and wallpaper intact.
        with urllib.request.urlopen(GITHUB_WALL, timeout=20) as response:
            data = response.read(25 * 1024 * 1024 + 1)
        if len(data) > 25 * 1024 * 1024 or not data.startswith(b'\x89PNG\r\n\x1a\n'):
            raise SystemExit('Wallpaper download is not a valid size-limited PNG.')
        loader = GdkPixbuf.PixbufLoader.new_with_type('png')
        loader.write(data)
        loader.close()
        pixbuf = loader.get_pixbuf()
        preserve(WALL, backup)
        pixbuf.savev(str(WALL), 'png', [], [])
        (STATE / 'wallpaper-source.json').write_text(json.dumps({'url': GITHUB_WALL, 'sha256': hashlib.sha256(data).hexdigest()}, indent=2)+'\n')
    elif not WALL.exists():
        pixbuf = GdkPixbuf.Pixbuf.new_from_file(str(svg))
        pixbuf.savev(str(WALL), 'png', [], [])
    STATE.mkdir(parents=True, exist_ok=True)
    background = STATE / 'wallpaper-all.ron'
    text = '(output: "all", source: Path(' + json.dumps(str(WALL)) + '), filter_by_theme: false, rotation_frequency: 3600, filter_method: Lanczos, scaling_mode: Zoom, sampling_method: Alphanumeric,)\n'
    if not background.exists() or background.read_text() != text:
        background.write_text(text)
    link(background, HOME / '.config/cosmic/com.system76.CosmicBackground/v1/all', backup)

    # Discover only profile paths, never read history, cookies, passwords or prefs.js.
    base = HOME / '.config/mozilla/firefox'
    if not (base / 'profiles.ini').exists():
        base = HOME / '.mozilla/firefox'
    profiles = configparser.ConfigParser()
    profiles.read(base / 'profiles.ini')
    chosen = next((profiles[s].get('Default') for s in profiles.sections() if s.startswith('Install') and profiles[s].get('Default')), None)
    if chosen:
        profile = base / chosen
    else:
        sections = [s for s in profiles.sections() if s.startswith('Profile')]
        selected = next((s for s in sections if profiles[s].get('Default') == '1'), sections[0] if len(sections) == 1 else None)
        if selected:
            item = profiles[selected]
            profile = (base / item['Path']) if item.get('IsRelative', '1') == '1' else Path(item['Path'])
        else:
            profile = None
    if profile and profile.is_dir():
        for name in ('userChrome.css', 'userContent.css'):
            link(REPO / 'home/.config/firefox-theme' / name, profile / 'chrome' / name, backup)
        link(REPO / 'home/.local/share/wallpapers/tokyo-night.svg', profile / 'chrome/nightfall.svg', backup)
        userjs = profile / 'user.js'
        preference = 'user_pref("toolkit.legacyUserProfileCustomizations.stylesheets", true);'
        current = userjs.read_text() if userjs.exists() else ''
        if preference not in current:
            preserve(userjs, backup)
            with userjs.open('a') as stream:
                stream.write('\n// Dotfiles: enable local Tokyo Night UI styles.\n' + preference + '\n')
        print('Firefox styling installed. Fully quit and reopen Firefox to load it.')
    else:
        print('No unambiguous Firefox profile found; browser styling is available in home/.config/firefox-theme/.')
    print('Wallpaper and local theme links installed. Private backups: ' + str(backup))

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--apply', action='store_true')
    parser.add_argument('--fetch-wallpaper', action='store_true', help='download the selected GitHub wallpaper instead of the bundled original')
    args = parser.parse_args()
    if args.apply:
        apply(args.fetch_wallpaper)
    else:
        print('Run python3 install.py --apply to install the complete rice. Use python3 rice.py --apply --fetch-wallpaper to select the GitHub wallpaper.')
