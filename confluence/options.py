import gtk.glade
import gconf
import os
import sys
import confluenceApi


class options():

    __shared_state = {}

    def __init__(self):
        self.__dict__ = self.__shared_state

        self.__gconfDir = "/apps/gedit-2/plugins/confluence"
        # create gconf directory if not set yet
        self.client = gconf.client_get_default()
        if not self.client.dir_exists(self.__gconfDir):
            self.client.add_dir(self.__gconfDir, gconf.CLIENT_PRELOAD_NONE)

        self.username = ""
        self.password = ""
        self.url = "https://your.confluence.url/rpc"

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

        except Exception, e: # catch, just in case
            print e

    def create_configure_dialog(self):
        self.dialogGladeFile = os.path.join(sys.path[0], "confluence",
            "confluencePluginConfigureDialog.glade")

        self.dialog = gtk.Builder()
        self.dialog.add_from_file(self.dialogGladeFile)
        self.dialog.connect_signals(self)

        self.dialogWindow = self.dialog.get_object(
            "confluencePluginConfigureDialog")

        self.dialogWindowUsername = self.dialog.get_object("loginUsername")
        self.dialogWindowUsername.set_text(self.username)

        self.dialogWindowPassword = self.dialog.get_object("loginPassword")
        self.dialogWindowPassword.set_text(self.password)

        self.dialogWindowUrl = self.dialog.get_object("loginURL")
        self.dialogWindowUrl.set_text(self.url)

        self.dialogSignals = {
            "on_closeButton_clicked": self.on_closeButton_clicked}
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

        if self.confluenceLogin() is True:
            self.dialogWindow.destroy()

    def confluenceLogin(self):
        try:
            confluenceApi.singleton(self.url).login(
                self.username, self.password)
            return True
        except Exception, err:
            message = gtk.MessageDialog(None,
                gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
                gtk.MESSAGE_ERROR, gtk.BUTTONS_OK, err.message.__str__())
            message.run()
            message.destroy()
            return False
