# Wallpapers

The bundled **Nightfall** wallpaper is an original, editable SVG: midnight navy,
layered mountains, a striped lavender moon, and a sparse star field. Its SVG is
versioned under `home/.local/share/wallpapers/`; the installer renders a 4K PNG
locally with GdkPixbuf. You may use, modify, and redistribute this original SVG
under the MIT license (copyright 2026 Dotfiles contributors).

## GitHub selection

For an alternative, this setup selects the dark abstract wallpaper from
[tokyo-night/wallpapers](https://github.com/tokyo-night/wallpapers/tree/main/night/abstract):

- File: `night/abstract/lockscreen_00_3840x2160.png`
- Source: https://github.com/tokyo-night/wallpapers/blob/main/night/abstract/lockscreen_00_3840x2160.png
- Upstream license: https://github.com/tokyo-night/wallpapers/blob/main/LICENSE.txt

Download and apply it without adding the binary to Git:

```sh
python3 rice.py --apply --fetch-wallpaper
```

This downloads an image only, validates its format, and records the source URL
and downloaded SHA-256 under `~/.local/state/dotfiles/`. It does not execute
anything from the upstream repository. A failed download leaves your wallpaper
unchanged. The bundled original was used during setup because direct downloads
were unavailable in the execution environment.

To return to Nightfall, move your generated
`~/.local/share/wallpapers/tokyo-night.png` aside and run `python3 rice.py --apply`.
The machine-specific COSMIC wallpaper path lives outside Git and is linked into
the desktop config, so no username or absolute home directory is published.
