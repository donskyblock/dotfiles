#!/usr/bin/env python3
"""Check the Git index without printing potentially sensitive contents."""
import hashlib
import re
import subprocess
from pathlib import Path
repo = Path(__file__).resolve().parent
allowed = {'.gitignore', 'README.md', 'CONTRIBUTING.md', 'KEYBINDS.md', 'install.py', 'check-public.py', 'manifest.txt', 'hooks/pre-commit', 'rice.py', 'WALLPAPERS.md'}

allowed.update({'sddm/tokyo-night/LICENSE', 'sddm/README.md', 'sddm/install.py', 'sddm/tests/Preview.qml', 'sddm/tests/check_install.py', 'sddm/tokyo-night/Main.qml', 'sddm/tokyo-night/metadata.desktop', 'sddm/tokyo-night/theme.conf', 'sddm/tokyo-night/ThemeButton.qml'})

allowed.update({'install.sh', 'sddm/tokyo-night/background.png',
                'sddm/tokyo-night/WALLPAPER.md', 'sddm/tokyo-night/WALLPAPER-LICENSE.txt'})

allowed.update({'git/setup.py', 'git/README.md'})

allowed.update({'cursor/apply.py', 'cursor/README.md'})

allowed.update({'discord/setup.py', 'discord/README.md', 'discord/discord-native.desktop.in', 'discord/theme.py'})

allowed.update({'desktop/settings.json', 'desktop/style.css', 'desktop/widget.py', 'desktop/cava.conf', 'desktop/WALLPAPER-LICENSE.txt', 'desktop/README.md', 'desktop/neon-sign.jpg', 'desktop/install.py'})

allowed.update({'companions/dms/tokyo-night.json', 'companions/mango/config.conf', 'companions/hypr/hyprland.conf', 'companions/hypr/hyprland.lua', 'companions/quickshell/shell.qml', 'companions/niri/config.kdl', 'companions/after-hours-shell', 'companions/install.py'})

allowed.update({'companions/README.md', 'companions/check_install.py'})

def git(*args):
    return subprocess.check_output(['git', '-C', str(repo), *args])
# Read the allowlist from the index too: checking a commit must not trust
# an unstaged manifest that differs from what is about to be published.
allowed.update('home/' + n for n in git('show', ':manifest.txt').decode().splitlines())
private_path = re.compile(r'(?:^|/)(?:\.ssh|\.aws|\.codex|\.env(?:\..*)?|\.bash_history|mozilla|pulse|credentials|cookies\.sqlite|key4\.db|logins\.json)(?:/|$)')
patterns = [
    rb'-----BEGIN (?:[A-Z0-9]+ )*PRIVATE KEY-----',
    rb'(?:gh[pousr]_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,})',
    rb'(?:AKIA|ASIA)[A-Z0-9]{16}',
    rb'sk-[A-Za-z0-9_-]{20,}',
    rb'(?i)(?:password|passwd|api[_-]?key|access[_-]?token|client[_-]?secret)\s*[=:]\s*[\x22\x27]?[A-Za-z0-9_+/=-]{8,}',
]
failed = False
for raw in git('ls-files', '--stage', '-z').split(b'\0'):
    if not raw:
        continue
    meta, encoded = raw.split(b'\t', 1)
    name = encoded.decode()
    mode, oid, stage = meta.split()
    if name not in allowed or private_path.search(name) or mode not in (b'100644', b'100755') or stage != b'0':
        print(f'Unapproved path or file type: {name}')
        failed = True
        continue
    data = git('cat-file', 'blob', oid.decode())
    # Only the reviewed upstream wallpaper is allowed as a binary asset.
    wallpaper_hashes = {
        'sddm/tokyo-night/background.png': '7b6a84b47d3d5ab837bc1c658cf987dc5342f71ec8ba09c059270ec2cc0d499c',
        'desktop/neon-sign.jpg': '1547c5ab67b9a778ced36fc1389eb93f3f24dedbe08e9db2ec9b587237f4982f',
    }
    if name in wallpaper_hashes:
        if hashlib.sha256(data).hexdigest() != wallpaper_hashes[name]:
            print('Wallpaper differs from the reviewed upstream asset.')
            failed = True
        continue
    if b'\0' in data or any(re.search(p, data) for p in patterns):
        print(f'Potential sensitive content: {name}')
        failed = True
if failed:
    raise SystemExit(1)
print('Staged public files passed the allowlist and secret-pattern checks.')
