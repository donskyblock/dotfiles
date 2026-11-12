#!/usr/bin/env python3
"""Prepare or install the self-contained Tokyo Night SDDM theme."""
import argparse
import configparser
from datetime import datetime
import json
import os
from pathlib import Path
import re
import shutil
import tempfile

BASE = Path(__file__).resolve().parent
REPO = BASE.parent
NAME = 'tokyo-night'
DEST = Path('/usr/share/sddm/themes') / NAME
DROPIN = Path('/etc/sddm.conf.d/90-tokyo-night.conf')
LEGACY = Path('/etc/sddm.conf')
BACKUPS = Path('/var/lib/dotfiles/sddm-backups')
SOURCES = ('Main.qml', 'ThemeButton.qml', 'metadata.desktop', 'theme.conf', 'LICENSE',
           'background.png', 'WALLPAPER-LICENSE.txt', 'WALLPAPER.md')


def prepare(destination):
    """Build without root. Never depend on access to a user's home at login."""
    destination.mkdir(parents=True, exist_ok=True)
    for name in SOURCES:
        shutil.copyfile(BASE / NAME / name, destination / name)
        (destination / name).chmod(0o644)
    destination.chmod(0o755)
    return destination


def patched_legacy(text):
    """Legacy config has precedence over drop-ins: align only theme selectors."""
    section = ''
    out = []
    for line in text.splitlines(keepends=True):
        match = re.match(r'\s*\[([^]]+)\]', line)
        if match:
            section = match[1].lower()
        key = re.match(r'\s*(Current|ThemeDir)\s*=', line, flags=re.I)
        if section == 'theme' and key:
            line = ('Current=tokyo-night\n' if key[1].lower() == 'current' else 'ThemeDir=/usr/share/sddm/themes\n')
        out.append(line)
    return ''.join(out)


def verify_theme(path):
    for name in (*SOURCES, 'background.png'):
        item = path / name
        if not item.is_file() or item.is_symlink() or not item.stat().st_size:
            raise RuntimeError(f'Invalid theme file: {name}')
    metadata = configparser.ConfigParser()
    metadata.read(path / 'metadata.desktop')
    assert metadata['SddmGreeterTheme']['QtVersion'] == '6'
    assert (path / 'background.png').read_bytes().startswith(b'\x89PNG\r\n\x1a\n')


def atomic_text(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temporary = tempfile.mkstemp(prefix='.tokyo-night-', dir=path.parent)
    try:
        with os.fdopen(fd, 'w') as stream:
            stream.write(text)
        os.chmod(temporary, 0o644)
        os.replace(temporary, path)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


def rollback(backup):
    backup = backup.resolve()
    if backup.parent != BACKUPS.resolve():
        raise SystemExit('Rollback path must be a timestamped directory under ' + str(BACKUPS))
    state = json.loads((backup / 'state.json').read_text())
    for path, key in ((DROPIN, 'dropin'), (LEGACY, 'legacy')):
        if state[key]:
            shutil.copy2(backup / key, path)
        elif key == 'dropin' and path.exists():
            path.unlink()
    if DEST.is_symlink():
        DEST.unlink()
    elif DEST.exists():
        shutil.rmtree(DEST)
    if state['theme']:
        saved = backup / 'theme'
        if saved.is_symlink():
            DEST.symlink_to(os.readlink(saved))
        else:
            shutil.copytree(saved, DEST)
    print('Previous theme and configuration restored. Your running session was not restarted.')


def install():
    if not shutil.which('sddm-greeter-qt6'):
        raise SystemExit('The sddm-greeter-qt6 executable is required.')
    # This performs no package, PAM, login-session, or service changes.
    with tempfile.TemporaryDirectory(prefix='tokyo-night-sddm-') as temporary:
        build = prepare(Path(temporary) / NAME)
        verify_theme(build)
        backup = BACKUPS / datetime.now().strftime('%Y%m%d-%H%M%S-%f')
        backup.mkdir(parents=True, mode=0o700)
        state = {'dropin': DROPIN.exists(), 'legacy': LEGACY.exists(), 'theme': os.path.lexists(DEST)}
        for path, key in ((DROPIN, 'dropin'), (LEGACY, 'legacy')):
            if state[key]:
                shutil.copy2(path, backup / key)
        if state['theme']:
            if DEST.is_symlink():
                (backup / 'theme').symlink_to(os.readlink(DEST))
            else:
                shutil.copytree(DEST, backup / 'theme')
        (backup / 'state.json').write_text(json.dumps(state, indent=2) + '\n')
        try:
            DEST.parent.mkdir(parents=True, exist_ok=True)
            staging = Path(tempfile.mkdtemp(prefix='.tokyo-night-', dir=DEST.parent))
            try:
                for source in build.iterdir():
                    shutil.copyfile(source, staging / source.name)
                    (staging / source.name).chmod(0o644)
                staging.chmod(0o755)
                if DEST.is_symlink():
                    DEST.unlink()
                elif DEST.exists():
                    shutil.rmtree(DEST)
                os.replace(staging, DEST)
            finally:
                if staging.exists():
                    shutil.rmtree(staging)
            atomic_text(DROPIN, '[Theme]\nCurrent=tokyo-night\nThemeDir=/usr/share/sddm/themes\n')
            if state['legacy']:
                original = LEGACY.read_text()
                changed = patched_legacy(original)
                if changed != original:
                    atomic_text(LEGACY, changed)
            verify_theme(DEST)
        except Exception:
            rollback(backup)
            raise
        print('Tokyo Night selected for the next SDDM login screen.')
        print('No restart performed; your current desktop session stays open.')
        print('Backup: ' + str(backup))
        print('Rollback: sudo python3 ' + str(BASE / 'install.py') + ' --rollback ' + str(backup))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group()
    group.add_argument('--apply', action='store_true', help='install and select the theme; requires root')
    group.add_argument('--rollback', type=Path, help='restore a backup created by this installer; requires root')
    parser.add_argument('--output', type=Path, help='prepare at this path instead of the default local state directory')
    args = parser.parse_args()
    if args.apply or args.rollback:
        if os.geteuid() != 0:
            raise SystemExit('System installation requires root. Run: sudo python3 ' + str(BASE / 'install.py') + ' --apply')
        rollback(args.rollback) if args.rollback else install()
    else:
        output = args.output or Path.home() / '.local/state/dotfiles/sddm/tokyo-night'
        prepare(output)
        verify_theme(output)
        print('Prepared and verified: ' + str(output))
        print('Preview: sddm-greeter-qt6 --test-mode --theme ' + str(output))
        print('Apply: sudo python3 ' + str(BASE / 'install.py') + ' --apply')
