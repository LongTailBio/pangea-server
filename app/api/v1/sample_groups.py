"""Sample Group API endpoint definitions."""

from flask import Blueprint, jsonify

from app.api.utils import slug2uuid
from app.sample_groups.sample_group_models import SampleGroup, sample_group_schema


# pylint: disable=invalid-name
sample_groups_blueprint = Blueprint('sample_groups', __name__)


@sample_groups_blueprint.route('/sample_group/<group_slug>', methods=['GET'])
def get_single_result(group_slug):
    """Get single sample group model."""
    response_object = {
        'status': 'fail',
        'message': 'Sample Group does not exist'
    }
    try:
        sample_group_id = slug2uuid(group_slug)
        sample_group = SampleGroup.query.filter_by(id=sample_group_id).first()
        if not sample_group:
            return jsonify(response_object), 404
        data = sample_group_schema.dump(sample_group).data
        response_object = {
            'status': 'success',
            'data': data,
        }

        query_result = sample_group.query_result
        if query_result:
            response_object['data']['sample_group']['query_result_id'] = str(query_result.id)
        return jsonify(response_object), 200
    except ValueError:
        return jsonify(response_object), 404
