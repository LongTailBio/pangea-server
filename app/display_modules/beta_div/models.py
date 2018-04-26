# pylint: disable=too-few-public-methods

"""Models for BetaDiversity Display Module."""

from app.extensions import mongoDB as mdb


class BetaDiversityResult(mdb.EmbeddedDocument):
    """Set of beta diversity results."""

    data = mdb.DictField(required=True)
