#!/usr/bin/env sh
set -e

REPO_ROOT="$(git rev-parse --show-toplevel 2>/dev/null || true)"

if [ -z "$REPO_ROOT" ]; then
  echo "Not inside a Git repository."
  exit 1
fi

if [ "$PWD" != "$REPO_ROOT" ]; then
  echo "Please run this script from the repo root:"
  echo "  $REPO_ROOT"
  exit 1
fi


sudo cp -r ./nixos/ /etc/nixos/

sudo nixos-rebuild switch --flake .#don

cp -r /mnt/storage/.ssh ~/.ssh
chmod 700 ~/.ssh

cp -r /mnt/storage/kde/config/* ~/.config/
cp -r /mnt/storage/kde/local-share/* ~/.local/share/
chown -R "$USER:$USER" ~/.config ~/.local/share