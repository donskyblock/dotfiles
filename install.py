#!/usr/bin/env python3
"""Link reviewed files into HOME; preserve existing files outside the repository."""
import argparse
import os
from pathlib import Path
import shutil
import subprocess
from datetime import datetime

repo = Path(__file__).resolve().parent
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--apply', action='store_true', help='create links (default: preview)')
args = parser.parse_args()
home = Path.home()
backup = home / '.local/state/dotfiles/backups' / datetime.now().strftime('%Y%m%d-%H%M%S-%f')
entries = []
for name in (repo / 'manifest.txt').read_text().splitlines():
    rel = Path(name)
    if rel.is_absolute() or '..' in rel.parts or not name.startswith('.'):
        raise SystemExit(f'Unsafe manifest entry: {name}')
    source, target = repo / 'home' / rel, home / rel
    if not source.is_file() or source.is_symlink():
        raise SystemExit(f'Missing or unsafe source: {name}')
    already_linked = target.is_symlink() and target.resolve() == source
    if target.is_dir() and not target.is_symlink():
        raise SystemExit(f'Refusing to replace directory: {target}')
    # Do not follow a parent symlink into another configuration tree.
    if any(p.is_symlink() for p in target.parents if p != home and home in p.parents):
        raise SystemExit(f'Refusing symlinked parent: {target}')
    entries.append((source, target, rel, already_linked))
if args.apply:
    # Verify wallpaper rendering dependencies before changing any links.
    import gi
    gi.require_version('GdkPixbuf', '2.0')
    from gi.repository import GdkPixbuf
for source, target, rel, already_linked in entries:
    if already_linked:
        if args.apply:
            # Refresh atomically so directory watchers notice edits through links.
            temporary = target.with_name(target.name + '.dotfiles-link')
            if os.path.lexists(temporary):
                raise SystemExit(f'Temporary link already exists: {temporary}')
            temporary.symlink_to(os.path.relpath(source, target.parent))
            os.replace(temporary, target)
        continue
    print(f'{target} -> {source}')
    if args.apply:
        target.parent.mkdir(parents=True, exist_ok=True)
        if os.path.lexists(target):
            saved = backup / rel
            saved.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(target), str(saved))
        target.symlink_to(os.path.relpath(source, target.parent))
if args.apply:
    subprocess.run(['git', '-C', str(repo), 'config', '--local', 'core.hooksPath', 'hooks'], check=True)
    subprocess.run(['python3', str(repo / 'rice.py'), '--apply'], check=True)
    subprocess.run(['python3', str(repo / 'cursor/apply.py')], check=True)
    print(f'Done. Any replaced originals are in {backup}')
else:
    print('Preview only. Run with --apply to install.')
