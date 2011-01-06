# Copyright (C) 2010 Curtis C. Hovey
#
# Copying and distribution of this file, with or without modification,
# are permitted in any medium without royalty provided the copyright notice
# and this notice are preserved.

AC_DEFUN([AC_CHECK_PYTHON_MODULE],[
    # AC_CHECK_PYTHON_MODULE(MODULE_NAME)
    MODULE_NAME=$1
    AC_MSG_CHECKING(for python module $MODULE_NAME)
    if test -z $PYTHON; then
        PYTHON="python"
    fi
    $PYTHON -c "import $MODULE_NAME" 2>/dev/null
    if test $? -eq 0; then
        AC_MSG_RESULT(yes)
    else
        AC_MSG_RESULT(not found)
        exit 1
    fi
])
