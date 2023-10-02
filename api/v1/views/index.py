#!/usr/bin/python3
"""This module define the blueprint of the views"""
from flask import jsonify
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity
from models.place import Place
from models.user import User
from models.city import City
from models.state import State
from models.review import Review


@app_views.route("/status", strict_slashes=False)
def status():
    """ Returns JSON """
    return jsonify(status="OK")


@app_views.route("/stats", strict_slashes=False)
def stats():
    """ Returns stat of all objects"""
    object_map = dict(
            amenities=Amenity,
            cities=City,
            places=Place,
            reviews=Review,
            states=State,
            users=User)
    objects_stats = {
            item: storage.count(object_map[item]) for item in object_map}
    return jsonify(objects_stats)
