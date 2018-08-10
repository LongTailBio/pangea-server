# pylint: disable=too-few-public-methods

"""Top Taxa display models."""

from app.extensions import mongoDB as mdb


class AbundPrev(mdb.EmbeddedDocument):
    """Store abundance and prevalence."""

    abundance = mdb.MapField(field=mdb.FloatField(), required=True)
    prevalence = mdb.MapField(field=mdb.FloatField(), required=True)


class TopTaxaResult(mdb.EmbeddedDocument):
    """AGS document type."""

    # cats -> vals
    categories = mdb.MapField(
        # vals -> tool
        field=mdb.MapField(
            # tool -> kingdom
            field=mdb.MapField(
                # kingdom -> abundance and prevalence
                field=mdb.MapField(
                    field=AbundPrev,
                    reuired=True,
                ),
                required=True,
            ),
            required=True,
        ),
        required=True,
    )
