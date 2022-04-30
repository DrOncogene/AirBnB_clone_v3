#!/usr/bin/python3
""" handles the part of the api that deals with place_amenity objects"""
from os import getenv
from flask import jsonify, abort, request, make_response
import json
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity
from models.place import Place
from models.user import User


storage_t = getenv('HBNB_TYPE_STORAGE')


@app_views.route('/places/<place_id>/amenities/', methods=['GET'],
                 strict_slashes=False)
def get_place_amenities(place_id):
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    place_amenities = []
    if storage_t == 'db':
        for amenity in place.amenities:
            place_amenities.append(amenity.to_dict())
    else:
        for id in place.amenity_ids:
            place_amenities.append(storage.get(Amenity, id).to_dict())
    return jsonify(place_amenities)


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['DELETE'])
def delete_place_amenity(place_id, amenity_id):
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    if storage_t == 'db':
        abort(404) if amenity not in place.amenities\
         else place.amenities.pop(amenity)
    else:
        abort(404) if amenity.id not in place.amenity_ids\
         else place.amenity_ids.pop(amenity.id)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['POST'], strict_slashes=False)
def link_place_amenity(place_id, amenity_id):
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    if amenity in place.amenities:
        return make_response(jsonify(amenity.to_dict()), 200)
    if storage_t == 'db':
        place.amenities.append(amenity)
    else:
        place.append(amenity)
    storage.save()
    return make_response(jsonify(amenity.to_dict()), 201)
