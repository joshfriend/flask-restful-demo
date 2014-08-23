#!/usr/bin/env python

from flask import abort, g
from flask.ext.restful import Resource, reqparse, marshal_with, fields

from demo.api import api, meta_fields
from demo.api.auth import self_only
from demo.models.user import User
from demo.helpers import paginate
from demo.extensions import auth

user_parser = reqparse.RequestParser()
user_parser.add_argument('username', type=str)
user_parser.add_argument('password', type=str)
user_parser.add_argument('email', type=str)
user_parser.add_argument('first_name', type=str)
user_parser.add_argument('last_name', type=str)


# Marshaled field definitions for user objects
user_fields = {
    'id': fields.Integer,
    'username': fields.String,
    'email': fields.String,
    'first_name': fields.String,
    'last_name': fields.String,
}

# Marshaled field definitions for collections of user objects
user_collection_fields = {
    'items': fields.List(fields.Nested(user_fields)),
    'meta': fields.Nested(meta_fields),
}


class UserResource(Resource):
    @marshal_with(user_fields)
    def get(self, user_id=0, username=None):
        user = None
        if username:
            user = User.get_by_username(username)
        elif user_id:
            user = User.get_by_id(user_id)

        if not user:
            abort(404)

        return user

    @auth.login_required
    @self_only
    @marshal_with(user_fields)
    def post(self, user_id=0, username=None):
        g.user.update(**user_parser.parse_args())
        return g.user

    @auth.login_required
    @self_only
    def delete(self, user_id=0, username=None):
        g.user.delete()
        return 204


class UserCollectionResource(Resource):
    @marshal_with(user_collection_fields)
    @paginate()
    def get(self):
        users = User.query
        return users

    @marshal_with(user_fields)
    def post(self):
        user = User.create(**user_parser.parse_args())
        return user, 201


api.add_resource(UserResource, '/users/<int:user_id>', '/users/<username>')
api.add_resource(UserCollectionResource, '/users')
