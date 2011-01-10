import gtk
from gettext import gettext as _


class Comments():

    def __init__(self, confluence):
        self.confluence = confluence

    def get(self, widget, pageId):
        try:
            comments = self.confluence.getComments(pageId)
        except:
            comments = []
        
        self.cntComments = len(comments)
        
        self.vbox = gtk.VBox()
        widget.add(self.vbox)
        
        self.vboxComments = gtk.VBox()
        
        if self.cntComments == 0:
            self.label = gtk.Label(_('No comments for this page'))
            self.vboxComments.pack_start(self.label)
        else:
            for i, o in enumerate(comments):
                pass
                #title = gtk.Button(o.title)
                #title.set_alignment(0, 0.5)
                
                #title.connect("clicked", self.edit, pageId)
                
                #self.vboxAttachments.pack_start(title, False, False, 2)
        
        scrolled = gtk.ScrolledWindow()
        port = gtk.Viewport()
        port.add(self.vboxComments)
        scrolled.add(port)
            
        self.vbox.pack_start(scrolled, True, True, 2)
        
        writeCommentHbox = gtk.HBox()

        writeCommentButton = gtk.Button(_('Write comment'), None)
        #fileChooserButton.connect("clicked", self.write, pageId, self.vboxAttachments)

        writeCommentHbox.pack_start(writeCommentButton, True, True, 2)
        
        self.vbox.pack_end(writeCommentHbox, False, False, 2)
