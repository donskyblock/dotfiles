# Tokyo Night · COSMIC

My dotfiles for **Void Linux + COSMIC**. Dark navy windows, blue and lavender
accents, a floating dock, and matching colours across the terminal, editor and
browser.

This is a personal desktop setup, so expect to adjust a few things for your own
machine. You can install the COSMIC setup together or pick individual parts.
There are also companion configs for Hyprland, Niri and Mango.

![Nightfall wallpaper — navy mountains under a starry sky](home/.local/share/wallpapers/tokyo-night.svg)

*The bundled Nightfall wallpaper. This is the artwork, not a desktop screenshot.*

[Install](#getting-started) · [Pick individual parts](#install-only-what-you-want) ·
[Keybinds](KEYBINDS.md) · [Customise](#make-it-yours) ·
[Restore](#undoing-changes) · [Contributing](CONTRIBUTING.md)

## What's included

- **COSMIC:** Tokyo Night colours, rounded corners, window gaps, an inset top
  panel and a compact dock that hides automatically.
- **Terminals and shell:** COSMIC Terminal and Foot palettes, Fish with a Git
  prompt, fuzzy history and file search, zoxide, and a Bash fallback.
- **Apps:** a local VS Code theme, Firefox styles, GTK colours, Fastfetch config
  and an Equicord theme.
- **Cursor:** a black 20 px theme generated from your installed Adwaita cursors.
- **Optional extras:** an SDDM login theme, neon wallpaper, desktop music widget,
  and companion compositor configs with Quickshell or DankMaterialShell.

## Getting started

Start from a working Void + COSMIC desktop. The scripts configure apps; they
**don't install packages or set up the operating system**.

For the complete desktop setup, have these installed first:

| Dependency | Used for |
| --- | --- |
| Git and Python 3 | Installing configs and enabling the repository hook |
| PyGObject, GdkPixbuf and the librsvg image loader | Rendering the wallpaper |
| Adwaita cursor assets | Building the cursor theme |
| Fish, fzf, zoxide and fd | The configured shell and its shortcuts |
| Noto Sans, DejaVu Sans Mono and Papirus-Dark | Fonts and icons |

On Void, the shell tools can be installed with:

```sh
sudo xbps-install -S fish-shell fzf zoxide fd
```

Fish needs to be installed before you open a configured terminal: COSMIC Terminal,
Foot and VS Code are set to launch `/usr/bin/fish`. Your system login shell is
left as it is.

Keep your checkout somewhere permanent, ideally `~/dotfiles` (the `dots` shortcut
uses that path). From the repository directory, preview the desktop changes:

```sh
./install.sh desktop
```

Then apply them as your normal user:

```sh
./install.sh desktop --apply
```

This links the files listed in `manifest.txt`, sets up the wallpaper and Firefox
styles, builds the cursor theme, applies the Equicord theme and enables the
repository's pre-commit hook. It includes the tracked Mango config alongside the
COSMIC settings. It does **not** install SDDM, the music widget or the separate
companion desktops.

`python3 install.py` and `python3 install.py --apply` are the equivalent direct
commands.

After installing:

1. Open a new terminal for the Fish prompt and shortcuts.
2. Fully quit and reopen Firefox and VS Code to load their themes. In VS Code,
   choose **Tokyo Night COSMIC** under **Preferences: Color Theme** if needed.
3. Save your work, then log out and back in to refresh the cursor. COSMIC usually
   picks up other settings live, but a fresh session also helps with stale visuals.

### Where your existing files go

The main installer creates individual symlinks into this checkout. Editing a
linked file here changes the configuration your app reads. Keep the checkout in
place; moving or deleting it breaks those links.

Files it replaces are preserved under:

```text
~/.local/state/dotfiles/backups/<timestamp>/
```

Wallpaper and Firefox backups use a `rice-` prefix in the same directory.
Re-running the installer refreshes existing links and preserves files that apps
have replaced since the previous install. It doesn't replace whole config folders.

## Install only what you want

Run `./install.sh` for an interactive menu. **The menu defaults to SDDM only.**
For an explicit choice, use one of these commands:

| Command | What it installs |
| --- | --- |
| `./install.sh sddm --apply` | SDDM login theme; requests sudo |
| `./install.sh wallpaper --apply` | Neon-sign wallpaper for COSMIC |
| `./install.sh widgets --apply` | Desktop music card, playback controls and audio spectrum |
| `./install.sh cursor --apply` | Black cursor theme |
| `./install.sh discord --apply` | Equicord theme |
| `./install.sh desktop --apply` | The complete desktop setup described above |
| `./install.sh all --apply` | The desktop setup plus SDDM |

Leave off `--apply` to preview. The SDDM preview prepares local theme files and
prints instructions for viewing them. In the interactive menu, answering yes to
“Apply” also installs the selected component.

`all` means **desktop + SDDM**; install widgets and companion desktops separately.

### Wallpapers and music widget

The full desktop setup renders the bundled Nightfall SVG into a local PNG. To
switch to the neon-sign wallpaper, run:

```sh
./install.sh wallpaper --apply
```

The music card sits behind windows in the bottom-right corner and starts at
COSMIC login. It reads playback information from apps that expose MPRIS; the
spectrum uses CAVA to show system audio. Its extra Void dependencies are:

```sh
sudo xbps-install gtk-layer-shell cava python3-gobject python3-cairo
./install.sh widgets --apply
```

See the [desktop guide](desktop/README.md) for placement, playback support and
stopping the widget. [Wallpaper sources and credits](WALLPAPERS.md) cover both
desktop images. SDDM uses its own café wallpaper, independently of the desktop.

### Other desktops

Install your compositor and its dependencies first, then choose a config:

```sh
./install.sh niri --apply          # Niri + the custom Quickshell bar
./install.sh hyprland --apply      # Hyprland + Quickshell
./install.sh mango --apply         # Mango + Quickshell
./install.sh companions --apply    # all three; Quickshell selected
./install.sh dms --apply           # switch the companion shell to DankMaterialShell
```

These installers copy their configs rather than linking them. Reinstalling can
replace local edits, so save those first. They don't install compositor packages,
register login sessions or switch your current desktop.

The [companion guide](companions/README.md) covers dependencies, keybindings,
Hyprland compatibility, shell selection and rollback.

## Everyday shell use

Fish supplies autosuggestions, syntax highlighting and completions. The prompt
shows your directory, Git state, Python environment, failed commands and the time
spent on commands that take over two seconds. No Nerd Font is needed.

See [KEYBINDS.md](KEYBINDS.md#fish) for shell shortcuts and command abbreviations,
alongside the bindings for each desktop. Run `shellhelp` for a reminder in your terminal.

Fisher is bundled, along with its license. The daily shell features work without
downloading plugins. To add one yourself, use `fisher install OWNER/PLUGIN`.
Avoid plugins that overwrite the custom files managed by this repository.

### Node, npm and pnpm

The bundled `nvm.fish` manages Node as your user. After installing the dotfiles,
run this **inside Fish** to download Node 22, npm 11 and the latest pnpm:

```fish
~/.local/bin/dotfiles-node-setup; and exec fish
```

It needs an internet connection and doesn't use sudo. Once installed, Node 22 is
selected for new Fish shells. Shell startup doesn't download anything.

```fish
nvm list
nvm use 22
nvm install    # use the nearest .nvmrc or .node-version
```

## Make it yours

| To change… | Edit… |
| --- | --- |
| COSMIC colours | `home/.config/cosmic/com.system76.CosmicTheme.Dark/v2/` and the matching `.Dark.Builder/v2/` files |
| Panel and dock spacing | `home/.config/cosmic/com.system76.CosmicPanel.Panel/v1/` and `CosmicPanel.Dock/v1/` |
| Fish behaviour | `home/.config/fish/config.fish` and `functions/` |
| Terminal colours and fonts | `home/.config/foot/foot.ini` or `home/.config/cosmic/com.system76.CosmicTerm/v1/` |
| VS Code appearance | `home/.config/Code/User/settings.json` and the theme under `home/.vscode/extensions/` |
| Firefox appearance | `home/.config/firefox-theme/` |
| Nightfall artwork | `home/.local/share/wallpapers/tokyo-night.svg` |

After editing COSMIC files, run `./install.sh desktop --apply` to refresh the links
so its config watchers notice. Apps can replace symlinks when saving settings;
check `git diff` and the installer backups if a change seems to disappear.

To re-render an edited Nightfall SVG, move
`~/.local/share/wallpapers/tokyo-night.png` aside, then run
`python3 rice.py --apply`.

Keep machine-specific or private shell settings in `~/.config/fish/local.fish`
or `~/.bashrc.local`. Both are loaded by their respective shells and stay outside
Git. The Fish `ma` launcher selects `/dev/dri/card1` for NVIDIA; adjust it for your
hardware before using it.

### More setup guides

- [SDDM](sddm/README.md): login theme, preview and system-level rollback.
- [Cursor](cursor/README.md): Adwaita requirements, scaling and refreshing the theme.
- [Discord + Equicord](discord/README.md): native client setup and injection.
  The `discord` installer choice above only applies the theme.
- [Git identity and signing](git/README.md): private identity, SSH/GPG keys and
  GitHub registration. Start with `python3 git/setup.py` in your terminal.

Firefox styling is installed only when a default profile can be identified.
The installer links the stylesheets and artwork and enables them in `user.js`;
Firefox updates may require CSS adjustments. COSMIC configs include v1 and v2
formats, but different COSMIC releases may need changes too. Companion configs
still need appearance checks in their respective live sessions.

## Keeping changes in Git

New files are ignored by default. To track another config, review its contents,
put it under `home/`, add it to `manifest.txt`, and allow the file and its parent
directories in `.gitignore`.

For edits to existing files:

```sh
git diff
git add -u
python3 check-public.py
git diff --cached
git commit -m "Tune Tokyo Night"
```

The pre-commit hook checks staged paths, file types and common secret patterns.
Still read the diff yourself. Credentials, browser profiles, shell history,
downloaded binaries and private backups belong outside the repository.

## Undoing changes

Close the affected app first. For the main desktop install, remove the symlink
created by this setup and restore the original file from the matching timestamped
backup under `~/.local/state/dotfiles/backups/`. Backup paths mirror the paths in
your home directory. If there was no original file, removing the link lets the app
use its defaults.

Firefox's original stylesheets and `user.js`, when present, are in a `rice-`
backup. If there was no original `user.js`, remove the
`toolkit.legacyUserProfileCustomizations.stylesheets` preference added by this
setup. Restoring that preference alone doesn't restore the stylesheets.

SDDM, the widget and companion desktops have their own restore instructions in
the guides linked above. There isn't a single uninstall command.

## Found an issue or want to help?

Open an issue if something breaks or the setup instructions leave you stuck. Include
your distro, desktop version, the command you ran and what happened. Fixes, ideas
and documentation improvements are welcome; [CONTRIBUTING.md](CONTRIBUTING.md)
covers bug reports, pull requests and the checks to run.

## Credits

- [Tokyo Night](https://github.com/enkia/tokyo-night-vscode-theme) for the palette inspiration.
- [COSMIC](https://github.com/pop-os/libcosmic) for the base theme schemas and data (MPL-2.0).
- [ExploitCraft/fastfetch-config](https://github.com/ExploitCraft/fastfetch-config) for the original Fastfetch layout.
- [tokyo-night/wallpapers](https://github.com/tokyo-night/wallpapers) for the optional wallpapers.

Third-party material keeps its original licensing. Nightfall is original artwork;
its permission notice is in [WALLPAPERS.md](WALLPAPERS.md). Fisher and nvm.fish
licenses are included alongside their bundled sources.
