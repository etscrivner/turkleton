# -*- coding: utf-8 -*-
"""
    turkleton.assignment.task
    ~~~~~~~~~~~~~~~~~~~~~~~~~
    Representations for the human intelligence task (HIT) portion of an
    assignment.

"""
import datetime

from boto.mturk import layoutparam
from boto.mturk import price

from turkleton import errors


def keywords_from_list(keywords):
    """Convert keywords from a list of strings into the appropriate format for
    creating a Mechanical Turk HIT.

    :param keywords: A list of keywords
    :type keywords: iterable
    :rtype: str or unicode
    """
    return u','.join(keywords) if keywords else None


def dict_to_layout_parameters(dict_to_convert):
    """Convert a dictionary into Mechanical Turk layout parameters. This is
    really equivalent to an XML formalization of a dictionary.

    :param dict_to_convert: A dictionary to be converted
    :type dict_to_convert: dict
    :rtype: boto.mturk.layoutparam.LayoutParameters
    """
    params = []

    if dict_to_convert:
        params = [
            layoutparam.LayoutParameter(k, v)
            for k, v in dict_to_convert.items()
        ]

    return layoutparam.LayoutParameters(params)


class BaseTask(object):
    """Base class for all human intelligence tasks"""

    class ValidationError(errors.Error):
        """Represents an error while validating task"""
        pass

    # The HIT layout ID from Mechanical Turk (changes each time HIT is saved)
    __layout_id__ = None
    # The reward for each completed assignment (eg. 0.25)
    __reward__ = None
    # The title of the assignment shown to turks
    __title__ = None
    # The description of the assignment shown to turkers
    __description__ = None
    # A list of keywords for this assignment (eg. ['parking', 'rates'])
    __keywords__ = None
    # The redundancy for each uploaded assignment (default is 1)
    __assignments_per_hit__ = 1
    # A datetime.timedelta indicating how long after upload before HIT expires
    __hit_expires_in__ = datetime.timedelta(days=7)
    # The amount of time each turk has to complete the assignment
    __time_per_assignment__ = datetime.timedelta(hours=1)
    # The amount of time to review submitted assignments before auto approval
    __auto_approval_delay__ = datetime.timedelta(hours=8)
    # The currency code for prices
    __currency_code__ = 'USD'

    def __init__(self, **assignment_params):
        """Initialize this object from the given keyword arguments

        :param assignment_params: A dict of assignment parameters
        :type assignment_params: dict
        """
        self.assignment_params = assignment_params

    def validate(self):
        """Validate the attributes of this class. Raises ValidationError if any
        problems are found."""
        required_fields = [
            '__layout_id__',
            '__reward__',
            '__title__',
            '__description__'
        ]

        for each in required_fields:
            if getattr(self, each) is None:
                raise self.ValidationError('Task is missing {}.'.format(each))

    def upload(self, mturk_connection, batch_id=None):
        """Attempt to upload this task to mechanical turk.

        :param mturk_connection: A mechanical turk connection
        :type mturk_connection: boto.mturk.connection.MTurkConnection
        :param batch_id: An optional ID to attach to this object
        :type batch_id: mixed
        """
        self.validate()

        params = dict_to_layout_parameters(self.assignment_params)
        reward_price = price.Price(
            amount=self.__reward__,
            currency_code=self.__currency_code__
        )
        keywords = keywords_from_list(self.__keywords__)
        return mturk_connection.create_hit(
            hit_layout=self.__layout_id__,
            reward=reward_price,
            title=self.__title__,
            description=self.__description__,
            keywords=keywords,
            max_assignments=self.__assignments_per_hit__,
            lifetime=self.__hit_expires_in__,
            duration=self.__time_per_assignment__,
            approval_delay=self.__auto_approval_delay__,
            annotation=batch_id,
            layout_params=params
        )
