#!/usr/bin/python3
""" handles the part of the api that deals with city objects"""

from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage
from models.city import City
from models.place import Place
from models.user import User
from models.state import State
from models.amenity import Amenity


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
    data = request.get_json(silent=True)
    if not data:
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
    data = request.get_json(silent=True)
    if not data:
        return make_response('Not a JSON', 400)
    for k, v in data.items():
        if k not in ['id', 'user_id', 'city_id', 'created_at', 'updated_at']:
            setattr(place, k, v)
    place.save()
    return make_response(jsonify(place.to_dict()), 200)


@app_views.route('/places_search', methods=['POST'])
def place_search():
    data = request.get_json(silent=True)
    if type(data) is not dict:
        return make_response('Not a JSON', 400)

    all_places = storage.all(Place)
    match = set()
    states = data.get('states') if data.get('states') else []
    cities = data.get('cities') if data.get('cities') else []
    amenities = data.get('amenities') if data.get('amenities') else []
    all_empty = not states and not cities and not amenities
    if all_empty:
        match = set(all_places.values())

    for state_id in states:
        state = storage.get(State, state_id)
        places_in_state = {place for place in all_places.values()
                           if storage.get(City, place.city_id) in state.cities}
        match = match.union(places_in_state)
    for city_id in cities:
        places_in_city = {place for place in all_places.values()
                          if place.city_id == city_id}
        match = match.union(places_in_city)

    if amenities:
        if len(match) == 0:
            match = set(all_places.values())
        amenities = {storage.get(Amenity, amenity_id)
                     for amenity_id in amenities}
        match = {place for place in match
                 if amenities.intersection(set(place.amenities)) == amenities}

    final_match = []
    for place in match:
        place_dict = place.to_dict()
        place_dict.pop('amenities', None)
        final_match.append(place_dict)

    return jsonify(final_match)
