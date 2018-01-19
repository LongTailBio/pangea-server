"""Organization API endpoint definitions."""

from uuid import UUID

from flask import Blueprint, jsonify, request
from sqlalchemy import exc

from app.api.utils import uuid2slug, slug2uuid
from app.extensions import db
from app.organizations.organization_models import Organization
from app.users.user_models import user_schema
from app.users.user_helpers import authenticate


# pylint: disable=invalid-name
organizations_blueprint = Blueprint('organizations', __name__)


@organizations_blueprint.route('/organizations', methods=['POST'])
@authenticate
# pylint: disable=unused-argument
def add_organization(resp):
    """Add organization."""
    post_data = request.get_json()
    if not post_data:
        response_object = {
            'status': 'fail',
            'message': 'Invalid payload.'
        }
        return jsonify(response_object), 400
    name = post_data.get('name')
    admin_email = post_data.get('adminEmail')
    try:
        organization = Organization.query.filter_by(name=name).first()
        if not organization:
            db.session.add(Organization(name=name, adminEmail=admin_email))
            db.session.commit()
            response_object = {
                'status': 'success',
                'message': f'{name} was added!'
            }
            return jsonify(response_object), 201
        response_object = {
            'status': 'fail',
            'message': 'Sorry. That name already exists.'
        }
        return jsonify(response_object), 400
    except exc.IntegrityError as e:
        print(e)
        db.session.rollback()
        response_object = {
            'status': 'fail',
            'message': 'Invalid payload.'
        }
        return jsonify(response_object), 400


@organizations_blueprint.route('/organizations/<organization_slug>', methods=['GET'])
def get_single_organization(organization_slug):
    """Get single organization details."""
    response_object = {
        'status': 'fail',
        'message': 'Organization does not exist'
    }
    try:
        organization_id = UUID(slug2uuid(organization_slug))
        organization = Organization.query.filter_by(id=organization_id).first()
        if not organization:
            return jsonify(response_object), 404
        response_object = {
            'status': 'success',
            'data': {
                'name': organization.name,
                'admin_email': organization.adminEmail,
                'created_at': organization.created_at,
            }
        }
        return jsonify(response_object), 200
    except ValueError:
        return jsonify(response_object), 404


@organizations_blueprint.route('/organizations/<organization_slug>/users', methods=['GET'])
def get_organization_users(organization_slug):
    """Get single organization's users."""
    response_object = {
        'status': 'fail',
        'message': 'Organization does not exist'
    }
    try:
        organization_id = UUID(slug2uuid(organization_slug))
        organization = Organization.query.filter_by(id=organization_id).first()
        if not organization:
            return jsonify(response_object), 404
        users = user_schema.dump(organization.users, many=True).data
        response_object = {
            'status': 'success',
            'data': {
                'users': users,
            }
        }
        return jsonify(response_object), 200
    except ValueError:
        return jsonify(response_object), 404


@organizations_blueprint.route('/organizations', methods=['GET'])
def get_all_organizations():
    """Get all organizations."""
    organizations = Organization.query.all()
    organizations_list = []
    for organization in organizations:
        organization_object = {
            'id': uuid2slug(str(organization.id)),
            'name': organization.name,
            'admin_email': organization.adminEmail,
            'created_at': organization.created_at
        }
        organizations_list.append(organization_object)
    response_object = {
        'status': 'success',
        'data': {
            'organizations': organizations_list
        }
    }
    return jsonify(response_object), 200
