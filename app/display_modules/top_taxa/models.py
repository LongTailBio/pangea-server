# pylint: disable=too-few-public-methods

"""Average Genome Size display models."""

from app.extensions import mongoDB as mdb
from app.display_modules.shared_models import DistributionResult


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
