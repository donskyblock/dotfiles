# Tokyo Night · COSMIC

Midnight navy, soft blue, lavender, and a quiet mountain skyline.
A complete desktop setup for **Void Linux + COSMIC**, with matching shell and app colours.

![Nightfall — original Tokyo Night wallpaper](home/.local/share/wallpapers/tokyo-night.svg)

## The look

| Layer | Details |
| --- | --- |
| SDDM | Matching Nightfall login screen, session selector, password controls, clock, and power actions |
| COSMIC | Navy surfaces, blue accents, rounded corners, 6 / 12 px window gaps, 2 px focus hint |
| Cursor | Complete black 20 px cursor set, matching toolkit settings, animated busy states |
| Panel & dock | Inset top panel, compact auto-hiding floating dock, restrained transparency and frosted system surfaces |
| Terminal | Matching COSMIC Terminal and Foot palettes, comfortable padding, soft text, blue cursor |
| Shell | Fish + Fisher, Tokyo Night Git prompt, fuzzy search, zoxide, and Bash fallback |
| Fastfetch | Void logo with blue / lavender headings and an OS-age helper |
| VS Code | Local Tokyo Night theme, matching syntax and terminal colours, clean tabs, Seti icons |
| Firefox | Navy tabs, toolbar, menus and sidebar; blue focus accents; Nightfall new-tab wallpaper |
| GTK | Matching named colours for GTK 3 / 4, dark preference, Papirus-Dark icons |
| MangoWC | Matching colours for the alternate compositor |
| Wallpaper | Original editable 4K Nightfall artwork; optional GitHub wallpaper download |

| Background | Surface | Text | Blue | Lavender | Cyan | Green | Rose |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `#1a1b26` | `#24283b` | `#c0caf5` | `#7aa2f7` | `#bb9af7` | `#7dcfff` | `#9ece6a` | `#f7768e` |

## Install

To install **just the login theme**, use the component installer:

```sh
./install.sh                 # menu; defaults to SDDM only
./install.sh sddm            # prepare a local preview
./install.sh sddm --apply    # install only SDDM (requests sudo)
```

Other choices: `wallpaper`, `widgets`, `cursor`, `discord`, `desktop` (existing complete desktop setup),
and `all` (desktop + SDDM). Changes require `--apply`, or an affirmative answer
in the menu. SDDM uses its own bundled nighttime café wallpaper from GitHub;
your desktop wallpaper stays independent. See [SDDM details](sddm/README.md).

Desktop additions can also be installed individually:

```sh
./install.sh wallpaper --apply  # selected neon-sign wallpaper
./install.sh widgets --apply    # now playing, playback controls, audio spectrum
```

See [desktop widget setup and placement](desktop/README.md). The music card sits
behind windows on COSMIC/Wayland and starts automatically at login.

Requires **Git, Python 3, PyGObject, GdkPixbuf, and the librsvg image loader**.
The setup uses already installed Noto Sans / DejaVu Sans Mono fonts and Papirus-Dark
icons. Install the relevant apps separately; this repository does not install packages.

Clone to a permanent location and run:

```sh
cd dotfiles
python3 install.py          # preview only
python3 install.py --apply  # preserve originals and install the complete rice
```

The repository contains the real files; individual symlinks put them where apps
expect them. Edit `home/.bashrc` here and your live `~/.bashrc` changes immediately.
The installer preserves replaced files under
`~/.local/state/dotfiles/backups/<timestamp>/`, outside Git. Re-running it refreshes
links without backing up the same links again, and notifies COSMIC's config watchers.
Unrelated configs stay independent.

Open a new terminal to get the prompt. **Fully quit and reopen Firefox** to load
its stylesheet. COSMIC usually watches config changes live; if any element stays
unchanged, log out and back in after saving your work.

Keep this repository in place. If you move it, remove its old links and run the
installer from the new location. The `dots` shell shortcut assumes `~/dotfiles`.

## Companion desktops

Matching Hyprland, Niri, and Mango setups now include a custom Quickshell bar
and a DankMaterialShell palette. Each can be installed independently:

```sh
./install.sh companions           # preview all companions
./install.sh companions --apply   # install all; Quickshell selected
./install.sh niri --apply         # just Niri + Quickshell
./install.sh dms --apply          # select DankMaterialShell instead
```

See [companion setup, shell selection, dependencies, and rollback](companions/README.md).

## Wallpaper

Nightfall is rendered locally from the tracked SVG to an untracked PNG. The actual
COSMIC wallpaper path is generated outside the repo, so it works under any username.
For the optional GitHub wallpaper:

```sh
python3 rice.py --apply --fetch-wallpaper
```

See [wallpaper sources and details](WALLPAPERS.md). The original setup used Nightfall
because direct GitHub downloads were unavailable in the execution environment.

## Cursor

