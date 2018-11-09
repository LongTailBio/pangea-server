"""Pangea v0.12 clean slate

Revision ID: 9ac024109a64
Revises: 
Create Date: 2018-11-09 13:26:29.455019

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '9ac024109a64'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # Sample Groups
    op.create_table('sample_groups',
        sa.Column('uuid', postgresql.UUID(as_uuid=True), server_default=sa.text('uuid_generate_v4()'), nullable=False),
        sa.Column('name', sa.String(length=128), nullable=False),
        sa.Column('owner_uuid', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('owner_name', sa.String(length=128), nullable=False),
        sa.Column('description', sa.String(length=300), nullable=False),
        sa.Column('is_library', sa.Boolean(), nullable=False),
        sa.Column('is_public', sa.Boolean(), nullable=False),
        sa.Column('analysis_result_uuid', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('uuid')
    )
    op.create_index(op.f('ix_sample_groups_name'), 'sample_groups', ['name'], unique=False)
    op.create_index(op.f('ix_sample_groups_owner_name'), 'sample_groups', ['owner_name'], unique=False)
    op.create_index(op.f('ix_sample_groups_owner_uuid'), 'sample_groups', ['owner_uuid'], unique=False)
    
    # Users
    op.create_table('users',
        sa.Column('uuid', postgresql.UUID(as_uuid=True), server_default=sa.text('uuid_generate_v4()'), nullable=False),
        sa.Column('username', sa.String(length=128), nullable=False),
        sa.Column('email', sa.String(length=128), nullable=False),
        sa.Column('user_type', postgresql.ENUM('user', 'organization', name='user_type'), nullable=False),
        sa.Column('is_deleted', sa.Boolean(), nullable=False),
        sa.Column('is_fake', sa.Boolean(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('uuid'),
        sa.UniqueConstraint('email')
    )

    # Password Authentication
    op.create_table('password_authentication',
        sa.Column('user_uuid', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('password', sa.String(length=255), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['user_uuid'], ['users.uuid'], ),
        sa.PrimaryKeyConstraint('user_uuid'),
        sa.UniqueConstraint('user_uuid')
    )

    # Organization membership
    op.create_table('organization_memberships',
        sa.Column('organization_uuid', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('user_uuid', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('role', postgresql.ENUM('admin', 'writeread', name='organization_role'), nullable=False),
        sa.Column('is_public', sa.Boolean(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['organization_uuid'], ['users.uuid'], ),
        sa.ForeignKeyConstraint(['user_uuid'], ['users.uuid'], ),
        sa.PrimaryKeyConstraint('organization_uuid', 'user_uuid'),
        sa.UniqueConstraint('organization_uuid', 'user_uuid', name='_organization_user_uc')
    )

    # Sample Placeholders
    op.create_table('sample_placeholder',
        sa.Column('sample_uuid', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('sample_group_uuid', postgresql.UUID(as_uuid=True), nullable=False),
        sa.ForeignKeyConstraint(['sample_group_uuid'], ['sample_groups.uuid'], ),
        sa.PrimaryKeyConstraint('sample_uuid', 'sample_group_uuid')
    )


def downgrade():
    op.drop_table('sample_placeholder')
    op.drop_table('password_authentication')
    op.drop_table('organization_memberships')
    op.drop_table('users')
    op.drop_index(op.f('ix_sample_groups_owner_uuid'), table_name='sample_groups')
    op.drop_index(op.f('ix_sample_groups_owner_name'), table_name='sample_groups')
    op.drop_index(op.f('ix_sample_groups_name'), table_name='sample_groups')
    op.drop_table('sample_groups')
