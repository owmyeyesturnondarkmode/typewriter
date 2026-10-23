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
gi.require_version("Adw", "1")

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
        self.file_chooser = None
        self.current_file = None
        self.document_title = "untitled — Typewriter"
        self.is_dirty = False

        open_action = Gio.SimpleAction.new("open", None)
        open_action.connect("activate", lambda *_args: self.open_file(None))
        self.add_action(open_action)
        self.set_accels_for_action("app.open", ["<Primary>o"])

        save_action = Gio.SimpleAction.new("save", None)
        save_action.connect("activate", lambda *_args: self.save_file(None))
        self.add_action(save_action)
        self.set_accels_for_action("app.save", ["<Primary>s"])

    def _show_editor(self, editor_content="", title="Typewriter"):
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

        header_bar = Adw.HeaderBar()

        open_button = Gtk.Button.new_from_icon_name("document-open-symbolic")
        open_button.set_tooltip_text("Open")
        open_button.connect("clicked", self.open_file)
        header_bar.pack_start(open_button)

        save_button = Gtk.Button.new_from_icon_name("document-save-symbolic")
        save_button.set_tooltip_text("Save")
        save_button.connect("clicked", self.save_file)
        header_bar.pack_end(save_button)

        self.window.set_titlebar(header_bar)

        scroller = Gtk.ScrolledWindow()
        scroller.set_child(self.text_view)
        self.window.set_child(scroller)

        self.document_title = title
        buffer = self.text_view.get_buffer()
        buffer.connect("changed", self._on_buffer_changed)
        buffer.set_text(editor_content)
        self.is_dirty = False
        self._update_window_title()
        self.window.present()
        return self.window

    def _on_buffer_changed(self, _buffer):
        self.is_dirty = True
        self._update_window_title()

    def _update_window_title(self):
        if self.window is not None:
            marker = "*" if self.is_dirty else ""
            self.window.set_title(f"{marker}{self.document_title}")

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

        self.current_file = file
        self._show_editor(text, f"{file.get_basename()} — Typewriter")

    def open_file(self, _button):
        self.file_chooser = Gtk.FileChooserNative.new(
            "Open File",
            self.window,
            Gtk.FileChooserAction.OPEN,
            "_Open",
            "_Cancel",
        )
        self.file_chooser.connect("response", self._on_open_response)
        self.file_chooser.show()

    def save_file(self, _button):
        if self.current_file is not None:
            self._write_current_file()
            return

        self.file_chooser = Gtk.FileChooserNative.new(
            "Save File",
            self.window,
            Gtk.FileChooserAction.SAVE,
            "_Save",
            "_Cancel",
        )
        self.file_chooser.set_current_name("untitled.txt")
        self.file_chooser.connect("response", self._on_save_response)
        self.file_chooser.show()

    def _write_current_file(self):
        buffer = self.text_view.get_buffer()
        contents = buffer.get_text(
            buffer.get_start_iter(), buffer.get_end_iter(), True
        ).encode("utf-8")
        try:
            self.current_file.replace_contents(
                contents, None, False, Gio.FileCreateFlags.NONE, None
            )
            self.is_dirty = False
            self._update_window_title()
            return True
        except GLib.Error as error:
            print(f"Could not save file: {error}")
            return False

    def _on_save_response(self, chooser, response):
        if response == Gtk.ResponseType.ACCEPT:
            self.current_file = chooser.get_file()
            self.document_title = (
                f"{self.current_file.get_basename()} — Typewriter"
            )
            self._write_current_file()
            self._update_window_title()

        chooser.destroy()
        self.file_chooser = None

    def _on_open_response(self, chooser, response):
        if response == Gtk.ResponseType.ACCEPT:
            file = chooser.get_file()
            try:
                _success, contents, _etag = file.load_contents(None)
                text = contents.decode("utf-8")
                self.current_file = file
                self.document_title = f"{file.get_basename()} — Typewriter"
                self.text_view.get_buffer().set_text(text)
                self.is_dirty = False
                self._update_window_title()
            except (GLib.Error, UnicodeDecodeError) as error:
                print(f"Could not open file: {error}")

        chooser.destroy()
        self.file_chooser = None

app = Typewriter()
app.run(sys.argv)