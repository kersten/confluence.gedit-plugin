SUBDIRS = confluence

NULL =

plugindir = $(GEDIT_PLUGIN_DIR)

plugin_in_files = \
	confluence.gedit-plugin.desktop.in \
	$(NULL)

%.gedit-plugin: %.gedit-plugin.desktop.in \
	$(INTLTOOL_MERGE) $(wildcard $(top_srcdir)/po/*po); \
	$(INTLTOOL_MERGE) $(top_srcdir)/po $< \
	$@ -d -u -c $(top_builddir)/po/.intltool-merge-cache

plugin_DATA = $(plugin_in_files:.gedit-plugin.desktop.in=.gedit-plugin)

EXTRA_DIST = $(plugin_in_files)

dist-hook:

CLEANFILES = *.bak *.pyc *.pyo $(plugin_DATA)
DISTCLEANFILES = *.bak *.pyc *.pyo $(plugin_DATA)
