# -*- coding: utf-8 -*-
import unittest
import uuid

import mock

from turkleton import connection


class BaseConnectionTestCase(unittest.TestCase):

    def setUp(self):
        super(BaseConnectionTestCase, self).setUp()
        self.access_key_fixture = str(uuid.uuid4())
        self.secret_access_key_fixture = str(uuid.uuid4())
        self.patch = mock.patch(
            'boto.mturk.connection.MTurkConnection'
        )
        self.mturk_connection = self.patch.__enter__()

    def tearDown(self):
        super(BaseConnectionTestCase, self).tearDown()
        self.patch.__exit__()

    def assert_make_connection_call_contains(self, argument_name, val):
        """Assert that the make connection call contains the given argument.

        :param argument_name: The argument name
        :type argument_name: str or unicode
        :param val: The argument value
        :type val: mixed
        """
        self.assertIn(argument_name, self.mturk_connection.call_args[1])
        self.assertEqual(
            val,
            self.mturk_connection.call_args[1][argument_name]
        )


class TestMakeConnection(BaseConnectionTestCase):

    def make_connection(self):
        return connection.make_connection(
            self.access_key_fixture, self.secret_access_key_fixture
        )

    def test_should_pass_along_correct_access_key(self):
        self.make_connection()
        self.assert_make_connection_call_contains(
            'aws_access_key_id', self.access_key_fixture
        )

    def test_should_pass_along_correct_secret_access_key(self):
        self.make_connection()
        self.assert_make_connection_call_contains(
            'aws_secret_access_key', self.secret_access_key_fixture
        )

    def test_should_return_mturk_connection(self):
        self.assertEqual(
            self.make_connection(), self.mturk_connection()
        )


class TestMakeSandboxConnection(BaseConnectionTestCase):

    def make_sandbox_connection(self):
        return connection.make_sandbox_connection(
            self.access_key_fixture, self.secret_access_key_fixture
        )

    def test_should_pass_along_correct_access_key(self):
        self.make_sandbox_connection()
        self.assert_make_connection_call_contains(
            'aws_access_key_id', self.access_key_fixture
        )

    def test_should_pass_along_correct_secret_access_key(self):
        self.make_sandbox_connection()
        self.assert_make_connection_call_contains(
            'aws_secret_access_key', self.secret_access_key_fixture
        )

    def test_should_pass_along_correct_host(self):
        self.make_sandbox_connection()
        self.assert_make_connection_call_contains(
            'host', connection.MTURK_SANDBOX_HOST
        )

    def test_should_return_mturk_connection(self):
        self.assertEqual(
            self.make_sandbox_connection(), self.mturk_connection()
        )


if __name__ == '__main__':
    unittest.main()
