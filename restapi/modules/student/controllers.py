__author__ = 'Tarun Chhabra'

import math
from flask import Blueprint, jsonify, request
from restapi.utils.decorators import crossdomain
from restapi.modules import responses, errors, statuscodes
from restapi.components.auth.decorators import require_app_key
from restapi.modules.student.models import Student, db, StudentSchema
from sqlalchemy.exc import IntegrityError

mod = Blueprint('student', __name__, url_prefix='/api/v<float:version>/student')

@mod.route('/<int:student_id>', methods=['GET'])
@crossdomain
def get_student(version, student_id):
    """
    Controller for API Function that gets a student by ID
    @param student_id: student id
    @return: Response and HTTP cod
    """

    if math.floor(version) == 1:
        student = Student.query.filter_by(id=student_id).first()

        if student is None:
            return jsonify(errors.error_object_not_found(), statuscodes.HTTP_NOT_FOUND)

        student_schema = StudentSchema()
        result = student_schema.dump(student)
        return jsonify(
            responses.create_single_object_response('success', result.data, "student")), statuscodes.HTTP_OK
    else:
        return jsonify(errors.error_incorrect_version(version)), statuscodes.HTTP_VERSION_UNSUPPORTED

@mod.route('/<int:student_id>', methods=['DELETE'])
@crossdomain
@require_app_key
def delete_student(version, student_id):
    """
    Controller for API Function that deletes a student by ID
    @param student_id: student id
    @return: Response and HTTP code
    """

    # API Version 1.X
    if math.floor(version) == 1:

        student = Student.query.filter_by(id=student_id).first()

        if student is None:
            return jsonify(errors.error_object_not_found()), statuscodes.HTTP_NOT_FOUND

        db.session.delete(student)

        try:
            db.session.commit()
        except IntegrityError as ex:
            return jsonify(errors.error_commit_error(ex)), statuscodes.HTTP_INTERNAL_ERROR

        student_schema = StudentSchema()
        result = student_schema.dump(student)
        return jsonify(
            responses.create_single_object_response('success', result.data, "student")), statuscodes.HTTP_OK

    # Unsupported Versions
    else:
        return jsonify(errors.error_incorrect_version(version)), statuscodes.HTTP_VERSION_UNSUPPORTED


@mod.route('/', methods=['GET'])
@crossdomain
def get_all_students(version):
    """
    Controller for API Function that gets all students in the database.
    @return: Response and HTTP code
    """

    # API Version 1.X
    if math.floor(version) == 1:

        students = Student.query.all()
        student_schema = StudentSchema(only=("id", "fname", "lname", "organization_id", "assign_id", "reputation"),
                                          # Here you can filter out stuff.
                                          many=True)
        results = student_schema.dump(students)
        return jsonify(
            responses.create_multiple_object_response('success', results.data, 'students')), statuscodes.HTTP_OK

    # Unsupported Versions
    else:
        return jsonify(errors.error_incorrect_version(version)), statuscodes.HTTP_VERSION_UNSUPPORTED


@mod.route('/', methods=['POST', 'PUT'])
@crossdomain
@require_app_key
def insert_student(version):
    """
    Controller for API Function that inserts new cakes in the database
    @return: Response and HTTP code
    """

    # GET POST DATA
    s_fname = request.form['fname']
    s_lname = request.form['lname']
    s_org_id = request.form['organization_id']
    s_assign_id = request.form['assign_id']
    s_reputation = request.form['reputation']


    # API Version 1.X
    if math.floor(version) == 1:

        student = Student(fname=s_fname, lname=s_lname, org_id=s_org_id,
                          assign_id=s_assign_id, reputation=s_reputation)
        db.session.add(student)

        try:
            db.session.commit()
        except IntegrityError as ex:
            return jsonify(errors.error_commit_error(ex)), statuscodes.HTTP_INTERNAL_ERROR

        student_schema = StudentSchema()
        result = student_schema.dump(student)
        return jsonify(
            responses.create_multiple_object_response('success', result.data,
                                                      'student')), statuscodes.HTTP_OK

    # Unsupported Versions
    else:
        return jsonify(errors.error_incorrect_version(version)), statuscodes.HTTP_VERSION_UNSUPPORTED

