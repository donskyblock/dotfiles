# Git identity, SSH authentication, and GPG signing

Public Git defaults live in `home/.config/git/config`. Your name, email,
key selection, private keys, and backups stay outside the repository.

## Generate keys on a new installation

Install the desktop keyring and graphical prompt on Void first:

```sh
sudo xbps-install -S gnome-keyring pinentry-gnome seahorse gcr
```

Then, after installing the dotfiles, run in your own terminal:

```sh
python3 ~/dotfiles/git/setup.py
```

The script asks for your Git name and email. Use an email verified on GitHub,
or your exact noreply address from GitHub → Settings → Emails. Your commit
identity and GPG public key contain these details, so choose them deliberately.

SSH and GPG then ask for passphrases using graphical GNOME Pinentry dialogs.
Do not enter passphrases in chat. Neither the script nor Git receives your
passphrases as command-line arguments, environment variables, or plaintext files.
Use non-empty passphrases at both prompts. Choose the remember/save option when
the keyring offers it. GNOME Keyring encrypts its persistent storage; use your
login password for the login keyring to allow SDDM/PAM to unlock it on later logins.

The script:

1. Creates a new, uniquely named Ed25519 SSH key with 100 KDF rounds.
2. Creates a two-year Ed25519 GPG certification key and a one-year signing subkey.
3. Exports only public keys to a private timestamped directory under
   `~/.local/state/git-keys/` and verifies a GPG test signature.
4. Configures Git identity and automatic commit/tag signing in untracked
   `~/.config/git/local.conf`, explicitly selecting the signing subkey.
5. Adds a private include to `~/.gitconfig` and selects the SSH key for GitHub.
6. Signs and verifies a disposable Git commit to check the final configuration.

Existing keys are kept. Existing private configuration files are backed up
before updates. If interrupted, generated keys remain available in `~/.ssh`
and `~/.gnupg`; inspect them before rerunning rather than assuming they vanished.
The script is interactive and intentionally refuses non-terminal input.

## Register on GitHub

The script prints paths to:

- `github-ssh-public.pub`: add as an **authentication** SSH key.
- `github-gpg-public.asc`: add as a **GPG** key.

Register these public keys at https://github.com/settings/keys. The script does
not upload them, change your GitHub account, or remove old registered keys.
Generating fresh keys does not revoke old ones: remove old GitHub keys when you
are ready, and revoke old GPG keys when appropriate.

After registration:

```sh
ssh -T git@github.com
```

On first connection, verify the host fingerprint against
[GitHub's published fingerprints](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/githubs-ssh-key-fingerprints).
GitHub reports successful SSH authentication but normally exits with status 1
because it does not provide shell access.

## Agent and passphrase handling

A desktop autostart entry starts GNOME Keyring's Secret Service and SSH components.
Fish prefers its SSH socket at `$XDG_RUNTIME_DIR/keyring/ssh` and the private
GitHub SSH config selects that socket explicitly, so GUI Git clients use it too.
The keyring wraps the system OpenSSH agent and unlocks keys through desktop dialogs.
An OpenSSH agent is only a fallback if the keyring is unavailable.

The setup script selects `pinentry-gnome3` in the private GPG agent config and
allows its external keyring cache. Fish and Bash also set `GPG_TTY`. The small
`dotfiles-ssh-askpass` helper connects OpenSSH key generation to graphical Pinentry:
its stdout is consumed only by OpenSSH, and it never logs responses.

Packages installed during an existing login do not retroactively run the PAM
keyring-unlock step. You may need to unlock/create the login keyring once in the
current session, or log out and back in. The pre-existing SDDM PAM configuration
already contains the optional GNOME Keyring hooks; this setup does not edit PAM.

GPG creates a revocation certificate under `~/.gnupg/openpgp-revocs.d/`.
Keep it and any secret-key backups in secure storage outside Git. The script
never exports your GPG private keys. Expiration can be extended later; it does
not require publishing a new identity on every expiration date.

## Public Git defaults

New repositories use `main`. Fetch prunes stale remote branches, pulls require
a fast-forward, pushes use a simple matching branch with automatic upstream
setup, and merge conflicts use `zdiff3`. Useful aliases: `git st`, `git lg`,
`git last`, and `git unstage`.

A private identity must be configured before committing (`user.useConfigOnly`).
Signing is enabled only after the key setup script has generated and tested the
keys. Machine-specific settings never belong in the tracked public config.
