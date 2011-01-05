import gtk
import tempfile


class Page():
    
    def __init__(self, confluence):
        self.confluence = confluence
    
    def open(self, pageId, geditWindow):
        # TODO: check permissions before opening page
        page = self.confluence.getPage(pageId)
        tf = tempfile.NamedTemporaryFile(delete=False)
        tf.seek(0)
        tf.write(page.content)
        tab = geditWindow.create_tab_from_uri('file://' + tf.name, None, 0, False, True)
        
        title = gtk.Entry()
        title.set_name('title')
        title.set_text(page.title);
        
        tags = self.confluence.getLabelsById(page.id)
        
        tagsEntry = gtk.Entry()
        tagsEntry.set_name('tags')
        
        tagsMerged = []
        
        hboxOldTags = gtk.HBox()
        hboxOldTags.pack_start(gtk.Label('Existing tags:'), False, False, 2)
        
        for i in tags:
            tag = gtk.Button(label=i.name)
            tag.connect("clicked", self._clickTagDelete, i.id, page.id)
            hboxOldTags.pack_start(tag, False, False, 2)
        
        hboxTitle = gtk.HBox()
        hboxTitle.pack_start(gtk.Label("Title:"), False, False, 2)
        hboxTitle.pack_end(title)
        
        hboxTags = gtk.HBox()
        hboxTags.pack_start(gtk.Label("Tags:"), False, False, 2)
        hboxTags.pack_end(tagsEntry)

        tab.pack_end(hboxOldTags, False, False, 2)
        tab.pack_end(hboxTags, False, False, 2)
        tab.pack_end(hboxTitle, False, False, 2)
        tab.show_all()

        return ['file://' + tf.name, page]

    def _remove(self, menuitem, pageId, path):
        self.confluence.removePage(pageId)
        

    def _clickTagDelete(self, widget, labelId, objectId):
        self.confluence.removeLabelById(labelId, objectId)
        widget.destroy()
