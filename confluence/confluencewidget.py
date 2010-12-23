import gtk
import gobject
import gedit
import options


class ConfluenceBrowser(gtk.VBox):
    """ A widget that resides in gedits side panel. """

    def __init__(self, geditwindow):
        """ geditwindow -- an instance of gedit.Window """

        gtk.VBox.__init__(self)
        self.geditwindow = geditwindow

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

        self.cellrendererpixbuf = gtk.CellRendererPixbuf()
        self.column.pack_start(self.cellrendererpixbuf, False)

        self.crt = gtk.CellRendererText()
        self.column.pack_start(self.crt, False)

        # connect stuff
        #self.browser.connect("row-activated", self.on_row_activated)
        self.show_all()
