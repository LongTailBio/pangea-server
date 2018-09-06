"""Base module for Tool Results."""

from uuid import UUID

from flask import request
from flask import current_app
from flask_api.exceptions import NotFound, ParseError, PermissionDenied
from mongoengine.errors import ValidationError, DoesNotExist
from sqlalchemy.orm.exc import NoResultFound

from app.conductor import SampleConductor, GroupConductor
from app.extensions import sample_upload_lock
from app.samples.sample_models import Sample
from app.sample_groups.sample_group_models import SampleGroup
from app.users.user_models import User
from app.users.user_helpers import authenticate
from app.utils import lock_function

from tool_packages.base import SampleToolResultModule, GroupToolResultModule


@lock_function(sample_upload_lock)
def receive_sample_tool_upload(cls, resp, uuid):
    """Define handler for receiving uploads of analysis tool results."""
    try:
        safe_uuid = UUID(uuid)
        sample = Sample.objects.get(uuid=safe_uuid)
    except ValueError:
        raise ParseError('Invalid UUID provided.')
    except DoesNotExist:
        raise NotFound('Sample does not exist.')

    # gh-21: Write actual validation:
    try:
        auth_user = User.query.filter_by(id=resp).one()
        print(auth_user)
    except NoResultFound:
        raise PermissionDenied('Authorization failed.')

    try:
        payload = request.get_json()
        payload = cls.run_upload_hooks(payload)

        tool_result = cls.make_result_model(payload).save()
        setattr(sample, cls.name(), tool_result)
        sample.save()
    except ValidationError as validation_error:
        raise ParseError(str(validation_error))

    # Kick off middleware tasks
    dryrun = request.args.get('dryrun', False)
    if not dryrun:
        try:
            downstream_modules = SampleConductor.downstream_modules(cls)
            SampleConductor(safe_uuid, downstream_modules).shake_that_baton()
        except Exception:  # pylint: disable=broad-except
            current_app.logger.exception('Exception while coordinating display modules.')

    # Return payload here to avoid per-class JSON serialization
    return payload, 201


def receive_group_tool_upload(cls, resp, uuid):
    """Define handler for receiving uploads of analysis tool results for sample groups."""
    try:
        safe_uuid = UUID(uuid)
        sample_group = SampleGroup.query.filter_by(id=safe_uuid).first()
    except ValueError:
        raise ParseError('Invalid UUID provided.')
    except NoResultFound:
        raise NotFound('Sample Group does not exist.')

    # gh-21: Write actual validation:
    try:
        auth_user = User.query.filter_by(id=resp).one()
        print(auth_user, str(safe_uuid))
    except NoResultFound:
        raise PermissionDenied('Authorization failed.')

    try:
        payload = request.get_json()
        payload['sample_group_uuid'] = sample_group.id
        group_tool_result = cls.make_result_model(payload)
        group_tool_result.save()
    except ValidationError as validation_error:
        raise ParseError(str(validation_error))

    # Kick off middleware tasks
    dryrun = request.args.get('dryrun', False)
    if not dryrun:
        try:
            downstream_modules = GroupConductor.downstream_modules(cls)
            GroupConductor(safe_uuid, downstream_modules).shake_that_baton()
        except Exception as exc:  # pylint: disable=broad-except
            current_app.logger.exception('Exception while coordinating display modules.')
            current_app.logger.exception(exc)

    # Return payload here to avoid per-class JSON serialization
    return payload, 201


def register_tool_result(cls, router):
    """Register API endpoint for this display module type."""
    endpoint_url = cls.endpoint()
    endpoint_name = f'post_{cls.name()}'

    @authenticate()
    def view_function(resp, uuid):
        """Wrap receive_upload to provide class."""
        if issubclass(cls, SampleToolResultModule):
            return receive_sample_tool_upload(cls, resp, uuid)
        elif issubclass(cls, GroupToolResultModule):
            return receive_group_tool_upload(cls, resp, uuid)
        raise ParseError('Tool Result of unrecognized type.')

    router.add_url_rule(endpoint_url,
                        endpoint_name,
                        view_function,
                        methods=['POST'])
