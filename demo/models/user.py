#!/usr/bin/env python

from werkzeug.security import generate_password_hash, check_password_hash
from demo.database import (
    db,
    Model,
    SurrogatePK,
    relationship,
)
from .task import Task


class User(SurrogatePK, Model):
    __tablename__ = 'users'
    username = db.Column(db.String, unique=True, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    first_name = db.Column(db.String, nullable=True)
    last_name = db.Column(db.String, nullable=True)

    tasks = relationship(Task, backref=db.backref('user'))

    def __init__(self, username, email, password, **kwargs):
        db.Model.__init__(self, username=username, email=email,
                          password=password, **kwargs)
        self.set_password(password)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, value):
        return check_password_hash(self.password, value)

    @property
    def full_name(self):
        return '%s %s' % (self.first_name, self.last_name)

    @classmethod
    def get_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    def __repr__(self):  # pragma: nocover
        return '<User({username!r})>'.format(username=self.username)
