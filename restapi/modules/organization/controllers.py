__author__ = 'Tarun Chhabra'

import math
from flask import Blueprint, jsonify, request
from restapi.utils.decorators import crossdomain
from restapi.modules import responses, errors, statuscodes
from restapi.components.auth.decorators import require_app_key
from restapi.modules.organization.models import Organization, db, OrganizationSchema
from sqlalchemy.exc import IntegrityError

mod = Blueprint('organization', __name__, url_prefix='/api/v<float:version>/organization')

@mod.route('/<int:org_id>', methods=['GET'])
@crossdomain
def get_organization(version, org_id):
    """
    Controller for API Function that gets a organization by ID
    @param org_id: org id
    @return: Response and HTTP cod
    """

    if math.floor(version) == 1:
        org = Organization.query.filter_by(id=org_id).first()

        if org is None:
            return jsonify(errors.error_object_not_found(), statuscodes.HTTP_NOT_FOUND)

        org_schema = OrganizationSchema()
        result = org_schema.dump(org)
        return jsonify(
            responses.create_single_object_response('success', result.data, "organization")), statuscodes.HTTP_OK
    else:
        return jsonify(errors.error_incorrect_version(version)), statuscodes.HTTP_VERSION_UNSUPPORTED

@mod.route('/<int:org_id>', methods=['DELETE'])
@crossdomain
@require_app_key
def delete_org(version, org_id):
    """
    Controller for API Function that gets a cake by ID
    @param org_id: org id
    @return: Response and HTTP code
    """

    # API Version 1.X
    if math.floor(version) == 1:

        org = Organization.query.filter_by(id=org_id).first()

        if org is None:
            return jsonify(errors.error_object_not_found()), statuscodes.HTTP_NOT_FOUND

        db.session.delete(org)

        try:
            db.session.commit()
        except IntegrityError as ex:
            return jsonify(errors.error_commit_error(ex)), statuscodes.HTTP_INTERNAL_ERROR

        org_schema = OrganizationSchema()
        result = org_schema.dump(org)
        return jsonify(
            responses.create_single_object_response('success', result.data, "organization")), statuscodes.HTTP_OK

    # Unsupported Versions
    else:
        return jsonify(errors.error_incorrect_version(version)), statuscodes.HTTP_VERSION_UNSUPPORTED


@mod.route('/', methods=['GET'])
@crossdomain
def get_all_orgs(version):
    """
    Controller for API Function that gets all organizations in the database.
    @return: Response and HTTP code
    """

    # API Version 1.X
    if math.floor(version) == 1:

        organizations = Organization.query.all()
        org_schema = OrganizationSchema(only=("id", "name", "address"),
                                          # Here you can filter out stuff.
                                          many=True)
        results = org_schema.dump(organizations)
        return jsonify(
            responses.create_multiple_object_response('success', results.data, 'organizations')), statuscodes.HTTP_OK

    # Unsupported Versions
    else:
        return jsonify(errors.error_incorrect_version(version)), statuscodes.HTTP_VERSION_UNSUPPORTED


@mod.route('/', methods=['POST', 'PUT'])
@crossdomain
@require_app_key
def insert_org(version):
    """
    Controller for API Function that inserts new cakes in the database
    @return: Response and HTTP code
    """

    # GET POST DATA
    org_name = request.form['name']
    org_address = request.form['address']

    # API Version 1.X
    if math.floor(version) == 1:

        org = Organization(name=org_name, address=org_address)
        db.session.add(org)

        try:
            db.session.commit()
        except IntegrityError as ex:
            return jsonify(errors.error_commit_error(ex)), statuscodes.HTTP_INTERNAL_ERROR

        org_schema = OrganizationSchema()
        result = org_schema.dump(org)
        return jsonify(
            responses.create_multiple_object_response('success', result.data,
                                                      'organization')), statuscodes.HTTP_OK

    # Unsupported Versions
    else:
        return jsonify(errors.error_incorrect_version(version)), statuscodes.HTTP_VERSION_UNSUPPORTED

