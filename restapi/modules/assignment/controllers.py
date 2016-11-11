__author__ = 'Tarun Chhabra'

import math
from flask import Blueprint, jsonify, request
from restapi.utils.decorators import crossdomain
from restapi.modules import responses, errors, statuscodes
from restapi.components.auth.decorators import require_app_key
from restapi.modules.assignment.models import Assignment, db, AssignmentSchema
from sqlalchemy.exc import IntegrityError

mod = Blueprint('assignment', __name__, url_prefix='/api/v<float:version>/assignment')

@mod.route('/<int:assign_id>', methods=['GET'])
@crossdomain
def get_organization(version, assign_id):
    """
    Controller for API Function that gets a cake by ID
    @param assign_id: org id
    @return: Response and HTTP cod
    """

    if math.floor(version) == 1:
        assignment = Assignment.query.filter_by(id=assign_id).first()

        if assignment is None:
            return jsonify(errors.error_object_not_found(), statuscodes.HTTP_NOT_FOUND)

        assign_schema = AssignmentSchema()
        result = assign_schema.dump(assignment)
        return jsonify(
            responses.create_single_object_response('success', result.data, "assignment")), statuscodes.HTTP_OK
    else:
        return jsonify(errors.error_incorrect_version(version)), statuscodes.HTTP_VERSION_UNSUPPORTED

@mod.route('/<int:assign_id>', methods=['DELETE'])
@crossdomain
@require_app_key
def delete_org(version, assign_id):
    """
    Controller for API Function that gets a cake by ID
    @param assign_id: assignment id
    @return: Response and HTTP code
    """

    # API Version 1.X
    if math.floor(version) == 1:

        assignment = Assignment.query.filter_by(id=assign_id).first()

        if assignment is None:
            return jsonify(errors.error_object_not_found()), statuscodes.HTTP_NOT_FOUND

        db.session.delete(assignment)

        try:
            db.session.commit()
        except IntegrityError as ex:
            return jsonify(errors.error_commit_error(ex)), statuscodes.HTTP_INTERNAL_ERROR

        assign_schema = AssignmentSchema()
        result = assign_schema.dump(assignment)
        return jsonify(
            responses.create_single_object_response('success', result.data, "assignment")), statuscodes.HTTP_OK

    # Unsupported Versions
    else:
        return jsonify(errors.error_incorrect_version(version)), statuscodes.HTTP_VERSION_UNSUPPORTED


@mod.route('/', methods=['GET'])
@crossdomain
def get_all_orgs(version):
    """
    Controller for API Function that gets all cakes in the database.
    @return: Response and HTTP code
    """

    # API Version 1.X
    if math.floor(version) == 1:

        assignments = Assignment.query.all()
        assign_schema = AssignmentSchema(only=("id", "name"),
                                          # Here you can filter out stuff.
                                          many=True)
        results = assign_schema.dump(assignments)
        return jsonify(
            responses.create_multiple_object_response('success', results.data, 'assignments')), statuscodes.HTTP_OK

    # Unsupported Versions
    else:
        return jsonify(errors.error_incorrect_version(version)), statuscodes.HTTP_VERSION_UNSUPPORTED


@mod.route('/', methods=['POST', 'PUT'])
@crossdomain
@require_app_key
def insert_assignment(version):
    """
    Controller for API Function that inserts new cakes in the database
    @return: Response and HTTP code
    """

    # GET POST DATA
    assign_name = request.form['name']

    # API Version 1.X
    if math.floor(version) == 1:

        assignment = Assignment(name=assign_name)
        db.session.add(assignment)

        try:
            db.session.commit()
        except IntegrityError as ex:
            return jsonify(errors.error_commit_error(ex)), statuscodes.HTTP_INTERNAL_ERROR

        assign_schema = AssignmentSchema()
        result = assign_schema.dump(assignment)
        return jsonify(
            responses.create_multiple_object_response('success', result.data,
                                                      'assignment')), statuscodes.HTTP_OK

    # Unsupported Versions
    else:
        return jsonify(errors.error_incorrect_version(version)), statuscodes.HTTP_VERSION_UNSUPPORTED

