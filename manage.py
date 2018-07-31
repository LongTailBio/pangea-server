"""Command line tools for Flask server app."""

from uuid import UUID

from flask_script import Manager
from flask_migrate import MigrateCommand, upgrade

from tool_packages.base.models import ToolResult, GroupToolResult

from app import create_app, db
from app.mongo import drop_mongo_collections
from app.users.user_models import User
from app.organizations.organization_models import Organization
from app.analysis_results.analysis_result_models import AnalysisResultMeta
from app.samples.sample_models import Sample
from app.sample_groups.sample_group_models import SampleGroup
from os import environ

app = create_app()
manager = Manager(app)  # pylint: disable=invalid-name
manager.add_command('db', MigrateCommand)

# These must be imported AFTER Mongo connection has been established during app creation
from seed import abrf_analysis_result, uw_analysis_result, reads_classified
from seed.fuzz import generate_metadata, create_saved_group


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
    return User(
        username=environ.get('SEED_USER_USERNAME', 'bchrobot'),
        email=environ.get('SEED_USER_EMAIL', 'benjamin.blair.chrobot@gmail.com'),
        password=environ.get('SEED_USER_PASSWORD', 'Foobar22')
    )


@manager.command
def seed_users():
    """Seed just the users for the database."""
    db.session.add(get_user())
    db.session.commit()


@manager.command
def seed_db():
    """Seed the database."""
    default_user = get_user()

    abrf_analysis_result_01 = AnalysisResultMeta(reads_classified=reads_classified).save()
    abrf_sample_01 = Sample(name='SomethingUnique_A',
                            analysis_result=abrf_analysis_result_01,
                            metadata=generate_metadata()).save()
    abrf_analysis_result_02 = AnalysisResultMeta(reads_classified=reads_classified).save()
    abrf_sample_02 = Sample(name='SomethingUnique_B',
                            analysis_result=abrf_analysis_result_02,
                            metadata=generate_metadata()).save()
    abrf_analysis_result.save()

    abrf_uuid = UUID('00000000-0000-4000-8000-000000000000')
    abrf_description = 'ABRF San Diego Mar 24th-29th 2017'
    abrf_2017_group = SampleGroup(name='ABRF 2017',
                                  analysis_result=abrf_analysis_result,
                                  description=abrf_description)
    abrf_2017_group.id = abrf_uuid
    abrf_2017_group.samples = [abrf_sample_01, abrf_sample_02]

    uw_analysis_result.save()
    uw_sample = Sample(name='UW_Madison_00', analysis_result=uw_analysis_result).save()
    uw_group_result = AnalysisResultMeta().save()
    uw_madison_group = SampleGroup(name='The UW Madison Project',
                                   analysis_result=uw_group_result)
    uw_madison_group.samples = [uw_sample]

    fuzz_uuid = UUID('00000000-0000-4000-8000-000000000001')
    fuzz_group = create_saved_group(uuid=fuzz_uuid)

    mason_lab = Organization(name='Mason Lab', admin_email='benjamin.blair.chrobot@gmail.com')
    mason_lab.users = [default_user]
    mason_lab.sample_groups = [abrf_2017_group, uw_madison_group, fuzz_group]

    db.session.add(mason_lab)
    db.session.commit()

    mason_lab.add_admin(default_user)
    db.session.commit()


if __name__ == '__main__':
    manager.run()
