import gtk
import gobject
import gedit
import os
import sys
import tempfile
import urllib
import webbrowser
import webkit

import confluencerpclib
import options
import page
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

        # add a treeview
        sw = gtk.ScrolledWindow()
        sw.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        sw.set_shadow_type(gtk.SHADOW_IN)
        
        TARGETS = [
            ('text/plain', 0, 1),
            ('TEXT', 0, 2),
            ('STRING', 0, 3),
            ]
        
        self.browser = gtk.TreeView()
        self.browser.set_headers_visible(False)
        
        self.browser.enable_model_drag_source(gtk.gdk.BUTTON1_MASK,
                                                TARGETS,
                                                gtk.gdk.ACTION_DEFAULT|
                                                gtk.gdk.ACTION_MOVE)
        self.browser.enable_model_drag_dest(TARGETS,
                                            gtk.gdk.ACTION_DEFAULT)
        
        sw.add(self.browser)
        
        self.browser.connect("button_press_event", self.__onClick)

        self.pack_start(sw)

        # add a text column to the treeview
        self.column = gtk.TreeViewColumn()
        self.browser.append_column(self.column)

        self.cellrendererpixbuf = gtk.CellRendererText()
        self.column.pack_start(self.cellrendererpixbuf, True)
        self.column.add_attribute(self.cellrendererpixbuf, 'text', 0)

        # connect stuff
        self.browser.connect("row-activated", self._onRowActivated)
        self.geditwindow.connect("active-tab-state-changed", self._onActiveTabStateChanged)
        self.geditwindow.connect("tab-removed", self._onTabRemoved)
        self.show_all()

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
                            #print i
                            roots[i[1]] = self.treestore.append(roots[id], (i[0], i[1], i[2]))
                            treeStore[id].remove(i)
                            
                    if treeStore.has_key(id) and len(treeStore[id]) == 0:
                        del(treeStore[id])
                if len(treeStore) is 0:
                    finished = True
        elif model[row][2] == 'isPage':
            loadedPage = page.Page(self.confluence).open(model[row][1], self.geditwindow)
            self.tabs[loadedPage[0]] = loadedPage[1]
    
    def _onActiveTabStateChanged(self, window):
        print self.tabs
        tabs = page.Page(self.confluence).save(window, self.tabs)
        #self.tabs = tabs

    def _onTabRemoved(self, window, tab):
        path = tab.get_document().get_uri()

        if self.tabs.has_key(path):
            os.remove(tab.get_document().get_uri_for_display())
            del self.tabs[path]

    def loadConfluenceBrowser(self, window, confluence):
        self.options = options.options()
        panel = window.get_side_panel()
        image = gtk.Image()

        f = urllib.urlopen(self.options.url.replace('/rpc/xmlrpc', '/favicon.ico'))
        data = f.read()
        pbl = gtk.gdk.PixbufLoader()
        pbl.write(data)
        pixbuf = pbl.get_pixbuf()
        pbl.close()
        image.set_from_pixbuf(pixbuf)
        
        self.treestore = gtk.TreeStore(str, str, str)
        
        self.confluence = confluence

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
    
    def _addPage(self, menuitem, spaceKey, parentPageId=None):
        loadedPage = page.Page(self.confluence).add(menuitem, self.geditwindow, spaceKey, parentPageId)
        
        if loadedPage is False:
            self._addPage(menuitem, spaceKey, parentPageId)
            return
        
        self.tabs[loadedPage[0]] = loadedPage[1]

    def _reloadSelectedItem(self, menuitem, model):
        model = self.browser.get_model()
    
    def _getComments(self, menuitem, spaceKey, pageId):
        comments = self.confluence.getComments(pageId)
        htmlString = ''
        
        print os.path.join(os.path.realpath(os.path.dirname(__file__)), 'css/comments.css')
        f = open(os.path.join(os.path.realpath(os.path.dirname(__file__)), 'css/comments.css'), 'r').read()
        htmlString += '<style>'+f+'</style>'
        
        if not comments:
            htmlString += '<div class="pageSection" id="comments-section"><p>No comments on this page</p></div>'
        else:
            htmlString += '<div class="pageSection" id="comments-section">'
            htmlString += '<ol id="page-comments" class="comment-threads top-level">'

        for i in comments:
            htmlString += '<li class="comment-thread" id="comment-thread-'+i.id+'"><div id="comment-'+i.id+'" class="comment">'
            htmlString += '<div class="comment-body"><div class="comment-content wiki-content">'

            user = self.confluence.getUser(i.creator)
            #htmlString += '<p>'+user.fullname+' says:</p>'
            htmlString += i.content
            htmlString += '</div></div></div></li>'
        
        if comments:
            htmlString += '</ol>'
            htmlString += '</div>'
        
        print htmlString
        
        webView = gtk.Window()
        browser = webkit.WebView()

        browser.load_html_string(htmlString, "file:///")

        box = gtk.VBox(homogeneous=False, spacing=0)
        webView.add(box)
        
        box.pack_start(browser, expand=True, fill=True, padding=0)

        webView.set_default_size(800, 600)
        webView.show_all()
    
    def _getAttachments(self, menuitem, spaceKey, pageId):
        pass

    def _openInBrowser(self, menuitem, pageId):
        page = self.confluence.getPage(pageId)
        webbrowser.open(page.url)
        return

    def __onClick(self, treeview, event):
        if event.button == 3:
            x, y = int(event.x), int(event.y)
            pthinfo = treeview.get_path_at_pos(x, y)
            if pthinfo is None: return
            path, col, cellx, celly = pthinfo
            
            model = self.browser.get_model()
            menu = gtk.Menu()
            
            if model[path][2] == 'isSpace':
                m = gtk.MenuItem('Reload selected item')
                menu.append(m)
                m.show()
                m.connect("activate", self._reloadSelectedItem, path)
                
                m = gtk.SeparatorMenuItem()
                m.show()
                menu.append(m)
                
                m = gtk.MenuItem('Add page')
                menu.append(m)
                m.show()
                m.connect("activate", self._addPage, model[path][1])
              
            if model[path][2] == 'isPage':
                m = gtk.MenuItem('Create page')
                menu.append(m)
                m.show()
                m.connect("activate", self._addPage, model[path[0]][1], model[path][1])
                
                m = gtk.MenuItem('Remove page')
                menu.append(m)
                m.show()
                m.connect("activate", page.Page(self.confluence).remove, model[path][1], path)
                
                m = gtk.SeparatorMenuItem()
                m.show()
                menu.append(m)
                
                m = gtk.MenuItem('Read comments')
                menu.append(m)
                m.show()
                m.connect("activate", self._getComments, model[path[0]][1], model[path][1])
                
                m = gtk.MenuItem('Show attachments')
                menu.append(m)
                m.show()
                m.connect("activate", self._getAttachments, model[path[0]][1], model[path][1])
                
                m = gtk.SeparatorMenuItem()
                m.show()
                menu.append(m)
                
                m = gtk.MenuItem('Open in browser')
                menu.append(m)
                m.show()
                m.connect("activate", self._openInBrowser, model[path][1])
            
            menu.popup( None, None, None, event.button, event.time)
