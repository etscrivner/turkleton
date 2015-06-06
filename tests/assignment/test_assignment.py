# -*- coding: utf-8 -*-
import unittest

import mock

from tests.assignment import factories
from turkleton import connection
from turkleton import errors
from turkleton.assignment import answer
from turkleton.assignment import assignment


class FakeAssignment(assignment.BaseAssignment):
    """Fake assignment used throughout testing"""
    age = answer.TextAnswer('Age', None)
    categories = answer.MultiChoiceAnswer('Categories')
    is_old = answer.BooleanAnswer('IsOld', True)


class BaseAssignmentTestCase(unittest.TestCase):

    def setUp(self):
        super(BaseAssignmentTestCase, self).setUp()
        self.assignment_fixture = {
            'Age': '29',
            'IsOld': '0',
            'Categories': 'Front|WaistUp'
        }
        self.boto_assignment_fixture = factories.make_boto_assignment(
            self.assignment_fixture
        )
        self.fake_assignment = FakeAssignment(self.boto_assignment_fixture)

    def test_should_correctly_initialize_age(self):
        self.assertEqual(
            self.assignment_fixture['Age'], self.fake_assignment.age
        )


class TestGetQuestionNameToAnswerAttributeTable(unittest.TestCase):

    def test_should_return_empty_dictionary_for_class_without_answers(self):
        self.assertEqual(
            {},
            assignment.get_question_name_to_answer_attribute_table(
                self.__class__
            )
        )

    def test_should_have_correct_set_of_question_names(self):
        result = assignment.get_question_name_to_answer_attribute_table(
            FakeAssignment
        )
        self.assertEqual(set(['Age', 'IsOld', 'Categories']), set(result))

    def test_should_have_correct_attribute_names(self):
        result = assignment.get_question_name_to_answer_attribute_table(
            FakeAssignment
        )
        self.assertEqual(
            set(['age', 'is_old', 'categories']),
            set(result.values())
        )


class TestGetAnswerToQuestion(unittest.TestCase):

    def setUp(self):
        super(TestGetAnswerToQuestion, self).setUp()
        self.assignment_fixture = {
            'Age': '29',
            'IsOld': '1',
            'Categories': 'Front'
        }
        self.mock_assignment = factories.make_boto_assignment(
            self.assignment_fixture
        )

    def test_shold_return_none_if_none_givne(self):
        self.assertIsNone(assignment.get_answer_to_question(None, 'Herp'))

    def test_should_return_none_if_answers_attribute_is_none(self):
        self.mock_assignment.answers = None
        self.assertIsNone(
            assignment.get_answer_to_question(self.mock_assignment, 'Herp')
        )

    def test_should_return_none_if_assignment_does_not_have_question(self):
        self.assertIsNone(
            assignment.get_answer_to_question(self.mock_assignment, 'Herp')
        )

    def test_should_return_correct_answer_to_question(self):
        result = assignment.get_answer_to_question(self.mock_assignment, 'Age')
        self.assertEqual(self.assignment_fixture['Age'], result)


class TestBaseAssignment(BaseAssignmentTestCase):

    def test_should_correctly_initialize_is_old(self):
        self.assertFalse(self.fake_assignment.is_old)

    def test_should_have_correct_categories(self):
        self.assertEqual(
            self.assignment_fixture['Categories'].split('|'),
            self.fake_assignment.categories
        )

    def test_should_have_correct_assignment_id(self):
        self.assertEqual(
            self.boto_assignment_fixture.AssignmentId,
            self.fake_assignment.assignment_id
        )

    def test_should_have_correct_hit_id(self):
        self.assertEqual(
            self.boto_assignment_fixture.HITId,
            self.fake_assignment.hit_id
        )

    def test_should_have_correct_worker_id(self):
        self.assertEqual(
            self.boto_assignment_fixture.WorkerId,
            self.fake_assignment.worker_id
        )


class TestApprove(BaseAssignmentTestCase):

    def test_should_pass_correct_information_to_boto_connection(self):
        mock_connection = mock.MagicMock()
        connection.set_connection(mock_connection)
        self.fake_assignment.approve('Good job!')
        mock_connection.approve_assignment.assert_called_once_with(
            self.fake_assignment.assignment_id,
            'Good job!'
        )


class TestReject(BaseAssignmentTestCase):

    def test_should_pass_correct_arguments_to_connection(self):
        mock_connection = mock.MagicMock()
        connection.set_connection(mock_connection)
        self.fake_assignment.reject('Bad job!')
        mock_connection.reject_assignment.assert_called_once_with(
            self.fake_assignment.assignment_id,
            'Bad job!'
        )


class TestGetByHitId(BaseAssignmentTestCase):

    def setUp(self):
        super(TestGetByHitId, self).setUp()
        self.mock_connection = mock.MagicMock()
        connection.set_connection(self.mock_connection)

    def test_should_pass_correct_information_to_retrieval_method(self):
        FakeAssignment.get_by_hit_id(
            self.fake_assignment.hit_id
        )
        self.mock_connection.get_assignments.assert_called_once_with(
            self.fake_assignment.hit_id
        )

    def test_should_wrap_assignment_class_around_each_result(self):
        self.mock_connection.get_assignments.return_value = [
            factories.make_boto_assignment(self.assignment_fixture)
        ]
        result = FakeAssignment.get_by_hit_id('1234')
        self.assertTrue(
            all([isinstance(each, FakeAssignment) for each in result])
        )
