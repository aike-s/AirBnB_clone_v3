#!/usr/bin/python3
"""

"""
from flask import Flask, request
from flask.json import jsonify
from models import storage
from werkzeug.exceptions import abort
from models.user import User

HBNB_API_HOST = '0.0.0.0'
HBNB_API_PORT = '5000'

app = Flask(__name__)


@app.route('/api/v1/users', method=['GET'], strict_slashes=False)
def get_all_users():
    """ Retrieves a list of all State objects """
    all_users = []
    user_objs = storage.all("User")

    for obj in user_objs.values():
        all_users.append(obj.to_dict())

    return jsonify(all_users)


@app.route('/api/v1/users/<int:user_id>', methods=['GET'], strict_slashes=False)
def get_state (user_id):
    """ Retrieve a state object based on the state id """
    user_obj = (storage.get(user_id)).to_dict()

    if user_obj is None:
        abort (404)
    else:
        return jsonify(user_obj)


@app.route('/api/v1/users/<int:user_id>', method=['DELETE'], strict_slashes=False)
def delete_state(user_id):
    """ Deletes a state object based on the state id """
    user_obj = (storage.get(user_id))

    if user_obj is None:
        abort (404)
    else:
        storage.delete(user_obj)
        return {}, 200


@app.route('/api/v1/users', methods=['POST'], strict_slashes=False)
def post_state():
    """ Creates a new state object """
    attributes = request.get_json

    if not attributes.is_json:
        abort(404, description="Not a JSON")
    if not attributes["name"]:
        abort(404, description="Missing name")
    else:
        new_state = User(attributes)
        storage.new(new_state)
        return jsonify(new_state.to_dict()), 201


@app.route('/api/v1/users/<int:user_id>', methods=["PUT"], strict_slashes=False)
def put_state(user_id):
    """ Updates a state object based on the state id """
    new_attributes = request.get_json
    user_obj = (storage.get(user_id))

    if not new_attributes.is_json:
        abort(404, description="Not a JSON")
    if user_obj is None:
        abort (404)

    new_attributes.pop('id', None)
    new_attributes.pop('updated_at', None)
    new_attributes.pop('created_at', None)

    setattr(user_obj, new_attributes)
    user_obj.save()
    return jsonify(user_obj.to_dict()), 200

if __name__ == "__main__":
    app.run(host=HBNB_API_HOST, port=HBNB_API_PORT, threaded=True)
