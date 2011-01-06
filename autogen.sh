#!/bin/sh
# Run this to generate all the initial makefiles, etc.

srcdir=`dirname $0`
test -z "$srcdir" && srcdir=.

PKG_NAME="gedit-developer-plugins"

(test -f $srcdir/configure.ac  && test -d $srcdir/src) || {
    echo -n "**Error**: Directory "\`$srcdir\'" does not look like the"
    echo " top-level $PKG_NAME directory"
    exit 1
    }

which gnome-autogen.sh || {
    echo "You need to install gnome-common from your distro or gnome.org"
    exit 1
    }

ACLOCAL_FLAGS="$ACLOCAL_FLAGS -I m4" \
    REQUIRED_AUTOMAKE_VERSION=1.9 \
    REQUIRED_MACROS=python.m4 \
    USE_GNOME2_MACROS=1 \
    . gnome-autogen.sh

