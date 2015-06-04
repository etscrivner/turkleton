# -*- coding: utf-8 -*-
"""
    turkleton.assignment.assignment
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    Representations for the results from uploaded HITs.

"""
from turkleton.assignment import answer


def get_question_name_to_answer_attribute_table(cls):
    """Get a question name to answer attribute translation table for the given
    class. This is used to determine which attributes to set when a given
    question is encountered in an assignment

    :param cls: A class
    :type cls: class
    :rtype: dict
    """
    return {
        value.question_name: attr_name
        for attr_name, value in cls.__dict__.items()
        if isinstance(value, answer.BaseAnswer)
    }


def get_answer_to_question(assignment, question_name):
    """Get the answer to the given question from an assignment.

    :param assignment: An assignment
    :type assignment: boto.mturk.Assignment
    :param question_name: The name of the question
    :type question_name: str or unicode
    :rtype: str or unicode
    """
    if not assignment:
        return None

    if not assignment.answers:
        return None

    for each in assignment.answers[0]:
        if each.qid == question_name:
            return each.fields[0] if each.fields else None

    return None


class BaseAssignment(object):
    """Base class for all assignments"""

    def __init__(self, assignment):
        """Initialize this class with the given assignment.

        :param assignment: An assignment
        :type assignment: boto.mturk.Assignment
        """
        self.assignment = assignment
        self.question_to_attr = get_question_name_to_answer_attribute_table(
            self.__class__
        )

        for question_name, attr_name in self.question_to_attr.items():
            answer = get_answer_to_question(self.assignment, question_name)
            setattr(self, attr_name, answer)

    @property
    def assignment_id(self):
        """Return the ID associated with this assignment.

        :rtype: str or unicode
        """
        return self.assignment.AssignmentId

    @property
    def hit_id(self):
        """Return the ID associated with this HIT.

        :rtype: str or unicode
        """
        return self.assignment.HITId

    @property
    def worker_id(self):
        """Return the ID of the worker who completed this assignment.

        :rtype: str or unicode
        """
        return self.assignment.WorkerId
