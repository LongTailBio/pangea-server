"""Common utility methods for use in testing."""

import datetime
import json
from uuid import uuid4

from functools import wraps

from app import db
from app.analysis_results.analysis_result_models import AnalysisResultMeta
from app.authentication.models import User, PasswordAuthentication
from app.samples.sample_models import Sample
from app.sample_groups.sample_group_models import SampleGroup


def add_user(username, email, password, created_at=datetime.datetime.utcnow()):
    """Wrap functionality for adding user."""
    user = User(
        username=username,
        email=email,
        user_type='user',
        created_at=created_at,
    )
    # pylint: disable=no-value-for-parameter
    user.password_authentication = PasswordAuthentication(password=password)
    db.session.add(user)
    db.session.commit()
    return user


def add_organization(name, email, created_at=datetime.datetime.utcnow()):
    """Wrap functionality for adding organization."""
    organization = User(
        username=name,
        email=email,
        user_type='organization',
        created_at=created_at,
    )
    db.session.add(organization)
    db.session.commit()
    return organization


# pylint: disable=too-many-arguments,dangerous-default-value
def add_sample(name, library_uuid=None, analysis_result=None,
               metadata={}, created_at=datetime.datetime.utcnow(),
               sample_kwargs={}):
    """Wrap functionality for adding sample."""
    if not library_uuid:
        library_uuid = uuid4()
    if not analysis_result:
        analysis_result = AnalysisResultMeta().save()

    for module_name, module_val in sample_kwargs.items():
        setattr(analysis_result, module_name, module_val)

    return Sample(library_uuid=library_uuid, name=name, metadata=metadata,
                  analysis_result=analysis_result, created_at=created_at,
                  ).save()


def add_sample_group(name, owner=None, analysis_result=None, is_library=False,
                     created_at=datetime.datetime.utcnow()):
    """Wrap functionality for adding sample group."""
    if not analysis_result:
        analysis_result = AnalysisResultMeta().save()
    group = SampleGroup(name=name,
                        owner_uuid=owner.uuid if owner else uuid4(),
                        owner_name=owner.username if owner else 'ausername',
                        is_library=is_library,
                        analysis_result=analysis_result,
                        created_at=created_at)
    db.session.add(group)
    db.session.commit()
    return group


def get_test_user(client):
    """Return auth headers and a test user."""
    login_user = add_user('test', 'test@test.com', 'test')
    with client:
        resp_login = client.post(
            '/api/v1/auth/login',
            data=json.dumps(dict(
                email='test@test.com',
                password='test'
            )),
            content_type='application/json'
        )
        auth_headers = dict(
            Authorization='Bearer ' + json.loads(
                resp_login.data.decode()
            )['data']['auth_token']
        )

    return auth_headers, login_user


def with_user(f):   # pylint: disable=invalid-name
    """Decorate API route calls requiring authentication."""
    @wraps(f)
    def decorated_function(self, *args, **kwargs):
        """Wrap function f."""
        auth_headers, login_user = get_test_user(self.client)
        return f(self, auth_headers, login_user, *args, **kwargs)

    return decorated_function
