import gtk
import gobject
import gedit
import options
import os
import sys
import tempfile

import confluencerpclib
#import Confluence, Page, PageUpdateOptions


class ConfluenceBrowser(gtk.VBox):
    """ A widget that resides in gedits side panel. """

    def __init__(self, geditwindow):
        """ geditwindow -- an instance of gedit.Window """

        gtk.VBox.__init__(self)
        self.geditwindow = geditwindow
        
        self.tabs = {}

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
        self.browser.connect("button_press_event", self.__onClick)

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
        self.geditwindow.connect("tab-removed", self.tab_removed)
        self.show_all()

    def on_row_activated(self, widget, row, col):
        model = widget.get_model()
        parentIter = model.get_iter(row)
        
        if model[row][2] == 'isSpace':
            #if model[parentIter].has_children():
            #    for i in parentIter.get_children():
            #        unset(parentInter[i])
            
            iter = self.treestore.iter_children(parentIter)
            while iter:
                print iter
                self.treestore.remove(iter)
            
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
                            #print i
                            roots[i[1]] = self.treestore.append(roots[id], (i[0], i[1], i[2]))
                            treeStore[id].remove(i)
                            
                    if treeStore.has_key(id) and len(treeStore[id]) == 0:
                        del(treeStore[id])
                if len(treeStore) is 0:
                    finished = True
        elif model[row][2] == 'isPage':
            page = self.confluence.getPage(model[row][1])
            tf = tempfile.NamedTemporaryFile(delete=False)
            tf.seek(0)
            tf.write(page.content)
            tab = self.geditwindow.create_tab_from_uri('file://' + tf.name, None, 0, False, True)
            self.tabs['file://' + tf.name] = page
            
            title = gtk.Entry()
            
            title.set_text(page.title);
            
            tags = gtk.Entry()
            #allow the user to press enter to do ok
            #entry.connect("activate", responseToDialog, dialog, gtk.RESPONSE_OK)
            #create a horizontal box to pack the entry and a label
            hboxTitle = gtk.HBox()
            hboxTitle.pack_start(gtk.Label("Title:"), False, False, 2)
            hboxTitle.pack_end(title)
            
            hboxTags = gtk.HBox()
            hboxTags.pack_start(gtk.Label("Tags:"), False, False, 2)
            hboxTags.pack_end(tags)
            #some secondary text
            #add it and show it
            tab.pack_end(hboxTags, False, False, 0)
            tab.pack_end(hboxTitle, False, False, 0)
            tab.show_all()
    
    def active_tab_state_changed(self, window):
        tab = window.get_active_tab()
        path = tab.get_document().get_uri()
        
        if tab and tab.get_state() == gedit.TAB_STATE_SAVING and self.tabs.has_key(path):
            print "Store page"
            self.tabs[path].content = tab.get_document().get_text(tab.get_document().get_start_iter(), tab.get_document().get_end_iter())
            
            updateOptions = confluencerpclib.PageUpdateOptions()
            updateOptions.versionComment = ''
            updateOptions.minorEdit = True
            
            self.tabs[path] = self.confluence.updatePage(self.tabs[path], updateOptions)
            #self.tabs[path].version += 1

    def tab_removed(self, window, tab):
        path = tab.get_document().get_uri()

        if self.tabs.has_key(path):
            os.remove(tab.get_document().get_uri_for_display())
            del self.tabs[path]

    def loadConfluenceBrowser(self, window):
        self.options = options.options()
        panel = window.get_side_panel()
        image = gtk.Image()

        filename = os.path.join(sys.path[0], "confluence", "pixmaps",
                                "confluence.png")
        pixbuf = gtk.gdk.pixbuf_new_from_file(filename)

        image.set_from_pixbuf(pixbuf)

        self.confluence = confluencerpclib.Confluence(self.options.url, True)
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
    
    def add_page(self, menuitem, spaceKey, parentPageId=None):
        dialog = gtk.MessageDialog(
            None,
            gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
            gtk.MESSAGE_QUESTION,
            gtk.BUTTONS_OK,
            None)
        dialog.set_markup('Please enter the title of the page:')
        #create the text input field
        entry = gtk.Entry()
        #allow the user to press enter to do ok
        #entry.connect("activate", responseToDialog, dialog, gtk.RESPONSE_OK)
        #create a horizontal box to pack the entry and a label
        hbox = gtk.HBox()
        hbox.pack_start(gtk.Label("Title:"), False, 5, 5)
        hbox.pack_end(entry)
        #some secondary text
        #add it and show it
        dialog.vbox.pack_end(hbox, True, True, 0)
        dialog.show_all()
        #go go go
        dialog.run()
        title = entry.get_text()
        
        if title.strip() == "" and gtk.RESPONSE_OK:
            dialog.destroy()
            self.add_page(menuitem, spaceKey, parentPageId)
            return
        
        dialog.destroy()
        if title.strip() != "":
            page = confluencerpclib.Page()
            page.space = spaceKey
            page.title = title
            page.content = 'New Page added'

            if parentPageId is not None:
                page.parentId = parentPageId
            
            page = self.confluence.storePage(page)
            tf = tempfile.NamedTemporaryFile(delete=False)
            tf.seek(0)
            tf.write(page.content)
            tab = self.geditwindow.create_tab_from_uri('file://' + tf.name, None, 0, False, True)
            self.tabs['file://' + tf.name] = page

    def reload_selected_item(self, menuitem, model):
        model = self.browser.get_model()
    
    def _deletePage(self, menuitem, model):
        model = self.browser.get_model()
    
    def _getComments(self, menuitem, model):
        model = self.browser.get_model()

    def __onClick(self, treeview, event):
        if event.button == 3:
            x, y = int(event.x), int(event.y)
            pthinfo = treeview.get_path_at_pos(x, y)
            if pthinfo is None: return
            path, col, cellx, celly = pthinfo
            
            model = self.browser.get_model()
            menu = gtk.Menu()
            
            m = gtk.MenuItem('Reload selected item')
            menu.append(m)
            m.show()
            m.connect("activate", self.reload_selected_item, path)
            
            if model[path][2] == 'isSpace':
                m = gtk.MenuItem('Add page')
                menu.append(m)
                m.show()
                m.connect("activate", self.add_page, model[path][1])
              
            if model[path][2] == 'isPage':
                m = gtk.MenuItem('Add page')
                menu.append(m)
                m.show()
                m.connect("activate", self.add_page, model[path[0]][1], model[path][1])
                
                m = gtk.MenuItem('Delete page')
                menu.append(m)
                m.show()
                m.connect("activate", self._deletePage, model[path[0]][1], model[path][1])
                
                m = gtk.SeparatorMenuItem()
                m.show()
                menu.append(m)
                
                m = gtk.MenuItem('Get comments')
                menu.append(m)
                m.show()
                m.connect("activate", self._getComments, model[path[0]][1], model[path][1])
            
            menu.popup( None, None, None, event.button, event.time)
