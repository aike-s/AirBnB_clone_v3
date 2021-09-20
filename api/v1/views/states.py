#!/usr/bin/python3
"""
All default RESTFul API actions for State objects
"""
from api.v1.views import app_views
from flask import request, abort, make_response, jsonify
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_all_states():
    """ Retrieves a list of all State objects """
    all_states = []
    state_objs = storage.all("State")

    for obj in state_objs.values():
        all_states.append(obj.to_dict())

    return jsonify(all_states)


@app_views.route('/states/<state_id>', methods=['GET'],
                 strict_slashes=False)
def get_state(state_id):
    """ Retrieve a state object based on the state id """
    state_obj = storage.get(State, state_id)

    if state_obj is None:
        abort(404)
    else:
        state_obj = state_obj.to_dict()
        return jsonify(state_obj)


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_state(state_id):
    """ Deletes a state object based on the state id """
    state_obj = storage.get(State, state_id)

    if state_obj is None:
        abort(404)
    else:
        storage.delete(state_obj)
        storage.save()
        return jsonify({}), 200


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def post_state():
    """ Creates a new state object """
    attribute = request.get_json(silent=True)

    if not attribute:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    if not attribute["name"]:
        return make_response(jsonify({"error": "Missing name"}), 400)
    else:
        new_state = State(**attribute)
        new_state.save()
        return jsonify(new_state.to_dict()), 201


@app_views.route('/states/<state_id>', methods=["PUT"],
                 strict_slashes=False)
def put_state(state_id):
    """ Updates a state object based on the state id """
    new_attributes = request.get_json(silent=True)
    state_obj = storage.get(State, state_id)

    if not new_attributes:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    if state_obj is None:
        abort(404)

    new_attributes.pop('id', None)
    new_attributes.pop('updated_at', None)
    new_attributes.pop('created_at', None)

    for key, value in new_attributes.items():
        setattr(state_obj, key, value)
    storage.save()
    return jsonify(state_obj.to_dict()), 200
