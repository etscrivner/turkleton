# -*- coding: utf-8 -*-
"""
    tests.assignment.factories
    ~~~~~~~~~~~~~~~~~~~~~~~~~~
    Factories for producing assignment related object.


"""
from turkleton.assignment import task


class CategorizationTaskFixture(task.BaseTask):
    """Represents a simple, testable task"""

    __layout_id__ = '3MCDHXBQ4Z7SJ2ZT2XZACNE142JWKX'
    __reward__ = 0.02
    __title__ = 'Categorize An Image'
    __description__ = 'Categorize this rad image.'
    __keywords__ = ['image', 'categorize']


def make_task(layout_parameters=None):
    """Create a new test task instance.

    :param layout_parameters: (Default is simple dict) The task layout
        parameters.
    :type layout_parameters: dict or None
    :rtype: CategorizationTaskFixture
    """
    if not layout_parameters:
        layout_parameters = {
            'image_url': 'http://herp.com/derp'
        }

    return CategorizationTaskFixture(**layout_parameters)
