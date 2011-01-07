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
        
        if len(attachments) == 0:
            widget.add(gtk.Label(_('No attachments for this page')))
            return
        
        vbox = gtk.VBox()
        widget.add(vbox)
        
        table = gtk.Table(len(attachments), 6)
        
        for i, o in enumerate(attachments):
            table.attach(gtk.Label(o.title), 0, 1, i, i+1, xoptions=gtk.SHRINK, yoptions=gtk.SHRINK)
            table.attach(gtk.Label(o.fileSize), 1, 2, i, i+1, xoptions=gtk.SHRINK, yoptions=gtk.SHRINK)
            table.attach(gtk.Label(o.creator), 2, 3, i, i+1, xoptions=gtk.SHRINK, yoptions=gtk.SHRINK)
            table.attach(gtk.Label(o.created), 3, 4, i, i+1, xoptions=gtk.SHRINK, yoptions=gtk.SHRINK)
            table.attach(gtk.Label(o.comment), 4, 5, i, i+1, xoptions=gtk.SHRINK, yoptions=gtk.SHRINK)

        scrolled = gtk.ScrolledWindow(None, gtk.Adjustment())
        port = gtk.Viewport()
        port.add(table)
        scrolled.add(port)
        
        vbox.pack_start(scrolled, True, True, 2)
