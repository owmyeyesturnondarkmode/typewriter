#!/usr/bin/env python3

copyright = """
Typewriter, a minimalist text editor based on libadw and GTK4.
Copyright (C) 2026 Jonathan Vacek <jonathanjames1941@outlook.com> 

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>
"""

import sys

import gi

gi.require_version("Gtk", "4.0")

from gi.repository import Gtk, Adw, GLib, Gio

print(copyright)

class Typewriter(Adw.Application):
    def __init__(self):
        super().__init__(
            application_id="com.typewriter.Typewriter",
            flags=Gio.ApplicationFlags.HANDLES_OPEN,
        )
        GLib.set_application_name("Typewriter")
        self.window = None
        self.text_view = None

    def _show_editor(self, editor_content="", title="Typewriter"):
        if self.window is None:
            Adw.StyleManager.get_default().set_color_scheme(
                Adw.ColorScheme.FORCE_LIGHT
            )

            self.window = Gtk.ApplicationWindow(
                application=self, title="Typewriter"
            )
            self.window.set_default_size(800, 600)

            self.text_view = Gtk.TextView()
            self.text_view.set_left_margin(10)
            self.text_view.set_top_margin(10)
            self.text_view.set_bottom_margin(10)

            scroller = Gtk.ScrolledWindow()
            scroller.set_child(self.text_view)
            self.window.set_child(scroller)

        self.text_view.get_buffer().set_text(editor_content)
        self.window.set_title(title)
        self.window.present()
        return self.window

    def do_activate(self):
        self._show_editor(title="untitled — Typewriter")

    def do_open(self, files, n_files, hint):
        file = files[0]
        try:
            _success, contents, _etag = file.load_contents(None)
            text = contents.decode("utf-8")
        except (GLib.Error, UnicodeDecodeError) as error:
            print(f"Could not open file: {error}")
            return

        self._show_editor(text, f"{file.get_basename()} — Typewriter")

app = Typewriter()
app.run(sys.argv)