__author__ = "Tarun Chhabra"

from restapi.modules.base import BaseModel, db
from marshmallow import Schema, fields


class Student(BaseModel):
    id = db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String(100), unique=True)
    lname = db.Column(db.String(100), unique=False)
    organization_id = db.Column(db.Integer, unique=False)
    assignment_id = db.Column(db.Integer, unique=False)
    reputation = db.Column(db.Float, unique=False)

    def __init__(self, name, address):
        self.name = name
        self.address = address

    def as_dict(self):
        org_dict = {}
        for c in self.__table__.columns:
            org_dict[c.name] = getattr(self, c.name)
        return org_dict

    def __repr__(self):
        return '<Organization %r>' % self.cakename


class OrganizationSchema(Schema):

    class Meta:
        fields = ('id', 'name', 'address')
