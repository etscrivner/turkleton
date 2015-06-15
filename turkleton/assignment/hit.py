# -*- coding: utf-8 -*-
"""
    turkleton.assignment.hit
    ~~~~~~~~~~~~~~~~~~~~~~~~
    Representations for HITs

"""
from six import moves

from turkleton import connection
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
            hit_id=utils.safe_getattr(raw_hit, 'HITId'),
            batch_id=utils.safe_getattr(raw_hit, 'RequesterAnnotation')
        )

    def dispose(self):
        """Dispose of this HIT. """
        if not self.hit_id:
            raise errors.Error('None HIT id for disposal.')

        connection.get_connection().dispose_hit(self.hit_id)


def transform_raw_hits(hits):
    """Convert multiple raw hits into internal hits representation

    :param hits: A list of HITs
    :type hits: list of boto.mturk.HIT
    :rtype: iterable of HIT
    """
    if not hits:
        return []

    return moves.map(HIT.create_from_boto_hit, hits)


def get_all():
    """Get all HITs

    :rtype: iterable of HIT
    """
    return transform_raw_hits(connection.get_connection().get_all_hits())


def get_all_by_batch_id(batch_id):
    """Get all HITs with the given batch id.

    :param batch_id: A batch id
    :type batch_id: str or unicode
    :rtype: iterable of HIT
    """
    return moves.filter(lambda each: each.batch_id == batch_id, get_all())


def get_reviewable_by_batch_id(batch_id):
    """Get all reviewable HITs within the given batch.

    :param batch_id: A batch id
    :type batch_id: str or unicode
    :rtype: iterable of HIT
    """
    boto_connection = connection.get_connection()
    all_reviewable_hits = transform_raw_hits(
        boto_connection.get_reviewable_hits()
    )
    return [each for each in all_reviewable_hits if each.batch_id == batch_id]
