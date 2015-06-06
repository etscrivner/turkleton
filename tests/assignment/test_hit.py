# -*- coding: utf-8 -*-
import unittest

import mock

from tests.assignment import factories
from turkleton import connection
from turkleton import errors
from turkleton.assignment import hit


class TestCreateFromBotoHit(unittest.TestCase):

    def setUp(self):
        self.boto_hit = factories.make_boto_hit()

    def test_should_raise_error_if_none_given(self):
        with self.assertRaisesRegexp(errors.Error, 'Invalid HIT given.'):
            hit.HIT.create_from_boto_hit(None)

    def test_should_correctly_handle_missing_hit_id(self):
        del self.boto_hit.HITId
        result = hit.HIT.create_from_boto_hit(self.boto_hit)
        self.assertIsNone(result.hit_id)

    def test_should_correctly_handle_missing_requester_annotation(self):
        del self.boto_hit.RequesterAnnotation
        result = hit.HIT.create_from_boto_hit(self.boto_hit)
        self.assertIsNone(result.batch_id)


class TestDispose(unittest.TestCase):

    def setUp(self):
        super(TestDispose, self).setUp()
        self.hit = hit.HIT.create_from_boto_hit(factories.make_boto_hit())
        self.mock_connection = mock.MagicMock()
        connection.set_connection(self.mock_connection)

    def test_should_raise_error_if_hit_id_is_none(self):
        self.hit.hit_id = None
        with self.assertRaisesRegexp(
                errors.Error, 'None HIT id for disposal.'):
            self.hit.dispose()

    def test_should_pass_hit_id_to_correct_method(self):
        self.hit.dispose()
        self.mock_connection.dispose_hit.assert_called_once_with(
            self.hit.hit_id
        )


class TestTransformRawHits(unittest.TestCase):

    def test_should_return_empty_list_when_none_given(self):
        self.assertEqual([], hit.transform_raw_hits(None))

    def test_should_return_empty_list_when_empty_list_given(self):
        self.assertEqual([], hit.transform_raw_hits([]))

    def test_should_return_appropriately_transformed_hits(self):
        fixture = [factories.make_boto_hit() for _ in range(10)]
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
        connection.set_connection(self.mock_connection)

    def test_should_return_empty_list_if_no_results(self):
        self.mock_connection.get_all_hits.return_value = []
        self.assertEqual([], list(hit.get_all()))

    def test_should_return_all_hits_from_connection(self):
        fake_hits = [
            factories.make_boto_hit(batch_id='1234'),
            factories.make_boto_hit(batch_id='4567')
        ]
        self.mock_connection.get_all_hits.return_value = fake_hits
        result = list(hit.get_all())
        self.assertEqual(2, len(result))
        result_hit_ids = [each.hit_id for each in result]
        self.assertTrue(all([
            each.HITId in result_hit_ids for each in fake_hits
        ]))


class TestGetAllByBatchId(unittest.TestCase):

    def setUp(self):
        super(TestGetAllByBatchId, self).setUp()
        self.mock_connection = mock.MagicMock()
        connection.set_connection(self.mock_connection)

    def test_test_should_return_empty_list_if_no_results(self):
        self.mock_connection.get_all_hits.return_value = []
        self.assertEqual(
            [],
            list(hit.get_all_by_batch_id('1234'))
        )

    def test_should_return_hit_ids_that_are_in_batch(self):
        fake_hits = [
            factories.make_boto_hit(batch_id='1234'),
            factories.make_boto_hit(batch_id='4567')
        ]
        self.mock_connection.get_all_hits.return_value = fake_hits
        result = list(hit.get_all_by_batch_id('1234'))
        self.assertEqual(1, len(result))
        self.assertEqual(result[0].hit_id, fake_hits[0].HITId)


class TestGetReviewableByBatchId(unittest.TestCase):

    def setUp(self):
        super(TestGetReviewableByBatchId, self).setUp()
        self.mock_connection = mock.MagicMock()
        connection.set_connection(self.mock_connection)

    def test_should_return_empty_list_if_no_results(self):
        self.mock_connection.get_reviewable_hits.return_value = []
        self.assertEqual(
            [],
            hit.get_reviewable_by_batch_id('1234')
        )

    def test_should_only_return_hit_ids_that_are_in_batch(self):
        fake_hits = [
            factories.make_boto_hit(batch_id='1234'),
            factories.make_boto_hit(batch_id='4567')
        ]
        self.mock_connection.get_reviewable_hits.return_value = fake_hits
        result = hit.get_reviewable_by_batch_id('1234')
        self.assertEqual(1, len(result))
        self.assertEqual(result[0].hit_id, fake_hits[0].HITId)
