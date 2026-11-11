#!/usr/bin/env python3
"""Install a user-owned native Discord and patch it with a local Equicord build."""
import argparse
from datetime import datetime
import json
import os
from pathlib import Path
import shutil
import subprocess
import tarfile
import tempfile
import urllib.request

REPO = Path(__file__).resolve().parent.parent
HOME = Path.home()
TARGET = HOME / '.local/opt/discord'
STATE = HOME / '.local/state/dotfiles/discord'
FLATPAK = Path('/var/lib/flatpak/app/com.discordapp.Discord/current/active/files/discord')
URL = 'https://discord.com/api/download?platform=linux&format=tar.gz'


def adapt_bundle(target):
    # The cached Flatpak application payload has two paths that are only valid
    # inside its sandbox. Official tarball installs do not need these fixes.
    info = target / 'resources/build_info.json'
    if info.exists():
        data = json.loads(info.read_text())
        if data.get('localModulesRoot', '').startswith('/app/'):
            data['localModulesRoot'] = str(TARGET / 'modules')
            info.write_text(json.dumps(data, indent=2) + '\n')
    for path in target.rglob('*'):
        if not path.is_symlink():
            continue
        original = os.readlink(path)
        if original.startswith('/var/data/mediapipe_models/'):
            model = target / 'mediapipe_models' / Path(original).name
            if not model.is_file():
                raise SystemExit('Required cached model is missing: ' + model.name)
            path.unlink()
            path.symlink_to(os.path.relpath(model, path.parent))


def launcher():
    applications = HOME / '.local/share/applications'
    applications.mkdir(parents=True, exist_ok=True)
    text = (REPO / 'discord/discord-native.desktop.in').read_text()
    escaped_home = str(HOME).replace('\\', '\\\\').replace('"', '\\"').replace('`', '\\`').replace('$', '\\$')
    (applications / 'discord-native.desktop').write_text(text.replace('@HOME@', escaped_home))
    icon = HOME / '.local/share/icons/hicolor/256x256/apps/discord-native.png'
    icon.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(TARGET / 'discord.png', icon)
    if shutil.which('update-desktop-database'):
        subprocess.run(['update-desktop-database', str(applications)], check=True)


def install(from_flatpak, source):
    if os.geteuid() == 0:
        raise SystemExit('Run as your normal user, without sudo.')
    source = source.expanduser().resolve()
    original_installer = source / 'dist/Installer/EquilotlCli-Linux'
    if not original_installer.is_file() or not (source / 'dist/desktop/patcher.js').is_file():
        raise SystemExit('The Equicord checkout needs its built dist/desktop and downloaded dist/Installer/EquilotlCli-Linux first.')
    TARGET.parent.mkdir(parents=True, exist_ok=True)
    STATE.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='.native-discord-', dir=TARGET.parent) as temporary:
        work = Path(temporary)
        if from_flatpak:
            if not (FLATPAK / 'Discord').is_file():
                raise SystemExit('No system Flatpak Discord application payload was found.')
            staged = work / 'Discord'
            shutil.copytree(FLATPAK, staged, symlinks=True)
            origin = str(FLATPAK)
        else:
            archive = work / 'discord.tar.gz'
            request = urllib.request.Request(URL, headers={'User-Agent': 'dotfiles-native-discord'})
            with urllib.request.urlopen(request, timeout=60) as response, archive.open('wb') as output:
                shutil.copyfileobj(response, output)
            with tarfile.open(archive, 'r:gz') as package:
                package.extractall(work / 'unpacked', filter='data')
            candidates = [p for p in (work / 'unpacked').iterdir() if p.is_dir() and (p / 'Discord').exists()]
            if len(candidates) != 1:
                raise SystemExit('The official archive does not contain the expected Discord application.')
            staged = candidates[0]
            origin = URL
        adapt_bundle(staged)
        dependencies = subprocess.run(['ldd', str(staged / 'Discord')], capture_output=True, text=True, check=True)
        missing = [line.strip() for line in dependencies.stdout.splitlines() if 'not found' in line]
        if missing:
            raise SystemExit('Missing system libraries:\n' + '\n'.join(missing))
        backup = None
        if os.path.lexists(TARGET):
            if TARGET.is_symlink():
                raise SystemExit('Refusing to replace a symlinked native application directory.')
            backup = STATE / ('backup-' + datetime.now().strftime('%Y%m%d-%H%M%S-%f'))
            shutil.move(str(TARGET), backup)
        try:
            shutil.move(str(staged), TARGET)
            shutil.copy2(original_installer, STATE / 'EquilotlCli-Linux')
            (STATE / 'EquilotlCli-Linux').chmod(0o755)
            env = dict(os.environ, EQUICORD_DEV_INSTALL='1', EQUICORD_DIRECTORY=str(source / 'dist/desktop'), EQUICORD_USER_DATA_DIR=str(HOME / '.config/Equicord'))
            subprocess.run([str(STATE / 'EquilotlCli-Linux'), '--install', '--location', str(TARGET)], env=env, check=True)
            launcher()
            (STATE / 'equicord-source.json').write_text(json.dumps({'path': str(source)}, indent=2) + '\n')
            (STATE / 'native-source.json').write_text(json.dumps({'source': origin, 'native_directory': str(TARGET)}, indent=2) + '\n')
        except BaseException:
            if TARGET.exists():
                shutil.rmtree(TARGET)
            if backup:
                shutil.move(str(backup), TARGET)
            raise
    print('Native Discord installed and Equicord patched: ' + str(TARGET))
    print('Launch Discord (Native) from Applications, or run: discord')
    print('The Flatpak and its profile were preserved. Log into native Discord separately.')
    if backup:
        print('Previous native application backup: ' + str(backup))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--from-flatpak', action='store_true', help='use the already installed application payload instead of downloading')
    parser.add_argument('--equicord-source', type=Path, help='path to your built Equicord checkout')
    args = parser.parse_args()
    source = args.equicord_source
    if source is None:
        saved = STATE / 'equicord-source.json'
        if not saved.exists():
            raise SystemExit('Specify --equicord-source /path/to/Equicord the first time.')
        source = Path(json.loads(saved.read_text())['path'])
    install(args.from_flatpak, source)
