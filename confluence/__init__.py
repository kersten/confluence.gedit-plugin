import gedit
import gtk
import options
import os
import sys

import confluencerpclib
from confluencewidget import ConfluenceBrowser


class confluencePluginPlugin(gedit.Plugin):

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
        pass

    def deactivate(self, window):
        if self.options.loginPassed is True:
            self.unloadConfluenceBrowser(window)
        pass

    def update_ui(self, window):
        pass

    def unloadConfluenceBrowser(self, window):
        panel = window.get_side_panel()
        panel.remove_item(self.confluencewidget)
        self.confluence.logout()
