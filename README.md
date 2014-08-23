Flask-RESTful Demo
======

This is sample Flask application created to show off some of the features of
the Flask-RESTful library.


Getting Started
===============

Requirements
------------

* Python
* GNU Make:
    * Windows: http://cygwin.com/install.html
    * Mac: https://developer.apple.com/xcode
    * Linux: http://www.gnu.org/software/make (likely already installed)
* virtualenv: https://pypi.python.org/pypi/virtualenv#installation


Installation
------------

Create a virtualenv:

    $ make env

Create the development database:

    $ make upgrade

Run a development server:

    $ make serve

Run the tests:

    $ make test

Run static analysis:

    $ make pep8
    $ make pep257
    $ make pylint
    $ make flake8
    $ make check  # includes all checks


Resources
---------

That guy who wrote the O'Rielly book on Flask did a PyCon presentation. I got
the `paginate` decorator from there:

http://pyvideo.org/video/2668/writing-restful-web-services-with-flask

Lots of examples of Flask "Best Practices":

https://github.com/sloria/cookiecutter-flask

What I based my sick makefile off of:

https://github.com/jacebrowning/template-python

The flask-restful docs:

http://flask-restful.readthedocs.org/en/latest/
