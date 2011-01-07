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
        
        if len(comments) == 0:
            widget.add(gtk.Label(_('No comments for this page')))
