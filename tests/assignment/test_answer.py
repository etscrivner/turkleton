# -*- coding: utf-8 -*-
import unittest

from turkleton.assignment import answer


class TestBaseAnswer(unittest.TestCase):

    class DescriptorTestClass(object):
        """Class for testing BaseAnswer descriptor behavior"""
        prop = answer.BaseAnswer('WhatIsIt', 'This')

    def setUp(self):
        super(TestBaseAnswer, self).setUp()
        self.question_name = 'WhatIsIt'
        self.default_value = 'This'
        self.base_answer = answer.BaseAnswer(
            self.question_name, self.default_value
        )

    def test_should_set_question_name(self):
        self.assertEqual(self.question_name, self.base_answer.question_name)

    def test_should_set_default_value(self):
        self.assertEqual(self.default_value, self.base_answer.default)

    def test_should_initially_contain_empty_value(self):
        self.assertTrue(self.base_answer.value is answer.BaseAnswer._EMPTY)

    def test_should_return_default_value_if_empty(self):
        inst = self.DescriptorTestClass()
        self.assertEqual(self.base_answer.default, inst.prop)

    def test_should_return_value_if_value_is_not_empty(self):
        inst = self.DescriptorTestClass()
        inst.prop = 123
        self.assertEqual(123, inst.prop)


class TestBooleanAnswer(unittest.TestCase):

    class DescriptorTestClass(object):
        """Class for testing descriptor properties of answer"""
        prop = answer.BooleanAnswer('Herp', False)

    class AlternateMappingDescriptorTestClass(object):
        """Class for testing descriptor with alternative str-bool mapping"""
        prop = answer.BooleanAnswer('Herp', False, {'T': True, 'F': False})

    def setUp(self):
        super(TestBooleanAnswer, self).setUp()
        self.descriptor_class = self.DescriptorTestClass()

    def test_should_be_able_to_set_to_true_from_string(self):
        self.descriptor_class.prop = '1'
        self.assertTrue(self.descriptor_class.prop)

    def test_should_be_able_to_set_to_false_from_string(self):
        self.descriptor_class.prop = '0'
        self.assertFalse(self.descriptor_class.prop)

    def test_should_be_able_to_set_to_boolean_true(self):
        self.descriptor_class.prop = True
        self.assertTrue(self.descriptor_class.prop)

    def test_should_be_able_to_set_to_boolean_false(self):
        self.descriptor_class.prop = False
        self.assertFalse(self.descriptor_class.prop)

    def test_should_leave_empty_if_none_given(self):
        self.descriptor_class.prop = None
        self.assertFalse(self.descriptor_class.prop)

    def test_should_be_able_to_redefine_true_values(self):
        alternate_class = self.AlternateMappingDescriptorTestClass()
        alternate_class.prop = 'T'
        self.assertTrue(alternate_class.prop)

    def test_should_be_able_to_redefine_false_values(self):
        alternate_class = self.AlternateMappingDescriptorTestClass()
        alternate_class.prop = 'F'
        self.assertFalse(alternate_class.prop)


class TestMultiChoiceAnswer(unittest.TestCase):

    class DescriptorTestClass(object):
        """Test the answer as a descriptor"""
        prop = answer.MultiChoiceAnswer('Herp')

    def setUp(self):
        super(TestMultiChoiceAnswer, self).setUp()
        self.descriptor_class = self.DescriptorTestClass()

    def test_should_correctly_handle_empty_string(self):
        self.descriptor_class.prop = ''
        self.assertEqual([], self.descriptor_class.prop)

    def test_should_correctly_handle_single_selected_choice(self):
        self.descriptor_class.prop = 'Face'
        self.assertEqual(['Face'], self.descriptor_class.prop)

    def test_should_correctly_handle_multi_items(self):
        self.descriptor_class.prop = 'Face|Neck|Hands'
        self.assertEqual(['Face', 'Neck', 'Hands'], self.descriptor_class.prop)
