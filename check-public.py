#!/usr/bin/env python3
"""Check the Git index without printing potentially sensitive contents."""
import re
import subprocess
from pathlib import Path
repo = Path(__file__).resolve().parent
allowed = {'.gitignore', 'README.md', 'install.py', 'check-public.py', 'manifest.txt', 'hooks/pre-commit', 'rice.py', 'WALLPAPERS.md'}

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
    if b'\0' in data or any(re.search(p, data) for p in patterns):
        print(f'Potential sensitive content: {name}')
        failed = True
if failed:
    raise SystemExit(1)
print('Staged public files passed the allowlist and secret-pattern checks.')
