__author__ = 'Tarun Chhabra'

import math
from flask import Blueprint, jsonify, request
from restapi.utils.decorators import crossdomain
from restapi.modules import responses, errors, statuscodes
from restapi.components.auth.decorators import require_app_key
from restapi.modules.score.models import Score, db, ScoreSchema
from sqlalchemy.exc import IntegrityError

mod = Blueprint('score', __name__, url_prefix='/api/v<float:version>/score')

@mod.route('/<int:org_id>', methods=['GET'])
@crossdomain
def get_organization(version, score_id):
    """
    Controller for API Function that gets a score by ID
    @param org_id: score id
    @return: Response and HTTP cod
    """

    if math.floor(version) == 1:
        score = Score.query.filter_by(id=score_id).first()

        if score is None:
            return jsonify(errors.error_object_not_found(), statuscodes.HTTP_NOT_FOUND)

        score_schema = ScoreSchema()
        result = score_schema.dump(score)
        return jsonify(
            responses.create_single_object_response('success', result.data, "score")), statuscodes.HTTP_OK
    else:
        return jsonify(errors.error_incorrect_version(version)), statuscodes.HTTP_VERSION_UNSUPPORTED

@mod.route('/<int:score_id>', methods=['DELETE'])
@crossdomain
@require_app_key
def delete_score(version, score_id):
    """
    Controller for API Function that gets an organization by ID
    @param org_id: org id
    @return: Response and HTTP code
    """

    # API Version 1.X
    if math.floor(version) == 1:

        score = Score.query.filter_by(id=score_id).first()

        if score is None:
            return jsonify(errors.error_object_not_found()), statuscodes.HTTP_NOT_FOUND

        db.session.delete(score)

        try:
            db.session.commit()
        except IntegrityError as ex:
            return jsonify(errors.error_commit_error(ex)), statuscodes.HTTP_INTERNAL_ERROR

        score_schema = ScoreSchema()
        result = score_schema.dump(score)
        return jsonify(
            responses.create_single_object_response('success', result.data, "score")), statuscodes.HTTP_OK

    # Unsupported Versions
    else:
        return jsonify(errors.error_incorrect_version(version)), statuscodes.HTTP_VERSION_UNSUPPORTED


@mod.route('/', methods=['GET'])
@crossdomain
def get_all_scores(version):
    """
    Controller for API Function that gets all organizations in the database.
    @return: Response and HTTP code
    """

    # API Version 1.X
    if math.floor(version) == 1:

        scores = Score.query.all()
        score_schema = ScoreSchema(only=("id", "student_id", "assignment_id","organization_id","task_id","review_type",
                                         "score", "max_score"),
                                          # Here you can filter out stuff.
                                          many=True)
        results = score_schema.dump(scores)
        return jsonify(
            responses.create_multiple_object_response('success', results.data, 'scores')), statuscodes.HTTP_OK

    # Unsupported Versions
    else:
        return jsonify(errors.error_incorrect_version(version)), statuscodes.HTTP_VERSION_UNSUPPORTED


@mod.route('/', methods=['POST', 'PUT'])
@crossdomain
@require_app_key
def insert_score(version):
    """
    Controller for API Function that inserts new score in the database
    @return: Response and HTTP code
    """

    # GET POST DATA
    student_id = request.form['student_id']
    assignment_id = request.form['assignment_id']
    organization_id = request.form['organization_id']
    task_id = request.form['task_id']
    review_type = request.form['review_type']
    score = request.form['score']
    max_score = request.form['max_score']

    # API Version 1.X
    if math.floor(version) == 1:

        score = Score(student_id=student_id, assignment_id=assignment_id,organization_id=organization_id,task_id=task_id,
                    review_type=review_type,score=score,max_score=max_score)
        db.session.add(score)

        try:
            db.session.commit()
        except IntegrityError as ex:
            return jsonify(errors.error_commit_error(ex)), statuscodes.HTTP_INTERNAL_ERROR

        score_schema = ScoreSchema()
        result = score_schema.dump(score)
        return jsonify(
            responses.create_multiple_object_response('success', result.data,
                                                      'score')), statuscodes.HTTP_OK

    # Unsupported Versions
    else:
        return jsonify(errors.error_incorrect_version(version)), statuscodes.HTTP_VERSION_UNSUPPORTED

