#!/usr/bin/python3
"""This module define the blueprint to handle states"""
from flask import jsonify, abort, make_response, request
from api.v1.views import app_views
from models import storage
from models.state import State
from models.city import City


@app_views.route(
        '/states/<state_id>/cities',
        methods=['GET', 'POST'],
        strict_slashes=False)
def state_cities(state_id):
    """Get state representation with a given id

    Return json of all states if state_id is None"""

    if request.method == 'GET':
        state = storage.get(State, state_id)
        if not state or state is None:
            abort(404)
        state_cities = state.cities
        state_cities = [city.to_dict() for city in state_cities]
        return make_response(jsonify(state_cities), 200)
    else:
        state = storage.get(State, state_id)
        if not state or state is None:
            abort(404)
        try:
            city_data = request.get_json()
            if city_data.get('name') is None:
                return make_response(jsonify(dict(error="Missin name")), 400)
            city_data['state_id'] = state_id
            new_city = City(**city_data)
            new_city.save()
            return make_response(jsonify(new_city.to_dict()), 201)
        except Exception as e:
            print(e)
            return make_response(jsonify(dict(error="Not a JSON")), 400)


@app_views.route(
        '/cities/<city_id>',
        methods=['GET', 'PUT', 'DELETE'],
        strict_slashes=False)
def cities(city_id):
    """Get the city with an id city_id"""

    city = storage.get(City, city_id)
    if not city or city is None:
        abort(404)
    if request.method == 'GET':
        return make_response(jsonify(city.to_dict()), 200)
    elif request.method == 'DELETE':
        storage.delete(city)
        storage.save()
        return make_response(jsonify({}), 200)
    else:
        try:
            request_data = request.get_json()
            to_ignore = ('id', 'created_at', 'updated_at')
            for key, value in request_data.items():
                if key not in to_ignore:
                    setattr(city, key, value)
            city.save()
            return make_response(jsonify(city.to_dict()), 200)
        except Exception as e:
            return make_response(jsonify(dict(error="Not a JSON")), 400)
