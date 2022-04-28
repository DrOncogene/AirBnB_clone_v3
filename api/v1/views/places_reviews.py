#!/usr/bin/python3
""" handles the part of the api that deals with place objects"""
from flask import jsonify, abort, request, make_response
import json
from api.v1.views import app_views
from models import storage
from models.review import Review
from models.place import Place
from models.user import User


@app_views.route('/places/<place_id>/reviews/', methods=['GET'],
                 strict_slashes=False)
def get_place_reviews(place_id):
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    place_reviews = []
    for review in place.reviews:
        place_reviews.append(review.to_dict())
    return jsonify(place_reviews)


@app_views.route('/reviews/<review_id>', methods=['GET'])
def get_review(review_id):
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route('/reviews/<review_id>', methods=['DELETE'])
def delete_review(review_id):
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    storage.delete(review)
    storage.save()
    return jsonify({})


@app_views.route('/places/<place_id>/reviews/', methods=['POST'],
                 strict_slashes=False)
def create_review(place_id):
    place = storage.get(Place, place_id)
    if not place:
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
    if 'text' not in data:
        return make_response('Missing text', 400)
    review = Review(place_id=place_id, user_id=user.id, text=data['text'])
    review.save()
    return make_response(jsonify(review.to_dict()), 201)


@app_views.route('/reviews/<review_id>', methods=['PUT'])
def update_review(review_id):
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    try:
        data = request.get_json()
        if not data:
            return make_response('Not a JSON', 400)
    except Exception:
        return make_response('Not a JSON', 400)
    for k, v in data.items():
        if k not in ['id', 'user_id', 'place_id', 'created_at', 'updated_at']:
            review.__dict__[k] = v
    review.save()
    return make_response(jsonify(review.to_dict()), 200)
