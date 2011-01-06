NULL =

plugindir = $(GEDIT_PLUGIN_DIR)/confluence

plugin_PYTHON = \
	__init__.py \
	attachments.py \
	comments.py \
	confluencewidget.py \
	options.py \
	page.py \
	$(NULL)

uidir = $(plugindir)
ui_DATA = \
	confluencePluginConfigureDialog.glade

EXTRA_DIST = $(ui_DATA)

dist-hook:
	mkdir $(distdir)/data
	cp -p $(srcdir)/data/* $(distdir)/data

CLEANFILES = *.bak *.pyc *.pyo $(plugin_DATA)
DISTCLEANFILES = *.bak *.pyc *.pyo $(plugin_DATA)
