#!/usr/bin/python3
"""This module define the blueprint to handle Amenities"""
from flask import jsonify, abort, make_response, request
from api.v1.views import app_views
from models.amenity import Amenity
from models import storage


@app_views.route('/amenities', methods=['GET', 'POST'], strict_slashes=False)
def amenit_list_create():
    """Handles listing and creating of amenity"""
    if request.method == 'GET':
        amenities = storage.all(Amenity)
        amenities = [ameni.to_dict() for key, ameni in amenities.items()]
        return make_response(jsonify(amenities), 200)
    try:
        data = request.get_json()
        if data.get("name") is None:
            return make_response(
                    jsonify({"error": "Missing name"}), 400)
        new_amenity = Amenity(**data)
        new_amenity.save()
        return make_response(
                jsonify(new_amenity.to_dict()), 201)
    except Exception as e:
        return make_response(jsonify({"error": "Not a JSON"}), 400)


@app_views.route(
        '/amenities/<amenity_id>',
        methods=['GET', 'DELETE', 'PUT'],
        strict_slashes=False)
def amenities_detail(amenity_id):
    """Handles amenity  CRUD representation"""

    if request.method == 'GET':
        amenity = storage.get(Amenity, amenity_id)
        if not amenity or amenity is None:
            abort(404)
        return make_response(jsonify(amenity.to_dict()), 200)
    elif request.method == 'DELETE':
        amenity = storage.get(Amenity, amenity_id)
        if not amenity or amenity is None:
            abort(404)
        amenity.delete()
        storage.save()
        return make_response(jsonify({}), 200)
    else:
        amenity = storage.get(Amenity, amenity_id)
        if not amenity or amenity is None:
            abort(404)
        try:
            data = request.get_json()
            to_ignore = ('id', 'created_at', 'updated_at')
            for key, value in data.items():
                if key not in to_ignore:
                    setattr(amenity, key, value)
            amenity.save()
            return make_response(
                    jsonify(amenity.to_dict()), 200)
        except Exception as e:
            return make_response(
                    jsonify({"error": "Not a JSON"}), 400)
