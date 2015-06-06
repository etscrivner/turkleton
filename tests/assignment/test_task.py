# -*- coding: utf-8 -*-
import datetime
import unittest
import uuid

from turkleton.assignment import task


class TestKeywordsFromList(unittest.TestCase):

    def test_should_return_none_when_given_none(self):
        self.assertIsNone(task.keywords_from_list(None))

    def test_should_return_none_if_given_empty_list(self):
        self.assertIsNone(task.keywords_from_list([]))

    def test_should_return_comma_separated_list(self):
        self.assertEqual(
            'herp,derp,hurp',
            task.keywords_from_list(['herp', 'derp', 'hurp'])
        )


class TestDictToLayoutParameters(unittest.TestCase):

    def test_should_return_empty_layout_parameters_for_none(self):
        result = task.dict_to_layout_parameters(None)
        self.assertEqual([], result.layoutParameters)

    def test_should_return_empty_layout_parameters_for_empty_dict(self):
        result = task.dict_to_layout_parameters({})
        self.assertEqual([], result.layoutParameters)

    def test_should_return_single_item_layout_param_for_single_item_dict(self):
        result = task.dict_to_layout_parameters({'hello': 'there'})
        self.assertEqual(1, len(result.layoutParameters))
        self.assertEqual('hello', result.layoutParameters[0].name)
        self.assertEqual('there', result.layoutParameters[0].value)


class TestBaseTask(unittest.TestCase):

    def setUp(self):
        super(TestBaseTask, self).setUp()
        self.task = task.BaseTask()

    def test_default_layout_id(self):
        self.assertIsNone(self.task.__layout_id__)

    def test_default_reward(self):
        self.assertIsNone(self.task.__reward__)

    def test_default_title(self):
        self.assertIsNone(self.task.__title__)

    def test_default_keywords(self):
        self.assertIsNone(self.task.__keywords__)

    def test_default_description(self):
        self.assertIsNone(self.task.__description__)

    def test_default_assignments_per_hit(self):
        self.assertEqual(1, self.task.__assignments_per_hit__)

    def test_default_initial_expiration_time(self):
        self.assertEqual(
            datetime.timedelta(days=7),
            self.task.__hit_expires_in__
        )

    def test_default_time_per_assignment(self):
        self.assertEqual(
            datetime.timedelta(hours=1),
            self.task.__time_per_assignment__
        )

    def test_default_auto_approval_delay(self):
        self.assertEqual(
            datetime.timedelta(hours=8),
            self.task.__auto_approval_delay__
        )

    def test_should_take_keyword_arguments_in_constructor(self):
        params = {
            'user_id': '1234',
            'image_url': 'http://www.google.com'
        }
        t = task.BaseTask(**params)
        self.assertEqual(t.assignment_params, params)


class TestValidate(unittest.TestCase):

    def setUp(self):
        super(TestValidate, self).setUp()
        self.base_task = task.BaseTask()
        self.base_task.__layout_id__ = '12345980234'
        self.base_task.__reward__ = 0.02
        self.base_task.__title__ = 'Hello'
        self.base_task.__description__ = 'There'

    def test_should_raise_error_if_layout_id_not_set(self):
        self.base_task.__layout_id__ = None
        self.assertRaisesRegexp(
            task.BaseTask.ValidationError,
            "Task is missing __layout_id__.",
            self.base_task.validate,
        )

    def test_should_raise_error_if_reward_is_missing(self):
        self.base_task.__reward__ = None
        self.assertRaisesRegexp(
            task.BaseTask.ValidationError,
            "Task is missing __reward__",
            self.base_task.validate
        )

    def test_should_raise_error_if_no_title(self):
        self.base_task.__title__ = None
        self.assertRaisesRegexp(
            task.BaseTask.ValidationError,
            "Task is missing __title__",
            self.base_task.validate
        )

    def test_should_raise_error_if_no_description(self):
        self.base_task.__description__ = None
        self.assertRaisesRegexp(
            task.BaseTask.ValidationError,
            "Task is missing __description__",
            self.base_task.validate
        )


class TestBatchedUpload(unittest.TestCase):

    def setUp(self):
        super(TestBatchedUpload, self).setUp()
        self.id_fixture = str(uuid.uuid4())
        task.current_batch_id = None

    def tearDown(self):
        super(TestBatchedUpload, self).tearDown()
        task.current_batch_id = None

    def test_should_set_global_batch_id(self):
        with task.batched_upload(self.id_fixture):
            self.assertEqual(self.id_fixture, task.current_batch_id)

    def test_should_return_current_batch_id_to_none_when_done(self):
        with task.batched_upload(self.id_fixture):
            pass
        self.assertIsNone(task.current_batch_id)

    def test_should_allow_for_nesting(self):
        id_fixture_2 = str(uuid.uuid4())
        with task.batched_upload(self.id_fixture):
            with task.batched_upload(id_fixture_2):
                self.assertEqual(id_fixture_2, task.current_batch_id)
            self.assertEqual(self.id_fixture, task.current_batch_id)


if __name__ == '__main__':
    unittest.main()
