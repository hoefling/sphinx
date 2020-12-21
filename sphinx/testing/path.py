"""
    sphinx.testing.path
    ~~~~~~~~~~~~~~~~~~~

    :copyright: Copyright 2007-2020 by the Sphinx team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""

import builtins
import os
import pathlib
import shutil
import sys
import warnings
from typing import Any, Callable, IO, List, Union, TYPE_CHECKING

from sphinx.deprecation import RemovedInSphinx50Warning

FILESYSTEMENCODING = sys.getfilesystemencoding() or sys.getdefaultencoding()


if TYPE_CHECKING:
    _PathLike = Union[str, os.PathLike[str]]
else:
    _PathLike = Union[str, os.PathLike]


class path(type(pathlib.Path())):
    """
    Represents a path with extended functionality.
    """

    def is_mount(self) -> bool:
        """
        Returns ``True`` if the path is a mount point.
        """
        return os.path.ismount(self)

    def rmtree(self, ignore_errors: bool = False, onerror: Callable[[Any, Any, Any], Any] = None) -> None:
        """
        Removes the file or directory and any files or directories it may
        contain.

        :param ignore_errors:
            If ``True`` errors are silently ignored, otherwise an exception
            is raised in case an error occurs.

        :param onerror:
            A callback which gets called with the arguments `func`, `path` and
            `exc_info`. `func` is one of :func:`os.listdir`, :func:`os.remove`
            or :func:`os.rmdir`. `path` is the argument to the function which
            caused it to fail and `exc_info` is a tuple as returned by
            :func:`sys.exc_info`.
        """
        shutil.rmtree(self, ignore_errors=ignore_errors, onerror=onerror)

    def copytree(self, destination: _PathLike, symlinks: bool = False) -> None:
        """
        Recursively copy a directory to the given `destination`. If the given
        `destination` does not exist it will be created.

        :param symlinks:
            If ``True`` symbolic links in the source tree result in symbolic
            links in the destination tree otherwise the contents of the files
            pointed to by the symbolic links are copied.
        """
        shutil.copytree(self, destination, symlinks=symlinks)

    def movetree(self, destination: _PathLike) -> None:
        """
        Recursively move the file or directory to the given `destination`
        similar to the  Unix "mv" command.

        If the `destination` is a file it may be overwritten depending on the
        :func:`os.rename` semantics.
        """
        shutil.move(self, destination)

    move = movetree

    def utime(self, arg: Any) -> None:
        os.utime(self, arg)

    def lexists(self) -> bool:
        """
        Returns ``True`` if the path exists unless it is a broken symbolic
        link.
        """
        return os.path.lexists(self)
