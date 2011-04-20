from gi.repository import Gtk, GdkPixbuf, Gedit

import urllib

import confluencerpclib
import page

class ConfluenceBrowserPanel(Gtk.Box):
    __gtype_name__ = "ConfluenceBrowserPanel"

    def __init__(self, window):
        Gtk.Box.__init__(self)

        self.geditwindow = window
        self.tabs = {}

        try:
            self.encoding = Gedit.encoding_get_current()
        except:
            self.encoding = Gedit.gedit_encoding_get_current()
        
        scrolled_window = Gtk.ScrolledWindow(None, None)
        scrolled_window.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        scrolled_window.set_shadow_type(Gtk.ShadowType.ETCHED_IN)

        self.browser = Gtk.TreeView()
        self.browser.set_headers_visible(False)

        scrolled_window.add(self.browser)

        self.pack_start(scrolled_window, True, True, 0)

        # add a text column to the treeview
        self.column = Gtk.TreeViewColumn()
        self.browser.append_column(self.column)

        self.cellrendererpixbuf = Gtk.CellRendererText()
        self.column.pack_start(self.cellrendererpixbuf, True)
        self.column.add_attribute(self.cellrendererpixbuf, 'text', 0)

        # connect stuff
        self.browser.connect("row-activated", self._onRowActivated)
        #window.connect("active-tab-state-changed", self._onActiveTabStateChanged)
        window.connect("tab-removed", self._onTabRemoved)
        
        self.show_all()

    def loadConfluenceBrowser(self, window, confluence):
        #self.options = options.options()
        panel = window.get_side_panel()
        image = Gtk.Image()

        f = urllib.urlopen('https://confluence.nurago.com/favicon.ico')
        data = f.read()
        pbl = GdkPixbuf.PixbufLoader()
        pbl.write(data)
        pixbuf = pbl.get_pixbuf()
        pbl.close()

        image = Gtk.Image()
        image.set_from_pixbuf(pixbuf)
        
        self.treestore = Gtk.TreeStore(str, str, str)
        
        self.confluence = confluence

         # we'll add some data now - 4 rows with 3 child rows each
        for parent in self.confluence.getSpaces():
            piter = self.treestore.append(None, (parent.name, parent.key, 'isSpace'))
            
        self.browser.set_model(self.treestore)
        self.browser.show_all()
        self.browser.queue_draw()

        #spaces = self.confluence.getSpaces()
        panel.add_item(self, "Confluence Browser", _("Confluence Browser"), image)

        statusbar = window.get_statusbar()
        self.context_id = statusbar.get_context_id("Character Description")

    def _onRowActivated(self, widget, row, col):
        model = widget.get_model()
        parentIter = model.get_iter(row)
        
        if model[row][2] == 'isSpace':
            children = self.treestore.iter_children(parentIter)
            if children is not None:
                while self.treestore.iter_is_valid(children):
                    self.treestore.remove(children)
            
            treeStore = {}
            
            for parent in self.confluence.getPages(model[row][1]):
                if parent.parentId != "0":
                    treeStore.setdefault(parent.parentId,[]).append((parent.title, parent.id, 'isPage'))
                else:
                    treeStore.setdefault('root',[]).append((parent.title, parent.id, 'isPage'))
                
            ids = treeStore.keys()
            ids.sort()
            
            roots = {}

            for i in treeStore['root']:
                roots[i[1]] = self.treestore.append(parentIter, (i[0], i[1], i[2]))
            
            finished = False
            while finished == False:
                for id in ids:
                    if treeStore.has_key(id) and id == "root":
                        del(treeStore[id])
                        continue
                    
                    if roots.has_key(id) and treeStore.has_key(id):
                        for i in treeStore[id]:
                            roots[i[1]] = self.treestore.append(roots[id], (i[0], i[1], i[2]))
                            treeStore[id].remove(i)
                            
                    if treeStore.has_key(id) and len(treeStore[id]) == 0:
                        del(treeStore[id])
                if len(treeStore) is 0:
                    finished = True
            
            self.browser.expand_row(model.get_path(parentIter), False)
        elif model[row][2] == 'isPage':
            if self.treestore.iter_has_child(parentIter):
                self.browser.expand_row(model.get_path(parentIter), False)
            else:
                loadedPage = page.Page(self.confluence).open(model[row][1], self.geditwindow)
                self.tabs[loadedPage[0]] = loadedPage[1]

    def _onActiveTabStateChanged(self, window):
        tabs = page.Page(self.confluence).save(window, self.tabs)
        #self.tabs = tabs

    def _onTabRemoved(self, window, tab):
        path = tab.get_document().get_uri()

        if self.tabs.has_key(path):
            os.remove(tab.get_document().get_uri_for_display())
            del self.tabs[path]
