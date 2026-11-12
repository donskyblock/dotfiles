#!/usr/bin/env python3
"""After Hours: a COSMIC/Wayland desktop music card. No remote content loaded."""
import argparse
import cairo
import json
import os
from pathlib import Path
import signal
import subprocess
import threading

import gi
gi.require_version('Gtk', '3.0')
gi.require_version('Gdk', '3.0')
from gi.repository import Gdk, Gio, GLib, Gtk, Pango

BASE = Path(__file__).resolve().parent
BUS_NAME = 'org.mpris.MediaPlayer2.'
PLAYER = 'org.mpris.MediaPlayer2.Player'
OBJECT = '/org/mpris/MediaPlayer2'
BARS = 32


def unpack(value):
    if isinstance(value, GLib.Variant):
        return unpack(value.unpack())
    if isinstance(value, dict):
        return {k: unpack(v) for k, v in value.items()}
    if isinstance(value, (tuple, list)):
        return [unpack(v) for v in value]
    return value


def choose_player(players, previous=None):
    """Keep a playing player stable; otherwise prefer playback over idle apps."""
    playing = [p for p in players if p['PlaybackStatus'] == 'Playing']
    pool = playing or players
    return next((p for p in pool if p['bus'] == previous), pool[0] if pool else None)


class Music(Gtk.Application):
    def __init__(self, preview=False):
        super().__init__(application_id='io.dotfiles.AfterHours', flags=Gio.ApplicationFlags.HANDLES_COMMAND_LINE)
        self.preview = preview
        self.window = None
        self.player = None
        self.properties = {}
        self.levels = [0.0] * BARS
        self.cava = None
        self.closed = False
        self.polling = False
        self.audio_available = False
        self.connect('command-line', self.command_line)
        self.connect('shutdown', self.shutdown)

    def command_line(self, app, command):
        argv = command.get_arguments()
        if '--quit' in argv:
            self.quit()
        elif '--status' in argv:
            command.print_literal(json.dumps({
                'running': self.window is not None,
                'player_connected': self.player is not None,
                'audio_frames_received': self.audio_available,
                'spectrum_bars': len(self.levels),
                'playback_controls_enabled': any(b.get_sensitive() for b in self.buttons.values()) if self.window else False,
            }) + '\n')
        elif '--snapshot' in argv and self.window:
            destination = argv[argv.index('--snapshot') + 1]
            box = self.window.get_child()
            self.window.check_resize()
            box.size_allocate(box.get_allocation())
            surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, box.get_allocated_width(), box.get_allocated_height())
            box.draw(cairo.Context(surface))
            surface.write_to_png(destination)
        else:
            self.activate()
        return 0

    def do_activate(self):
        if self.window:
            return
        settings = json.loads((BASE / 'settings.json').read_text())
        self.window = Gtk.ApplicationWindow(application=self, title='After Hours')
        self.window.set_default_size(settings['width'], -1)
        self.window.set_resizable(False)
        self.window.set_decorated(False)
        self.window.set_app_paintable(True)
        visual = self.window.get_screen().get_rgba_visual()
        if visual:
            self.window.set_visual(visual)
        if not self.preview:
            gi.require_version('GtkLayerShell', '0.1')
            from gi.repository import GtkLayerShell as Layer
            if not Layer.is_supported():
                raise RuntimeError('The compositor does not support Wayland layer shell.')
            Layer.init_for_window(self.window)
            Layer.set_namespace(self.window, 'dotfiles-after-hours')
            Layer.set_layer(self.window, Layer.Layer.BOTTOM)
            Layer.set_keyboard_mode(self.window, Layer.KeyboardMode.NONE)
            Layer.set_exclusive_zone(self.window, 0)
            Layer.set_anchor(self.window, Layer.Edge.RIGHT, True)
            Layer.set_anchor(self.window, Layer.Edge.BOTTOM, True)
            Layer.set_margin(self.window, Layer.Edge.RIGHT, settings['right'])
            Layer.set_margin(self.window, Layer.Edge.BOTTOM, settings['bottom'])
            display = Gdk.Display.get_default()
            if 0 <= settings['monitor'] < display.get_n_monitors():
                Layer.set_monitor(self.window, display.get_monitor(settings['monitor']))
        css = Gtk.CssProvider()
        css.load_from_path(str(BASE / 'style.css'))
        Gtk.StyleContext.add_provider_for_screen(self.window.get_screen(), css, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        box.get_style_context().add_class('music-card')
        self.window.add(box)
        self.status = self.label('AFTER HOURS / READY', 'eyebrow')
        self.title = self.label('Nothing playing', 'title')
        self.artist = self.label('Open a music player to begin.', 'artist')
        for label in (self.status, self.title, self.artist):
            box.pack_start(label, False, False, 0)
        self.spectrum = Gtk.DrawingArea()
        self.spectrum.set_size_request(-1, 64)
        self.spectrum.connect('draw', self.draw)
        box.pack_start(self.spectrum, False, False, 4)
        controls = Gtk.Box(spacing=10)
        self.buttons = {}
        for method, caption in [('Previous', '⏮'), ('PlayPause', '▶'), ('Next', '⏭')]:
            button = Gtk.Button(label=caption)
            button.set_tooltip_text({'Previous': 'Previous track', 'PlayPause': 'Play / pause', 'Next': 'Next track'}[method])
            button.connect('clicked', lambda _, m=method: self.control(m))
            button.set_sensitive(False)
            controls.pack_start(button, True, True, 0)
            self.buttons[method] = button
        box.pack_start(controls, False, False, 0)
        self.hint = self.label('SYSTEM AUDIO · WAITING', 'hint')
        box.pack_start(self.hint, False, False, 0)
        self.window.show_all()
        self.start_cava()
        self.poll()
        GLib.timeout_add_seconds(2, self.poll)

    @staticmethod
    def label(text, name):
        label = Gtk.Label(label=text, xalign=0)
        label.set_ellipsize(Pango.EllipsizeMode.END)
        label.set_max_width_chars(34)
        label.get_style_context().add_class(name)
        return label

    def poll(self):
        if self.closed or self.polling:
            return not self.closed
        self.polling = True
        threading.Thread(target=self.read_players, daemon=True).start()
        return True

    def read_players(self):
        players = []
        try:
            bus = Gio.bus_get_sync(Gio.BusType.SESSION, None)
            names = bus.call_sync('org.freedesktop.DBus', '/org/freedesktop/DBus', 'org.freedesktop.DBus', 'ListNames', None, None, Gio.DBusCallFlags.NONE, 700, None).unpack()[0]
            for name in sorted(n for n in names if n.startswith(BUS_NAME)):
                try:
                    result = bus.call_sync(name, OBJECT, 'org.freedesktop.DBus.Properties', 'GetAll', GLib.Variant('(s)', (PLAYER,)), None, Gio.DBusCallFlags.NONE, 500, None)
                    props = unpack(result)[0]
                    props['bus'] = name
                    props.setdefault('PlaybackStatus', 'Stopped')
                    players.append(props)
                except GLib.Error:
                    continue  # Player may have exited while enumerating it.
        except GLib.Error:
            pass
        GLib.idle_add(self.update_player, choose_player(players, self.player))

    def update_player(self, player):
        self.polling = False
        if self.closed:
            return False
        self.properties = player or {}
        self.player = player['bus'] if player else None
        meta = self.properties.get('Metadata', {})
        status = self.properties.get('PlaybackStatus', 'Stopped')
        title = meta.get('xesam:title') or 'Nothing playing'
        artists = meta.get('xesam:artist', [])
        artist = ', '.join(artists) if isinstance(artists, list) else str(artists)
        self.title.set_text(title)
        self.title.set_tooltip_text(title)
        self.artist.set_text(artist or ('Media player connected' if player else 'Open a music player to begin.'))
        self.artist.set_tooltip_text(artist)
        self.status.set_text('AFTER HOURS / ' + (status.upper() if player else 'READY'))
        can = self.properties.get('CanControl', False)
        for method, capability in [('Previous', 'CanGoPrevious'), ('Next', 'CanGoNext'), ('PlayPause', 'CanPause' if status == 'Playing' else 'CanPlay')]:
            self.buttons[method].set_sensitive(can and self.properties.get(capability, False))
        self.buttons['PlayPause'].set_label('Ⅱ' if status == 'Playing' else '▶')
        return False

    def control(self, method):
        if not self.player:
            return
        try:
            bus = Gio.bus_get_sync(Gio.BusType.SESSION, None)
            bus.call(self.player, OBJECT, PLAYER, method, None, None, Gio.DBusCallFlags.NONE, 1000, None, self.control_done)
        except GLib.Error:
            self.poll()

    def control_done(self, bus, result):
        try:
            bus.call_finish(result)
        except GLib.Error:
            pass
        self.poll()

    def start_cava(self):
        try:
            self.cava = subprocess.Popen(['cava', '-p', str(BASE / 'cava.conf')], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
            threading.Thread(target=self.read_audio, daemon=True).start()
        except OSError:
            self.hint.set_text('VISUALIZER UNAVAILABLE · INSTALL CAVA')

    def read_audio(self):
        # Coalesce frames: at most one update is queued on GTK's main loop.
        self.latest_frame = None
        self.frame_pending = False
        for line in self.cava.stdout:
            try:
                levels = [max(0, min(1, int(v) / 1000)) for v in line.decode('ascii').strip().split(';') if v]
            except (ValueError, UnicodeError):
                continue
            if len(levels) == BARS and not self.closed:
                self.latest_frame = levels
                if not self.frame_pending:
                    self.frame_pending = True
                    GLib.idle_add(self.update_audio)
        if not self.closed:
            GLib.idle_add(self.audio_stopped)

    def update_audio(self):
        self.frame_pending = False
        if self.closed:
            return False
        self.levels = self.latest_frame
        self.audio_available = True
        self.spectrum.queue_draw()
        self.hint.set_text('SYSTEM AUDIO · LIVE' if max(self.levels) > 0.005 else 'SYSTEM AUDIO · QUIET')
        return False

    def audio_stopped(self):
        self.levels = [0.0] * BARS
        self.spectrum.queue_draw()
        self.hint.set_text('AUDIO UNAVAILABLE · CHECK CAVA / PIPEWIRE')
        return False

    def draw(self, widget, cr):
        w, h = widget.get_allocated_width(), widget.get_allocated_height()
        step = w / BARS
        for i, value in enumerate(self.levels):
            # Cyan-to-lavender gradient across real frequency bins; silence is flat.
            t = i / (BARS - 1)
            cr.set_source_rgba(0.49 + 0.24*t, 0.81 - 0.2*t, 0.98, 0.9)
            height = max(2, value * (h - 2))
            cr.rectangle(i * step, h - height, max(1, step - 3), height)
            cr.fill()
        return False

    def shutdown(self, *_):
        self.closed = True
        if self.cava:
            self.cava.terminate()
            try:
                self.cava.wait(timeout=2)
            except subprocess.TimeoutExpired:
                self.cava.kill()
                self.cava.wait()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--preview', action='store_true', help='ordinary window for previewing without layer shell')
    parser.add_argument('--status', action='store_true', help='report widget connection health without song details')
    parser.add_argument('--snapshot', type=Path, help='save just the running widget as a PNG')
    parser.add_argument('--quit', action='store_true', help='stop the running widget')
    args = parser.parse_args()
    if not args.preview and not args.quit:
        try:
            gi.require_version('GtkLayerShell', '0.1')
        except ValueError:
            raise SystemExit('Missing gtk-layer-shell. On Void: sudo xbps-install gtk-layer-shell')
    app = Music(args.preview)
    GLib.unix_signal_add(GLib.PRIORITY_DEFAULT, signal.SIGTERM, lambda: (app.quit(), False)[1])
    forwarded = ['--quit'] if args.quit else ['--status'] if args.status else ['--snapshot', str(args.snapshot)] if args.snapshot else []
    raise SystemExit(app.run([__file__] + forwarded))
