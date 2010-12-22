import gedit
import options
import confluenceApi


class confluencePluginPlugin(gedit.Plugin):

    def create_configure_dialog(self):
        return options.singleton().create_configure_dialog()

    def is_configurable(self):
        return True

    def activate(self, window):
        options.singleton().confluenceLogin()
        #print confluenceApi.singleton().getSpaces()
        print confluenceApi.singleton().getPages('SupportDaphne')
        print confluenceApi.singleton().getPageById('29458504')
        pass

    def deactivate(self, window):
        pass

    def update_ui(self, window):
        pass
