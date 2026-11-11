# Tokyo Night · SDDM

An original Qt 6 login theme matching the COSMIC setup: Nightfall mountains,
midnight navy card, blue focus accents, lavender details, and a quiet clock.

The theme includes:

- Editable username, masked password, and optional password reveal.
- Installed desktop-session selection, with the remembered session selected initially.
- Enter to submit, Tab navigation, visible keyboard focus, and Caps Lock warning.
- Keyboard layout switching when multiple layouts are available.
- Sign-in progress and failed-login recovery; repeated submissions are suppressed.
- Sleep, restart, and shutdown where SDDM supports them; restart and shutdown require confirmation.
- A smaller centered layout and scrolling form when space is limited.

It uses standard Qt Quick Controls and installed Noto Sans. No shader effects,
external icon fonts, network requests, package installations, or home-directory
assets are required by the installed greeter. Passwords are passed directly to
SDDM and are never logged or saved by the theme. Authentication remains SDDM/PAM's responsibility.

## Prepare and preview

From the dotfiles repository:

```sh
python3 sddm/install.py
sddm-greeter-qt6 --test-mode --theme "$HOME/.local/state/dotfiles/sddm/tokyo-night"
```

Preview mode cannot authenticate or perform real power actions. It may use
example users rather than your real account. Close the preview normally.

Preparation renders a PNG from the tracked Nightfall SVG, avoiding differences
between Qt's SVG renderer and the desktop wallpaper renderer. The build stays
outside Git. PyGObject / GdkPixbuf / librsvg are required for preparation; the
greeter only needs the generated PNG and Qt 6.

## Apply

```sh
sudo python3 sddm/install.py --apply
```

The installer copies a self-contained theme to `/usr/share/sddm/themes/tokyo-night`
and selects it in `/etc/sddm.conf.d/90-tokyo-night.conf`. Existing theme selectors
in legacy `/etc/sddm.conf` have higher priority; only those selectors are updated
if present. Other configuration and comments are preserved.

Previous files are backed up to a private timestamped directory under
`/var/lib/dotfiles/sddm-backups/`. The installer prints the exact rollback command.
It does not change PAM, user accounts, autologin, desktop sessions, the selected
display server, or runit services. **It does not restart SDDM or close your session.**
The new theme appears the next time SDDM opens its login screen (typically after
logging out or rebooting); COSMIC's lock screen is a separate component.

System installation could not be performed by the setup agent because its
system directories were read-only. Run the apply command above from your terminal.

## Check and restore

```sh
python3 sddm/tests/check_install.py
sudo python3 sddm/install.py --rollback /var/lib/dotfiles/sddm-backups/TIMESTAMP
```

The automated installer checks use disposable directories. QML was also loaded
with the installed Qt 6 SDDM greeter in offscreen test mode. The mock preview
fixture checks submission and failed-login recovery without accessing PAM or
real accounts. Visual previews use the fictional account `nightowl`.

To render that fixture, prepare the theme, copy `tests/Preview.qml` into the build
directory as `Preview.qml`, then run the Qt 6 `qmlscene` tool from that directory.
Set `checkFailure: true` in the copied fixture to exercise failure recovery.
It writes `preview.png` alongside the prepared theme and exits. Run with
`QT_QPA_PLATFORM=offscreen QT_QUICK_BACKEND=software` for a headless preview.

The QML and accompanying theme files are original and MIT-licensed. See
[tokyo-night/LICENSE](tokyo-night/LICENSE).
