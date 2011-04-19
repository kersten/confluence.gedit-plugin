import gtk
from gettext import gettext as _
from gobject import idle_add, PARAM_READWRITE, SIGNAL_RUN_FIRST, TYPE_PYOBJECT

import options
from CellRendererVBox import CellRendererWidget

class Comments():

    def __init__(self, confluence):
        self.confluence = confluence
        self.options = options.options()

    def get(self, widget, pageId):
        try:
            comments = self.confluence.getComments(pageId)
        except:
            comments = []
        
        self.cntComments = len(comments)
        
        self.vbox = gtk.VBox()
        widget.add(self.vbox)
        
        self.commentBrowser = gtk.TreeView()
        self.commentBrowser.set_headers_visible(False)
        
        self.column = gtk.TreeViewColumn('first', CellRendererWidget(gtk.VBox))
        #self.column.pack_start(self.cellRenderer, True)
        #self.column.add_attribute(self.cellRenderer, widget=1)
        
        self.commentBrowser.append_column(self.column)
        
        self.treestore = gtk.TreeStore(TYPE_PYOBJECT, bool)
        
        self.vboxComments = gtk.VBox()
        
        #self.treestore.append(None, self.vboxComments)
        iter = self.treestore.append(None)
        hb = gtk.VBox()
        hb.pack_start(gtk.Button('testSFDFJLSDHFSDBHFLSDBFLIUSDBFISDBFABDFKBASZFBASDBFUADBFUADBFOUAVFUASVFOUZASVFOUZAVFOUZAVFOUZAVFOUVAOFVBAOUDFZVAODFVOADFVOZUADFVOUZAVFOUZAF'))
        self.treestore.set(iter, 0, hb, 1, True)
        
        self.commentBrowser.set_model(self.treestore)
        self.commentBrowser.show_all()
        
        '''if self.cntComments == 0:
            self.label = gtk.Label(_('No comments for this page'))
            self.vboxComments.pack_start(self.label)
        else:
            lastId = ''
            
            for i, o in enumerate(comments):
                commentVbox = gtk.VBox()
                commentHeaderHbox = gtk.HBox()
                
                if len(lastId) != '' and lastId == o.parentId:
                    commentVbox.pack_start(commentHeaderHbox, False, False, 10)
                else:
                    commentVbox.pack_start(commentHeaderHbox, False, False, 2)
                
                commentByLabel = gtk.Label(_('Written by:'))
                commentAuthorLabel = gtk.Label(self.confluence.getUser(o.creator).fullname)
                
                commentHeaderHbox.pack_start(commentByLabel, False, False, 2)
                commentHeaderHbox.pack_start(commentAuthorLabel, False, False, 2)
                
                commentEditImage = gtk.Image()
                commentAddImage = gtk.Image()
                commentDeleteImage = gtk.Image()
                
                if o.creator == self.options.username:
                    commentEditImage.set_from_stock(gtk.STOCK_EDIT, gtk.ICON_SIZE_MENU)
                
                commentAddImage.set_from_stock(gtk.STOCK_ADD, gtk.ICON_SIZE_MENU)
                
                if o.creator == self.options.username:
                    commentDeleteImage.set_from_stock(gtk.STOCK_DELETE, gtk.ICON_SIZE_MENU)
                
                commentHeaderHbox.pack_end(commentDeleteImage, False, False, 2)
                commentHeaderHbox.pack_end(commentAddImage, False, False, 2)
                commentHeaderHbox.pack_end(commentEditImage, False, False, 2)
                
                self.vboxComments.pack_start(commentVbox, False, False, 2)
                
                lastId = o.id
                #title = gtk.Button(o.title)
                #title.set_alignment(0, 0.5)
                
                #title.connect("clicked", self.edit, pageId)
                
                #self.vboxAttachments.pack_start(title, False, False, 2)
        '''
        scrolled = gtk.ScrolledWindow()
        port = gtk.Viewport()
        port.add(self.commentBrowser)
        scrolled.add(port)
            
        self.vbox.pack_start(scrolled, True, True, 2)
        
        writeCommentHbox = gtk.HBox()

        writeCommentButton = gtk.Button(_('Write comment'), None)
        #fileChooserButton.connect("clicked", self.write, pageId, self.vboxAttachments)

        writeCommentHbox.pack_start(writeCommentButton, True, True, 2)
        
        self.vbox.pack_end(writeCommentHbox, False, False, 2)
