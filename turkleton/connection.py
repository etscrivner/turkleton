# -*- coding: utf-8 -*-
"""
    mturk.connection
    ~~~~~~~~~~~~~~~~
    Simplified interface for connecting to Mechanical Turk.

"""
from boto.mturk import connection

from turkleton import errors


# The host for the Mechanical Turk sandbox.
MTURK_SANDBOX_HOST = 'mechanicalturk.sandbox.amazonaws.com'
# Global containing the boto connection to Mechanical Turk for this process.
mturk_connection = None


class ConnectionError(errors.Error):
    """Error involving the connection to Mechanical Turk"""
    pass


def get_connection():
    """Return the Mechanical Turk connection for this process.

    :rtype: boto.mturk.connection.MTurkConnection
    """
    global mturk_connection

    if not mturk_connection:
        raise ConnectionError(
            'It is required that you setup() turkleton before use.'
        )

    return mturk_connection


def set_connection(boto_connection):
    """Set the Mechanical Turk connection for this process.

    :param boto_connection: A connection
    :type boto_connection: boto.mturk.connection.MTurkConnection
    """
    global mturk_connection
    mturk_connection = boto_connection


def setup(access_key_id, secret_access_key, host=None):
    """Setup the global connection to Mechanical Turk.

    :param access_key_id: The access key id
    :type access_key_id: str or unicode
    :param secret_access_key: The access secret key
    :type secret_access_key: str or unicode
    :param host: The host to connect to
    :type host: str or unicode
    :rtype: boto.mturk.connection.Connection
    """
    boto_connection = connection.MTurkConnection(
        aws_access_key_id=access_key_id,
        aws_secret_access_key=secret_access_key,
        host=host
    )
    set_connection(boto_connection)
    return boto_connection


def setup_sandbox(access_key_id, secret_access_key):
    """Setup a global connection to the Mechanical Turk sandbox.

    :param access_key_id: The access key id
    :type access_key_id: str or unicode
    :param secret_access_key: The access secret key
    :type secret_access_key: str or unicode
    :rtype: boto.mturk.connection.Connection
    """
    return setup(
        access_key_id, secret_access_key, MTURK_SANDBOX_HOST
    )
