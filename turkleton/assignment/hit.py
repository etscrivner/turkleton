# -*- coding: utf-8 -*-
"""
    turkleton.assignment.hit
    ~~~~~~~~~~~~~~~~~~~~~~~~
    Representations for HITs

"""
import collections


# Simplified tuple representation of a HIT
HIT = collections.namedtuple('HIT', ['hit_id', 'batch_id'])


def transform_raw_hits(hits):
    """Convert raw hits into internal hits representation

    :param hits: A list of HITs
    :type hits: list of boto.mturk.HIT
    :rtype: list of HIT
    """
    if not hits:
        return []

    return [
        HIT(hit_id=each.HITId, batch_id=each.RequesterAnnotation)
        for each in hits
    ]


def get_all_by_batch_id(boto_connection, batch_id):
    """Get all HITs with the given batch id.

    :param boto_connection: A boto connection
    :type boto_connection: mturk.boto.MTurkConnection
    :param batch_id: A batch id
    :type batch_id: str or unicode
    :rtype: iterable of HIT
    """
    all_hits = transform_raw_hits(
        boto_connection.get_all_hits()
    )
    return [each in all_hits if each.batch_id == batch_id]


def get_reviewable_by_batch_id(boto_connection, batch_id):
    """Get all reviewable HITs within the given batch.

    :param boto_connection: A boto connection
    :type boto_connection: mturk.boto.MTurkConnection
    :param batch_id: A batch id
    :type batch_id: str or unicode
    :rtype: iterable of HIT
    """
    all_reviewable_hits = transform_raw_hits(
        boto_connection.get_reviewable_hits(batch_id)
    )
    return [each in all_reviewable_hits if each.batch_id == batch_id]
