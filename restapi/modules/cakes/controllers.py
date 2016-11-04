__author__ = 'Tarun Chhabra'

import math
from flask import Blueprint, jsonify, request
from restapi.utils.decorators import crossdomain
from restapi.modules import responses, errors, statuscodes
from restapi.components.auth.decorators import require_app_key
from restapi.modules.cakes.models import Cake, db, CakeSchema
from sqlalchemy.exc import  IntegrityError

mod = Blueprint('cakes', __name__, url_prefix='/api/v<float:version>/cakes')

@mod.route('/<int:cake_id>', methods=['GET'])
@crossdomain
def get_cake(version, cake_id):
    """
    Controller for API Function that gets a cake by ID
    @param cake_id: cake id
    @return: Response and HTTP cod
    """

    if math.floor(version) == 1:
        cake = Cake.query.filter_by(id=cake_id).first()

        if cake is None:
            return jsonify(errors.error_object_not_found(), statuscodes.HTTP_NOT_FOUND)

        cake_schema = CakeSchema()
        result = cake_schema.dump(cake)
        return jsonify(
            responses.create_single_object_response('success', result.data, "cake")), statuscodes.HTTP_OK
    else:
        return jsonify(errors.error_incorrect_version(version)), statuscodes.HTTP_VERSION_UNSUPPORTED

@mod.route('/<int:cake_id>', methods=['DELETE'])
@crossdomain
@require_app_key
def delete_cake(version, cake_id):
    """
    Controller for API Function that gets a cake by ID
    @param cake_id: cake id
    @return: Response and HTTP code
    """

    # API Version 1.X
    if math.floor(version) == 1:

        cake = Cake.query.filter_by(id=cake_id).first()

        if cake is None:
            return jsonify(errors.error_object_not_found()), statuscodes.HTTP_NOT_FOUND

        db.session.delete(cake)

        try:
            db.session.commit()
        except IntegrityError as ex:
            return jsonify(errors.error_commit_error(ex)), statuscodes.HTTP_INTERNAL_ERROR

        cake_schema = CakeSchema()
        result = cake_schema.dump(cake)
        return jsonify(
            responses.create_single_object_response('success', result.data, "cake")), statuscodes.HTTP_OK

    # Unsupported Versions
    else:
        return jsonify(errors.error_incorrect_version(version)), statuscodes.HTTP_VERSION_UNSUPPORTED


@mod.route('/', methods=['GET'])
@crossdomain
def get_all_cakes(version):
    """
    Controller for API Function that gets all cakes in the database.
    @return: Response and HTTP code
    """

    # API Version 1.X
    if math.floor(version) == 1:

        cakes = Cake.query.all()
        cake_schema = CakeSchema(only=("id", "cakename", "bakername", "price", "price_range"),
                                          # Here you can filter out stuff.
                                          many=True)
        results = cake_schema.dump(cakes)
        return jsonify(
            responses.create_multiple_object_response('success', results.data, 'cakes')), statuscodes.HTTP_OK

    # Unsupported Versions
    else:
        return jsonify(errors.error_incorrect_version(version)), statuscodes.HTTP_VERSION_UNSUPPORTED


@mod.route('/', methods=['POST', 'PUT'])
@crossdomain
@require_app_key
def insert_cake(version):
    """
    Controller for API Function that inserts new cakes in the database
    @return: Response and HTTP code
    """

    # GET POST DATA
    cakename = request.form['cakename']
    baker = request.form['baker']
    price = request.form['price']

    # API Version 1.X
    if math.floor(version) == 1:

        cake = Cake(cakename, baker, price)
        db.session.add(cake)

        try:
            db.session.commit()
        except IntegrityError as ex:
            return jsonify(errors.error_commit_error(ex)), statuscodes.HTTP_INTERNAL_ERROR

        cake_schema = CakeSchema()
        result = cake_schema.dump(cake)
        return jsonify(
            responses.create_multiple_object_response('success', result.data,
                                                      'cakes')), statuscodes.HTTP_OK

    # Unsupported Versions
    else:
        return jsonify(errors.error_incorrect_version(version)), statuscodes.HTTP_VERSION_UNSUPPORTED

