#!/usr/bin/python3
'''Contains the users view for the API.'''
from flask import abort, jsonify, make_response, request
from api.v1.views import app_views
from models import storage
from models.user import User


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def users():
    """Retrieves the list of all User objects"""
    objs = storage.all(User)
    return jsonify([obj.to_dict() for obj in objs.values()])


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def single_user(user_id):
    """Retrieves a User object"""
    obj = storage.get(User, user_id)
    if not obj:
        abort(404)
    return jsonify(obj.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def del_user(user_id):
    """Returns an empty dictionary with the status code 200"""
    obj = storage.get(User, user_id)
    if not obj:
        abort(404)
    obj.delete()
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def post_user():
    """Returns the new User with the status code 201"""
    try:
        new_user = request.get_json()
        if 'email' not in new_user:
            return make_response(
                    jsonify(dict(error="Missing email")), 400)
        if 'password' not in new_user:
            return make_response(
                    jsonify(dict(error="Missing password")), 400)
    except Exception as e:
        return make_response(jsonify(
            dict(error="Not a JSON")), 400)
    obj = User(**new_user)
    storage.new(obj)
    storage.save()
    return make_response(jsonify(obj.to_dict()), 201)


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def put_user(user_id):
    """Returns the User object with the status code 200"""
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    try:
        req = request.get_json()
        to_ignore = ['id', 'email', 'created_at', 'updated_at']

        for key, value in req.items():
            if key not in to_ignore:
                setattr(user, key, value)
        user.save()
        return make_response(jsonify(user.to_dict()), 200)
    except Exception as e:
        return make_response(jsonify(
            dict(error="Not a JSON")), 400)
