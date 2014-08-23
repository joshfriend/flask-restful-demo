#!/usr/bin/env python

import os
from flask.ext.script import Manager, Shell, Server
from flask.ext.migrate import MigrateCommand

from demo import create_app
from demo.models.user import User
from demo.settings import DevConfig, ProdConfig
from demo.database import db

if os.environ.get("FLASK_ENV") == 'prod':
    app = create_app(ProdConfig)
else:
    app = create_app(DevConfig)

manager = Manager(app)


def _make_context():
    """Return context dict for a shell session so you can access
    app, db, and the User model by default.
    """
    return {'app': app, 'db': db, 'User': User}


@manager.command
def test():
    """Run the tests."""
    import pytest
    exit_code = pytest.main(['tests', '-q'])
    return exit_code


manager.add_command('server', Server())
manager.add_command('shell', Shell(make_context=_make_context))
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
