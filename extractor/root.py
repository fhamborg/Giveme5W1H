import importlib
import os

"""
the only purpose of this file is to resolve path always to this file,
because the python path system is a mess

"""

def path(x):
    return os.path.abspath(os.path.join(os.path.dirname(__file__), x))

