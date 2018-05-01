"""Command line tools for Flask server app."""

from gevent import monkey
monkey.patch_socket()

import unittest
import coverage


COV = coverage.coverage(
    branch=True,
    include='app/*',
    omit=[
        'tests/*',
        '*/test_*.py',
        '*/tests/*',
    ]
)
COV.start()

from uuid import UUID

from flask_script import Manager
from flask_migrate import MigrateCommand, upgrade

from app import create_app, db
from app.users.user_models import User
from app.organizations.organization_models import Organization
from app.analysis_results.analysis_result_models import AnalysisResultMeta
from app.samples.sample_models import Sample
from app.sample_groups.sample_group_models import SampleGroup

from seed import abrf_analysis_result, uw_analysis_result, reads_classified
from seed.worldquant import create_saved_group


app = create_app()
manager = Manager(app)  # pylint: disable=invalid-name
manager.add_command('db', MigrateCommand)


@manager.command
def test():
    """Run the tests without code coverage."""
    tests = unittest.TestLoader().discover('./tests', pattern='test*.py')
    tests.addTests(unittest.TestLoader().discover('./app', pattern='test*.py'))
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1


@manager.command
def cov():
    """Run the unit tests with coverage."""
    tests = unittest.TestLoader().discover('./tests', pattern='test*.py')
    tests.addTests(unittest.TestLoader().discover('./app', pattern='test*.py'))
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        COV.stop()
        COV.save()
        print('Coverage Summary:')
        COV.report()
        COV.html_report()
        COV.erase()
        return 0
    return 1


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
    AnalysisResultMeta.drop_collection()
    Sample.drop_collection()


@manager.command
def seed_db():
    """Seed the database."""
    bchrobot = User(username='bchrobot',
                    email='benjamin.blair.chrobot@gmail.com',
                    password='Foobar22')
    dcdanko = User(username='dcdanko',
                   email='dcd3001@med.cornell.edu',
                   password='Foobar22')
    cmason = User(username='cmason',
                  email='chm2042@med.cornell.edu',
                  password='Foobar22')

    worldquant_uuid = UUID('00000000-0000-4000-8000-000000000000')
    worldquant_group = create_saved_group(uuid=worldquant_uuid)

    mason_lab = Organization(name='Mason Lab', admin_email='benjamin.blair.chrobot@gmail.com')
    mason_lab.users = [bchrobot, dcdanko, cmason]
    mason_lab.sample_groups = [worldquant_group]

    db.session.add(mason_lab)
    db.session.commit()

    mason_lab.add_admin(bchrobot)
    mason_lab.add_admin(dcdanko)
    db.session.commit()


if __name__ == '__main__':
    manager.run()
