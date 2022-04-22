#!/usr/bin/python3
""" the index view"""
from flask import jsonify
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


@app_views.route('/status')
def status():
    return jsonify({ "status": "OK" })


@app_views.route('/stats')
def stats():
    st = ["amenities", "cities", "places", "reviews", "states", "users"]
    stats = {}
    classes = [Amenity, City, Place, Review, State, User]
    for cls in classes:
        stats.update({st[classes.index(cls)]: storage.count(cls)})

    return stats
