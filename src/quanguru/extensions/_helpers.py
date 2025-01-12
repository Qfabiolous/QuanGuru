import os
import sys

def makeDir(path=None):
    """
    A simple method to check if the directory for a given path exist and create the directory if not.
    Or, it can be used get `sys.path[0]` with the default `path=None`.

    Parameters
    ----------
    path : str or None, optional
        path to a directory that may or may not exist, by default None

    Returns
    -------
    str
        the given path or the `sys.path[0]`
    """

    if path is None:
        path = sys.path[0]

    if not os.path.isdir(path):
        os.mkdir(path)
    return path
