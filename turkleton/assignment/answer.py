# -*- coding: utf-8 -*-
"""
    turkleton.assignment.answer
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~
    Representations for various answer types from uploaded HITs.

"""
import six


class BaseAnswer(object):
    """Base class for all answer types. This is a descriptor class."""

    #: Indicates that the value of this answer has not been set.
    _EMPTY = object()
    #: Value to indicate the default value if none is given
    _DEFAULT = object()

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
        if self.value is self._EMPTY:
            return self.default

        return self.value

    def __set__(self, obj, val):
        """Descriptor method for setting attribute value"""
        self.value = val


class TextAnswer(BaseAnswer):
    """An answer representing simple textual input"""


class BooleanAnswer(BaseAnswer):
    """An answer representing a boolean choice"""

    #: Default mapping of strings to booleans
    DEFAULT_STRING_TO_BOOL = {'1': True, '0': False}

    def __init__(self, question_name, default, string_to_bool=None):
        """Initialize the boolean answer with the given information.

        :param question_name: A question name
        :type question_name: str or unicode
        :param default: Default value for boolean
        :type default: mixed
        :param string_to_bool: (Default is {'1': True, '0': False}) A
            dictionary mapping string values to booleans.
        :type string_to_bool: dict or None
        """
        super(BooleanAnswer, self).__init__(
            question_name=question_name,
            default=default
        )
        self.string_to_bool = (
            string_to_bool
            if string_to_bool
            else self.DEFAULT_STRING_TO_BOOL
        )

    def __set__(self, obj, val):
        """Set this value to the given answer. If a string it will attempt to
        convert it into a boolean.
        """
        self.value = val
        if isinstance(val, six.string_types):
            self.value = self.string_to_bool.get(val, self._EMPTY)


class MultiChoiceAnswer(BaseAnswer):
    """An answer with multiple potential choices for input"""

    def __init__(self, question_name, default=BaseAnswer._DEFAULT):
        super(MultiChoiceAnswer, self).__init__(question_name, default)

    def __get__(self, obj, objtype):
        """Return the value or the default value. If default value is _DEFAULT then
        this will return an empty list"""
        if self.value is self._EMPTY:
            return [] if self.default is self._DEFAULT else self.default
        return self.value

    def __set__(self, obj, val):
        """In Mechanical Turk multi-choice answers come across as text answers
        separated by the pipe (|) character. Handle this type of input here"""
        self.value = val
        if isinstance(val, six.string_types):
            self.value = val.split('|') if val else self._EMPTY
