# -*- coding: utf-8 -*-
import unittest

import mock

from turkleton import utils


class TestSafeGetAttr(unittest.TestCase):

    def setUp(self):
        super(TestSafeGetAttr, self).setUp()
        self.mock_obj = mock.MagicMock()

    def test_should_corretly_return_the_attribute_named(self):
        self.mock_obj.herp = 'Herp'
        self.assertEqual(
            self.mock_obj.herp,
            utils.safe_getattr(self.mock_obj, 'herp')
        )

    def test_should_return_none_if_attribute_not_present(self):
        del self.mock_obj.herp
        self.assertIsNone(utils.safe_getattr(self.mock_obj, 'herp'))
