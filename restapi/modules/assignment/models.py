__author__ = "Tarun Chhabra"

from restapi.modules.base import BaseModel, db
from marshmallow import Schema, fields


class Assignment(BaseModel):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True)

    def __init__(self, name):
        self.name = name

    def as_dict(self):
        org_dict = {}
        for c in self.__table__.columns:
            org_dict[c.name] = getattr(self, c.name)
        return org_dict

    def __repr__(self):
        return '<Assignment %r>' % self.name


class AssignmentSchema(Schema):

    class Meta:
        fields = ('id', 'name')
