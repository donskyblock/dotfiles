#!/usr/bin/env python3
"""Install just the neon wallpaper and/or desktop music widget."""
import argparse
from datetime import datetime
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

BASE = Path(__file__).resolve().parent
SOURCE = 'https://github.com/tokyo-night/wallpapers/blob/9a72582d7505da9a28b2fd77c155fbf140f6c8f0/misc/cityscape/neon-sign_00_1920x1080.jpg'
FILES = ('widget.py', 'settings.json', 'style.css', 'cava.conf')


def dependencies():
    import gi
    gi.require_version('Gtk', '3.0')
    gi.require_version('GtkLayerShell', '0.1')
    from gi.repository import GtkLayerShell
    if not shutil.which('cava'):
        raise RuntimeError('cava is required')
    import cairo


def apply(component, home=None, start=True):
    home = home or Path.home()
    if component in ('widgets', 'both'):
        try:
            dependencies()
        except (ImportError, ValueError, RuntimeError) as e:
            raise SystemExit(f'Widget dependency missing: {e}\nOn Void: sudo xbps-install gtk-layer-shell cava python3-gobject python3-cairo')
    state = home / '.local/state/dotfiles'
    backup = state / 'backups' / ('desktop-' + datetime.now().strftime('%Y%m%d-%H%M%S-%f'))

    def write(path, data):
        # Preserve originals and replace atomically, including existing symlinks.
        if any(p.is_symlink() for p in path.parents if p != home and home in p.parents):
            raise RuntimeError(f'Refusing symlinked parent: {path}')
        if path.is_dir() and not path.is_symlink():
            raise RuntimeError(f'Refusing to replace directory: {path}')
        if os.path.lexists(path):
            saved = backup / path.relative_to(home)
            saved.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(path, saved, follow_symlinks=False)
            if path.is_symlink() and path.is_file():
                # Save its contents too; the link may point to generated state.
                saved.with_name(saved.name + '.contents').write_bytes(path.read_bytes())
        path.parent.mkdir(parents=True, exist_ok=True)
        fd, tmp = tempfile.mkstemp(prefix='.after-hours-', dir=path.parent)
        try:
            with os.fdopen(fd, 'wb') as stream:
                stream.write(data)
            os.chmod(tmp, 0o644)
            os.replace(tmp, path)
        finally:
            if os.path.exists(tmp):
                os.unlink(tmp)

    if component in ('wallpaper', 'both'):
        import gi
        gi.require_version('GdkPixbuf', '2.0')
        from gi.repository import GdkPixbuf
        # Validate before writing any desktop configuration.
        pixbuf = GdkPixbuf.Pixbuf.new_from_file(str(BASE / 'neon-sign.jpg'))
        if pixbuf.get_width() != 1920 or pixbuf.get_height() != 1081:
            raise RuntimeError('Unexpected wallpaper dimensions')
        wall = home / '.local/share/wallpapers/tokyo-night.png'
        success, png = pixbuf.save_to_bufferv('png', [], [])
        if not success:
            raise RuntimeError('Could not convert wallpaper')
        write(wall, png)
        config = home / '.config/cosmic/com.system76.CosmicBackground/v1'
        ron = '(output: "all", source: Path(' + json.dumps(str(wall)) + '), filter_by_theme: false, rotation_frequency: 3600, filter_method: Lanczos, scaling_mode: Zoom, sampling_method: Alphanumeric,)\n'
        write(config / 'all', ron.encode())
        write(config / 'same-on-all', b'true\n')
        write(state / 'wallpaper-source.json', (json.dumps({'url': SOURCE, 'sha256': hashlib.sha256((BASE / 'neon-sign.jpg').read_bytes()).hexdigest()}, indent=2) + '\n').encode())
        print('Neon-sign desktop wallpaper selected for all COSMIC outputs.')
    if component in ('widgets', 'both'):
        dest = home / '.local/share/dotfiles/desktop'
        for name in FILES:
            # Keep user placement preferences on subsequent installations.
            if name == 'settings.json' and (dest / name).exists():
                continue
            write(dest / name, (BASE / name).read_bytes())
        executable = str(dest / 'widget.py')
        if any(c in executable for c in '\n\r'):
            raise RuntimeError('Unsupported newline in installation path')
        # Desktop Entry Exec escaping, independent from shell quoting.
        quoted = executable.replace('\\', '\\\\').replace('"', '\\"').replace('`', '\\`').replace('$', '\\$').replace('%', '%%')
        entry = ('[Desktop Entry]\nType=Application\nName=After Hours music widget\nComment=Now playing and system audio spectrum\nExec=python3 "' + quoted + '"\nTerminal=false\nOnlyShowIn=COSMIC;\n')
        write(home / '.config/autostart/dotfiles-music-widget.desktop', entry.encode())
        print('Music widget installed; autostart enabled for COSMIC.')
        if start:
            state.mkdir(parents=True, exist_ok=True)
            with (state / 'music-widget.log').open('ab') as log:
                subprocess.run([sys.executable, executable, '--quit'], stdout=log, stderr=log, timeout=5, check=False)
                subprocess.Popen([sys.executable, executable], stdout=log, stderr=log, start_new_session=True)
            print('Widget launched. Diagnostics: ' + str(state / 'music-widget.log'))
    print('Replaced files preserved in: ' + str(backup))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('component', choices=('wallpaper', 'widgets', 'both'), default='both', nargs='?')
    parser.add_argument('--apply', action='store_true')
    parser.add_argument('--no-start', action='store_true', help='install widget for next login without launching now')
    args = parser.parse_args()
    if args.apply:
        if os.geteuid() == 0:
            raise SystemExit('Run as your normal desktop user, without sudo.')
        apply(args.component, start=not args.no_start)
    else:
        print(f'Preview: install {args.component} only. Run again with --apply to change your desktop.')
        if args.component in ('widgets', 'both'):
            try:
                dependencies()
                print('Widget dependencies available.')
            except (ImportError, ValueError, RuntimeError) as e:
                print(f'Missing widget dependency: {e}')
                print('Void: sudo xbps-install gtk-layer-shell cava python3-gobject python3-cairo')
