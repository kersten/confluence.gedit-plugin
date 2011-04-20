from gi.repository import GObject, Gtk, Gdk, Gedit, GdkPixbuf, Peas, PeasGtk, Gio

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
from options import ConfluenceBrowserConfigWidget

from panel import ConfluenceBrowserPanel

class ConfluencePlugin(GObject.Object, Gedit.WindowActivatable, PeasGtk.Configurable):
    __gtype_name__ = "Confluence"

    window = GObject.property(type=Gedit.Window)

    def __init__(self):
        GObject.Object.__init__(self)

        print sys.getdefaultencoding()

    def do_activate(self):
        self.confluencewidget = ConfluenceBrowserPanel(self.window)
        self.options = ConfluenceBrowserConfigWidget()
        
        if self.options._settings.get_boolean(self.options.LOGINPASSED) is True:
            self.confluence = confluencerpclib.Confluence(self.options._settings.get_string(self.options.URL), True)
            self.confluence.login(self.options._settings.get_string(self.options.USERNAME), self.options._settings.get_string(self.options.PASSWORD))
            self.confluencewidget.loadConfluenceBrowser(self.window, self.confluence)

    def do_deactivate(self):
        panel = self.window.get_side_panel()
        panel.remove_item(panel)

    def do_update_state(self):
        pass

    def do_create_configure_widget(self):
        config_widget = ConfluenceBrowserConfigWidget()

        return config_widget.configure_widget(self.plugin_info.get_data_dir())

    def create_confluence_browser_panel(self):
        self.panel = ConfluenceBrowserPanel(self.window)

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
