#!/usr/bin/python3
"""
"""
from api.v1.views import app_views
from flask import request
from flask.json import jsonify
from models import storage
from werkzeug.exceptions import abort
from models import user
from models.user import User


@app_views.route('/api/v1/users', method=['GET'], strict_slashes=False)
def get_all_users():
    """ Retrieves a list of all State objects """
    all_users = []
    user_objs = storage.all("User")

    for obj in user_objs.values():
        all_users.append(obj.to_dict())

    return jsonify(all_users)


@app_views.route('/api/v1/users/<int:user_id>', methods=['GET'],
                 strict_slashes=False)
def get_state(user_id):
    """ Retrieve a state object based on the state id """
    user_obj = storage.get(User, user_id)

    if user_obj is None:
        abort(404)
    else:
        user_obj.to_dict()
        return jsonify(user_obj)


@app_views.route('/api/v1/users/<int:user_id>', method=['DELETE'],
                 strict_slashes=False)
def delete_state(user_id):
    """ Deletes a state object based on the state id """
    user_obj = storage.get(User, user_id)

    if user_obj is None:
        abort(404)
    else:
        storage.delete(user_obj)
        return jsonify({}), 200


@app_views.route('/api/v1/users', methods=['POST'], strict_slashes=False)
def post_state():
    """ Creates a new state object """
    attributes = request.get_json(silent=True)

    if not attributes.is_json:
        abort(404, description="Not a JSON")
    if not attributes["name"]:
        abort(404, description="Missing name")
    else:
        new_user = User(**attributes)
        new_user.save()
        return jsonify(new_user.to_dict()), 201


@app_views.route('/api/v1/users/<int:user_id>', methods=["PUT"],
                 strict_slashes=False)
def put_state(user_id):
    """ Updates a state object based on the state id """
    new_attributes = request.get_json(silent=True)
    user_obj = storage.get(User, user_id)

    if not new_attributes:
        abort(404, description="Not a JSON")
    if user_obj is None:
        abort(404)

    new_attributes.pop('id', None)
    new_attributes.pop('updated_at', None)
    new_attributes.pop('created_at', None)

    for key, value in new_attributes.items():
        setattr(user_obj, key, value)
    user_obj.save()
    return jsonify(user_obj.to_dict()), 200
