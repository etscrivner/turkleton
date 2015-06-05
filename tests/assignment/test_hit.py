# -*- coding: utf-8 -*-
import unittest

import mock

from tests.assignment import factories
from turkleton.assignment import hit


class TestTransformRawHits(unittest.TestCase):

    def test_should_return_empty_list_when_none_given(self):
        self.assertEqual([], hit.transform_raw_hits(None))

    def test_should_return_empty_list_when_empty_list_given(self):
        self.assertEqual([], hit.transform_raw_hits([]))

    def test_should_return_appropriately_transformed_hits(self):
        fixture = [factories.make_hit() for _ in range(10)]
        fixture_hit_ids = [each.HITId for each in fixture]
        result = list(hit.transform_raw_hits(fixture))
        self.assertEqual(10, len(result))
        self.assertTrue(
            all([each.hit_id in fixture_hit_ids for each in result])
        )


class TestGetAll(unittest.TestCase):

    def setUp(self):
        super(TestGetAll, self).setUp()
        self.mock_connection = mock.MagicMock()

    def test_should_return_empty_list_if_no_results(self):
        self.mock_connection.get_all_hits.return_value = []
        self.assertEqual([], list(hit.get_all(self.mock_connection)))

    def test_should_return_all_hits_from_connection(self):
        fake_hits = [
            factories.make_hit(batch_id='1234'),
            factories.make_hit(batch_id='4567')
        ]
        self.mock_connection.get_all_hits.return_value = fake_hits
        result = list(hit.get_all(self.mock_connection))
        self.assertEqual(2, len(result))
        result_hit_ids = [each.hit_id for each in result]
        self.assertTrue(all([
            each.HITId in result_hit_ids for each in fake_hits
        ]))


class TestGetAllByBatchId(unittest.TestCase):

    def setUp(self):
        super(TestGetAllByBatchId, self).setUp()
        self.mock_connection = mock.MagicMock()

    def test_test_should_return_empty_list_if_no_results(self):
        self.mock_connection.get_all_hits.return_value = []
        self.assertEqual(
            [],
            list(hit.get_all_by_batch_id(self.mock_connection, '1234'))
        )

    def test_should_return_hit_ids_that_are_in_batch(self):
        fake_hits = [
            factories.make_hit(batch_id='1234'),
            factories.make_hit(batch_id='4567')
        ]
        self.mock_connection.get_all_hits.return_value = fake_hits
        result = list(hit.get_all_by_batch_id(self.mock_connection, '1234'))
        self.assertEqual(1, len(result))
        self.assertEqual(result[0].hit_id, fake_hits[0].HITId)


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
