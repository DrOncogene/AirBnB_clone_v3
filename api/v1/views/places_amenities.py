#!/usr/bin/python3
""" handles the part of the api that deals with place_amenity objects"""
from flask import jsonify, abort, make_response
from api.v1.views import app_views
from models import storage, storage_t
from models.amenity import Amenity
from models.place import Place


@app_views.route('/places/<place_id>/amenities/', methods=['GET'],
                 strict_slashes=False)
def get_place_amenities(place_id):
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    place_amenities = []
    for amenity in place.amenities:
        place_amenities.append(amenity.to_dict())
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
    place.save()
    return jsonify({})


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
        place.amenity_ids.append(amenity.id)
    place.save()
    return make_response(jsonify(amenity.to_dict()), 201)
