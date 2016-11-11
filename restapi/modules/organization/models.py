__author__ = "Tarun Chhabra"

from restapi.modules.base import BaseModel, db
from marshmallow import Schema, fields


class Organization(BaseModel):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    address = db.Column(db.String(255), unique=False)

    def __init__(self, name, address):
        self.name = name
        self.address = address

    def as_dict(self):
        org_dict = {}
        for c in self.__table__.columns:
            org_dict[c.name] = getattr(self, c.name)
        return org_dict

    def __repr__(self):
        return '<Organization %r>' % self.name


class OrganizationSchema(Schema):

    class Meta:
        fields = ('id', 'name', 'address')
