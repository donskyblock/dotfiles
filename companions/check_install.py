#!/usr/bin/env python3
"""Exercise installer behavior in an isolated home, without starting a desktop."""
import importlib.util
import json
from pathlib import Path
import tempfile

spec = importlib.util.spec_from_file_location('companions_install', Path(__file__).with_name('install.py'))
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
with tempfile.TemporaryDirectory(prefix='companions-check-') as folder:
    home = Path(folder)
    settings = home / '.config/DankMaterialShell/settings.json'
    settings.parent.mkdir(parents=True)
    original = '{"volumeStep": 7, "currentThemeName": "old"}\n'
    settings.write_text(original)
    files = module.plan('companions', 'dms', home)
    assert settings.read_text() == original  # planning is read-only
    module.install(files, home)
    data = json.loads(settings.read_text())
    assert data['volumeStep'] == 7 and data['currentThemeName'] == 'custom'
    assert Path(data['customThemeFile']).is_file()
    backups = list((home / '.local/state/dotfiles/backups').glob('companions-*'))
    assert len(backups) == 1
    assert (backups[0] / settings.relative_to(home)).read_text() == original
    module.install(module.plan('companions', 'dms', home), home)
    assert len(list(backups[0].parent.iterdir())) == 1
    assert (home / '.local/bin/after-hours-shell').stat().st_mode & 0o777 == 0o755
    for component in ('hyprland', 'niri', 'mango', 'quickshell', 'dms'):
        assert module.plan(component, 'dms' if component == 'dms' else 'quickshell', home)
    assert '.config/hypr/hyprland.conf' in module.plan('hyprland', 'quickshell', home, True)
    settings.write_text('[]')
    try:
        module.plan('dms', 'dms', home)
    except ValueError:
        pass
    else:
        raise AssertionError('Non-object settings accepted')
    settings.write_text(original)
    (home / '.config/niri').rename(home / '.config/niri-original')
    (home / '.config/niri').symlink_to(home / '.config/DankMaterialShell', target_is_directory=True)
    try:
        module.plan('niri', 'quickshell', home)
    except ValueError:
        pass
    else:
        raise AssertionError('Symlinked parent accepted')
print('Companion installer checks passed.')
