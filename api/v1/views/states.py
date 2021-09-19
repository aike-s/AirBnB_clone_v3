#!/usr/bin/python3
"""

"""
from flask import Flask, request
from flask.json import jsonify
from models import storage
from werkzeug.exceptions import abort
from models.state import State

HBNB_API_HOST = '0.0.0.0'
HBNB_API_PORT = '5000'

app = Flask(__name__)


@app.route('/api/v1/states', method=['GET'], strict_slashes=False)
def get_all_states():
    """ Retrieves a list of all State objects """
    all_states = []
    state_objs = storage.all("State")

    for obj in state_objs.values():
        all_states.append(obj.to_dict())

    return jsonify(all_states)


@app.route('/api/v1/states/<int:state_id>', methods=['GET'], strict_slashes=False)
def get_state (state_id):
    """ Retrieve a state object based on the state id """
    state_obj = (storage.get(State, state_id)).to_dict()

    if state_obj is None:
        abort (404)
    else:
        return jsonify(state_obj)


@app.route('/api/v1/states/<int:state_id>', method=['DELETE'], strict_slashes=False)
def delete_state(state_id):
    """ Deletes a state object based on the state id """
    state_obj = storage.get(State, state_id)

    if state_obj is None:
        abort (404)
    else:
        storage.delete(state_obj)
        return {}, 200


@app.route('/api/v1/states', methods=['POST'], strict_slashes=False)
def post_state():
    """ Creates a new state object """
    attribute = request.get_json

    if not attribute.is_json:
        abort(404, description="Not a JSON")
    if not attribute["name"]:
        abort(404, description="Missing name")
    else:
        new_state = State(attribute)
        storage.new(new_state)
        return jsonify(new_state.to_dict()), 201


@app.route('/api/v1/states/<int:state_id>', methods=["PUT"], strict_slashes=False)
def put_state(state_id):
    """ Updates a state object based on the state id """
    new_attributes = request.get_json
    state_obj = storage.get(State, state_id)

    if not new_attributes.is_json:
        abort(404, description="Not a JSON")
    if state_obj is None:
        abort (404)

    """ pop() deletes a key if it exists or do nothing otherwise """
    new_attributes.pop('id', None)
    new_attributes.pop('updated_at', None)
    new_attributes.pop('created_at', None)

    setattr(state_obj, new_attributes)
    state_obj.save()
    return jsonify(state_obj.to_dict()), 200

if __name__ == "__main__":
    app.run(host=HBNB_API_HOST, port=HBNB_API_PORT, threaded=True)
