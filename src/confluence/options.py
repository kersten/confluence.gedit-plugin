import os
from gi.repository import Gio, Gtk, Gdk

from confluencerpclib import Confluence

__all__ = ('ConfluenceBrwoserConfigWidget')

class ConfluenceBrowserConfigWidget(object):

    BASE = 'org.gnome.gedit.plugins.confluence'
    USERNAME = 'username'
    PASSWORD = 'password'
    URL = 'url'
    LOGINPASSED = 'loginpassed'

    def __init__(self):
        object.__init__(self)
        
        self._settings = Gio.Settings.new(self.BASE)
        self._ui = Gtk.Builder()

    def configure_widget(self, datadir):
        self._ui_path = os.path.join(datadir, 'confluencePluginConfigureDialog.glade')
        self._ui.add_objects_from_file(self._ui_path, ["time_dialog_content"])

        print self._settings.get_string(self.PASSWORD)

        self.set_default_values(self._ui.get_object('username'),
                                   self._settings.get_string(self.USERNAME))
        self.set_default_values(self._ui.get_object('password'),
                                   self._settings.get_string(self.PASSWORD))
        self.set_default_values(self._ui.get_object('url'),
                                   self._settings.get_string(self.URL))

        self._ui.connect_signals(self)

        widget = self._ui.get_object('time_dialog_content')

        return widget

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
        self.username = self._ui.get_object('username').get_text()
        self.password = self._ui.get_object('password').get_text()
        self.url = self._ui.get_object('url').get_text()

        if self.confluenceLogin() is True:
            msg = "Login successful"
            
            self.loginPassed = True
            self._settings.set_string(self.USERNAME, self._ui.get_object('username').get_text())
            self._settings.set_string(self.PASSWORD, self._ui.get_object('password').get_text())
            self._settings.set_string(self.URL, self._ui.get_object('url').get_text())
            self._settings.set_boolean(self.LOGINPASSED, True)
        else:
            msg = "Login failed"

        message = Gtk.MessageDialog(None,
            Gtk.DialogFlags.MODAL | Gtk.DialogFlags.DESTROY_WITH_PARENT,
            Gtk.MessageType.INFO, Gtk.ButtonsType.OK, msg)
        message.run()
        message.destroy()

    def confluenceLogin(self):
        try:
            self.confluence = Confluence(self._ui.get_object('url').get_text(), True)
            if self.confluence.login(self._ui.get_object('username').get_text(), self._ui.get_object('password').get_text()) is True:
                self.confluence.logout()
                return True
        except Exception, err:
            return False
    
    def _removeCredentials(self, widget):
        self.username = ""
        self.password = ""
        self.url = "https://your.confluence.url/rpc/xmlrpc"
        self.loginPassed = False
        
        print self.initWindow
        self.initWindow.unloadConfluenceBrowser(self.initWindow)
        self.dialogWindow.destroy()
    
    def on_loginUsername_changed(self, widget):
        self.loginPassed = False
        return

    def on_loginPassword_changed(self, widget):
        self.loginPassed = False
        return

    def on_loginURL_changed(self, widget):
        self.loginPassed = False
        return

    @staticmethod
    def set_default_values(widget, value):
        widget.set_text(value)

    def on_colorbutton_command_color_set(self, colorbutton):
        self._settings.set_string(self.CONSOLE_KEY_COMMAND_COLOR,
                                  colorbutton.get_color().to_string())

    def on_colorbutton_error_color_set(self, colorbutton):
        self._settings.set_string(self.CONSOLE_KEY_ERROR_COLOR,
                                  colorbutton.get_color().to_string())
