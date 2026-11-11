#!/usr/bin/env python3
"""Build a complete black 20px cursor theme from installed Adwaita assets."""
import argparse
import hashlib
import json
import math
import os
from pathlib import Path
import shutil
import struct
import subprocess
import tempfile

THEME = 'TokyoNight-Black'
SIZE = 20
SOURCE = Path('/usr/share/icons/Adwaita/cursors')
IMAGE = 0xfffd0002
MAGIC = 0x72756358


def images(path):
    data = path.read_bytes()
    magic, header, version, count = struct.unpack_from('<4I', data)
    if magic != MAGIC:
        raise ValueError('Invalid Xcursor: ' + str(path))
    frames = []
    for index in range(count):
        kind, nominal, offset = struct.unpack_from('<3I', data, header + 12 * index)
        if kind != IMAGE:
            continue
        chunk, _, _, _, width, height, xhot, yhot, delay = struct.unpack_from('<9I', data, offset)
        pixels = data[offset + chunk:offset + chunk + width * height * 4]
        if len(pixels) != width * height * 4:
            raise ValueError('Truncated Xcursor: ' + str(path))
        frames.append((nominal, width, height, xhot, yhot, delay, pixels))
    if not frames:
        raise ValueError('No cursor frames: ' + str(path))
    return frames


def scale(frame, nominal):
    old, width, height, xhot, yhot, delay, pixels = frame
    ratio = nominal / old
    w, h = max(1, round(width * ratio)), max(1, round(height * ratio))
    output = bytearray(w * h * 4)
    # Xcursor uses premultiplied BGRA. Interpolate those channels directly to
    # preserve transparent edges, outlines, and colours without dark halos.
    for y in range(h):
        sy = max(0, min(height - 1, (y + .5) * height / h - .5))
        y0 = math.floor(sy); y1 = min(height - 1, y0 + 1); fy = sy - y0
        for x in range(w):
            sx = max(0, min(width - 1, (x + .5) * width / w - .5))
            x0 = math.floor(sx); x1 = min(width - 1, x0 + 1); fx = sx - x0
            sources = ((y0 * width + x0) * 4, (y0 * width + x1) * 4, (y1 * width + x0) * 4, (y1 * width + x1) * 4)
            weights = ((1-fx)*(1-fy), fx*(1-fy), (1-fx)*fy, fx*fy)
            for channel in range(4):
                output[(y * w + x) * 4 + channel] = round(sum(pixels[i + channel] * weight for i, weight in zip(sources, weights)))
    return (nominal, w, h, min(w-1, round(xhot * ratio)), min(h-1, round(yhot * ratio)), delay, bytes(output))


def encode(frames):
    toc, chunks = [], []
    offset = 16 + len(frames) * 12
    for nominal, width, height, xhot, yhot, delay, pixels in frames:
        chunk = struct.pack('<9I', 36, IMAGE, nominal, 1, width, height, xhot, yhot, delay) + pixels
        toc.append(struct.pack('<3I', IMAGE, nominal, offset))
        chunks.append(chunk)
        offset += len(chunk)
    return struct.pack('<4I', MAGIC, 16, 0x10000, len(frames)) + b''.join(toc) + b''.join(chunks)


def build(home):
    if not SOURCE.is_dir():
        raise SystemExit('Install adwaita-icon-theme before building the cursor theme.')
    target = home / '.local/share/icons' / THEME
    source_id = hashlib.sha256(Path(__file__).read_bytes() + b''.join(p.read_bytes() for p in sorted(SOURCE.iterdir()) if p.is_file() and not p.is_symlink())).hexdigest()
    marker = target / 'build.json'
    if not marker.exists() or json.loads(marker.read_text()).get('source') != source_id:
        target.parent.mkdir(parents=True, exist_ok=True)
        with tempfile.TemporaryDirectory(prefix='.cursor-build-', dir=target.parent) as temporary:
            stage = Path(temporary)
            (stage / 'cursors').mkdir()
            for source in SOURCE.iterdir():
                destination = stage / 'cursors' / source.name
                if source.is_symlink():
                    # Preserve the complete installed alias set within this theme.
                    destination.symlink_to(os.readlink(source))
                    continue
                if not source.is_file():
                    continue
                frames = images(source)
                available = sorted(set(f[0] for f in frames))
                output = []
                for nominal in (SIZE, SIZE * 2, SIZE * 3):
                    nearest = min(available, key=lambda n: abs(n - nominal))
                    output.extend(scale(f, nominal) for f in frames if f[0] == nearest)
                destination.write_bytes(encode(output))
            (stage / 'index.theme').write_text('[Icon Theme]\nName=Tokyo Night Black\nComment=Complete black Adwaita cursor set at 20px\nInherits=Adwaita\n')
            (stage / 'build.json').write_text(json.dumps({'source': source_id, 'size': SIZE, 'base': 'Adwaita'}, indent=2)+'\n')
            for folder in (stage, stage / 'cursors'):
                folder.chmod(0o755)
            for file in stage.rglob('*'):
                if file.is_file() and not file.is_symlink():
                    file.chmod(0o644)
            if target.is_symlink():
                raise SystemExit('Refusing to replace a symlinked generated theme.')
            if target.exists():
                shutil.rmtree(target)
            shutil.copytree(stage, target, symlinks=True)
    # libXcursor and older clients search ~/.icons; GTK also finds the XDG path.
    legacy = home / '.icons' / THEME
    legacy.parent.mkdir(parents=True, exist_ok=True)
    if not os.path.lexists(legacy):
        legacy.symlink_to(os.path.relpath(target, legacy.parent))
    elif not legacy.is_symlink() or legacy.resolve() != target:
        raise SystemExit('Conflicting legacy cursor theme: ' + str(legacy))
    for name in ('default', 'pointer', 'text', 'wait', 'progress', 'ew-resize', 'ns-resize', 'grab', 'grabbing', 'crosshair', 'not-allowed'):
        if not (target / 'cursors' / name).is_file():
            raise SystemExit('Missing cursor shape: ' + name)
    print(f'{THEME}: complete {SIZE}px cursor theme built and verified.')


def live():
    environment = dict(os.environ, XCURSOR_THEME=THEME, XCURSOR_SIZE=str(SIZE))
    # Run inside the real desktop session (also invoked by autostart). Changing
    # environment variables cannot retroactively update an existing compositor.
    for key, value in (('cursor-theme', THEME), ('cursor-size', str(SIZE))):
        subprocess.run(['gsettings', 'set', 'org.gnome.desktop.interface', key, value], env=environment, check=True)
    if shutil.which('xrdb') and os.environ.get('DISPLAY'):
        subprocess.run(['xrdb', '-merge'], input=f'Xcursor.theme: {THEME}\nXcursor.size: {SIZE}\n', text=True, env=environment, check=True)
    if shutil.which('dbus-update-activation-environment'):
        subprocess.run(['dbus-update-activation-environment', 'XCURSOR_THEME', 'XCURSOR_SIZE'], env=environment, check=True)
    print('Desktop cursor preference updated. Log out and back in for compositor/app caches.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--live', action='store_true', help='also update preferences through the current desktop session bus')
    args = parser.parse_args()
    build(Path.home())
    if args.live:
        live()
