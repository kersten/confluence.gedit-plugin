# Process this file with autoconf to produce a configure script.

AC_PREREQ(2.61)

m4_define(gc_major_version, 0)
m4_define(gc_minor_version, 1)
m4_define(gc_micro_version, 0)
m4_define(gc_version, gdp_major_version.gdp_minor_version.gdp_micro_version)

AC_INIT(gedit-confluence, gdp_version, kerstenk@gmail.com)
AM_INIT_AUTOMAKE([1.9 -Wno-portability])
IT_PROG_INTLTOOL([0.35.0])

AM_MAINTAINER_MODE

# Command line options.
AC_ARG_WITH([home],
    AS_HELP_STRING([--without-home],
        [Do not install the plugins in $HOME/.gnome2/gedit]),
    ,
    [with_home=yes]
)

# Checks for programs.
AM_PATH_PYTHON

# Checks for libraries.
# We should check for Gedit, but the package pkg-config data is
# not always available. gtksourceview is a good indicator of the
# Gedit version.
PKG_CHECK_MODULES(GEDIT, [
    pygtk-2.0 >= 2.14
    gedit-2.20 >= 2.29.0
])

# i18n configuration.
GETTEXT_PACKAGE=gedit-confluence-plugin
AC_SUBST([GETTEXT_PACKAGE])
AC_DEFINE_UNQUOTED([GETTEXT_PACKAGE], "$GETTEXT_PACKAGE", [Gettext package])
AM_GLIB_GNU_GETTEXT

# Checks for header files.

# Checks for typedefs, structures, and compiler characteristics.

# Checks for library functions.
AC_CHECK_PYTHON_MODULE(pocketlint)

libdir=${prefix}/lib
sharedir=${prefix}/share

# Set the location to install the plugins. The personal location (.gnome2)
# is different from public locations.
AC_DEFUN([GEDIT_PLUGIN], [
    if test $with_home = 'yes'; then
        gedit_plugin_dir="${HOME}/.gnome2/gedit/plugins"
        prefix=`echo "${HOME}/.local"`
    else
        gedit_plugin_dir="${libdir}/gedit-2/plugins"
    fi
    AC_SUBST(GEDIT_PLUGIN_DIR, [$gedit_plugin_dir])
])
GEDIT_PLUGIN

# Automake files to create
AC_CONFIG_FILES([
    Makefile
    src/Makefile
    src/confluence/Makefile
    po/Makefile.in
])
AC_OUTPUT

echo "

Configuration:
    prefix: ${prefix}
    gedit plugin dir: $GEDIT_PLUGIN_DIR
"
