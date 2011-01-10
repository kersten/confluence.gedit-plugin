import gtk
import os
import mimetypes
from gettext import gettext as _

import confluencerpclib


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

        fileChooserButton = gtk.FileChooserButton(_('Add attachment'), None)
        fileChooserButton.connect("file-set", self.upload, pageId)

        uploadHbox.pack_start(fileChooserButton, True, True, 2)
        
        vbox.pack_end(uploadHbox, False, False, 2)

    def upload(self, widget, pageId):
        dialog = gtk.MessageDialog(
            None,
            gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
            gtk.MESSAGE_QUESTION,
            gtk.BUTTONS_OK,
            None)
        dialog.set_title(_('Upload %s' % widget.get_filename()))
        #create the text input field
        title = gtk.Entry()
        hbox = gtk.HBox()
        hbox.pack_start(gtk.Label(_("Title:")), False, 5, 5)
        hbox.pack_end(title)
        
        dialog.vbox.pack_start(hbox, True, True, 0)
        
        comment = gtk.Entry()
        hbox = gtk.HBox()
        hbox.pack_start(gtk.Label(_("Comment:")), False, 5, 5)
        hbox.pack_end(comment)
        
        #some secondary text
        #add it and show it
        dialog.vbox.pack_end(hbox, True, True, 0)
        dialog.show_all()
        #go go go
        dialog.run()
        
        mime, encoding = mimetypes.guess_type(widget.get_filename())
        filesize = os.stat(widget.get_filename()).st_size
        fd = open(widget.get_filename(), 'rb')
        file = fd.read()
        fd.close()

        attachment = confluencerpclib.Attachment()
        attachment.pageId = pageId
        attachment.title = title.get_text()
        attachment.fileName = os.path.basename(widget.get_filename())
        attachment.fileSize = filesize
        attachment.contentType = mime
        attachment.comment = comment.get_text()
        
        self.confluence.addAttachment(pageId, attachment, file)
        dialog.destroy()
