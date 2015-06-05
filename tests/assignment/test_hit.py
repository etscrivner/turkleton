# -*- coding: utf-8 -*-
import unittest

import mock

from tests.assignment import factories
from turkleton.assignment import hit


class TestInBatch(unittest.TestCase):

    def test_should_return_false_if_batch_id_is_none(self):
        fake_hit = factories.make_hit()
        self.assertFalse(hit.in_batch(None, fake_hit))

    def test_should_return_false_if_none_given_for_hit(self):
        self.assertFalse(hit.in_batch('1234', None))

    def test_should_return_true_if_batch_in_hit(self):
        fake_hit = factories.make_hit()
        self.assertTrue(hit.in_batch(fake_hit.RequesterAnnotation, fake_hit))


class TestGetReviewableByBatchId(unittest.TestCase):

    def setUp(self):
        super(TestGetReviewableByBatchId, self).setUp()
        self.mock_connection = mock.MagicMock()

    def test_should_return_empty_list_if_no_results(self):
        self.mock_connection.get_reviewable_hits.return_value = []
        self.assertEqual(
            [],
            hit.get_reviewable_by_batch_id(self.mock_connection, '1234')
        )

    def test_should_only_return_hit_ids_that_are_in_batch(self):
        fake_hits = [
            factories.make_hit(batch_id='1234'),
            factories.make_hit(batch_id='4567')
        ]
        self.mock_connection.get_reviewable_hits.return_value = fake_hits
        result = hit.get_reviewable_by_batch_id(self.mock_connection, '1234')
        self.assertEqual(1, len(result))
        self.assertEqual(result[0].hit_id, fake_hits[0].HITId)
