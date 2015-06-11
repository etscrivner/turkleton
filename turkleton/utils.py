# -*- coding: utf-8 -*-
"""
    turkleton.utils
    ~~~~~~~~~~~~~~~
    Miscellaneous utility methods

"""


def safe_getattr(obj, attr_name):
    """Get the attribute of an object returning None if the attribute does not
    exist.

    :param obj: An object
    :type obj: mixed
    :param attr_name: The name of the attribute
    :type attr_name: str or unicode
    """
    try:
        return getattr(obj, attr_name)
    except AttributeError:
        return None
