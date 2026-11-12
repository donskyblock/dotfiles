# After Hours desktop

A neon-sign wallpaper plus a compact Tokyo Night music card in the bottom-right
corner. The widget sits on the Wayland bottom layer, behind normal windows,
without reserving desktop space or taking keyboard focus. It starts on COSMIC
login and runs as a single instance.

```sh
./install.sh wallpaper --apply  # wallpaper only
./install.sh widgets --apply    # music card + audio spectrum only
python3 desktop/install.py both --apply  # both together
```

The wallpaper is the unmodified upstream
[`neon-sign_00_1920x1080.jpg`](https://github.com/tokyo-night/wallpapers/blob/9a72582d7505da9a28b2fd77c155fbf140f6c8f0/misc/cityscape/neon-sign_00_1920x1080.jpg),
pinned to commit `9a72582d7505da9a28b2fd77c155fbf140f6c8f0`. Despite its filename,
the actual image measures 1920 × 1081. The upstream MIT notice is preserved in
[WALLPAPER-LICENSE.txt](WALLPAPER-LICENSE.txt). Installation converts it to the
existing local PNG wallpaper path and selects it for all COSMIC monitors.
SDDM uses its separate café image.

The widget reads song/artist and playback capabilities through MPRIS on your
session bus. It prefers playing players over paused ones and keeps the current
playing player stable. Supported music apps and browsers must expose MPRIS;
otherwise the card shows “Nothing playing.” Previous, play/pause, and next are
enabled only when the player supports them. Album artwork and remote URLs are
not fetched. CAVA captures the default output monitor through PulseAudio /
PipeWire's PulseAudio compatibility service. The spectrum represents all system
audio, and stays flat during silence. Microphone input is not selected.

On Void, dependencies are:

```sh
sudo xbps-install gtk-layer-shell cava python3-gobject python3-cairo
```

Placement is configured in
`~/.local/share/dotfiles/desktop/settings.json`: `right` and `bottom` are margins,
`width` is requested width, and `monitor` is the zero-based monitor index.
A bottom margin of 100 leaves room for the dock. Restart after editing:

```sh
python3 ~/.local/share/dotfiles/desktop/widget.py --quit
python3 ~/.local/share/dotfiles/desktop/widget.py
```

The installer preserves placement settings on reinstall. To inspect or stop it:

```sh
python3 ~/.local/share/dotfiles/desktop/widget.py --status
python3 ~/.local/share/dotfiles/desktop/widget.py --quit
```

Diagnostics: `~/.local/state/dotfiles/music-widget.log`. To disable autostart,
add `Hidden=true` to
`~/.config/autostart/dotfiles-music-widget.desktop`, then stop the widget.
Reinstalling the widgets enables autostart again. `--preview` opens an ordinary
window for styling instead of a desktop-layer surface.

Installers preserve replaced files under
`~/.local/state/dotfiles/backups/desktop-TIMESTAMP/`, retaining their home-relative
paths. Restore the files you want from that backup after stopping the widget.
For replaced symlinks, `.contents` also preserves the original target contents.
Wallpaper and widget setup leaves browser configuration and other rice components
alone. No package installation or remote downloads occur in these installers.
