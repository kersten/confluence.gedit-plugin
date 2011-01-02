import gedit
import gtk
import options
import os
import sys

from confluencerpclib import Confluence
from confluencewidget import ConfluenceBrowser


class confluencePluginPlugin(gedit.Plugin):

    def __init__(self):
        gedit.Plugin.__init__(self)

    def create_configure_dialog(self):
        return self.options.create_configure_dialog()

    def is_configurable(self):
        return True

    def activate(self, window):
        self.options = options.options()
        #options.singleton().confluenceLogin()
        #print confluenceApi.singleton().getSpaces()
        #print confluenceApi.singleton().getPages('SupportDaphne')
        #print confluenceApi.singleton().getPageById('29458504')
        #self.confluence = Confluence(self.options.url, True)
        #self.confluence.login(self.options.username, self.options.password)

        #print self.confluence.token
        #self.confluence.getPage('29458504')
        confluencewidget = ConfluenceBrowser(window)

        if self.options.loginPassed is True:
            confluencewidget.loadConfluenceBrowser(window)
        pass

    def deactivate(self, window):
        if self.options.loginPassed is True:
            self.unloadConfluenceBrowser(window)
            self.confluence.logout()
        pass

    def update_ui(self, window):
        pass

    def unloadConfluenceBrowser(self, window):
        pane = window.get_side_panel()
        pane.remove_item(self.confluencebrowser)
        windowdata = window.get_data("ConfluenceBrowserPluginWindowDataKey")
        manager = window.get_ui_manager()
        manager.remove_action_group(windowdata["action_group"])
