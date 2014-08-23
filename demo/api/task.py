#!/usr/bin/env python

from flask import abort, g
from flask.ext.restful import Resource, reqparse, marshal_with, fields

from demo.api import api, meta_fields
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
    @marshal_with(task_fields)
    def get(self, task_id=0):
        task = Task.get_by_id(task_id)

        if not task:
            abort(404)

        return task

    @auth.login_required
    @marshal_with(task_fields)
    def post(self, task_id=0):
        task = Task.get_by_id(task_id)

        if not task:
            abort(404)

        if task.user_id != g.user.id:
            # Users can only modify their own tasks
            abort(403)

        task.update(**task_parser.parse_args())
        return task

    @auth.login_required
    def delete(self, task_id=0):
        task = Task.get_by_id(task_id)

        if not task:
            abort(404)

        if task.user_id != g.user.id:
            # Users can only delete their own tasks
            abort(403)

        task.delete()
        return {'message': 'deleted', 'status': 204}, 204


class TaskCollectionResource(Resource):
    @marshal_with(task_collection_fields)
    @paginate()
    def get(self, user_id=0, username=''):
        # Find user that task goes with
        if user_id:
            user = User.get_by_id(user_id)
        elif username:
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

    @auth.login_required
    @marshal_with(task_fields)
    def post(self, user_id=0, username=''):
        # find the user that the new task will go with
        if user_id:
            user = User.get_by_id(user_id)
        elif username:
            user = User.get_by_username(username)

        if not user:
            abort(404)

        if user.id != g.user.id:
            # Users can only create tasks for themselves
            abort(403)

        args = task_parser.parse_args()
        # user owns the task
        args['user_id'] = user.id
        task = Task.create(**args)
        return task, 201


api.add_resource(TaskResource, '/tasks/<int:task_id>')
api.add_resource(TaskCollectionResource, '/users/<int:user_id>/tasks',
                 '/users/<username>/tasks')
