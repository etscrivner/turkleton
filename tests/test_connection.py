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
        connection.set_connection(None)
        self.mturk_connection = self.patch.__enter__()

    def tearDown(self):
        super(BaseConnectionTestCase, self).tearDown()
        self.patch.__exit__()

    def assert_boto_connection_call_contains(self, argument_name, val):
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


class TestGlobalConnection(unittest.TestCase):

    def setUp(self):
        super(TestGlobalConnection, self).setUp()
        connection.set_connection(None)

    def test_should_initially_raise_error(self):
        self.assertRaisesRegexp(
            connection.ConnectionError,
            r'It is required that you setup\(\) turkleton before use.',
            connection.get_connection
        )

    def test_should_take_value_after_set(self):
        fixture = 'Herp'
        connection.set_connection(fixture)
        self.assertEqual(fixture, connection.get_connection())


class TestSetup(BaseConnectionTestCase):

    def setup_connection(self):
        return connection.setup(
            self.access_key_fixture, self.secret_access_key_fixture
        )

    def test_should_pass_along_correct_access_key(self):
        self.setup_connection()
        self.assert_boto_connection_call_contains(
            'aws_access_key_id', self.access_key_fixture
        )

    def test_should_pass_along_correct_secret_access_key(self):
        self.setup_connection()
        self.assert_boto_connection_call_contains(
            'aws_secret_access_key', self.secret_access_key_fixture
        )

    def test_should_return_mturk_connection(self):
        self.assertEqual(
            self.setup_connection(), self.mturk_connection()
        )


class TestSetupSandbox(BaseConnectionTestCase):

    def setup_sandbox(self):
        return connection.setup_sandbox(
            self.access_key_fixture, self.secret_access_key_fixture
        )

    def test_should_pass_along_correct_access_key(self):
        self.setup_sandbox()
        self.assert_boto_connection_call_contains(
            'aws_access_key_id', self.access_key_fixture
        )

    def test_should_pass_along_correct_secret_access_key(self):
        self.setup_sandbox()
        self.assert_boto_connection_call_contains(
            'aws_secret_access_key', self.secret_access_key_fixture
        )

    def test_should_pass_along_correct_host(self):
        self.setup_sandbox()
        self.assert_boto_connection_call_contains(
            'host', connection.MTURK_SANDBOX_HOST
        )

    def test_should_return_mturk_connection(self):
        self.assertEqual(
            self.setup_sandbox(), self.mturk_connection()
        )


if __name__ == '__main__':
    unittest.main()
