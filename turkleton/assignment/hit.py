# -*- coding: utf-8 -*-
"""
    turkleton.assignment.hit
    ~~~~~~~~~~~~~~~~~~~~~~~~
    Representations for HITs

"""
from six import moves

from turkleton import errors
from turkleton import utils


class HIT(object):
    """Simple internal representation of a Mechanical Turk human intelligence
    task (HIT)."""

    def __init__(self, hit_id, batch_id):
        """Initialize a HIT"""
        self.hit_id = hit_id
        self.batch_id = batch_id

    @classmethod
    def create_from_boto_hit(cls, raw_hit):
        """Safely convert a raw boto hit into internal representation.

        :param raw_hit: A raw hit
        :type raw_hit: boto.mturk.HIT
        :rtype: turkleton.assignment.hit.HIT
        """
        if not raw_hit:
            raise errors.Error('Invalid HIT given.')

        return cls(
            hit_id=utils.safe_get_attr(raw_hit, 'HITId'),
            batch_id=utils.safe_get_attr(raw_hit, 'RequesterAnnotation')
        )

    def dispose(self, boto_connection):
        """Dispose of this HIT using the given boto connection.

        :param boto_connection: A boto connection
        :type boto_connection: boto.mturk.MTurkConnection
        """
        if not self.hit_id:
            raise errors.Error('None HIT id for disposal.')

        boto_connection.dispose_hit(self.hit_id)


def transform_raw_hits(hits):
    """Convert multiple raw hits into internal hits representation

    :param hits: A list of HITs
    :type hits: list of boto.mturk.HIT
    :rtype: iterable of HIT
    """
    if not hits:
        return []

    return moves.map(HIT.create_from_boto_hit, hits)


def get_all(boto_connection):
    """Get all HITs

    :param boto_connection: A boto connection
    :type boto_connection: boto.mturk.MTurkConnection
    :rtype: iterable of HIT
    """
    return transform_raw_hits(boto_connection.get_all_hits())


def get_all_by_batch_id(boto_connection, batch_id):
    """Get all HITs with the given batch id.

    :param boto_connection: A boto connection
    :type boto_connection: mturk.boto.MTurkConnection
    :param batch_id: A batch id
    :type batch_id: str or unicode
    :rtype: iterable of HIT
    """
    return moves.filter(
        lambda each: each.batch_id == batch_id,
        get_all(boto_connection)
    )


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
    return [each for each in all_reviewable_hits if each.batch_id == batch_id]
