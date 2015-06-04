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

    def test_should_raise_error_when_attempt_made_to_get_value(self):
        inst = self.DescriptorTestClass()
        with self.assertRaisesRegexp(NotImplementedError,
                                     "Attempt to read value of BaseAnswer."):
            inst.prop

    def test_should_raise_error_when_attempt_made_to_set_value(self):
        inst = self.DescriptorTestClass()
        with self.assertRaisesRegexp(NotImplementedError,
                                     "Attempt to write value of BaseAnswer."):
            inst.prop = 123
