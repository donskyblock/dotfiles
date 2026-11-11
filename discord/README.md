# Native Discord + local Equicord

Discord is installed as your user at `~/.local/opt/discord`. The Applications
launcher is **Discord (Native)**, and the shell command is `discord`.
Equicord is injected into that writable application directory, so patching does
not require root or modifications to a system Flatpak deployment.

The initial installation reused the installed Flatpak's application payload
because direct downloads were unavailable. Its Flatpak-only module path and
model symlinks were adapted for native use. It runs the Discord executable
directly with host libraries, without the Flatpak launcher or runtime.
No sandbox-disabling flags are added.

The original Flatpak application and profile were preserved. Native Discord uses
its own default profile; log in separately. No session cookies, credentials, chat
state, or Discord profile data were copied into dotfiles.

## Rebuild and reinject Equicord

After rebuilding your Equicord checkout:

```sh
pnpm build
equicord-inject
```

`equicord-inject` uses the cached Equilotl CLI and an explicit native installation
path. It avoids the interactive picker that previously selected the system
Flatpak. The path to your local build is stored privately under
`~/.local/state/dotfiles/discord/`, outside Git. To choose a different build:

```sh
equicord-inject /path/to/Equicord
```

Keep that checkout and its `dist/desktop` directory available: the injected
application loads that local build. Equilotl's optional self-update check can
print a network warning when offline; its local development-mode patch does
not need to download Equicord.

## Replace or update the native application

Quit native Discord first. To download the official stable Linux tarball and
reapply the local Equicord build:

```sh
python3 discord/setup.py --equicord-source /path/to/Equicord
```

To use an already installed system Flatpak's application files without downloading:

```sh
python3 discord/setup.py --from-flatpak --equicord-source /path/to/Equicord
```

The source argument can be omitted once a checkout has been recorded. The script
checks the native binary's shared-library dependencies, keeps the previous native
application under `~/.local/state/dotfiles/discord/backup-*`, patches the replacement,
and regenerates its desktop launcher. It restores the previous application if
installation or injection fails. It does not install system dependencies or delete
the Flatpak.

The main dotfiles installer links the launcher/injection helpers but does not
copy or download Discord automatically on a fresh machine. Run this separate
installer after building your Equicord checkout and obtaining its Equilotl CLI.
Application binaries, generated launchers/icons, installation paths, and client
profiles stay outside the public repository.

The initial setup verified the native application's libraries and Equicord patch.
A full GUI launch could not be tested inside the agent's execution sandbox;
open **Discord (Native)** from your desktop to verify login and voice features.

## Nightfall · Tokyo Night theme

The matching Equicord theme lives at
`home/.config/Equicord/themes/tokyo-night.theme.css`. Its colours match COSMIC,
Firefox, VS Code, and the shell: midnight navy, darker sidebar, blue controls,
lavender mentions/reactions, and a faint local Nightfall wallpaper in chat.
It covers both the legacy Discord variables and the newer surface/component
variables, with small selector-based refinements for channels, the composer,
menus, attachments, code blocks, focus states, and reduced-motion preferences.

```sh
python3 discord/theme.py --apply
```

The main dotfiles installer also runs this step. It links the theme and shared
wallpaper into Equicord's themes directory and adds one managed local import at
the top of your private QuickCSS. This uses Equicord's live file watcher; existing
QuickCSS and all plugin/account settings are preserved. Re-running it does not
add duplicate imports. Modified originals are backed up privately under
`~/.local/state/dotfiles/backups/equicord-theme-*`.

QuickCSS must be enabled in Equicord settings (it was enabled during setup).
The theme is activated through that local import, so you do not need to enable
it again in the theme list. If an existing window has not refreshed, press Ctrl-R.
After editing the tracked CSS, rerun the theme helper or reload Discord to avoid
cached CSS imports. There are no remote imports, web fonts, scripts, or asset
requests; the only image uses Equicord's local `vencord:///themes/` protocol.

Customize the palette at the top of the CSS. To remove the wallpaper, set
`--tn-wallpaper: none;`. To disable the complete theme, remove the block between
`BEGIN DOTFILES TOKYO NIGHT` and `END DOTFILES TOKYO NIGHT` in your private QuickCSS.
Restore the matching QuickCSS backup to return to its previous contents.
Discord UI updates can rename selectors; semantic colour tokens are the primary
styling mechanism so most colour changes do not depend on hashed class names.
