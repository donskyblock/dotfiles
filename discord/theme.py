#!/usr/bin/env python3
"""Load the local Tokyo Night theme through Equicord's live QuickCSS watcher."""
import argparse
from datetime import datetime
import json
import os
from pathlib import Path
import re
import shutil

REPO = Path(__file__).resolve().parent.parent
THEME = 'tokyo-night.theme.css'
BEGIN = '/* BEGIN DOTFILES TOKYO NIGHT */'
END = '/* END DOTFILES TOKYO NIGHT */'


def apply(home):
    base = home / '.config/Equicord'
    themes = base / 'themes'
    themes.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now().strftime('%Y%m%d-%H%M%S-%f')
    backup = home / '.local/state/dotfiles/backups' / ('equicord-theme-' + stamp)
    def preserve(path):
        backup.mkdir(parents=True, exist_ok=True, mode=0o700)
        backup.chmod(0o700)
        shutil.copy2(path, backup / path.name, follow_symlinks=False)
    # The main dotfiles installer owns the CSS symlink. The wallpaper stays a
    # single shared source used by the desktop and other applications too.
    for target, source in [
        (themes / THEME, REPO / 'home/.config/Equicord/themes' / THEME),
        (themes / 'nightfall.svg', REPO / 'home/.local/share/wallpapers/tokyo-night.svg'),
    ]:
        if target.is_symlink() and target.resolve() == source:
            continue
        if os.path.lexists(target):
            if target.is_dir():
                raise SystemExit('Refusing to replace theme directory: ' + str(target))
            preserve(target)
            target.unlink()
        target.symlink_to(os.path.relpath(source, target.parent))
    quick = base / 'settings/quickCss.css'
    quick.parent.mkdir(parents=True, exist_ok=True)
    if quick.is_symlink():
        raise SystemExit('QuickCSS is already symlinked; refusing to write through it.')
    original = quick.read_text() if quick.exists() else ''
    clean = re.sub(re.escape(BEGIN) + r'.*?' + re.escape(END) + r'\n?', '', original, flags=re.S)
    block = BEGIN + '\n@import url("vencord:///themes/' + THEME + '");\n' + END + '\n'
    # @import must precede ordinary CSS. Keep a user's charset declaration first.
    charset = re.match(r'\s*@charset\s+["\'][^"\']+["\'];\s*', clean)
    if charset:
        updated = clean[:charset.end()] + block + clean[charset.end():]
    else:
        updated = block + clean
    if updated != original:
        if quick.exists():
            preserve(quick)
        # Keep the inode: Equicord watches this file directly with fs.watch.
        quick.write_text(updated)
    settings = base / 'settings/settings.json'
    enabled = True
    if settings.exists():
        enabled = json.loads(settings.read_text()).get('useQuickCss', True)
    print('Nightfall theme installed; QuickCSS import is ready' + (' and enabled.' if enabled else '. Enable QuickCSS in Equicord settings.'))
    print('Private Equicord settings and existing QuickCSS were preserved.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--apply', action='store_true')
    args = parser.parse_args()
    if args.apply:
        apply(Path.home())
    else:
        print('Run python3 discord/theme.py --apply to install the theme and live QuickCSS import.')
