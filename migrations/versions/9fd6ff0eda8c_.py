"""Add access_scheme to Organizations.

Revision ID: 9fd6ff0eda8c
Revises: 19cbee51fb1c
Create Date: 2018-05-15 12:00:04.462056

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9fd6ff0eda8c'
down_revision = '19cbee51fb1c'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('organizations', sa.Column('access_scheme', sa.String(length=128),
                                             nullable=False, server_default='public'))
    op.alter_column('organizations', 'access_scheme', server_default=False)


def downgrade():
    op.drop_column('organizations', 'access_scheme')
