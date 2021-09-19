#!/usr/bin/python3
"""
"""
from flask import Flask, request
from flask.json import jsonify
from models import storage
from werkzeug.exceptions import abort
from models.amenity import Amenity

HBNB_API_HOST = '0.0.0.0'
HBNB_API_PORT = '5000'

app = Flask(__name__)


@app.route('/api/v1/amenities', method=['GET'], strict_slashes=False)
def get_all_amenities():
    """ Retrieves a list of all State objects """
    all_amenities = []
    amenity_objs = storage.all("Amenity")

    for obj in amenity_objs.values():
        all_amenities.append(obj.to_dict())

    return jsonify(all_amenities)


@app.route('/api/v1/amenities/<int:amenity_id>', methods=['GET'], strict_slashes=False)
def get_state (amenity_id):
    """ Retrieve a state object based on the state id """
    amenity_obj = (storage.get(Amenity, amenity_id)).to_dict()

    if amenity_obj is None:
        abort (404)
    else:
        return jsonify(amenity_obj)


@app.route('/api/v1/amenities/<int:amenity_id>', method=['DELETE'], strict_slashes=False)
def delete_state(amenity_id):
    """ Deletes a state object based on the state id """
    amenity_obj = storage.get(Amenity, amenity_id)

    if amenity_obj is None:
        abort (404)
    else:
        storage.delete(amenity_obj)
        return {}, 200


@app.route('/api/v1/amenities', methods=['POST'], strict_slashes=False)
def post_state():
    """ Creates a new state object """
    attributes = request.get_json

    if not attributes.is_json:
        abort(404, description="Not a JSON")
    if not attributes["name"]:
        abort(404, description="Missing name")
    else:
        new_amenity = Amenity(attributes)
        storage.new(new_amenity)
        return jsonify(new_amenity.to_dict()), 201


@app.route('/api/v1/amenities/<int:amenity_id>', methods=["PUT"], strict_slashes=False)
def put_state(amenity_id):
    """ Updates a state object based on the state id """
    new_attributes = request.get_json
    amenity_obj = storage.get(Amenity, amenity_id)

    if not new_attributes.is_json:
        abort(404, description="Not a JSON")
    if amenity_obj is None:
        abort (404)

    new_attributes.pop('id', None)
    new_attributes.pop('updated_at', None)
    new_attributes.pop('created_at', None)

    setattr(amenity_obj, new_attributes)
    amenity_obj.save()
    return jsonify(amenity_obj.to_dict()), 200


if __name__ == "__main__":
    app.run(host=HBNB_API_HOST, port=HBNB_API_PORT, threaded=True)
