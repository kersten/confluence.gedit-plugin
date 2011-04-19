from gi.repository import GObject, Gtk, Gdk, Gedit, GdkPixbuf

import os
import sys
import urllib
import gettext

try:
    gettext.bindtextdomain(GETTEXT_PACKAGE, GP_LOCALEDIR)
    _ = lambda s: gettext.dgettext(GETTEXT_PACKAGE, s);
except:
    _ = lambda s: s

import confluencerpclib
from panel import ConfluenceBrowserPanel

#import options

class ConfluencePlugin(GObject.Object, Gedit.WindowActivatable):
    __gtype_name__ = "Confluence"

    window = GObject.property(type=Gedit.Window)

    def __init__(self):
        GObject.Object.__init__(self)

    def do_activate(self):
        #self.editor_settings = Gio.Settings.new("org.gnome.gedit.preferences.editor")
        #self.editor_settings.connect("changed::use-default-font", self.font_changed)
        #self.editor_settings.connect("changed::editor-font", self.font_changed)
        #self.system_settings = Gio.Settings.new("org.gnome.desktop.interface")
        #self.system_settings.connect("changed::monospace-font-name", self.font_changed)

        panel = self.window.get_side_panel()
        
        f = urllib.urlopen('https://confluence.nurago.com/favicon.ico')
        data = f.read()
        pbl = GdkPixbuf.PixbufLoader()
        pbl.write(data)
        pixbuf = pbl.get_pixbuf()
        pbl.close()

        image = Gtk.Image()
        image.set_from_pixbuf(pixbuf)

        self.create_confluence_browser_panel()
        panel.add_item(self.panel, "ConfluenceBrowserPanel", _("Confluence Browser"), image)

        statusbar = self.window.get_statusbar()
        self.context_id = statusbar.get_context_id("Confluence Description")

    def do_deactivate(self):
        panel = self.window.get_side_panel()
        panel.remove_item(self.panel)

    def do_update_state(self):
        pass

    def create_confluence_browser_panel(self):
        self.panel = ConfluenceBrowserPanel()

        # Use the same font as the document
        #self.font_changed()

        #chartable.connect("notify::active-character", self.on_table_sync_active_char)
        #chartable.connect("focus-out-event", self.on_table_focus_out_event)
        #chartable.connect("status-message", self.on_table_status_message)
        #chartable.connect("activate", self.on_table_activate)

        self.panel.show()

'''class confluencePluginPlugin(gedit.Plugin):

    def __init__(self):
        gedit.Plugin.__init__(self)

    def create_configure_dialog(self):
        return self.options.create_configure_dialog()

    def is_configurable(self):
        return True

    def activate(self, window):
        self.confluencewidget = ConfluenceBrowser(window)
        self.options = options.options(window, self.confluencewidget)

        if self.options.loginPassed is True:
            self.confluence = confluencerpclib.Confluence(self.options.url, True)
            self.confluence.login(self.options.username, self.options.password)
            self.confluencewidget.loadConfluenceBrowser(window, self.confluence)

    def deactivate(self, window):
        if self.options.loginPassed is True:
            self.unloadConfluenceBrowser(window)
            panel = window.get_side_panel()
            panel.remove_item(self.confluencewidget)
            self.confluence.logout()

    def update_ui(self, window):
        pass

    def unloadConfluenceBrowser(self, window):
        panel = window.get_side_panel()
        panel.remove_item(self.confluencewidget)
        self.confluence.logout()
'''
