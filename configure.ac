# Process this file with autoconf to produce a configure script.

AC_PREREQ(2.63.2)

m4_define(gc_major_version, 0)
m4_define(gc_minor_version, 1)
m4_define(gc_micro_version, 1)
m4_define(gc_version, gc_major_version.gc_minor_version.gc_micro_version)

AC_INIT(gedit-confluence, gc_version, kerstenk@gmail.com)
AC_CONFIG_HEADERS([config.h])
AC_CONFIG_SRCDIR([src])
AC_CONFIG_MACRO_DIR([m4])
AC_CONFIG_AUX_DIR([build-aux])
AC_PREFIX_PROGRAM([gedit])

AM_INIT_AUTOMAKE([1.10 dist-bzip2 no-dist-gzip])
AM_MAINTAINER_MODE([enable])

m4_ifdef([AM_SILENT_RULES],[AM_SILENT_RULES([yes])])

# Check for programs
AC_PROG_CC
AC_PROG_INSTALL
AC_PROG_MAKE_SET
AC_SYS_LARGEFILE
PKG_PROG_PKG_CONFIG
# needed on osx
AC_PROG_OBJC

AM_PATH_PYTHON

# Initialize libtool
LT_PREREQ([2.2.6])
LT_INIT(disable-static)

GTK_DOC_CHECK([1.0],[--flavour=no-tmpl])

AC_CHECK_FUNC(sigaction)
AC_CHECK_LIB(m, floor)

dnl make sure we keep ACLOCAL_FLAGS around for maintainer builds to work
AC_SUBST(ACLOCAL_AMFLAGS, "$ACLOCAL_FLAGS -I m4")

dnl check for win32 platform
AC_MSG_CHECKING([for some Win32 platform])
case "$host" in
  *-*-mingw*|*-*-cygwin*)
    platform_win32=yes
    ;;
  *)
    platform_win32=no
    ;;
esac
AC_MSG_RESULT([$platform_win32])
AM_CONDITIONAL(PLATFORM_WIN32, test "$platform_win32" = "yes")

# ================================================================
# Gettext stuff.
# ================================================================
IT_PROG_INTLTOOL([0.40.0])

AM_GNU_GETTEXT_VERSION([0.17])
AM_GNU_GETTEXT([external])

GETTEXT_PACKAGE=gedit-plugins
AC_SUBST(GETTEXT_PACKAGE)
AC_DEFINE_UNQUOTED(GETTEXT_PACKAGE,"$GETTEXT_PACKAGE", [Gettext package])

# ================================================================
# Start of pkg-config checks
# ================================================================

PKG_CHECK_MODULES(GEDIT, [
	glib-2.0 >= 2.26.0
	gio-2.0 >= 2.26.0
	gtk+-3.0 >= 3.0.0
	gtksourceview-3.0 >= 3.0.0
	libpeas-1.0 >= 0.7.3
	libpeas-gtk-1.0 >= 0.7.3
	gedit >= 3.0.0
])

dnl ================================================================
dnl GSettings stuff
dnl ================================================================

GLIB_GSETTINGS

AC_SUBST(PLUGIN_LIBTOOL_FLAGS)

GEDIT_PLUGINS_LIBS_DIR="$libdir/gedit/plugins"
AC_SUBST(GEDIT_PLUGINS_LIBS_DIR)

GEDIT_PLUGINS_DATA_DIR="$datadir/gedit/plugins"
AC_SUBST(GEDIT_PLUGINS_DATA_DIR)

# Automake files to create
AC_CONFIG_FILES([
    Makefile
    src/Makefile
    src/confluence/Makefile
    src/org.gnome.gedit.plugins.confluence.gschema.xml.in
    po/Makefile.in
])
AC_OUTPUT

echo "

Configuration:
    prefix: ${prefix}
    gedit plugin dir: $GEDIT_PLUGIN_DIR
"
