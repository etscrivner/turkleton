# -*- coding: utf-8 -*-
"""
    turkleton.assignment.hit
    ~~~~~~~~~~~~~~~~~~~~~~~~
    Representations for HITs

"""
import collections
import functools


# Simplified tuple representation of a HIT
HIT = collections.namedtuple('HIT', ['hit_id'])


def in_batch(batch_id, hit):
    """Indicates whether or not the given HIT is in a batch.

    :param batch_id: A batch id
    :type batch_id: str or unicode
    :param hit: A HIT
    :type hit: boto.mturk.HIT
    :rtype: bool
    """
    try:
        return str(batch_id) in hit.RequesterAnnotation
    except AttributeError:
        return False


def get_reviewable_by_batch_id(boto_connection, batch_id):
    """Get all reviewable HITs within the given batch.

    :param boto_connection: A boto connection
    :type boto_connection: mturk.boto.MTurkConnection
    :param batch_id: A batch id
    :type batch_id: str or unicode
    :rtype: iterable of HIT
    """
    is_in_batch = functools.partial(in_batch, batch_id)
    return [
        HIT(hit_id=each.HITId) for each
        in filter(is_in_batch, boto_connection.get_reviewable_hits(batch_id))
    ]
