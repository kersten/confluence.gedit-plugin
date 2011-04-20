from gi.repository import GObject, Gtk, Gdk, Gedit, Gio
import tempfile

try:
    gettext.bindtextdomain(GETTEXT_PACKAGE, GP_LOCALEDIR)
    _ = lambda s: gettext.dgettext(GETTEXT_PACKAGE, s);
except:
    _ = lambda s: s

import confluencerpclib
from options import ConfluenceBrowserConfigWidget
#import attachments
#import comments


class Page():
    
    def __init__(self, confluence):
        self.confluence = confluence
        self.options = ConfluenceBrowserConfigWidget()
    
    def open(self, pageId, geditWindow):
        # TODO: check permissions before opening page
        try:
            self.page = self.confluence.getPage(pageId)
        except Exception, err:
                if err.__str__().find('InvalidSessionException'):
                    self.confluence.login(self.options._settings.get_string(self.options.USERNAME),
                                          self.options._settings.get_string(self.options.PASSWORD))
                    self.page = self.confluence.getPage(pageId)

        tf = tempfile.NamedTemporaryFile(delete=False)
        tf.seek(0)
        tf.write(self.page.content.encode('utf-8'))

        gfile = Gio.file_new_for_uri('file://' + tf.name)
        
        tab = geditWindow.create_tab_from_location(gfile, None,
                                              0, False, True, True)
        
        title = Gtk.Entry()
        title.set_name('title')
        title.set_text(self.page.title);
        
        tags = self.confluence.getLabelsById(self.page.id)
        
        tagsEntry = Gtk.Entry()
        tagsEntry.set_name('tags')
        
        tagsMerged = []
        
        hboxOldTags = Gtk.HBox()
        hboxOldTags.pack_start(Gtk.Label(_('Existing labels:')), False,
                               False, 2)
        
        for i in tags:
            tag = Gtk.Button(label=i.name)
            tag.connect("clicked", self._clickTagDelete, i.id, self.page.id)
            hboxOldTags.pack_start(tag, False, False, 2)
        
        hboxTitle = Gtk.HBox()
        hboxTitle.pack_start(Gtk.Label(_('Title:')), False, False, 2)
        hboxTitle.pack_start(title, False, False, 2)
        
        hboxTags = Gtk.HBox()
        hboxTags.pack_start(Gtk.Label(_('Labels:')), False, False, 2)
        hboxTags.pack_start(tagsEntry, False, False, 2)

        tab.pack_start(hboxTitle, False, False, 2)
        tab.pack_start(hboxTags, False, False, 2)
        tab.pack_start(hboxOldTags, False, False, 2)
        
        hbox = Gtk.HBox()
        tab.get_children()[3].reparent(hbox)
        
        vbox = Gtk.VBox()
        
        #commentsFrame = Gtk.Frame(_('Comments'))
        #attachmentsFrame = Gtk.Frame(_('Attachments'))

        commentsFrame = Gtk.Frame()
        attachmentsFrame = Gtk.Frame()
        
        vbox.pack_start(commentsFrame, True, True, 2)
        vbox.pack_end(attachmentsFrame, True, True, 2)
        
        #comments.Comments(self.confluence).get(commentsFrame, page.id)
        #attachments.Attachments(self.confluence).get(attachmentsFrame, page.id)
        
        paned = Gtk.HPaned()
        paned.set_position(1000)
        
        #paned.add1(hbox)
        paned.add2(vbox)
        
        tab.pack_start(hbox, True, True, 2)
        
        #hbox.pack_start(vbox, True, True, 2)
        #tab.get_parent().get_tab_label(tab).get_children()[0].get_children()[0].get_children()[2].set_text(page.title)
        tab.get_document().set_short_name_for_display(self.page.title)

        tab.get_document().connect("saving", self._save, tab, self.page)
        
        tab.show_all()
        #tab.get_document().set_short_name_for_display(page.title)
        #tab.get_parent().get_tab_label(tab).get_children()[0].get_children()[0].get_children()[2].set_text(page.title)

        return ['file://' + tf.name, self.page]

    def add(self, menuitem, geditWindow, spaceKey, parentPageId=None):
        dialog = Gtk.MessageDialog(
            None,
            Gtk.DIALOG_MODAL | Gtk.DIALOG_DESTROY_WITH_PARENT,
            Gtk.MESSAGE_QUESTION,
            Gtk.BUTTONS_OK,
            None)
        dialog.set_markup('Please enter the title of the page:')
        #create the text input field
        entry = Gtk.Entry()
        hbox = Gtk.HBox()
        hbox.pack_start(Gtk.Label("Title:"), False, 5, 5)
        hbox.pack_end(entry)
        #some secondary text
        #add it and show it
        dialog.vbox.pack_end(hbox, True, True, 0)
        dialog.show_all()
        #go go go
        dialog.run()
        title = entry.get_text()
        
        if title.strip() == "" and Gtk.RESPONSE_OK:
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

    def _save(self, document, arg1, arg2, tab, page):
        path = tab.get_document().get_location()

        title = tab.get_children()[0].get_children()[1].get_text()
        tags = tab.get_children()[1].get_children()[1].get_text()

        self.page.title = title
        self.page.content = tab.get_document().get_text(tab.get_document().get_start_iter(), tab.get_document().get_end_iter(), True)
        
        updateOptions = confluencerpclib.PageUpdateOptions()
        updateOptions.versionComment = ''
        updateOptions.minorEdit = True
        
        try:
            self.page = self.confluence.updatePage(self.page, updateOptions)
        except Exception, err:
            if err.__str__().find('InvalidSessionException'):
                self.confluence.login(self.options._settings.get_string(self.options.USERNAME),
                                    self.options._settings.get_string(self.options.PASSWORD))
                self.page = self.confluence.updatePage(self.page, updateOptions)
        
        if tags.strip() != "":
            self.confluence.addLabelByName(tags, self.page.id)

    def save(self, window, tabs):
        tab = window.get_active_tab()
        path = tab.get_document().get_location()

        print tab.get_state()
        
        if tab and tab.get_state() == GEDIT_TAB_STATE_SAVING and tabs.has_key(path):
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
                self.confluence.addLabelByName(tags, tabs[path].id)
            
            return tabs

    def _clickTagDelete(self, widget, labelId, objectId):
        self.confluence.removeLabelById(labelId, objectId)
        widget.destroy()
