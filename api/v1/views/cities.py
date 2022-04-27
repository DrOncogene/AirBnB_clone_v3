#!/usr/bin/python3
""" handles the part of the api that deals with state objects"""
from flask import jsonify, abort, request, make_response
import json
from api.v1.views import app_views
from models import storage
from models.state import State
from models.city import City


@app_views.route('/states/<state_id>/cities/', methods=['GET'],
                 strict_slashes=False)
def get_state_cities(state_id):
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    state_cities = []
    for city in state.cities:
        state_cities.append(city.to_dict())
    return jsonify(state_cities)


@app_views.route('/cities/<city_id>', methods=['GET'])
def get_city(city_id):
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route('/cities/<city_id>', methods=['DELETE'])
def delete_city(city_id):
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    storage.delete(city)
    storage.save()
    return jsonify({})


@app_views.route('/states/<state_id>/cities/', methods=['POST'],
                 strict_slashes=False)
def create_city(state_id):
    try:
        data = request.get_json()
        if not data:
            return make_response('Not a JSON', 400)
    except Exception:
        return make_response('Not a JSON', 400)
    if 'name' not in data:
        return make_response('Missing name', 400)
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    city = City(state_id=state_id, name=data['name'])
    city.save()
    return make_response(jsonify(city.to_dict()), 201)


@app_views.route('/cities/<city_id>', methods=['PUT'])
def update_city(city_id):
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    try:
        data = request.get_json()
        if not data:
            return make_response('Not a JSON', 400)
    except Exception:
        return make_response('Not a JSON', 400)
    for k, v in data.items():
        if k not in ['id', 'created_at', 'updated_at']:
            city.__dict__[k] = v
    city.save()
    return make_response(jsonify(city.to_dict()), 200)
