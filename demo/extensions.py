# -*- coding: utf-8 -*-
"""Extensions module. Each extension is initialized in the app factory located
in __init__.py
"""


from flask.ext.sqlalchemy import SQLAlchemy
db = SQLAlchemy()

from flask.ext.migrate import Migrate
migrate = Migrate()

from flask.ext.httpauth import HTTPBasicAuth
auth = HTTPBasicAuth()
