#!/usr/bin/env bash
# Each choice invokes only its own installer. No implicit full-desktop install.
set -euo pipefail
REPO_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
usage() {
    cat <<'HELP'
Usage: ./install.sh [sddm|wallpaper|widgets|cursor|discord|desktop|all|hyprland|niri|mango|quickshell|dms|companions] [--apply]

Without arguments: choose one component interactively (default: SDDM).
Without --apply: preview, or prepare the SDDM theme locally.
  sddm     SDDM login theme only (system install needs sudo)
  wallpaper Neon-sign desktop wallpaper only
  widgets  Desktop music card and audio visualizer only
  cursor   Cursor theme only
  discord  Equicord theme only
  desktop  Complete existing desktop rice, excluding SDDM
  all      Desktop rice and SDDM
  hyprland, niri, mango   Companion compositor + selected shell
  quickshell, dms         Select and install a companion shell
  companions             All companion compositors and both shell assets
HELP
}
component=""
apply=false
for arg in "$@"; do
    case "$arg" in
        --apply) apply=true ;;
        -h|--help) usage; exit 0 ;;
        sddm|wallpaper|widgets|cursor|discord|desktop|all|hyprland|niri|mango|quickshell|dms|companions)
            if [[ -n "$component" ]]; then echo 'Choose one component.' >&2; exit 2; fi
            component="$arg" ;;
        *) usage >&2; exit 2 ;;
    esac
done
if [[ -z "$component" ]]; then
    if [[ ! -t 0 ]]; then usage >&2; exit 2; fi
    printf '\nChoose what to install:\n  1) SDDM only [default]\n  2) Cursor only\n  3) Discord theme only\n  4) Desktop rice\n  5) Everything\n  6) Desktop wallpaper only\n  7) Music widget + visualizer only\n  8) All companion desktops (Quickshell selected)\n  9) DankMaterialShell companion\n  q) Quit\n'
    read -r -p 'Selection [1]: ' choice
    case "${choice:-1}" in
        1) component=sddm ;; 2) component=cursor ;; 3) component=discord ;;
        4) component=desktop ;; 5) component=all ;; 6) component=wallpaper ;; 7) component=widgets ;; 8) component=companions ;; 9) component=dms ;; q|Q) exit 0 ;;
        *) echo 'Invalid selection.' >&2; exit 2 ;;
    esac
    if ! "$apply"; then
        read -r -p "Apply $component? [y/N] " answer
        case "$answer" in y|Y|yes|YES) apply=true ;; esac
    fi
fi
# Avoid creating root-owned files in the user's home for desktop components.
if [[ "$EUID" -eq 0 && "$component" != sddm ]]; then
    echo 'Run this script as your normal user; SDDM requests sudo when needed.' >&2
    exit 2
fi
sddm_install() {
    if "$apply"; then
        if [[ "$EUID" -eq 0 ]]; then
            python3 "$REPO_DIR/sddm/install.py" --apply
        else
            sudo python3 "$REPO_DIR/sddm/install.py" --apply
        fi
    else
        python3 "$REPO_DIR/sddm/install.py"
    fi
}
desktop_install() {
    local flags=()
    if "$apply"; then flags+=(--apply); fi
    python3 "$REPO_DIR/install.py" "${flags[@]}"
}
case "$component" in
    hyprland|niri|mango|quickshell|dms|companions)
        flags=()
        if "$apply"; then flags+=(--apply); fi
        python3 "$REPO_DIR/companions/install.py" "$component" "${flags[@]}" ;;
    sddm) sddm_install ;;
    wallpaper|widgets)
        flags=()
        if "$apply"; then flags+=(--apply); fi
        python3 "$REPO_DIR/desktop/install.py" "$component" "${flags[@]}" ;;
    cursor)
        if "$apply"; then python3 "$REPO_DIR/cursor/apply.py"
        else echo "Would build cursor theme with: python3 $REPO_DIR/cursor/apply.py"; fi ;;
    discord)
        if "$apply"; then python3 "$REPO_DIR/discord/theme.py" --apply
        else python3 "$REPO_DIR/discord/theme.py"; fi ;;
    desktop) desktop_install ;;
    all) desktop_install; sddm_install ;;
esac
