#!/usr/bin/env python3
"""Exercise system installation and rollback against disposable directories."""
import importlib.util
from pathlib import Path
import tempfile

source = Path(__file__).resolve().parents[1] / 'install.py'
spec = importlib.util.spec_from_file_location('sddm_installer', source)
installer = importlib.util.module_from_spec(spec)
spec.loader.exec_module(installer)

for existing in (False, True):
    with tempfile.TemporaryDirectory() as temporary:
        root = Path(temporary)
        installer.DEST = root / 'usr/share/sddm/themes/tokyo-night'
        installer.DROPIN = root / 'etc/sddm.conf.d/90-tokyo-night.conf'
        installer.LEGACY = root / 'etc/sddm.conf'
        installer.BACKUPS = root / 'var/lib/dotfiles/sddm-backups'
        original = '# Keep this comment\n[Users]\nRememberLastUser=true\n[Theme]\nCurrent=previous-theme\nThemeDir=/previous/path\n'
        if existing:
            installer.LEGACY.parent.mkdir(parents=True)
            installer.LEGACY.write_text(original)
            installer.DROPIN.parent.mkdir(parents=True)
            installer.DROPIN.write_text('[Theme]\nCurrent=old\n')
            installer.DEST.mkdir(parents=True)
            (installer.DEST / 'original.txt').write_text('previous theme\n')
        installer.install()
        installer.verify_theme(installer.DEST)
        assert 'Current=tokyo-night' in installer.DROPIN.read_text()
        if existing:
            text = installer.LEGACY.read_text()
            assert '# Keep this comment' in text and 'RememberLastUser=true' in text
            assert 'Current=tokyo-night' in text and 'ThemeDir=/usr/share/sddm/themes' in text
        backup = next(installer.BACKUPS.iterdir())
        installer.rollback(backup)
        if existing:
            assert installer.LEGACY.read_text() == original
            assert installer.DROPIN.read_text() == '[Theme]\nCurrent=old\n'
            assert (installer.DEST / 'original.txt').read_text() == 'previous theme\n'
            assert not (installer.DEST / 'Main.qml').exists()
        else:
            assert not installer.DROPIN.exists() and not installer.LEGACY.exists() and not installer.DEST.exists()
print('Clean install, replacement install, legacy precedence, backups, and rollback passed.')
