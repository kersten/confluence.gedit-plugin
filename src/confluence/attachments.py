import gtk
from gettext import gettext as _


class Attachments():

    def __init__(self, confluence):
        self.confluence = confluence

    def get(self, widget, pageId):
        try:
            attachments = self.confluence.getAttachments(pageId)
        except:
            attachments = []
        
        vbox = gtk.VBox()
        widget.add(vbox)
        
        if len(attachments) == 0:
           vbox.pack_start(gtk.Label(_('No attachments for this page')))
        else:
            vboxAttachments = gtk.VBox()
            
            for i, o in enumerate(attachments):
                title = gtk.Label(o.title)
                title.set_alignment(0, 0.5)
                
                vboxAttachments.pack_start(title, False, False, 2)
                #table.attach(gtk.Label(o.fileSize), 1, 2, i, i+1, xoptions=gtk.SHRINK, yoptions=gtk.SHRINK)
                #table.attach(gtk.Label(o.creator), 2, 3, i, i+1, xoptions=gtk.SHRINK, yoptions=gtk.SHRINK)
                #table.attach(gtk.Label(o.created), 3, 4, i, i+1, xoptions=gtk.SHRINK, yoptions=gtk.SHRINK)
                #table.attach(gtk.Label(o.comment), 4, 5, i, i+1, xoptions=gtk.SHRINK, yoptions=gtk.SHRINK)

            scrolled = gtk.ScrolledWindow()
            port = gtk.Viewport()
            port.add(vboxAttachments)
            scrolled.add(port)
            
            vbox.pack_start(scrolled, True, True, 2)
        
        uploadHbox = gtk.HBox()

        fileChooserButton = gtk.FileChooserButton(_('Add attachment'))
        uploadButton = gtk.Button(_('Upload attachment'))
        #btn.set_alignment(1.0, 0.5)

        uploadHbox.pack_start(fileChooserButton, True, True, 2)
        uploadHbox.pack_end(uploadButton, False, False, 2)
        
        vbox.pack_end(uploadHbox, False, False, 2)
