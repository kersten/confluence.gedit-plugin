import gtk.glade
import gconf
import os
import sys

from confluencerpclib import Confluence
from confluencewidget import ConfluenceBrowser


class options():

    __shared_state = {}

    def __init__(self, initWindow=None, confluencewidget=None):
        self.__dict__ = self.__shared_state
        
        self.initWindow = initWindow
        self.confluencewidget = confluencewidget

        self.__gconfDir = "/apps/gedit-2/plugins/confluence"
        # create gconf directory if not set yet
        self.client = gconf.client_get_default()
        if not self.client.dir_exists(self.__gconfDir):
            self.client.add_dir(self.__gconfDir, gconf.CLIENT_PRELOAD_NONE)

        self.username = ""
        self.password = ""
        self.url = "https://your.confluence.url/rpc/xmlrpc"
        self.loginPassed = False

        # get the gconf keys, or stay with default if key not set
        try:
            self.username = self.client.get_string(
                self.__gconfDir + "/username") \
                or self.username

            self.password = self.client.get_string(
                self.__gconfDir + "/password") \
                or self.password

            self.url = self.client.get_string(
                self.__gconfDir + "/url") or self.url

            self.loginPassed = self.client.get_bool(
                self.__gconfDir + "/loginPassed") or self.loginPassed

        except Exception, e: # catch, just in case
            print e

    def create_configure_dialog(self):
        print self.initWindow
        print self.confluencewidget
        self.dialogGladeFile = os.path.join(sys.path[0], "confluence",
                               "confluencePluginConfigureDialog.glade")

        self.dialog = gtk.Builder()
        self.dialog.add_from_file(self.dialogGladeFile)
        #self.dialog.connect_signals(self)

        self.dialogWindow = self.dialog.get_object(
                            "confluencePluginConfigureDialog")

        self.dialogWindowUsername = self.dialog.get_object("loginUsername")
        self.dialogWindowUsername.set_text(self.username)

        self.dialogWindowPassword = self.dialog.get_object("loginPassword")
        self.dialogWindowPassword.set_text(self.password)

        self.dialogWindowUrl = self.dialog.get_object("loginURL")
        self.dialogWindowUrl.set_text(self.url)

        self.dialogSignals = {
            "on_closeButton_clicked": self.on_closeButton_clicked,
            "on_testButton_clicked": self.on_testButton_clicked,
            "on_removeCredentials_clicked": self._removeCredentials,
            "on_loginUsername_changed": self._inputChanged,
            "on_loginPassword_changed": self._inputChanged,
            "on_loginURL_changed": self._inputChanged}
        self.dialog.connect_signals(self.dialogSignals)

        return self.dialogWindow

    def on_closeButton_clicked(self, widget):
        self.username = self.dialogWindowUsername.get_text()
        self.password = self.dialogWindowPassword.get_text()
        self.url = self.dialogWindowUrl.get_text()

         # write changes to gconf
        self.client = gconf.client_get_default()

        self.client.set_string(self.__gconfDir + "/username",
                               self.username)
        self.client.set_string(self.__gconfDir + "/password",
                               self.password)
        self.client.set_string(self.__gconfDir + "/url",
                               self.url)

        if self.loginPassed is False:
            message = gtk.MessageDialog(None,
                gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
                gtk.MESSAGE_ERROR, gtk.BUTTONS_OK, "You have not verified "
                                                   "your Confluence "
                                                   "credentials, please "
                                                   "click \"test\" to "
                                                  "do this!")
            message.run()
            message.destroy()
        else:
            self.dialogWindow.destroy()
            self.confluencewidget.loadConfluenceBrowser(self.window)

    def on_testButton_clicked(self, widget):
        self.username = self.dialogWindowUsername.get_text()
        self.password = self.dialogWindowPassword.get_text()
        self.url = self.dialogWindowUrl.get_text()

        if self.confluenceLogin() is True:
            msg = "Login successful"
            
            self.loginPassed = True
            self.client.set_bool(self.__gconfDir + "/loginPassed",
                                 self.loginPassed)
        else:
            msg = "Login failed"

        message = gtk.MessageDialog(None,
            gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
            gtk.MESSAGE_INFO, gtk.BUTTONS_OK, msg)
        message.run()
        message.destroy()
    
    def _removeCredentials(self, widget):
        self.username = ""
        self.password = ""
        self.url = "https://your.confluence.url/rpc/xmlrpc"
        self.loginPassed = False
        
        '''self.client = gconf.client_get_default()

        self.client.set_string(self.__gconfDir + "/username",
                               self.username)
        self.client.set_string(self.__gconfDir + "/password",
                               self.password)
        self.client.set_string(self.__gconfDir + "/url",
                               self.url)
        self.client.set_bool(self.__gconfDir + "/loginPassed",
                                 self.loginPassed)'''
        print self.initWindow
        self.initWindow.unloadConfluenceBrowser(self.initWindow)
        self.dialogWindow.destroy()
    
    def _inputChanged(self, widget):
        self.loginPassed = False
        return

    def confluenceLogin(self):
        try:
            self.confluence = Confluence(self.url, True)
            if self.confluence.login(self.username, self.password) is True:
                self.confluence.logout()
                return True
        except Exception, err:
            return False
