# -*- coding: utf-8 -*-
"""
    turkleton.assignment.answer
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~
    Representations for various answer types from uploaded HITs.

"""


class BaseAnswer(object):
    """Base class for all answer types. This is a descriptor class."""

    #: Default value of an answer. Different from None.
    _EMPTY = object()

    def __init__(self, question_name, default):
        """Initialize an answer with the given information.

        :param question_name: The question name
        :type question_name: str or unicode
        :param default: The default value
        :type default: str or unicode
        """
        self.question_name = question_name
        self.default = default
        self.value = self._EMPTY

    def __get__(self, obj, obtype):
        """Descriptor method for retrieving attribute value"""
        raise NotImplementedError('Attempt to read value of BaseAnswer.')

    def __set__(self, obj, val):
        """Descriptor method for setting attribute value"""
        raise NotImplementedError('Attempt to write value of BaseAnswer.')
