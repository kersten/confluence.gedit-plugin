import gtk
import gedit
import tempfile
from gettext import gettext as _

import confluencerpclib
import options
import attachments
import comments


class Page():
    
    def __init__(self, confluence):
        self.confluence = confluence
        self.options = options.options()
    
    def open(self, pageId, geditWindow):
        # TODO: check permissions before opening page
        try:
            page = self.confluence.getPage(pageId)
        except Exception, err:
                if err.__str__().find('InvalidSessionException'):
                    self.confluence.login(self.options.username,
                                          self.options.password)
                    page = self.confluence.getPage(pageId)

        tf = tempfile.NamedTemporaryFile(delete=False)
        tf.seek(0)
        tf.write(page.content)
        tab = geditWindow.create_tab_from_uri('file://' + tf.name, None,
                                              0, False, True)
        
        title = gtk.Entry()
        title.set_name('title')
        title.set_text(page.title);
        
        tags = self.confluence.getLabelsById(page.id)
        
        tagsEntry = gtk.Entry()
        tagsEntry.set_name('tags')
        
        tagsMerged = []
        
        hboxOldTags = gtk.HBox()
        hboxOldTags.pack_start(gtk.Label(_('Existing labels:')), False,
                               False, 2)
        
        for i in tags:
            tag = gtk.Button(label=i.name)
            tag.connect("clicked", self._clickTagDelete, i.id, page.id)
            hboxOldTags.pack_start(tag, False, False, 2)
        
        hboxTitle = gtk.HBox()
        hboxTitle.pack_start(gtk.Label(_('Title:')), False, False, 2)
        hboxTitle.pack_start(title)
        
        hboxTags = gtk.HBox()
        hboxTags.pack_start(gtk.Label(_('Labels:')), False, False, 2)
        hboxTags.pack_start(tagsEntry)

        tab.pack_start(hboxTitle, False, False, 2)
        tab.pack_start(hboxTags, False, False, 2)
        tab.pack_start(hboxOldTags, False, False, 2)
        
        hbox = gtk.HBox()
        tab.get_children()[3].reparent(hbox)
        
        vbox = gtk.VBox()
        
        commentsFrame = gtk.Frame(_('Comments'))
        attachmentsFrame = gtk.Frame(_('Attachments'))
        
        vbox.pack_start(commentsFrame, True, True, 2)
        vbox.pack_end(attachmentsFrame, True, True, 2)
        
        comments.Comments(self.confluence).get(commentsFrame, page.id)
        attachments.Attachments(self.confluence).get(attachmentsFrame, page.id)
        
        paned = gtk.HPaned()
        paned.set_position(1000)
        
        paned.add1(hbox)
        paned.add2(vbox)
        
        tab.pack_start(paned, True, True, 2)
        
        #hbox.pack_start(vbox, True, True, 2)
        
        tab.show_all()
        tab.get_parent().get_tab_label(tab).get_children()[0].get_children()[0].get_children()[2].set_text(page.title)

        return ['file://' + tf.name, page]

    def add(self, menuitem, geditWindow, spaceKey, parentPageId=None):
        dialog = gtk.MessageDialog(
            None,
            gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
            gtk.MESSAGE_QUESTION,
            gtk.BUTTONS_OK,
            None)
        dialog.set_markup('Please enter the title of the page:')
        #create the text input field
        entry = gtk.Entry()
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
            #self._add(menuitem, spaceKey, parentPageId)
            return False
        
        dialog.destroy()
        if title.strip() != "":
            newPage = confluencerpclib.Page()
            newPage.space = spaceKey
            newPage.title = title
            newPage.content = 'New Page added'

            if parentPageId is not None:
                newPage.parentId = parentPageId
            else:
                del newPage.parentId
            
            try:
                storedPage = self.confluence.storePage(newPage)
            except Exception, err:
                if err.__str__().find('InvalidSessionException'):
                    self.confluence.login(self.options.username,
                                          self.options.password)
                    storedPage = self.confluence.storePage(newPage)

            return self.open(storedPage.id, geditWindow)

    def remove(self, menuitem, pageId, path):
        self.confluence.removePage(pageId)

    def save(self, window, tabs):
        tab = window.get_active_tab()
        path = tab.get_document().get_uri()
        
        if tab and tab.get_state() == gedit.TAB_STATE_SAVING and tabs.has_key(path):
            title = tab.get_children()[0].get_children()[1].get_text()
            tags = tab.get_children()[1].get_children()[1].get_text()

            tabs[path].title = title
            tabs[path].content = tab.get_document().get_text(tab.get_document().get_start_iter(), tab.get_document().get_end_iter())
            
            updateOptions = confluencerpclib.PageUpdateOptions()
            updateOptions.versionComment = ''
            updateOptions.minorEdit = True
            
            try:
                tabs[path] = self.confluence.updatePage(tabs[path], updateOptions)
            except Exception, err:
                if err.__str__().find('InvalidSessionException'):
                    self.confluence.login(self.options.username, self.options.password)
                    tabs[path] = self.confluence.updatePage(tabs[path], updateOptions)
            
            if tags.strip() != "":
                self.confluence.addLabelByName(tags, self.tabs[path].id)
            
            return tabs

    def _clickTagDelete(self, widget, labelId, objectId):
        self.confluence.removeLabelById(labelId, objectId)
        widget.destroy()
