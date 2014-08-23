#!/usr/bin/env python

from flask import g
from demo.extensions import auth
from demo.models.user import User


@auth.verify_password
def verify_password(username, password):
    """Validate user passwords and store user in the 'g' object"""
    g.user = User.query.filter_by(username=username).first()
    return g.user is not None and g.user.check_password(password)
