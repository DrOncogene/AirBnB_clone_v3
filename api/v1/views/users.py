#!/usr/bin/python3
""" handles the part of the api that deals with user objects"""
from flask import jsonify, abort, request, make_response
import json
from api.v1.views import app_views
from models import storage
from models.user import User


@app_views.route('/users/', methods=['GET'], strict_slashes=False)
def users():
    users = [user.to_dict() for user in
             storage.all(User).values()]
    return jsonify(users)


@app_views.route('/users/<user_id>', methods=['GET'])
def get_user(user_id):
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    storage.delete(user)
    storage.save()
    return jsonify({})


@app_views.route('/users/', methods=['POST'], strict_slashes=False)
def create_user():
    try:
        data = request.get_json()
        if not data:
            return make_response('Not a JSON', 400)
    except Exception:
        return make_response('Not a JSON', 400)
    if 'email' not in data:
        return make_response('Missing email', 400)
    if 'password' not in data:
        return make_response('Missing password', 400)
    user = User(name=data['name'], password=data['password'])
    user.save()
    return make_response(jsonify(user.to_dict()), 201)


@app_views.route('/users/<user_id>', methods=['PUT'])
def update_user(user_id):
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    try:
        data = request.get_json()
        if not data:
            return make_response('Not a JSON', 400)
    except Exception:
        return make_response('Not a JSON', 400)
    for k, v in data.items():
        if k not in ['id', 'email', 'created_at', 'updated_at']:
            user.__dict__[k] = v
    user.save()
    return make_response(jsonify(user.to_dict()), 200)
