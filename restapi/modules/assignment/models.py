__author__ = "Tarun Chhabra"

from restapi.modules.base import BaseModel, db
from marshmallow import Schema

class AssignmentType(BaseModel):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), unique=False)

    def __init__(self,name):
        self.name = name;

    def as_dict(self):
        assign_t_dict = {}
        for c in self.__table__.columns:
            assign_t_dict[c.name] = getattr(self,self.name)
        return assign_t_dict

    def __repr__(self):
        return '<AssignmentType %r>' % self.name

class AssignmentTypeSchema(Schema):

    class Meta:
        fields = ('id', 'name')

class Assignment(BaseModel):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True)
    type = db.Column(db.Integer, db.ForeignKey(AssignmentType.id))

    def __init__(self, name,type):
        self.name = name
        self.type = type

    def as_dict(self):
        assign_dict = {}
        for c in self.__table__.columns:
            assign_dict[c.name] = getattr(self, c.name)
        return assign_dict

    def __repr__(self):
        return '<Assignment %r>' % self.name


class AssignmentSchema(Schema):

    class Meta:
        fields = ('id', 'name')

