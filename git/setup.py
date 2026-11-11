#!/usr/bin/env python3
"""Create passphrase-protected SSH/GPG keys and private Git identity settings."""
import argparse
from datetime import datetime
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile


def run(*args, **kwargs):
    return subprocess.run(args, check=True, **kwargs)


def private_directory(path):
    if path.is_symlink():
        raise SystemExit(f'Refusing symlinked private directory: {path}')
    path.mkdir(parents=True, exist_ok=True, mode=0o700)
    path.chmod(0o700)


def backup(path, destination):
    if path.exists() or path.is_symlink():
        shutil.copy2(path, destination, follow_symlinks=False)


def read_identity(value, label):
    value = value or input(label).strip()
    if not value or any(c in value for c in '\r\n\0<>'):
        raise SystemExit('Use a non-empty name/email without angle brackets or control characters.')
    return value


def fingerprint(output, kind):
    for line in output.splitlines():
        match = re.fullmatch(r'\[GNUPG:\] KEY_CREATED ([BPS]) ([A-F0-9]{40,64})', line)
        if match and match[1] in kind:
            return match[2]
    raise SystemExit('Could not identify the new GPG key. Check gpg --list-secret-keys before retrying.')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--name')
    parser.add_argument('--email')
    args = parser.parse_args()
    if not sys.stdin.isatty():
        raise SystemExit('Run this in your terminal: passphrases must be entered locally, never in chat.')
    for program in ('git', 'gpg', 'gpgconf', 'ssh-keygen'):
        if not shutil.which(program):
            raise SystemExit('Missing program: ' + program)
    os.umask(0o077)
    home = Path.home()
    configured_name = subprocess.run(['git', 'config', '--global', '--includes', '--get', 'user.name'], capture_output=True, text=True).stdout.strip()
    configured_email = subprocess.run(['git', 'config', '--global', '--includes', '--get', 'user.email'], capture_output=True, text=True).stdout.strip()
    name = read_identity(args.name or configured_name, 'Git display name: ')
    email = read_identity(args.email or configured_email, 'Git email (your verified GitHub email or exact noreply address): ')
    if not re.fullmatch(r'[^\s@]+@[^\s@]+\.[^\s@]+', email):
        raise SystemExit('Please enter a valid email address.')
    stamp = datetime.now().strftime('%Y%m%d-%H%M%S-%f')
    ssh = home / '.ssh'
    gpg = home / '.gnupg'
    state = home / '.local/state/git-keys' / stamp
    for directory in (ssh, gpg, state):
        private_directory(directory)
    pinentry = shutil.which('pinentry-gnome3')
    if not pinentry or not shutil.which('gnome-keyring-daemon'):
        raise SystemExit('Install desktop keyring support first: sudo xbps-install -S gnome-keyring pinentry-gnome seahorse gcr')
    askpass = home / '.local/bin/dotfiles-ssh-askpass'
    if not askpass.is_file():
        raise SystemExit('Run the dotfiles installer before generating keys.')
    environment = dict(os.environ, GNUPGHOME=str(gpg), GPG_TTY=os.ttyname(sys.stdin.fileno()), SSH_ASKPASS=str(askpass), SSH_ASKPASS_REQUIRE='force')
    run(str(home / '.local/bin/dotfiles-keyring-session'), env=environment)
    if not os.environ.get('XDG_RUNTIME_DIR'):
        raise SystemExit('Run setup in your desktop session, where XDG_RUNTIME_DIR is set.')
    keyring_socket = Path(os.environ['XDG_RUNTIME_DIR']) / 'keyring/ssh'
    if not keyring_socket.is_socket():
        raise SystemExit('Desktop keyring SSH agent is not ready. Log out and back in, then retry.')
    environment['SSH_AUTH_SOCK'] = str(keyring_socket)
    agent_config = gpg / 'gpg-agent.conf'
    if agent_config.is_symlink():
        raise SystemExit('Refusing to replace a symlinked private GPG agent config.')
    backup(agent_config, state / 'previous-gpg-agent.conf')
    current = agent_config.read_text() if agent_config.exists() else ''
    current = re.sub(r'(?m)^\s*(pinentry-program|no-allow-external-cache)\b[^\n]*\n?', '', current)
    agent_config.write_text(current.rstrip() + '\npinentry-program ' + pinentry + '\n')
    agent_config.chmod(0o600)
    run('gpgconf', '--reload', 'gpg-agent', env=environment)
    print('SSH key passphrase dialogs will open on your desktop. Use a non-empty passphrase.')
    key = ssh / ('id_ed25519_github_' + stamp)
    run('ssh-keygen', '-t', 'ed25519', '-a', '100', '-C', email, '-f', str(key), env=environment)
    print('GPG will now use the desktop Pinentry and keyring as well.')
    uid = name + ' <' + email + '>'
    created = run('gpg', '--status-fd', '1', '--quick-generate-key', uid, 'ed25519', 'cert', '2y', env=environment, stdout=subprocess.PIPE, text=True)
    primary = fingerprint(created.stdout, 'BP')
    (state / 'primary-fingerprint.txt').write_text(primary + '\n')
    created = run('gpg', '--status-fd', '1', '--quick-add-key', primary, 'ed25519', 'sign', '1y', env=environment, stdout=subprocess.PIPE, text=True)
    signing = fingerprint(created.stdout, 'S')
    (state / 'signing-fingerprint.txt').write_text(signing + '\n')
    public = state / 'github-gpg-public.asc'
    with public.open('w') as stream:
        run('gpg', '--armor', '--export', primary, env=environment, stdout=stream)
    shutil.copyfile(key.with_suffix('.pub'), state / 'github-ssh-public.pub')
    # Prove signing works before enabling it globally.
    sample = state / 'signing-check.txt'
    sample.write_text('Local Git signing verification.\n')
    run('gpg', '--local-user', signing + '!', '--armor', '--detach-sign', str(sample), env=environment)
    run('gpg', '--verify', str(sample) + '.asc', str(sample), env=environment)

    gitdir = home / '.config/git'
    gitdir.mkdir(parents=True, exist_ok=True)
    local = gitdir / 'local.conf'
    if local.is_symlink():
        raise SystemExit('Refusing a symlinked private Git config: ' + str(local))
    backup(local, state / 'previous-git-local.conf')
    values = {'user.name': name, 'user.email': email, 'user.signingkey': signing + '!', 'gpg.format': 'openpgp', 'gpg.program': 'gpg', 'commit.gpgsign': 'true', 'tag.gpgsign': 'true'}
    for setting, value in values.items():
        run('git', 'config', '--file', str(local), setting, value)
    local.chmod(0o600)
    # A private include in ~/.gitconfig also handles existing global config files
    # whose identity values override the XDG defaults.
    global_config = home / '.gitconfig'
    if global_config.is_symlink():
        raise SystemExit('Refusing to write identity settings through a global config symlink. Add the private include manually.')
    backup(global_config, state / 'previous-gitconfig')
    includes = subprocess.run(['git', 'config', '--file', str(global_config), '--get-all', 'include.path'], capture_output=True, text=True)
    if str(local) not in includes.stdout.splitlines():
        run('git', 'config', '--file', str(global_config), '--add', 'include.path', str(local))
    global_config.chmod(0o600)

    sshconfig = ssh / 'config'
    if sshconfig.is_symlink():
        raise SystemExit('Refusing to write private SSH settings through a symlink.')
    backup(sshconfig, state / 'previous-ssh-config')
    original = sshconfig.read_text() if sshconfig.exists() else ''
    original = re.sub(r'(?ms)^# BEGIN DOTFILES GITHUB\n.*?^# END DOTFILES GITHUB\n?', '', original)
    block = '# BEGIN DOTFILES GITHUB\nHost github.com\n    HostName github.com\n    User git\n    IdentityFile ' + str(key) + '\n    IdentityAgent ' + str(keyring_socket) + '\n    IdentitiesOnly yes\n    AddKeysToAgent no\n# END DOTFILES GITHUB\n'
    sshconfig.write_text(block + '\n' + original)
    sshconfig.chmod(0o600)
    # Ask the desktop keyring to unlock the new SSH key on demand; it recognizes
    # the public key beside the private key. Keyring persistence is chosen in its dialog.
    # End-to-end test: sign and verify a disposable Git commit using the
    # configured identity. The verification repository is removed afterward.
    with tempfile.TemporaryDirectory(prefix='git-signing-check-', dir=state) as temporary:
        run('git', 'init', '--quiet', temporary, env=environment)
        run('git', '-C', temporary, 'commit', '--quiet', '--allow-empty', '-m', 'Verify local signing', env=environment)
        run('git', '-C', temporary, 'verify-commit', 'HEAD', env=environment)
    print('\nKeys generated and signing verified. Existing keys were preserved.')
    print('SSH private key: ' + str(key))
    print('Public SSH key to add on GitHub: ' + str(state / 'github-ssh-public.pub'))
    print('Public GPG key to add on GitHub: ' + str(public))
    print('Primary fingerprint: ' + primary)
    print('Signing subkey fingerprint: ' + signing)
    print('GPG revocation certificate: ' + str(gpg / 'openpgp-revocs.d' / (primary + '.rev')))
    print('Private backups and public exports: ' + str(state))
    print('Add the two PUBLIC keys at https://github.com/settings/keys')
    print('Then test SSH from your terminal with: ssh -T git@github.com')
    print('Old GitHub keys remain valid until you remove them from GitHub.')


if __name__ == '__main__':
    main()
