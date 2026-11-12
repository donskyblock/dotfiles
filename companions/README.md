# After Hours companion desktops

Tokyo Night companions for Hyprland, Niri, and Mango, with two interchangeable
shell choices. The custom Quickshell bar has an inset navy surface, lavender
MPRIS track display with click to pause/play, an app launcher, and a clock on
each monitor. DankMaterialShell supplies its own full desktop controls using
the matching custom palette. These configs reuse the neon wallpaper from the
main COSMIC setup.

```sh
./install.sh companions                 # preview
./install.sh companions --apply         # all three compositors; Quickshell selected
./install.sh hyprland --apply
./install.sh niri --apply
./install.sh mango --apply
./install.sh quickshell --apply          # select the custom bar
./install.sh dms --apply                 # select DankMaterialShell
```

For a compositor with DMS selected immediately:

```sh
python3 companions/install.py niri --shell dms --apply
python3 companions/install.py companions --shell dms --apply
```

`companions` installs both shell assets and selects one. The shell choice is
stored in `~/.config/after-hours/shell`. Log out and back in after switching it.
Choose the compositor's installed session in SDDM; this installer does not
change the active session, install packages, or register compositor sessions.
The existing `desktop` and `all` choices retain their original COSMIC scope.

Install the compositor and its desktop portal backend separately. Shared tools:
Python 3, Foot, Noto Sans. Quickshell requires Quickshell with QtQuick Layouts,
MPRIS support, a Wayland-capable Rofi, and optionally swaybg for the wallpaper.
DMS requires a working `dms run` installation and its upstream dependencies;
select `~/.local/share/wallpapers/after-hours.jpg` in DMS's wallpaper controls.
DMS handles its own notifications, launcher, tray, audio, and wallpaper. The
custom Quickshell bar is deliberately compact: it has no tray, notification
server, lock screen, or network/audio settings. Install those tools separately
if you choose that shell. Both shells work without systemd in these configs.

The helper starts only from the companion compositor, keeps one instance per
Wayland display, and resolves commands through PATH. With Quickshell it manages
its own swaybg child. It does not start either shell in COSMIC. Existing bars or
notification daemons started elsewhere should be disabled in those sessions to
avoid duplicates, especially when selecting DMS.

See [the keybind reference](../KEYBINDS.md) for each compositor's shortcuts.

Mango preserves the established bindings, layouts, and gestures; it adds the
shared terminal and launcher shortcuts. Hardware device paths are not forced.

Hyprland defaults to the current Lua API. For an older Hyprland installation:

```sh
python3 companions/install.py hyprland --legacy-hyprland --apply
```

That installs `hyprland.conf` instead of `hyprland.lua`. If an existing Lua config
is present, Hyprland may prefer it: move it aside yourself before using the
legacy config. Mango targets the installed 0.18 snake_case format. Niri uses
its KDL configuration. Adjust keyboard layout (`us` by default), output scaling,
and monitor placement to your hardware.

Installations copy files so local compositor edits do not modify this repository.
Replaced files, including symlinks and their contents, are preserved beneath
`~/.local/state/dotfiles/backups/companions-TIMESTAMP/`, using home-relative paths.
DMS settings are merged with existing JSON settings; theme selection changes
while unrelated keys survive. Reapplying replaces managed config files, so keep
local edits before reinstalling. New DMS config.d overrides may take precedence;
check them if a previous theme remains selected.

To restore, log out of the companion session, move the matching backup files
back to their home-relative locations, and remove generated files that had no
original. Log into your preferred session afterward. Keep copied theme assets
when leaving DMS settings pointing at them.

Reference schemas: [Hyprland example](https://github.com/hyprwm/Hyprland/blob/main/example/hyprland.lua),
[Niri default config](https://github.com/niri-wm/niri/blob/main/resources/default-config.kdl),
[Quickshell PanelWindow](https://quickshell.org/docs/v0.2.0/types/Quickshell/PanelWindow/),
[DMS custom themes](https://duxlabs.dev/docs/dankmaterialshell/custom-themes).

Validation here: Mango's native config checker; Python syntax; isolated installer
checks for backups, repeat installs, DMS settings preservation, preview behavior,
and unsafe destination handling. Hyprland, Niri, and Quickshell are not installed
in the build environment, so their live parsing and appearance need verification
in those sessions.
