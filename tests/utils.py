"""Common utility methods for use in testing."""

import datetime
import json

from functools import wraps

from app import db
from app.analysis_results.analysis_result_models import AnalysisResultMeta
from app.users.user_models import User
from app.organizations.organization_models import Organization
from app.samples.sample_models import Sample
from app.sample_groups.sample_group_models import SampleGroup


def add_user(username, email, password, created_at=datetime.datetime.utcnow()):
    """Wrap functionality for adding user."""
    user = User(
        username=username,
        email=email,
        password=password,
        created_at=created_at)
    db.session.add(user)
    db.session.commit()
    return user


def add_organization(name, admin_email, access_scheme='public',
                     created_at=datetime.datetime.utcnow()):
    """Wrap functionality for adding organization."""
    organization = Organization(name=name, admin_email=admin_email,
                                access_scheme=access_scheme, created_at=created_at)
    db.session.add(organization)
    db.session.commit()
    return organization


def add_sample(name, analysis_result=None, metadata={},  # pylint: disable=dangerous-default-value
               created_at=datetime.datetime.utcnow(), sample_kwargs={}):
    """Wrap functionality for adding sample."""
    if not analysis_result:
        analysis_result = AnalysisResultMeta().save()

    for module_name, module_val in sample_kwargs.items():
        setattr(analysis_result, module_name, module_val)
    return Sample(
        name=name, metadata=metadata,
        analysis_result=analysis_result, created_at=created_at,
    ).save()


def add_sample_group(name, analysis_result=None,
                     access_scheme='public', created_at=datetime.datetime.utcnow()):
    """Wrap functionality for adding sample group."""
    if not analysis_result:
        analysis_result = AnalysisResultMeta().save()
    group = SampleGroup(name=name, analysis_result=analysis_result,
                        access_scheme=access_scheme, created_at=created_at)
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
