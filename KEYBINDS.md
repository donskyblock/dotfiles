# Keybinds

Shortcuts configured by this repository, grouped by desktop and shell. These are
Linux desktop configurations; the desktop you log into determines which bindings
apply, rather than the distro underneath it.

**Super** is usually the Windows/logo key. **Return** means Enter. `1–9` means any
number in that range, and “arrows” means Left, Right, Up or Down.

[README](README.md) · [COSMIC](#cosmic) · [Hyprland](#hyprland) ·
[Niri](#niri) · [Mango](#mango) · [Fish](#fish)

## COSMIC

This repository themes COSMIC but doesn't ship custom desktop keybindings.
View or change your session's bindings in **COSMIC Settings → Input Devices →
Keyboard → Keyboard Shortcuts**. Your installed COSMIC defaults and any personal
changes apply.

The shell shortcuts below work in a Fish terminal within COSMIC too.

## Hyprland

Sources: [Lua config](companions/hypr/hyprland.lua) (default) and
[legacy config](companions/hypr/hyprland.conf).

| Shortcut | Action |
| --- | --- |
| Super+Return | Open Foot |
| Super+D | Open the selected shell's launcher |
| Super+Q | Close the focused window |
| Super+V | Toggle floating |
| Super+arrows | Focus a window in that direction |
| Super+1–9 | Switch workspace |
| Super+Shift+1–9 | Move the window to that workspace |
| Super+left mouse drag | Move a window |
| Super+right mouse drag | Resize a window |
| Super+Shift+E | Exit Hyprland |
| Super+F | Fullscreen toggle **in the legacy config only** |

The default Lua config doesn't currently bind fullscreen or directional window
movement. Don't assume every legacy shortcut is present in both versions.

## Niri

Source: [Niri config](companions/niri/config.kdl). `Mod` is Niri's session modifier (normally Super).

| Shortcut | Action |
| --- | --- |
| Mod+Return | Open Foot |
| Mod+D | Open the selected shell's launcher |
| Mod+Q | Close the focused window |
| Mod+F | Toggle maximized column |
| Mod+Shift+F | Toggle fullscreen window |
| Mod+V | Toggle floating |
| Mod+Left / Right | Focus the previous / next column |
| Mod+Up / Down | Focus the window above / below |
| Mod+Shift+Left / Right | Move the column left / right |
| Mod+Shift+Up / Down | Move the window up / down |
| Mod+1–9 | Switch workspace |
| Mod+Shift+1–9 | Move the column to that workspace |
| Mod+Shift+E | Exit Niri |

## Mango

Sources: [base desktop config](home/.config/mango/config.conf) and
[companion config](companions/mango/config.conf). Both keep the bindings below.
The companion adds Super+Return for Foot and Super+D for the selected shell's
launcher. Its Alt+Space also uses that launcher; the base config calls Rofi directly.

### Apps and windows

| Shortcut | Action |
| --- | --- |
| Alt+Return | Open Foot |
| Alt+Space | Open the launcher |
| Alt+Q | Close the focused window |
| Super+Tab | Focus the next window |
| Alt+arrows | Focus a window in that direction |
| Super+Shift+arrows | Move a tiled window in that direction |
| Alt+Tab | Toggle jump (`togglejump`) |
| Alt+Backslash | Toggle floating |
| Alt+A | Toggle maximized screen |
| Alt+F | Toggle fullscreen |
| Alt+Shift+F | Toggle fake fullscreen |
| Super+I / Super+Shift+I | Minimize / restore a window |
| Super+G | Toggle global window state |
| Super+O | Toggle overlay state |
| Alt+Z | Toggle scratchpad |
| Ctrl+Shift+arrows | Move a window by 50 px |
| Ctrl+Alt+arrows | Resize a window by 50 px |
| Super+R | Reload config |
| Super+M | Exit Mango |

### Tags, monitors and layouts

| Shortcut | Action |
| --- | --- |
| Ctrl+1–9 | View tag |
| Alt+1–9 | Move the window to a tag and follow it |
| Super+Left / Right | View previous / next tag |
| Ctrl+Left / Right | View previous / next tag containing windows |
| Ctrl+Super+Left / Right | Send the window to the previous / next tag |
| Alt+Shift+Left / Right | Focus the monitor to the left / right |
| Super+Alt+Left / Right | Send the window to the monitor to the left / right |
| Super+N | Cycle layout |
| Alt+E | Set scroller proportion to 1.0 |
| Alt+X | Cycle scroller proportion presets |
| Alt+Super+Ctrl+arrows | Stack in that direction in the scroller layout |
| Alt+Shift+Return | Toggle split direction in manual dwindle mode |
| Alt+Shift+X / Z | Increase / decrease gaps |
| Alt+Shift+R | Toggle gaps |

### Mouse and touchpad

| Input | Action |
| --- | --- |
| Super+left mouse drag | Move a window |
| Super+right mouse drag | Resize a window |
| Middle mouse button | Toggle maximized screen |
| Super+scroll up / down | Previous / next tag containing windows |
| Three-finger swipe | Focus a window in the swipe direction |
| Four-finger swipe right / left | Previous / next tag containing windows |
| Four-finger swipe up / down | Enter / leave overview |

## Fish

These work in an interactive Fish shell on any of the desktops above. The fuzzy
pickers require `fzf`; installing `fd` improves file and directory searches.

Source: [Fish config](home/.config/fish/config.fish).

| Shortcut | Action |
| --- | --- |
| Ctrl+R | Fuzzy command history |
| Ctrl+T | Find and insert a file path |
| Alt+C | Pick a directory and enter it |
| Right / Ctrl+F | Accept an autosuggestion |
| Tab | Complete a command or path |

### Commands and abbreviations

These are typed commands, rather than key combinations. Fish expands the
abbreviations as you type.

| Command | Action |
| --- | --- |
| `z NAME` / `zi` | Jump to a frequent directory / choose interactively (requires zoxide) |
| `..` / `...` | Go up one / two directories |
| `ll` / `la` | Detailed listing including hidden files / list hidden entries |
| `mkcd NAME` | Create a directory and enter it |
| `dots` | Go to `~/dotfiles` |
| `g` | `git` |
| `gs` | Git status, short format with branch |
| `gd` / `gds` | Git diff / staged diff |
| `ga` / `gc` | Git add / commit |
| `gl` | Recent Git graph (15 commits) |
| `shellhelp` | Print a shortcut reminder |

## Changing a shortcut

Edit the source linked in the relevant section. Companion installers copy their
configs: edit the installed config for a local change, or the repository version
for a change you want to keep and reinstall. Save local edits before reinstalling.
Fish configs are linked by the main installer, so edits in the checkout apply to
new shells. COSMIC desktop shortcuts are managed in Settings.

If you change a shared binding, update this file too. Bindings for apps such as
VS Code and Firefox remain under those apps' own settings.
