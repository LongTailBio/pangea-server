"""Command line tools for Flask server app."""

# pylint: disable=no-value-for-parameter

from os import environ
from uuid import UUID

from flask_script import Manager
from flask_migrate import MigrateCommand, upgrade

from app import create_app, db
from app.mongo import drop_mongo_collections
from app.authentication.models import User, PasswordAuthentication, OrganizationMembership
from app.samples.sample_models import Sample
from app.sample_groups.sample_group_models import SampleGroup

app = create_app()
manager = Manager(app)  # pylint: disable=invalid-name
manager.add_command('db', MigrateCommand)

# These must be imported AFTER Mongo connection has been established during app creation
# pylint: disable=wrong-import-position
from seed import create_abrf_analysis_result as create_abrf_result
from seed.fuzz import generate_metadata, create_saved_group
# pylint: enable=wrong-import-position


@manager.command
def recreate_db():
    """Recreate a database using migrations."""
    # We cannot simply use db.drop_all() because it will not drop the alembic_versions table
    sql = 'SELECT \
        \'drop table if exists "\' || tablename || \'" cascade;\' as pg_drop \
        FROM \
        pg_tables \
        WHERE \
        schemaname=\'public\';'

    drop_statements = db.engine.execute(sql)
    if drop_statements.rowcount > 0:
        drop_statement = '\n'.join([x['pg_drop'] for x in drop_statements])
        drop_statements.close()
        db.engine.execute(drop_statement)

    # Run migrations
    upgrade()

    # Empty Mongo database
    drop_mongo_collections()


def get_user():
    """Get the password from env vars or a default."""
    username = environ.get('SEED_USER_USERNAME', 'bchrobot')
    email = environ.get('SEED_USER_EMAIL', 'benjamin.blair.chrobot@gmail.com')
    password = environ.get('SEED_USER_PASSWORD', 'Foobar22')

    new_user = User(
        username=username,
        email=email,
        user_type='user',
    )
    new_user.password_authentication = PasswordAuthentication(password=password)

    return new_user


@manager.command
def seed_users():
    """Seed just the users for the database."""
    db.session.add(get_user())
    db.session.commit()


@manager.command
def seed_db():
    """Seed the database."""
    default_user = get_user()

    # Create Mason Lab
    mason_lab = User(
        username='MasonLab',
        email='benjamin.blair.chrobot+masonlab@gmail.com',
        user_type='organization',
    )
    membership = OrganizationMembership(role='admin')
    membership.user = default_user
    mason_lab.user_memberships.append(membership)
    db.session.add_all([mason_lab, membership])
    db.session.commit()

    # Create ABRF sample group
    abrf_uuid = UUID('00000000-0000-4000-8000-000000000000')
    abrf_description = 'ABRF San Diego Mar 24th-29th 2017'
    abrf_2017_group = SampleGroup(name='ABRF 2017',
                                  owner_uuid=mason_lab.uuid,
                                  owner_name=mason_lab.username,
                                  is_library=True,
                                  analysis_result=create_abrf_result(save=True),
                                  description=abrf_description)
    abrf_2017_group.uuid = abrf_uuid

    abrf_sample_01 = Sample(name='SomethingUnique_A',
                            library_uuid=abrf_uuid,
                            analysis_result=create_abrf_result(save=True),
                            metadata=generate_metadata()).save()
    abrf_sample_02 = Sample(name='SomethingUnique_B',
                            library_uuid=abrf_uuid,
                            analysis_result=create_abrf_result(save=True),
                            metadata=generate_metadata()).save()
    abrf_2017_group.samples = [abrf_sample_01, abrf_sample_02]
    db.session.add(abrf_2017_group)
    db.session.commit()

    # Create fuzzed group
    fuzz_uuid = UUID('00000000-0000-4000-8000-000000000001')
    create_saved_group(owner=mason_lab, uuid=fuzz_uuid)


if __name__ == '__main__':
    manager.run()
