import gedit
import options
import confluencerpclib


class confluencePluginPlugin(gedit.Plugin):

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
        self.confluence = confluencerpclib.connect(self.options.url)
        self.confluence.login(self.options.username, self.options.password)

        print self.confluence.token
        pass

    def deactivate(self, window):
        self.confluence.logout()
        pass

    def update_ui(self, window):
        pass
