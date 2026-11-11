# dotfiles

A small collection of Linux desktop and shell preferences: Void Linux, MangoWC,
COSMIC, and a green Fastfetch theme.

The real files live in this repository. Symlinks put them where applications
expect them, so editing `home/.bashrc` here updates `~/.bashrc` immediately.

## What's inside

| Config | Purpose |
| --- | --- |
| Bash | Prompt, aliases, local bin path, and `ma` compositor launcher |
| Readline | System input defaults |
| MangoWC | Layouts, animations, colours, and key bindings |
| Fastfetch | Void-themed system summary and installation-age estimate |
| COSMIC | Dock, panel, tiling, background, and clock preferences |
| Autostart | Disable the COSMIC Store update notifier |

`manifest.txt` is the explicit list of managed files. Individual files are linked;
unrelated files in `~/.config` stay independent.

## Install

Requires Python 3 and Git. Clone this repository to a permanent location, then run:

```sh
cd dotfiles
python3 install.py          # preview
python3 install.py --apply  # back up originals and create symlinks
```

Existing files are moved to `~/.local/state/dotfiles/backups/<timestamp>/`,
outside Git. Re-running the installer leaves correct links alone and refuses
conflicting directories or symlinked parent directories. Keep this repository
in place after installation. To move it, remove its old links and run the installer
from the new location.

The installer also enables this repository's pre-commit check. Git hooks are local:
run the installer on each clone. It does not install packages or change system services.

## Everyday use

Edit files under `home/`, then review and commit:

```sh
git diff
git add -u
python3 check-public.py
git diff --cached
git commit -m "Update desktop preferences"
```

Reload the shell or the relevant application to apply settings. Desktop apps may
rewrite configuration files by replacing symlinks; re-run the installer if that
happens (the replaced file is backed up so you can compare changes).

Put private shell exports and machine-specific overrides in `~/.bashrc.local`.
That file is loaded by Bash and is outside this repository.

The `ma` launcher selects `/dev/dri/card1` for NVIDIA; adjust it for your hardware.
Mango bindings expect `mango`, `dbus-run-session`, `foot`, and `rofi`. Fastfetch's
age helper uses GNU `stat` and `date`. COSMIC preferences require a compatible COSMIC
installation. Choose the relevant manifest entries before installing on a different setup.

## Adding a config safely

1. Copy only the config files you want to share into `home/`, preserving their paths.
2. Review the entire contents for credentials and identifying information.
3. Add each file to `manifest.txt` and explicitly allow its file and parent directories
   in `.gitignore` (the repository ignores new paths by default).
4. Stage it, run `python3 check-public.py`, review the staged diff, then install.

Browser profiles, cookies, passwords, shell history, SSH/cloud credentials, app state,
logs, and backups do not belong here. The commit hook checks the staged files against
the manifest and common secret patterns; it cannot detect every secret and can be
bypassed. Review changes before pushing, and enable GitHub secret scanning when available.
Never put secrets into tracked files, including temporarily: Git preserves history.

## Restore original files

Close the relevant application, remove only the symlinks created by this installer,
and move the matching files from your timestamped backup to their original paths.
Files with no original backup can simply have their symlinks removed.

## Credits

The Fastfetch config retains its attribution to
[ExploitCraft/fastfetch-config](https://github.com/ExploitCraft/fastfetch-config).
Mango's config retains its upstream configuration reference. Third-party material
remains subject to its original licensing.
