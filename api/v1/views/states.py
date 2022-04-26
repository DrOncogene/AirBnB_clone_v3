#!/usr/bin/python3
""" handles the part of the api that deals with state objects"""
from flask import jsonify, abort, request, make_response
from api.v1.views import app_views
from models import storage
from models.state import State


@app_views.route('/states')
def states():
    all_states = [state.to_dict() for state in storage.all(State).values()]
    return jsonify(all_states)


@app_views.route('/states/<state_id>', methods=['GET'])
def get_state(state_id):
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    return jsonify(state.to_dict())


@app_views.route('/states/<state_id>', methods=['DELETE'])
def delete_state(state_id):
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    storage.delete(state)
    storage.save()
    return jsonify("{}")


@app_views.route('/states', methods=['POST'])
def create_state():
    data = request.json
    if not data:
        return make_response('Not a JSON', 400)
    if 'name' not in data:
        return make_response('Missing name', 400)
    state = State(name=data['name'])
    storage.new(state)
    storage.save()
    return make_response(jsonify(state.to_dict()), 201)

@app_views.route('/states/<state_id>', methods=['PUT'])
def update_state(state_id):
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    data = request.json
    if not data:
        return make_response('Not a JSON', 400)
    for k, v in data.items():
        state.__dict__.update({k: v})
    storage.new(state)
    storage.save()
    return make_response(jsonify(state.to_dict()), 200)
