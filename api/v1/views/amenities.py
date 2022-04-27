#!/usr/bin/python3
""" handles the part of the api that deals with amenity objects"""
from flask import jsonify, abort, request, make_response
import json
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities/', methods=['GET'], strict_slashes=False)
def amenities():
    amenities = [amenity.to_dict() for amenity in storage.all(Amenity).values()]
    return jsonify(amenities)


@app_views.route('/amenities/<amenity_id>', methods=['GET'])
def get_amenity(amenity_id):
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    return jsonify(amenity.to_dict())


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'])
def delete_amenity(amenity_id):
    amenity = storage.get(amenity, amenity_id)
    if not amenity:
        abort(404)
    storage.delete(amenity)
    storage.save()
    return jsonify({})


@app_views.route('/amenities/', methods=['POST'], strict_slashes=False)
def create_amenity():
    try:
        data = request.get_json()
        if not data:
            return make_response('Not a JSON', 400)
    except Exception:
        return make_response('Not a JSON', 400)
    if 'name' not in data:
        return make_response('Missing name', 400)
    amenity = Amenity(name=data['name'])
    amenity.save()
    return make_response(jsonify(amenity.to_dict()), 201)


@app_views.route('/amenities/<amenity_id>', methods=['PUT'])
def update_amenity(amenity_id):
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    try:
        data = request.get_json()
        if not data:
            return make_response('Not a JSON', 400)
    except Exception:
        return make_response('Not a JSON', 400)
    for k, v in data.items():
        if k not in ['id', 'created_at', 'updated_at']:
            amenity.__dict__[k] = v
    amenity.save()
    return make_response(jsonify(amenity.to_dict()), 200)
