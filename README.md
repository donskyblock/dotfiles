# Tokyo Night · COSMIC

Midnight navy, soft blue, lavender, and a quiet mountain skyline.
A complete desktop setup for **Void Linux + COSMIC**, with matching shell and app colours.

![Nightfall — original Tokyo Night wallpaper](home/.local/share/wallpapers/tokyo-night.svg)

## The look

| Layer | Details |
| --- | --- |
| COSMIC | Navy surfaces, blue accents, rounded corners, 6 / 12 px window gaps, 2 px focus hint |
| Panel & dock | Inset top panel, compact auto-hiding floating dock, restrained transparency and frosted system surfaces |
| Terminal | Matching COSMIC Terminal and Foot palettes, comfortable padding, soft text, blue cursor |
| Shell | Two-line Bash prompt, coloured file listings, `ll` and `dots` shortcuts |
| Fastfetch | Void logo with blue / lavender headings and an OS-age helper |
| VS Code | Local Tokyo Night theme, matching syntax and terminal colours, clean tabs, Seti icons |
| Firefox | Navy tabs and toolbar, blue active-tab underline, matching address bar and new-tab page |
| GTK | Matching named colours for GTK 3 / 4, dark preference, Papirus-Dark icons |
| MangoWC | Matching colours for the alternate compositor |
| Wallpaper | Original editable 4K Nightfall artwork; optional GitHub wallpaper download |

| Background | Surface | Text | Blue | Lavender | Cyan | Green | Rose |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `#1a1b26` | `#24283b` | `#c0caf5` | `#7aa2f7` | `#bb9af7` | `#7dcfff` | `#9ece6a` | `#f7768e` |

## Install

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

## Wallpaper

Nightfall is rendered locally from the tracked SVG to an untracked PNG. The actual
COSMIC wallpaper path is generated outside the repo, so it works under any username.
For the optional GitHub wallpaper:

```sh
python3 rice.py --apply --fetch-wallpaper
```

See [wallpaper sources and details](WALLPAPERS.md). The initial setup used Nightfall
because direct GitHub downloads were unavailable in the execution environment.

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
two stylesheets, and adds the preference required to load them to `user.js`.
Existing files are preserved in private backups. No history, cookies, saved logins,
`prefs.js`, or other profile contents are copied into this repository.
If no default profile can be identified, the browser step is skipped with a message.
The CSS styles the browser UI and built-in new-tab page; website colours remain
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
