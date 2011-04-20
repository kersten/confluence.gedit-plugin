import gtk
from gobject import idle_add, PARAM_READWRITE, SIGNAL_RUN_FIRST, TYPE_PYOBJECT
import pango


class CellRendererWidget(gtk.GenericCellRenderer):
    __gtype_name__ = 'CellRendererWidget'
    __gproperties__ = {
        'widget': (TYPE_PYOBJECT, 'Widget', 'The column containing the widget to render', PARAM_READWRITE),
    }

    XPAD = 2
    YPAD = 2


    # INITIALIZERS #
    def __init__(self, strfunc, default_width=-1):
        gtk.GenericCellRenderer.__init__(self)

        self.default_width = default_width
        self._editing = False
        self.strfunc = strfunc
        self.widget = None
        self.pango_l  = None
        self.text = ""
        self.xpad = 1; self.ypad = 0
        self.xalign = 0.5; self.yalign = 0.5


    # INTERFACE METHODS #
    def do_set_property(self, pspec, value):
        setattr(self, pspec.name, value)

    def do_get_property(self, pspec):
        return getattr(self, pspec.name)

    def on_get_size(self, widget, cell_area):
        if cell_area:
            calc_width = cell_area.width - 2*self.xpad
            calc_height = cell_area.height - 2*self.ypad
            x_offset = int(self.xalign * (cell_area.width - calc_width))
            x_offset = max(x_offset, 0)
            y_offset = int(self.yalign * (cell_area.height - calc_height))
            y_offset = max(y_offset, 0)
        else:
            x_offset = 0
            y_offset = 0
            calc_width = 20
            calc_height = 16
        return x_offset, y_offset, calc_width, calc_height

    def on_render(self, window, widget, bg_area, cell_area, expose_area, flags):
        x_offset, y_offset, width, height = self.on_get_size(widget, 
                cell_area)
        widget.style.paint_box(window,
                               gtk.STATE_NORMAL, gtk.SHADOW_OUT,
                               cell_area, widget, None,
                               cell_area.x,
                               cell_area.y,
                               cell_area.width,  cell_area.height)
        if self.pango_l is None:
            context = widget.create_pango_context()
            self.pango_l = pango.Layout(context)
        self.pango_l.set_text(self.text)
        w, h = self.pango_l.get_pixel_size()
        widget.style.paint_layout(window, gtk.STATE_NORMAL, True,
                cell_area, widget, None,
                cell_area.x + x_offset + (width -w)/2,
                cell_area.y + y_offset + (height -h)/2,
                self.pango_l)
        #window.draw_rectangle(self.gc, True, cell_area.x+x_offset, 
        #                      cell_area.y+ y_offset, width, height)

    def on_start_editing(self, event, tree_view, path, bg_area, cell_area, flags):
        #print '%s>> on_start_editing(flags=%s, event=%s)' % (self.strfunc(self.widget), flagstr(flags), event)
        return False
        
        editable = self.widget
        if not isinstance(editable, gtk.CellEditable):
            editable = CellWidget(editable)
        editable.show_all()
        editable.grab_focus()
        return editable

    # METHODS #
    def create_pango_layout(self, string, widget, width):
        font = widget.get_pango_context().get_font_description()
        layout = pango.Layout(widget.get_pango_context())
        layout.set_font_description(font)
        layout.set_wrap(pango.WRAP_WORD_CHAR)
        layout.set_width(width * pango.SCALE)
        layout.set_markup(string)
        # This makes no sense, but mostly has the desired effect to align things correctly for
        # RTL languages which is otherwise incorrect. Untranslated entries is still wrong.
        if widget.get_direction() == gtk.TEXT_DIR_RTL:
            layout.set_alignment(pango.ALIGN_RIGHT)
            layout.set_auto_dir(False)
        return layout

    def _start_editing(self, treeview):
        """Force the cell to enter editing mode by going through the parent
            gtk.TextView."""
        if self._editing:
            return
        return
        self._editing = True

        model, iter = treeview.get_selection().get_selected()
        path = model.get_path(iter)
        col = [c for c in treeview.get_columns() if self in c.get_cell_renderers()]
        if len(col) < 1:
            self._editing = False
            return
        treeview.set_cursor_on_cell(path, col[0], self, True)
        # XXX: Hack to make sure that the lock (_start_editing) is not released before the next on_render() is called.
        def update_lock():
            self._editing = False
        idle_add(update_lock)
