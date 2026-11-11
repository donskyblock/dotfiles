# Black desktop cursors

The desktop uses **TokyoNight-Black at 20 logical pixels**, down from the default
24. It derives a complete black cursor set from the locally installed Adwaita
assets and keeps their light outlines, aliases, and busy animations.

The installed Adwaita set starts at 24 px. Merely requesting 20 can still choose
that larger asset in COSMIC, so the builder creates actual 20 / 40 / 60 px images
for normal, 2×, and 3× displays. Hotspots scale with the images; premultiplied alpha
is preserved. Arrow, link, text, drag/grab, resize, and busy states stay distinct.

```sh
python3 cursor/apply.py         # build and verify the local theme
python3 cursor/apply.py --live  # also update toolkit preferences in your desktop session
```

The main dotfiles installer builds it automatically. Generated cursor binaries
live at `~/.local/share/icons/TokyoNight-Black`, with a compatibility link under
`~/.icons`. They stay outside Git. The builder and settings are versioned.
The source is your installed `/usr/share/icons/Adwaita/cursors`; install the
Adwaita cursor/icon package before using this setup on another machine.

Both default cursor search locations inherit the complete theme. Bash login and
Fish export `XCURSOR_THEME` / `XCURSOR_SIZE` before GUI apps start, GTK 3 / 4 use
the same theme and size, and the desktop autostart entry updates GSettings and
Xresources where available. Mango's alternate compositor config also requests 20.

**Log out and back in after installation.** COSMIC reads and caches its cursor
theme at compositor startup; changing a shell variable in an existing terminal
cannot update that process. The autostart step runs on the real desktop bus,
which the setup environment cannot access. Apps already running can also retain
cached cursor images until restarted. Apps can intentionally choose their own
cursor or keep an arrow over controls; this config supplies the standard shapes
rather than overriding application behaviour.

The installed session defaults requested a `Pop` cursor theme that was absent,
and no system `default` cursor theme was installed. This setup removes that
missing-theme fallback path. It does not change pointer speed, acceleration,
buttons, drivers, or the hardware cursor rendering path.

Adwaita artwork remains subject to the licensing of your installed Adwaita
package. Derived binaries are generated locally; the repository does not bundle
or redistribute the cursor artwork.
