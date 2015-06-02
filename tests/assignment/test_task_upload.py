# -*- coding: utf-8 -*-
import unittest

from boto.mturk import price
import mock

from turkleton.assignment import task


class CategorizationTask(task.BaseTask):
    """Represents a simple, testable task"""

    __layout_id__ = '3MCDHXBQ4Z7SJ2ZT2XZACNE142JWKX'
    __reward__ = 0.02
    __title__ = 'Categorize An Image'
    __description__ = 'Categorize this rad image.'
    __keywords__ = ['image', 'categorize']


class TestTaskUpload(unittest.TestCase):

    def setUp(self):
        super(TestTaskUpload, self).setUp()
        self.params = {
            'image_url': 'http://herp.com/derp'
        }
        self.categorization_task = CategorizationTask(**self.params)
        self.mock_connection = mock.Mock()
        self.expected_reward = price.Price(
            self.categorization_task.__reward__,
            self.categorization_task.__currency_code__
        )
        self.expected_keywords = task.keywords_from_list(
            self.categorization_task.__keywords__
        )
        self.expected_layout_params = task.dict_to_layout_parameters(
            self.params
        )
        self.batch_id_fixture = '1234'

    def mocked_upload(self):
        return self.categorization_task.upload(
            mturk_connection=self.mock_connection,
            batch_id=self.batch_id_fixture
        )

    def assert_upload_called_with(self, param_name, expected_value):
        """Assert that the upload method was called with the given parameter
        set to the given value.

        :param param_name: A param name
        :type param_name: str or unicode
        :param expected_value: The expected value
        :type expected_value: mixed
        """
        self.mocked_upload()
        self.assertEqual(
            expected_value,
            self.mock_connection.create_hit.call_args[1][param_name]
        )

    def test_should_raise_validation_error_if_task_is_invalid(self):
        self.categorization_task.__layout_id__ = None
        with self.assertRaisesRegexp(
                task.BaseTask.ValidationError,
                "Task is missing __layout_id__."):
            self.mocked_upload()

    def test_should_use_correct_layout_id(self):
        self.assert_upload_called_with(
            'hit_layout',
            self.categorization_task.__layout_id__
        )

    def test_should_use_correct_reward_price(self):
        self.mocked_upload()
        result = self.mock_connection.create_hit.call_args[1]['reward']
        self.assertEqual(self.expected_reward.amount, result.amount)
        self.assertEqual(
            self.expected_reward.currency_code,
            result.currency_code
        )

    def test_should_use_correct_title(self):
        self.assert_upload_called_with(
            'title', self.categorization_task.__title__
        )

    def test_should_use_correct_description(self):
        self.assert_upload_called_with(
            'description', self.categorization_task.__description__
        )

    def test_should_use_correct_keywords(self):
        self.assert_upload_called_with(
            'keywords', self.expected_keywords
        )

    def test_should_use_correct_max_assignments(self):
        self.assert_upload_called_with(
            'max_assignments', self.categorization_task.__assignments_per_hit__
        )

    def test_should_use_correct_lifetime(self):
        self.assert_upload_called_with(
            'lifetime', self.categorization_task.__hit_expires_in__
        )

    def test_should_use_correct_duration(self):
        self.assert_upload_called_with(
            'duration', self.categorization_task.__time_per_assignment__
        )

    def test_should_use_correct_approval_delay(self):
        self.assert_upload_called_with(
            'approval_delay', self.categorization_task.__auto_approval_delay__
        )

    def test_should_use_correct_annotation(self):
        self.assert_upload_called_with(
            'annotation', self.batch_id_fixture
        )

    def test_should_use_correct_layout_parameters(self):
        self.mocked_upload()
        result = self.mock_connection.create_hit.call_args[1]['layout_params']
        self.assertEqual(
            self.expected_layout_params.get_as_params(),
            result.get_as_params()
        )

    def test_should_return_resulting_hit(self):
        result = self.mocked_upload()
        self.assertEqual(result, self.mock_connection.create_hit())


if __name__ == '__main__':
    unittest.main()
