#!/usr/bin/python3
""" handles the part of the api that deals with city objects"""
from flask import jsonify, abort, request, make_response
import json
from api.v1.views import app_views
from models import storage
from models.place import Place
from models.city import City
from models.user import User


@app_views.route('/cities/<city_id>/places/', methods=['GET'],
                 strict_slashes=False)
def get_city_places(city_id):
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    city_places = [place.to_dict() for place in storage.all(Place).values()
                   if place.city_id == city_id]
    return jsonify(city_places)


@app_views.route('/places/<place_id>', methods=['GET'])
def get_place(place_id):
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'])
def delete_place(place_id):
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    storage.delete(place)
    storage.save()
    return jsonify({})


@app_views.route('/cities/<city_id>/places/', methods=['POST'],
                 strict_slashes=False)
def create_place(city_id):
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    try:
        data = request.get_json()
        if not data:
            return make_response('Not a JSON', 400)
    except Exception:
        return make_response('Not a JSON', 400)
    if 'user_id' not in data:
        return make_response('Missing user_id', 400)
    user = storage.get(User, data['user_id'])
    if not user:
        abort(404)
    if 'name' not in data:
        return make_response('Missing name', 400)
    place = Place(city_id=city_id, user_id=user.id, name=data['name'])
    place.save()
    return make_response(jsonify(place.to_dict()), 201)


@app_views.route('/places/<place_id>', methods=['PUT'])
def update_place(place_id):
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    try:
        data = request.get_json()
        if not data:
            return make_response('Not a JSON', 400)
    except Exception:
        return make_response('Not a JSON', 400)
    for k, v in data.items():
        if k not in ['id', 'user_id', 'city_id', 'created_at', 'updated_at']:
            place.__dict__[k] = v
    place.save()
    return make_response(jsonify(place.to_dict()), 200)


@app_views.route('/places_search', methods=['POST'])
def place_search():
    try:
        data = request.get_json()
    except Exception:
        return make_response('Not a JSON', 400)

    all_places = storage.all(Place)
    match = set()
    states = data.get('states') if data else []
    cities = data.get('cities') if data else []
    amenities = data.get('amenities') if data else []
    all_empty = not len(states) and not len(cities) and not len(amenities)
    if not data or all_empty:
        match = [place.to_dict() for place in all_places.values()]
        return jsonify(match)
    states = data['states']
    for state_id in states:
        pass
