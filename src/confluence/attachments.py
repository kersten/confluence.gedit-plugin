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
        
        self.cntAttachments = len(attachments)
        
        self.vbox = gtk.VBox()
        widget.add(self.vbox)
        
        self.vboxAttachments = gtk.VBox()
        
        if self.cntAttachments == 0:
            self.label = gtk.Label(_('No attachments for this page'))
            self.vboxAttachments.pack_start(self.label)
        else:
            for i, o in enumerate(attachments):
                title = gtk.Button(o.title)
                title.set_alignment(0, 0.5)
                
                title.connect("clicked", self.edit, pageId)
                
                self.vboxAttachments.pack_start(title, False, False, 2)

        scrolled = gtk.ScrolledWindow()
        port = gtk.Viewport()
        port.add(self.vboxAttachments)
        scrolled.add(port)
            
        self.vbox.pack_start(scrolled, True, True, 2)
        
        uploadHbox = gtk.HBox()

        fileChooserButton = gtk.FileChooserButton(_('Add attachment'), None)
        fileChooserButton.connect("file-set", self.upload, pageId, self.vboxAttachments)

        uploadHbox.pack_start(fileChooserButton, True, True, 2)
        
        self.vbox.pack_end(uploadHbox, False, False, 2)

    def edit(self, widget, pageId):
        dialog = gtk.Window()
        dialog.set_title(_('Upload %s' % widget.get_label()))
        
        dialog.show_all()

    def upload(self, widget, pageId, attachmentWidget):
        dialog = gtk.MessageDialog(
            None,
            gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
            gtk.MESSAGE_QUESTION,
            gtk.BUTTONS_OK,
            None)
        dialog.set_title(_('Upload %s' % widget.get_filename()))
        #create the text input field
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
        attachment.fileName = os.path.basename(widget.get_filename())
        attachment.fileSize = filesize
        attachment.contentType = mime
        attachment.comment = comment.get_text()
        
        try:
            responseAttachment = self.confluence.addAttachment(pageId, attachment, file)

            title = gtk.Button(attachment.fileName)
            title.set_alignment(0, 0.5)
                
            title.connect("clicked", self.edit, pageId)
            if self.cntAttachments == 0:
                attachmentWidget.remove(self.label)

            attachmentWidget.pack_start(title, False, False, 2)
            attachmentWidget.show_all()
        except Exception, err:
            print err

        dialog.destroy()
