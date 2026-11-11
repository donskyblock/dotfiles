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
    if target.is_symlink() and target.resolve() == source:
        continue
    if target.is_dir() and not target.is_symlink():
        raise SystemExit(f'Refusing to replace directory: {target}')
    # Do not follow a parent symlink into another configuration tree.
    if any(p.is_symlink() for p in target.parents if p != home and home in p.parents):
        raise SystemExit(f'Refusing symlinked parent: {target}')
    entries.append((source, target, rel))
for source, target, rel in entries:
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
    print(f'Done. Any replaced originals are in {backup}')
else:
    print('Preview only. Run with --apply to install.')
