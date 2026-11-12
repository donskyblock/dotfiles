# Wallpapers

The bundled **Nightfall** wallpaper is an original, editable SVG: midnight navy,
layered mountains, a striped lavender moon, and a sparse star field. Its SVG is
versioned under `home/.local/share/wallpapers/`; the installer renders a 4K PNG
locally with GdkPixbuf. You may use, modify, and redistribute this original SVG
under the MIT license (copyright 2026 Dotfiles contributors).

## GitHub selection

For an alternative, this setup selects the neon-sign wallpaper from
[tokyo-night/wallpapers](https://github.com/tokyo-night/wallpapers/tree/main/misc/cityscape):

- File: `misc/cityscape/neon-sign_00_1920x1080.jpg`
- Source: https://github.com/tokyo-night/wallpapers/blob/main/misc/cityscape/neon-sign_00_1920x1080.jpg
- Upstream license: https://github.com/tokyo-night/wallpapers/blob/main/LICENSE.txt

The reviewed image is bundled in `desktop/neon-sign.jpg` with its upstream license.
Apply it without changing other desktop components:

```sh
./install.sh wallpaper --apply
```

The older combined wallpaper/browser helper can also download it:

```sh
python3 rice.py --apply --fetch-wallpaper
```

This downloads an image only, validates its format, and records the source URL
and downloaded SHA-256 under `~/.local/state/dotfiles/`. It does not execute
anything from the upstream repository. A failed download leaves your wallpaper
unchanged. The standalone wallpaper installer uses the bundled image and needs no network.

To return to Nightfall, move your generated
`~/.local/share/wallpapers/tokyo-night.png` aside and run `python3 rice.py --apply`.
The machine-specific COSMIC wallpaper path lives outside Git and is linked into
the desktop config, so no username or absolute home directory is published.

## SDDM: After Hours

SDDM bundles a separate [nighttime café wallpaper](sddm/tokyo-night/WALLPAPER.md)
from the same GitHub collection, including its upstream license. Preparing or
installing SDDM does not download anything or change the desktop wallpaper.
