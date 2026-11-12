#!/usr/bin/env python3
"""Install selectable companion desktops; default is a read-only preview."""
import argparse
from datetime import datetime
import json
import os
from pathlib import Path
import shutil
import tempfile

BASE = Path(__file__).resolve().parent
REPO = BASE.parent

def plan(component, shell, home, legacy=False):
    files = {
        '.local/bin/after-hours-shell': (BASE / 'after-hours-shell').read_bytes(),
        '.config/after-hours/shell': (shell + '\n').encode(),
        '.local/share/wallpapers/after-hours.jpg': (REPO / 'desktop/neon-sign.jpg').read_bytes(),
    }
    targets = ('hyprland', 'niri', 'mango') if component == 'companions' else (component,)
    for name in targets:
        source, target = {
            'hyprland': ('hypr/hyprland.conf' if legacy else 'hypr/hyprland.lua',
                         '.config/hypr/hyprland.conf' if legacy else '.config/hypr/hyprland.lua'),
            'niri': ('niri/config.kdl', '.config/niri/config.kdl'),
            'mango': ('mango/config.conf', '.config/mango/config.conf'),
        }.get(name, (None, None))
        if source:
            files[target] = (BASE / source).read_bytes()
    if shell == 'quickshell' or component == 'companions':
        files['.config/quickshell/after-hours/shell.qml'] = (BASE / 'quickshell/shell.qml').read_bytes()
    if shell == 'dms' or component == 'companions':
        theme = '.config/DankMaterialShell/themes/after-hours.json'
        files[theme] = (BASE / 'dms/tokyo-night.json').read_bytes()
        settings = home / '.config/DankMaterialShell/settings.json'
        data = json.loads(settings.read_text()) if settings.exists() else {}
        if not isinstance(data, dict):
            raise ValueError('DMS settings must be a JSON object')
        data.update(currentThemeName='custom', customThemeFile=str(home / theme))
        files['.config/DankMaterialShell/settings.json'] = (json.dumps(data, indent=2) + '\n').encode()
    # Preflight every destination before changing anything.
    for rel in files:
        target = home / rel
        if any(p.is_symlink() for p in target.parents if p != home and home in p.parents):
            raise ValueError(f'Refusing symlinked parent: {target}')
        if target.is_dir() and not target.is_symlink():
            raise ValueError(f'Refusing directory: {target}')
    return files

def install(files, home):
    backup = home / '.local/state/dotfiles/backups' / ('companions-' + datetime.now().strftime('%Y%m%d-%H%M%S-%f'))
    for rel, data in files.items():
        target = home / rel
        mode = 0o755 if rel == '.local/bin/after-hours-shell' else 0o644
        if not target.is_symlink() and target.is_file() and target.read_bytes() == data and target.stat().st_mode & 0o777 == mode:
            continue
        if os.path.lexists(target):
            saved = backup / rel
            saved.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(target, saved, follow_symlinks=False)
            if target.is_symlink() and target.is_file():
                saved.with_name(saved.name + '.contents').write_bytes(target.read_bytes())
        target.parent.mkdir(parents=True, exist_ok=True)
        fd, temporary = tempfile.mkstemp(prefix='.after-hours-', dir=target.parent)
        try:
            with os.fdopen(fd, 'wb') as stream:
                stream.write(data)
            os.chmod(temporary, mode)
            os.replace(temporary, target)
        finally:
            if os.path.exists(temporary):
                os.unlink(temporary)
    print(f'Installed. Replaced files preserved in {backup}')

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('component', choices=['hyprland', 'niri', 'mango', 'quickshell', 'dms', 'companions'])
    parser.add_argument('--shell', choices=['quickshell', 'dms'])
    parser.add_argument('--legacy-hyprland', action='store_true', help='install the pre-Lua .conf instead of .lua')
    parser.add_argument('--apply', action='store_true')
    args = parser.parse_args()
    home = Path.home()
    selected = args.shell or ('dms' if args.component == 'dms' else 'quickshell')
    if args.component in ('quickshell', 'dms') and selected != args.component:
        parser.error('shell component and --shell must agree')
    files = plan(args.component, selected, home, args.legacy_hyprland)
    for rel in files:
        print(home / rel)
    if args.apply:
        install(files, home)
    else:
        print('Preview only. Add --apply to install. Log into the desired compositor afterward.')

if __name__ == '__main__':
    main()
