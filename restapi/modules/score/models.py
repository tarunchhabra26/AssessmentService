from restapi.modules.base import BaseModel, db
from restapi.modules.assignment.models import Assignment
from restapi.modules.organization.models import Organization
from restapi.modules.student.models import Student
from marshmallow import Schema

__author__ = "Tarun Chhabra"


class Task(BaseModel):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=False)
    assignment_id = db.Column(db.Integer, db.ForeignKey(Assignment.id))

    def __init__(self, name, assignment_id):
        self.name = name
        self.assignment_id = assignment_id

    def as_dict(self):
        task_dict = {}
        for c in self.__table__.columns:
            task_dict[c.name] = getattr(self, c.name)
        return task_dict

    def __repr__(self):
        return '<Task %r>' % self.id


class TaskSchema(Schema):
    class Meta:
        fields = ('id', 'name', 'assignment_id')


class ReviewType(BaseModel):
    id = db.column(db.Integer, primary_key=True)
    name = db.column(db.String, unique=True)

    def as_dict(self):
        review_dict = {}
        for c in self.__table__.columns:
            review_dict[c.name] = getattr(self, c.name)
        return review_dict

    def __repr__(self):
        return '<ReviewType %r>' % self.id

class ReviewTypeSchema(Schema):
    class Meta:
        fields = ('id', 'name')



class Score(BaseModel):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey(Student.id))
    assignment_id = db.Column(db.Integer, db.ForeignKey(Assignment.id))
    organization_id = db.Column(db.Integer, db.ForeignKey(Organization.id))
    task_id = db.Column(db.Integer, db.ForeignKey(Task.id))
    review_type = db.Column(db.Integer, unique=False)
    score = db.Column(db.Float, unique=False)
    max_score = db.Column(db.Float, unique=False)

    def __init__(self, student_id, assignment_id, organization_id, task_id, review_type, score, max_score):
        self.student_id = student_id
        self.assignment_id = assignment_id
        self.organization_id = organization_id
        self.task_id = task_id
        self.review_type = review_type
        self.score = score
        self.max_score = max_score

    def as_dict(self):
        score_dict = {}
        for c in self.__table__.columns:
            score_dict[c.name] = getattr(self, c.name)
        return score_dict

    def __repr__(self):
        return '<Score %r>' % self.id


class ScoreSchema(Schema):
    class Meta:
        fields = ('id', 'student_id', 'assignment_id', 'organization_id', 'task_id',
                  'review_id', 'score', 'max_score')
