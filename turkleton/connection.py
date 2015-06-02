# -*- coding: utf-8 -*-
"""
    mturk.connection
    ~~~~~~~~~~~~~~~~
    Simplified interface for connecting to Mechanical Turk.

"""
from boto.mturk import connection


# The host for the Mechanical Turk sandbox
MTURK_SANDBOX_HOST = 'mechanicalturk.sandbox.amazonaws.com'


def make_connection(access_key_id, secret_access_key, host=None):
    """Make a new production connection to Mechanical Turk.

    :param access_key_id: The access key id
    :type access_key_id: str or unicode
    :param secret_access_key: The access secret key
    :type secret_access_key: str or unicode
    :param host: The host to connect to
    :type host: str or unicode
    :rtype: boto.mturk.connection.Connection
    """
    return connection.MTurkConnection(
        aws_access_key_id=access_key_id,
        aws_secret_access_key=secret_access_key,
        host=host
    )


def make_sandbox_connection(access_key_id, secret_access_key):
    """Make a connection to the Mechanical Turk sandbox.

    :param access_key_id: The access key id
    :type access_key_id: str or unicode
    :param secret_access_key: The access secret key
    :type secret_access_key: str or unicode
    :rtype: boto.mturk.connection.Connection
    """
    return make_connection(
        access_key_id, secret_access_key, MTURK_SANDBOX_HOST
    )
