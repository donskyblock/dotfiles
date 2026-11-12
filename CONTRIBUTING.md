# Contributing

Found something broken, confusing or just awkward to use? Open an issue. Small
fixes, clearer docs and reports from other machines are all welcome.

[Back to the README](README.md) · [Keybinds](KEYBINDS.md)

## Reporting a problem

Check existing issues first, then open one with:

- What you were trying to do, and what happened instead.
- The command you ran and the relevant error output.
- Your distro, desktop/compositor and affected app versions.
- Whether this was a fresh install or an update to an existing setup.
- Steps to reproduce it, if you have them.

For visual problems, a screenshot helps. Crop out private tabs, notifications and
account details. Read logs before posting them and remove credentials or personal
information. If you're unsure whether something is a bug, it's fine to ask.

This setup is primarily for Void Linux with COSMIC. Reports from other distros
are useful too; mention anything you had to change to get it working.

## Suggesting a change

Explain the problem you'd like solved and how you use the setup. For a bigger
change, such as another desktop or a new dependency, open an issue before spending
a lot of time on it. A typo or small fix can go straight to a pull request.

## Sending a fix

1. Fork the repository and make a branch for your change.
2. Keep the change focused. Follow the style of the surrounding config or script.
3. Update the relevant guide when behaviour, dependencies or installation steps
   change. Update [KEYBINDS.md](KEYBINDS.md) when changing shortcuts.
4. Check your diff and explain what you tested in the pull request. For appearance
   changes, include a screenshot when you can.

Don't apply the entire desktop just to test a small change. Use the component's
preview first, then test in a disposable home or a session you can restore. For
installer changes, check that existing files are backed up, repeat installs work,
and preview mode doesn't apply changes. SDDM's preview does prepare local assets.

Useful checks from the repository root:

```sh
git diff --check
python3 companions/check_install.py     # companion installer changes
python3 sddm/tests/check_install.py     # SDDM installer changes
```

Run the checks relevant to your change. If you couldn't test a desktop or app
live, say so in the pull request.

## Adding files

This repository ignores new paths by default and checks an explicit public-file
allowlist before committing.

- Allow new files and any ignored parent directories in `.gitignore`.
- For configs installed by the main symlink installer, add the home-relative path
  to `manifest.txt`. `check-public.py` derives those allowed paths from the manifest.
- For documentation, scripts or other component assets, add the path to the
  allowlist in `check-public.py`.
- Include the source and license for any third-party material you add.

Stage only the intended files, then review and check them:

```sh
git diff --cached
python3 check-public.py
```

That check reads the **Git index**, so new files and manifest changes need to be
staged first. Keep credentials, private keys, browser profiles, history and local
backups out of commits. The checker is a useful guard, but it can't catch everything.

Keep feedback respectful and specific. You don't need a perfect patch to start a
conversation about something that could work better.
