#!/usr/bin/python3
"""This module define the blueprint to handle Places"""
from flask import jsonify, abort, make_response, request
from api.v1.views import app_views
from models.place import Place
from models.city import City
from models.user import User
from models import storage


@app_views.route(
        '/cities/<city_id>/places',
        methods=['GET', 'POST'],
        strict_slashes=False)
def city_place_list_create(city_id):
    """Handles listing and creating of places for giviven city"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)

    if request.method == 'GET':
        places = [place.to_dict() for place in city.places]
        return make_response(jsonify(places), 200)
    try:
        data = request.get_json()
        if data.get("user_id") is None:
            return make_response(
                    jsonify({"error": "Missing user_id"}), 400)
        user = storage.get(User, data.get("user_id"))
        if not user or user is None:
            abort(404)

        if data.get("name") is None:
            return make_response(
                    jsonify({"error": "Missing name"}), 400)

        place = Place(**data)
        place.save()
        return make_response(
                jsonify(place.to_dict()), 201)

    except Exception as e:
        return make_response(jsonify({"error": "Not a JSON"}), 400)


@app_views.route(
        '/places/<place_id>',
        methods=['GET', 'DELETE', 'PUT'],
        strict_slashes=False)
def place_retrieve_delete_update(place_id):
    """Handles place  List, Update and Create"""

    place = storage.get(Place, place_id)
    if not place or place is None:
        abort(404)
    if request.method == 'GET':
        return make_response(jsonify(place.to_dict()), 200)
    elif request.method == 'DELETE':
        place.delete()
        storage.save()
        return make_response(jsonify({}), 200)
    else:
        try:
            data = request.get_json()
            to_ignore = ('id', 'user_id', 'city_id', 'created_at', 'updated_at')
            for key, value in data.items():
                if key not in to_ignore:
                    setattr(place, key, value)
            place.save()
            return make_response(
                    jsonify(place.to_dict()), 200)
        except Exception as e:
            return make_response(
                    jsonify({"error": "Not a JSON"}), 400)
