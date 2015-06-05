# -*- coding: utf-8 -*-
"""
    tests.assignment.factories
    ~~~~~~~~~~~~~~~~~~~~~~~~~~
    Factories for producing assignment related object.

"""
import uuid

import mock

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


def make_boto_assignment(values):
    """Creates a new boto assignment mock class with the given fields
    supplied with the specified values.

    :param values: A dictionary mapping question names to values
    :type values: dict
    :rtype: mock.MagicMock
    """
    assignment = mock.MagicMock()
    assignment.AssignmentId = str(uuid.uuid4())
    assignment.HITId = str(uuid.uuid4())
    assignment.WorkerId = str(uuid.uuid4())

    assignment.answers = [[]]
    for key, value in values.items():
        answer_mock = mock.MagicMock()
        answer_mock.qid = key
        answer_mock.fields = [value]
        assignment.answers[0].append(answer_mock)

    return assignment


def make_boto_hit(hit_id=None, batch_id=None):
    """Create a new random HIT.

    :rtype: mock.MagicMock
    """
    hit = mock.MagicMock()
    hit.HITId = (hit_id if hit_id else str(uuid.uuid4()))
    hit.RequesterAnnotation = (batch_id if batch_id else str(uuid.uuid4()))
    return hit
