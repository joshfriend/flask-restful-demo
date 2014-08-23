#!/usr/bin/env python

from demo.database import (
    db,
    Model,
    SurrogatePK,
    ReferenceCol,
)


class Task(SurrogatePK, Model):
    __tablename__ = 'tasks'
    # Define a foreign key relationship to a User object
    user_id = ReferenceCol('users')
    complete = db.Column(db.Boolean, default=False)
    summary = db.Column(db.String, nullable=True)
    description = db.Column(db.String, nullable=True)

    def __init__(self, **kwargs):
        db.Model.__init__(self, **kwargs)
