# -*- coding: utf-8 -*-
import decimal
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
        self.assertTrue(
            self.base_answer.value_store[self.base_answer]
            is answer.BaseAnswer._EMPTY
        )

    def test_should_return_default_value_if_empty(self):
        inst = self.DescriptorTestClass()
        self.assertEqual(self.base_answer.default, inst.prop)

    def test_should_return_value_if_value_is_not_empty(self):
        inst = self.DescriptorTestClass()
        inst.prop = 123
        self.assertEqual(123, inst.prop)

    def test_should_preserve_values_across_separate_instances(self):
        inst1 = self.DescriptorTestClass()
        inst1.prop = '1'
        inst2 = self.DescriptorTestClass()
        inst2.prop = '2'
        self.assertEqual('1', inst1.prop)
        self.assertEqual('2', inst2.prop)


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

    def test_should_preserve_value_across_separate_instances(self):
        desc1 = self.DescriptorTestClass()
        desc1.prop = '1'
        desc2 = self.DescriptorTestClass()
        desc2.prop = '0'
        self.assertTrue(desc1.prop)
        self.assertFalse(desc2.prop)


class TestIntegerAnswer(unittest.TestCase):

    class DescriptorTestClass(object):
        """Test integer answer descriptor"""
        prop = answer.IntegerAnswer('Herp', 0)

    def setUp(self):
        super(TestIntegerAnswer, self).setUp()
        self.descriptor_class = self.DescriptorTestClass()

    def test_should_initialy_be_default_value(self):
        self.descriptor_class.prop = 0
        self.assertEqual(0, self.descriptor_class.prop)

    def test_should_correctly_cast_string_to_integer(self):
        self.descriptor_class.prop = '123456'
        self.assertEqual(123456, self.descriptor_class.prop)

    def test_should_raise_error_if_value_given_is_not_integer(self):
        with self.assertRaises(ValueError):
            self.descriptor_class.prop = 'hello'

    def test_should_preserve_value_across_separate_instances(self):
        desc1 = self.DescriptorTestClass()
        desc1.prop = '123'
        desc2 = self.DescriptorTestClass()
        desc2.prop = '245'
        self.assertEqual(123, desc1.prop)
        self.assertEqual(245, desc2.prop)


class TestDecimalAnswer(unittest.TestCase):

    class DescriptorTestClass(object):
        prop = answer.DecimalAnswer('Herp', 0)

    def setUp(self):
        super(TestDecimalAnswer, self).setUp()
        self.descriptor_class = self.DescriptorTestClass()

    def test_should_correctly_convert_string_to_decimal_value(self):
        self.descriptor_class.prop = '1.2345'
        self.assertEqual(decimal.Decimal('1.2345'), self.descriptor_class.prop)

    def test_should_raise_error_if_invalid_decimal_given(self):
        with self.assertRaises(decimal.InvalidOperation):
            self.descriptor_class.prop = 'hello'

    def test_should_preserve_value_across_separate_instances(self):
        desc1 = self.DescriptorTestClass()
        desc1.prop = '1.23'
        desc2 = self.DescriptorTestClass()
        desc2.prop = '4.56'
        self.assertEqual(decimal.Decimal('1.23'), desc1.prop)
        self.assertEqual(decimal.Decimal('4.56'), desc2.prop)


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

    def test_should_correctly_handle_list_of_items(self):
        self.descriptor_class.prop = ['Face', 'Neck', 'Hands']
        self.assertEqual(['Face', 'Neck', 'Hands'], self.descriptor_class.prop)

    def test_should_preserve_value_across_separate_instances(self):
        desc1 = self.DescriptorTestClass()
        desc1.prop = 'Hand|Foot'
        desc2 = self.DescriptorTestClass()
        desc2.prop = 'Foot|Mouth'
        self.assertEqual(['Hand', 'Foot'], desc1.prop)
        self.assertEqual(['Foot', 'Mouth'], desc2.prop)
