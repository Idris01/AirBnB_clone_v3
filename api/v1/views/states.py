#!/usr/bin/python3
"""This module define the blueprint to handle states"""
from flask import jsonify, abort, make_response, request
from api.v1.views import app_views
from models import storage
from models.state import State

state_methods = ['GET', 'POST', 'PUT', 'DELETE']


@app_views.route('/states', methods=state_methods, strict_slashes=False)
@app_views.route(
        '/states/<state_id>',
        methods=state_methods,
        strict_slashes=False)
def states(state_id=None):
    """Get state representation with a given id

    Return json of all states if state_id is None"""

    if request.method == 'GET':
        return get_state(state_id)
    elif request.method == 'DELETE':
        return delete_state(state_id)
    elif request.method == "POST":
        return post_state()
    elif request.method == "PUT":
        return update_state(state_id)


def get_state(state_id=None):
    """Handles state get methods"""
    if state_id is None:
        all_states = storage.all(State)
        json_data = [
                state.to_dict() for key, state in all_states.items()]
        return make_response(jsonify(json_data), 200)
    state_data = storage.get(State, state_id)
    if not state_data:
        abort(404)

    return make_response(jsonify(state_data.to_dict()), 200)


def delete_state(state_id=None):
    """Handles state delete request"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    state.delete()
    storage.save()
    return make_response(jsonify({}), 200)


def post_state():
    """handles post request on State object"""
    try:
        request_body = request.get_json()
        if request_body.get('name') is None:
            return make_response(jsonify({"error": "Missing name"}), 400)
        new_state = State(**request_body)
        new_state.save()
        return make_response(
                jsonify(new_state.to_dict()), 201)
    except Exception as e:
        return make_response(jsonify({"error": "Not a JSON"}), 400)


def update_state(state_id=None):
    """Handles the state update for a given state id"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    try:
        to_ignore = ('id', 'created_at', 'updated_at')
        state_data = request.get_json()
        for key, value in state_data.items():
            if key not in to_ignore:
                setattr(state, key, value)
        state.save()
        return make_response(jsonify(state.to_dict()), 200)

    except Exception as e:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
