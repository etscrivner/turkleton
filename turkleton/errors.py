# -*- coding: utf-8 -*-
"""
    turkleton.errors
    ~~~~~~~~~~~~~~~~
    Defines base classes for all errors


"""


class Error(Exception):
    """Base class for all errors"""
    pass


class ConnectionError(Error):
    """Error involving a connection to a service"""
    pass
