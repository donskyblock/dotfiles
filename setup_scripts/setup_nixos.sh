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

# NixOS

sudo cp -r ./nixos/ /etc/nixos/

sudo nixos-rebuild switch --flake .#don

# SSH
cp -r /mnt/storage/.ssh ~/.ssh
chmod 700 ~/.ssh


# KDE
cp -r /mnt/storage/kde/config/* ~/.config/
cp -r /mnt/storage/kde/local-share/* ~/.local/share/
chown -R "$USER:$USER" ~/.config ~/.local/share

# Prism
cp /mnt/stroage/creds/accounts.json ~/.local/share/PrismLauncher/

# Create Utils I use

mkdir ~/development
mkdir ~/code-course
mkdir ~/Documents/saved-gifs
mkdir ~/Pictures/OpenCom-Files

# Pull some of my utils I use for OpenCom not currently up tho

# git pull  

# Clone Some Projects Im always working on

cd ~/Development 

git clone git@github.com:donskyblock/OpenCom.git

git clone git@github.com:donskyblock/donskyblock-site.git

git clone git@github.com:donskyblock/MicReactive.git

# Script to clone some other private repos

# Create the target folder
mkdir -p ~/tmp/private-scripts

# Check if the source folder exists
if [ -d "/mnt/storage/scripts" ]; then
    # Copy and execute private-repos.sh
    cp /mnt/storage/scripts/private-repos.sh ~/tmp/private-scripts/private-repos.sh
    bash ~/tmp/private-scripts/private-repos.sh

    # Copy and execute misc-private.sh
    cp /mnt/storage/scripts/misc-private.sh ~/tmp/private-scripts/private.sh
    bash ~/tmp/private-scripts/private.sh
else
    echo "/mnt/storage/scripts does not exist. Skipping private scripts."
fi