__author__ = "Tarun Chhabra"

from restapi.modules.base import BaseModel, db
from marshmallow import Schema, fields


class Student(BaseModel):
    id = db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String(100), unique=False)
    lname = db.Column(db.String(100), unique=False)
    organization_id = db.Column(db.Integer, primary_key=True)
    assignment_id = db.Column(db.Integer, primary_key=True)
    reputation = db.Column(db.Float, unique=False)

    def __init__(self, fname, lname, org_id, assign_id, reputation):
        self.fname = fname
        self.lname = lname
        self.organization_id = org_id
        self.assign_id = assign_id
        self.reputation = reputation

    def as_dict(self):
        org_dict = {}
        for c in self.__table__.columns:
            org_dict[c.name] = getattr(self, c.name)
        return org_dict

    def __repr__(self):
        return '<Student ID : %r Name : %r>' % (self.id, self.fname + ' ' + self.lname)


class StudentSchema(Schema):

    class Meta:
        fields = ('id', 'fname', 'lname', 'organization', 'assign_id', 'reputation')
