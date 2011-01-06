SUBDIRS = po src

NULL =

EXTRA_DIST = \
	intltool-merge.in \
	intltool-update.in \
	intltool-extract.in	\
	ChangeLog \
	AUTHORS \
	COPYING \
	HACKING \
	INSTALL \
	NEWS \
	README \
	test.py \
	$(NULL)

DISTCLEANFILES = \
	intltool-extract \
	intltool-merge \
	intltool-update \
	po/.intltool-merge-cache \
	$(NULL)

DISTCHECK_CONFIGURE_FLAGS = \
	--with-home

dist-hook:
	(cd $(srcdir) && utils/gen-gedit.py)
	mkdir $(distdir)/gedit
	cp -p $(srcdir)/gedit/* $(distdir)/gedit
	mkdir $(distdir)/utils
	cp -p $(srcdir)/utils/* $(distdir)/utils