The black cursor is 20 px, with distinct text, link, drag, and resize shapes.
It is generated from installed Adwaita assets and configured consistently for
COSMIC, GTK, and Xcursor clients. **Log out and back in after installing** to
refresh COSMIC's cached cursor theme. See [cursor setup](cursor/README.md).

## SDDM login screen

The matching Qt 6 login theme has a separate system installer:

```sh
python3 sddm/install.py             # prepare and show preview instructions
sudo python3 sddm/install.py --apply
```

It backs up existing configuration and selects the theme for the next login
screen without restarting your session. See [SDDM setup, preview, and rollback](sddm/README.md).

## Fish + Fisher

On Void, install the dependencies with:

```sh
sudo xbps-install -S fish-shell fzf zoxide fd
python3 install.py --apply
exec fish
```

New COSMIC Terminal, Foot, and VS Code terminals launch `/usr/bin/fish`. The system
login shell stays unchanged; Bash remains available with `bash`. Fish-dependent
terminal settings require Fish to be installed before using the complete setup.

The prompt shows the current directory, Git branch and working-tree state, Python
virtual environment, failed-command status, and elapsed time for commands over two
seconds. It uses installed fonts without requiring Nerd Font icons. Native Fish
provides autosuggestions, highlighting, completions, and directory history.

| Shortcut | Action |
| --- | --- |
| Ctrl-R | Fuzzy command history |
| Ctrl-T | Find and insert a file path |
| Alt-C | Pick and enter a directory |
| Right / Ctrl-F | Accept an autosuggestion |
| `z NAME` / `zi` | Smart directory jump / interactive jump |
| `ll` / `la` | Detailed listing / hidden entries |
| `mkcd NAME` | Create a directory and enter it |
| `dots` | Go to this repository |
| `gs` / `gd` / `gds` / `gl` | Git status / diff / staged diff / recent graph |
| `shellhelp` | Show the shortcuts |

