"""Organization API endpoint definitions."""

from uuid import UUID

from flask import Blueprint, current_app, request
from flask_api.exceptions import NotFound, ParseError
from sqlalchemy import and_, or_
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound

from app.extensions import db
from app.api.exceptions import InvalidRequest, InternalError
from app.db_models import Sample, SampleGroup
from app.authentication.helpers import authenticate


samples_blueprint = Blueprint('samples', __name__)    # pylint: disable=invalid-name


@samples_blueprint.route('/samples', methods=['POST'])
@authenticate()
def add_sample(_):
    """Add sample."""
    try:
        post_data = request.get_json()
        library = SampleGroup.from_uuid(post_data['library_uuid'])
        sample = library.sample(post_data['name'], force_new=True)
    except TypeError:
        raise ParseError('Missing Sample creation payload.')
    except KeyError:
        raise ParseError('Invalid Sample creation payload.')
    except NoResultFound:
        raise InvalidRequest('Library does not exist!')
    except IntegrityError:
        raise InvalidRequest('A Sample with that name already exists in the library.')
    return sample.serializable(), 201


@samples_blueprint.route('/samples', methods=['GET'])
@authenticate()
def get_all_samples(authn):  # pylint: disable=unused-argument
    """Get all samples that the user is allowed to see."""
    try:
        org_uuids = {membership.uuid for membership in authn.memberships}
        sample_groups = SampleGroup.query.filter(and_(
            SampleGroup.is_library,
            or_(
                SampleGroup.is_public,
                SampleGroup.organization_uuid in org_uuids
            )
        )).all()
        samples = []
        for sample_group in sample_groups:
            for sample in sample_group.samples:
                samples.append(sample.serializable())
        result = {'samples': samples}
        return result, 200
    except NoResultFound:
        raise NotFound('No accessible samples found.')


@samples_blueprint.route('/samples/<sample_uuid>', methods=['GET'])
def get_single_sample(sample_uuid):
    """Get single sample details."""
    try:
        sample = Sample.from_uuid(UUID(sample_uuid))
        return sample.serializable(), 200
    except ValueError:
        raise ParseError('Invalid UUID provided.')
    except DoesNotExist:
        raise NotFound('Sample does not exist.')


@samples_blueprint.route('/samples/<sample_uuid>/metadata', methods=['GET'])
def get_single_sample_metadata(sample_uuid):
    """Get single sample metadata."""
    try:
        sample = Sample.from_uuid(UUID(sample_uuid))
        result = { 
            'sample': {
                'uuid': sample.uuid,
                'name': sample.name,
                'metadata': sample.sample_metadata,
            },
        }
        return result, 200
    except ValueError:
        raise ParseError('Invalid UUID provided.')
    except DoesNotExist:
        raise NotFound('Sample does not exist.')


@samples_blueprint.route('/samples/<sample_uuid>/metadata', methods=['POST'])
def post_single_sample_metadata(sample_uuid):
    """Upload metadata for a single sample."""
    try:
        post_data = request.get_json()
        sample = Sample.from_uuid(UUID(sample_uuid))
        sample.set_sample_metadata(post_data['metadata'])
        return sample.serializable(), 200
    except ValueError:
        raise ParseError('Invalid UUID provided.')
    except DoesNotExist:
        raise NotFound('Sample does not exist.')
    except TypeError:
        raise ParseError('Missing Sample metadata payload.')
    except KeyError:
        raise ParseError('Invalid Sample metadata payload.')
