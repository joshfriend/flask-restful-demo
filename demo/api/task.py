#!/usr/bin/env python

from flask import abort
from flask_restful import Resource, reqparse, marshal_with, fields

from demo.api import api, meta_fields
from demo.api.auth import self_only
from demo.models.task import Task
from demo.models.user import User
from demo.helpers import paginate
from demo.extensions import auth

task_parser = reqparse.RequestParser()
task_parser.add_argument('complete', type=bool)
task_parser.add_argument('summary', type=str, required=True)
task_parser.add_argument('description', type=str)

task_collection_parser = reqparse.RequestParser()
task_collection_parser.add_argument('complete', type=int)


# Marshaled field definitions for task objects
task_fields = {
    'id': fields.Integer,
    'user_id': fields.Integer,
    'complete': fields.Boolean,
    'summary': fields.String,
    'description': fields.String,
}

# Marshaled field definitions for collections of task objects
task_collection_fields = {
    'items': fields.List(fields.Nested(task_fields)),
    'meta': fields.Nested(meta_fields),
}


class TaskResource(Resource):
    decorators = [
        self_only,
        auth.login_required,
    ]

    @marshal_with(task_fields)
    def get(self, task_id=0, **kwargs):
        task = Task.get_by_id(task_id)

        if not task:
            abort(404)

        return task

    @marshal_with(task_fields)
    def post(self, task_id=0, **kwargs):
        task = Task.get_by_id(task_id)

        if not task:
            abort(404)

        task.update(**task_parser.parse_args())
        return task

    def delete(self, task_id=0, **kwargs):
        task = Task.get_by_id(task_id)

        if not task:
            abort(404)

        task.delete()
        return 204


class TaskCollectionResource(Resource):
    decorators = [
        self_only,
        auth.login_required,
    ]

    @marshal_with(task_collection_fields)
    @paginate()
    def get(self, user_id=None, username=None):
        # Find user that task goes with
        user = None
        if user_id:
            user = User.get_by_id(user_id)
        else:
            user = User.get_by_username(username)

        if not user:
            abort(404)

        # Get the user's tasks
        tasks = Task.query.filter_by(user_id=user.id)

        args = task_collection_parser.parse_args()
        # fancy url argument query filtering!
        if args['complete'] is not None:
            tasks.filter_by(complete=args['complete'])

        return tasks

    @marshal_with(task_fields)
    def post(self, user_id=None, username=None):
        args = task_parser.parse_args()
        # user owns the task
        args['user_id'] = g.user.id
        task = Task.create(**args)
        return task, 201


api.add_resource(TaskResource, '/users/<int:user_id>/tasks/<int:task_id>',
                 '/users/<username>/tasks/<int:task_id>')
api.add_resource(TaskCollectionResource, '/users/<int:user_id>/tasks',
                 '/users/<username>/tasks')
