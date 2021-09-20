#!/usr/bin/python3
"""
All default RESTFul API actions for Amenity objects
"""
from api.v1.views import app_views
from flask import request, abort
from flask.json import jsonify
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def get_all_amenities():
    """ Retrieves a list of all State objects """
    all_amenities = []
    amenity_objs = storage.all("Amenity")

    for obj in amenity_objs.values():
        all_amenities.append(obj.to_dict())

    return jsonify(all_amenities)


@app_views.route('/amenities/<amenity_id>', methods=['GET'],
                 strict_slashes=False)
def get_amenity(amenity_id):
    """ Retrieve a state object based on the state id """
    amenity_obj = storage.get(Amenity, amenity_id)

    if amenity_obj is None:
        abort(404)
    else:
        amenity_obj.to_dict()
        return jsonify(amenity_obj)


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_amenity(amenity_id):
    """ Deletes a state object based on the state id """
    amenity_obj = storage.get(Amenity, amenity_id)

    if amenity_obj is None:
        abort(404)
    else:
        storage.delete(amenity_obj)
        return jsonify({}), 200


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def post_amenity():
    """ Creates a new state object """
    attributes = request.get_json(silent=True)

    if not attributes:
        abort(404, description="Not a JSON")
    if not attributes["name"]:
        abort(404, description="Missing name")
    else:
        new_amenity = Amenity(**attributes)
        storage.new(new_amenity)
        return jsonify(new_amenity.to_dict()), 201


@app_views.route('/amenities/<amenity_id>', methods=["PUT"],
                 strict_slashes=False)
def put_amenity(amenity_id):
    """ Updates a state object based on the state id """
    new_attributes = request.get_json(silent=True)
    amenity_obj = storage.get(Amenity, amenity_id)

    if not new_attributes:
        abort(404, description="Not a JSON")
    if amenity_obj is None:
        abort(404)

    new_attributes.pop('id', None)
    new_attributes.pop('updated_at', None)
    new_attributes.pop('created_at', None)

    for key, value in new_attributes.items():
        setattr(amenity_obj, key, value)
    amenity_obj.save()
    return jsonify(amenity_obj.to_dict()), 200
