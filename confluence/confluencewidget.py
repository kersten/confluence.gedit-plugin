import gtk
import gobject
import gedit
import options
import os
import sys
import tempfile

from confluencerpclib import Confluence


class ConfluenceBrowser(gtk.VBox):
    """ A widget that resides in gedits side panel. """

    def __init__(self, geditwindow):
        """ geditwindow -- an instance of gedit.Window """

        gtk.VBox.__init__(self)
        self.geditwindow = geditwindow
        
        self.tabs = []

        try:
            self.encoding = gedit.encoding_get_current()
        except:
            self.encoding = gedit.gedit_encoding_get_current()

        self.active_timeout = False

        self.parser = None
        self.document_history = [] # contains tuple (doc,line,col)
        self.history_pos = 0
        self.previousline = 0

        #self.back = gtk.ToolButton(gtk.STOCK_GO_BACK)
        #self.back.connect("clicked", self.history_back)
        #self.back.set_sensitive(False)
        #self.forward = gtk.ToolButton(gtk.STOCK_GO_FORWARD)
        #self.forward.connect("clicked", self.history_forward)
        #self.forward.set_sensitive(False)

        #tb = gtk.Toolbar()
        #tb.add(self.back)
        #tb.add(self.forward)
        #self.pack_start(tb,False,False)

        # add a treeview
        sw = gtk.ScrolledWindow()
        sw.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        sw.set_shadow_type(gtk.SHADOW_IN)
        self.browser = gtk.TreeView()
        self.browser.set_headers_visible(False)
        sw.add(self.browser)
        #self.browser.connect("button_press_event", self.__onClick)

        self.pack_start(sw)

        # add a text column to the treeview
        self.column = gtk.TreeViewColumn()
        self.browser.append_column(self.column)

        self.cellrendererpixbuf = gtk.CellRendererText()
        self.column.pack_start(self.cellrendererpixbuf, True)
        self.column.add_attribute(self.cellrendererpixbuf, 'text', 0)

        #self.crt = gtk.CellRendererText()
        #self.column.pack_start(self.crt, False)

        # connect stuff
        self.browser.connect("row-activated", self.on_row_activated)
        self.geditwindow.connect("active-tab-state-changed", self.active_tab_state_changed)
        self.show_all()

    def on_row_activated(self, widget, row, col):
        model = widget.get_model()
        parentIter = model.get_iter(row)
        print model[row][2]
        if model[row][2] == 'isSpace':
            for parent in self.confluence.getPages(model[row][1]):
                piter = self.treestore.append(parentIter, (parent.title, parent.id, 'isPage'))
        elif model[row][2] == 'isPage':
            page = self.confluence.getPage(model[row][1])
            tf = tempfile.NamedTemporaryFile(delete=False)
            tf.seek(0)
            tf.write(page.content)
            self.geditwindow.create_tab_from_uri('file://' + tf.name, None, 0, False, True)
            self.tabs = ['file://' + tf.name,]
        return
        
        spaceKey = model[row][1]
        
        #self.confluence.getSpace(spaceKey)
        
        with tempfile.TemporaryFile() as f:
            f.write(text)
            self.geditwindow.create_tab_from_uri(f.name, None, None, False, True)
        print text
    
    def active_tab_state_changed(self, window):
        tab = window.get_active_tab()
        path = tab.get_document().get_uri()
        
        print path
        print self.tabs
        if tab and tab.get_state() == gedit.TAB_STATE_SAVING and path in self.tabs:
            print tab.get_state()
        
    def loadConfluenceBrowser(self, window):
        self.options = options.options()
        panel = window.get_side_panel()
        image = gtk.Image()

        filename = os.path.join(sys.path[0], "confluence", "pixmaps",
                                "confluence.png")
        pixbuf = gtk.gdk.pixbuf_new_from_file(filename)

        image.set_from_pixbuf(pixbuf)

        self.confluence = Confluence(self.options.url, True)
        self.confluence.login(self.options.username, self.options.password)
        
        self.treestore = gtk.TreeStore(str, str, str)

         # we'll add some data now - 4 rows with 3 child rows each
        for parent in self.confluence.getSpaces():
            piter = self.treestore.append(None, (parent.name, parent.key, 'isSpace'))
            
        self.browser.set_model(self.treestore)
        self.browser.show_all()
        self.browser.queue_draw()

        #spaces = self.confluence.getSpaces()
        panel.add_item(self, "Confluence Browser", image)

        # store per window data in the window object
        windowdata = {"ConfluenceBrowser": self}