[Fisher](https://github.com/jorgebucaran/fisher) 4.4.8 is bundled as an autoloaded
function, with its MIT license in `home/.config/fish/FISHER-LICENSE`. It works without
a network connection for local plugins. Remote plugin installation needs network:

```fish
fisher install OWNER/PLUGIN
fisher list
fisher update OWNER/PLUGIN
fisher remove OWNER/PLUGIN
```

Fisher itself is versioned here; update its bundled source and license deliberately
rather than asking Fisher to overwrite its own managed files. The daily features
use Fish, fzf, and zoxide directly, with no extra downloaded plugins.

Put private overrides in `~/.config/fish/local.fish`. Fish history, universal
variables, zoxide's database, Fisher's installed-plugin metadata, and newly downloaded
plugin files stay outside the tracked allowlist. To version an extra plugin, review
its source and license and add only the intended files to the manifest and allowlist.
Fisher can replace symlinks when updating a plugin, so avoid letting plugins own the
same files as your custom configuration.

## Native Discord + Equicord

The user-owned native Discord application and explicit Equicord injection helper
are documented in [native Discord setup](discord/README.md). Launch **Discord
(Native)** or run `discord`; after rebuilding Equicord, run `equicord-inject`.
Client profiles and application binaries are outside Git. The original **Nightfall ·
Tokyo Night** Equicord theme matches the desktop and loads through a local QuickCSS
import; its CSS is versioned under `home/.config/Equicord/themes/`.

## Node, npm, and pnpm

Fish uses [nvm.fish](https://github.com/jorgebucaran/nvm.fish), a Fish-native Node
version manager. It is bundled with its MIT license as `NVM-LICENSE`; the index
helper rejects HTTP failures and installation stops when an index download fails.
The POSIX `nvm-sh` script is not needed or installed.

After installing the dotfiles, download the runtimes and package managers once:

```fish
~/.local/bin/dotfiles-node-setup; and exec fish
```

This installs the latest **Node 22.x**, **npm 11.x**, and current **pnpm** as your
user. It needs internet access and never uses `sudo`. The setup agent could not
perform these downloads because its environment could not resolve `nodejs.org`.
The helper checks all three version commands before reporting success.

`zz-node-default.fish` selects Node 22 for new interactive and noninteractive Fish
shells, including VS Code terminals and Fish tasks, after it is installed. Before
installation, shell startup stays quiet and does not attempt any downloads.
`nvm_default_packages` installs npm 11 and pnpm with future Node installs; those
package versions require a compatible Node release. `PNPM_HOME` is set to
`~/.local/share/pnpm`, with its global executable directory on PATH.

```fish
nvm list
nvm use 22
nvm install                 # read the nearest .nvmrc or .node-version
node --version
npm --version
pnpm --version
```

Node binaries, npm credentials, pnpm's store, and downloaded package state stay
outside Git. No npm prefix is forced, so the version manager owns global packages
inside the active Node installation. Fisher itself and this bundled nvm.fish
configuration are versioned here; avoid assigning another plugin ownership of
these managed files without reviewing conflicts.

## VS Code

A local colour-theme extension lives under `home/.vscode/extensions/`; its package
and theme JSON files are linked into VS Code's extension directory. No Marketplace
download or executable extension code is needed. User appearance settings are linked
from `home/.config/Code/User/settings.json`. Workspace storage, chat state, extension
state, authentication, and sync data stay outside this repository.

After installation, fully quit and reopen VS Code so it discovers the local theme.
If needed, choose **Tokyo Night COSMIC** from **Preferences: Color Theme**.
The setup uses installed DejaVu Sans Mono, built-in Seti file icons, and a matching
integrated terminal palette. Keep tokens and private settings out of the tracked
user settings; use environment variables for credentials.

## Firefox

The installer finds the default Firefox profile from `profiles.ini`, links only the
two stylesheets and the Nightfall wallpaper, and adds the preference required to load them to `user.js`.
Existing files are preserved in private backups. No history, cookies, saved logins,
`prefs.js`, or other profile contents are copied into this repository.
If no default profile can be identified, the browser step is skipped with a message.
The CSS styles the browser UI, settings pages, and built-in new-tab page; website colours remain
under each website's control. Firefox updates can require stylesheet adjustments.

## Make it yours

- Change COSMIC colours in `home/.config/cosmic/com.system76.CosmicTheme.Dark/v2/`.
  The matching `.Dark.Builder` settings preserve the palette when editing Appearance.
  Both installed v1 and v2 formats are included for compatibility.
- Change dock and panel spacing in the `CosmicPanel.Dock` / `CosmicPanel.Panel` folders.
- Edit `home/.local/share/wallpapers/tokyo-night.svg`; move the generated PNG aside
  and run `python3 rice.py --apply` to render again.
- Keep private shell exports in `~/.bashrc.local`; it is loaded by Bash and stays outside Git.
- Mango's `ma` launcher selects `/dev/dri/card1` for NVIDIA; adjust that for your hardware.

After editing repo files, run `python3 install.py --apply` to refresh COSMIC's watched
links. Some apps rewrite config files by replacing symlinks; the installer preserves
those files so you can compare changes. Settings can regenerate compiled theme values;
review your diff afterward. GTK / libadwaita apps vary in how much custom CSS they honor.
The setup was checked against the installed COSMIC 1.5-era schemas; other releases
may change config formats. Complete live desktop appearance was not screenshot-verified
because the setup environment could not access the desktop session bus.

## Git identity and signing

The public Git defaults are versioned; personal identity and key settings are
private. To generate fresh SSH/GPG keys and configure signed commits, run
`python3 ~/dotfiles/git/setup.py` in your terminal. It prompts locally for your
identity and passphrases, preserves old keys, and verifies signing. See
[Git key setup and GitHub registration](git/README.md).

## Version control & privacy

```sh
git diff
git add -u
python3 check-public.py
git diff --cached
git commit -m "Tune Tokyo Night"
```

New paths are ignored by default. To add a config, review its entire contents, copy
it under `home/`, add its path to `manifest.txt`, and explicitly allow the file and
parent directories in `.gitignore`. Stage it and review the staged diff before committing.

The installer enables a pre-commit hook. It checks the staged allowlist, file types,
common credential paths, and secret patterns without printing suspected secrets.
Hooks can be bypassed and pattern checks cannot detect every secret. Review every
push; never put credentials into tracked files, even temporarily, because Git keeps history.
Browser data, cloud/SSH credentials, history, logs, downloaded binaries, and private
backups are excluded. No screenshots containing personal browser tabs are included.

## Restore

Before restoring, close the relevant app. Remove only links created by this setup
and move the matching original files from a timestamped private backup into place.
For files with no previous original, remove the links to use application defaults.
The initial Git commit preserves the pre-rice configs. Restoring those tracked files
and refreshing their links restores the original shell / desktop preferences; remove
new theme links separately. Firefox's original stylesheets and `user.js`, if present,
are in the `rice-*` backup. If `user.js` did not exist before, remove the single
`toolkit.legacyUserProfileCustomizations.stylesheets` preference added by this setup.

## Credits

- [Tokyo Night](https://github.com/enkia/tokyo-night-vscode-theme): palette inspiration.
- [COSMIC](https://github.com/pop-os/libcosmic): installed default theme schemas and base data (MPL-2.0).
- [ExploitCraft/fastfetch-config](https://github.com/ExploitCraft/fastfetch-config): original Fastfetch layout attribution retained.
- [tokyo-night/wallpapers](https://github.com/tokyo-night/wallpapers): optional GitHub wallpaper source.

Third-party material remains subject to its original licensing. Nightfall is original
artwork; its permission notice is in [WALLPAPERS.md](WALLPAPERS.md).
