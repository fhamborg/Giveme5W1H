import os

"""
the only purpose of this file is to resolve path always relative to this file,
because the python path system is a mess
"""


def path(x):
    """
    return a path relative to the give file
    :param x: a path
    :return:
    """
    return os.path.abspath(os.path.join(os.path.dirname(__file__), x))
