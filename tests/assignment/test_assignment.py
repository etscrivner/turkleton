# -*- coding: utf-8 -*-
import unittest

from turkleton.assignment import answer
from turkleton.assignment import assignment
from tests.assignment import factories


class FakeAssignment(assignment.BaseAssignment):
    """Fake assignment used throughout testing"""
    age = answer.TextAnswer('Age', None)
    categories = answer.MultiChoiceAnswer('Categories')
    is_old = answer.BooleanAnswer('IsOld', True)


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
        self.assertEqual(['Age', 'IsOld', 'Categories'], result.keys())

    def test_should_have_correct_attribute_names(self):
        result = assignment.get_question_name_to_answer_attribute_table(
            FakeAssignment
        )
        self.assertEqual(['age', 'is_old', 'categories'], result.values())


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


class TestBaseAssignment(unittest.TestCase):

    def setUp(self):
        super(TestBaseAssignment, self).setUp()
        self.assignment_fixture = {
            'Age': '29',
            'IsOld': '0',
            'Categories': 'Front|WaistUp'
        }
        self.boto_assignment_fixture = factories.make_boto_assignment(
            self.assignment_fixture
        )

    def test_should_correctly_initialize_age(self):
        fake_assignment = FakeAssignment(self.boto_assignment_fixture)
        self.assertEqual(self.assignment_fixture['Age'], fake_assignment.age)

    def test_should_correctly_initialize_is_old(self):
        fake_assignment = FakeAssignment(self.boto_assignment_fixture)
        self.assertFalse(fake_assignment.is_old)

    def test_should_have_correct_categories(self):
        fake_assignment = FakeAssignment(self.boto_assignment_fixture)
        self.assertEqual(
            self.assignment_fixture['Categories'].split('|'),
            fake_assignment.categories
        )
