"""Command line tools for Flask server app."""

from os import environ
from uuid import UUID

from flask_script import Manager
from flask_migrate import MigrateCommand, upgrade

from app import create_app, db
from app.authentication.models import User, PasswordAuthentication, OrganizationMembership

app = create_app()
manager = Manager(app)  # pylint: disable=invalid-name
manager.add_command('db', MigrateCommand)

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
        email=default_user.email,
        user_type='organization',
    )
    membership = OrganizationMembership(role='admin')
    membership.user = default_user
    mason_lab.user_memberships.append(membership)
    db.session.add_all([mason_lab, membership])
    db.session.commit()


if __name__ == '__main__':
    manager.run()
