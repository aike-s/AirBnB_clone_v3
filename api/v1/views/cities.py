#!/usr/bin/python3
"""

"""
from flask import Flask, request
from flask.json import jsonify
from models import storage
from werkzeug.exceptions import abort
from models.city import City

HBNB_API_HOST = '0.0.0.0'
HBNB_API_PORT = '5000'

app = Flask(__name__)


@app.route('/api/v1/states/<int:state_id>/cities', method=['GET'], strict_slashes=False)
def get_all_cities(state_id):
    """ Retrieves a list of all City objects based on the state id"""
    all_state_cities = []
    city_objs = storage.all("City")

    for obj in city_objs.values():
        obj = obj.to_dict()
        if obj['state_id'] is state_id:
            all_state_cities.append(obj)

    if len[all_state_cities] < 1:
        abort(404)
    else:
        return jsonify(all_state_cities)


@app.route('/api/v1/cities/<int:city_id>', methods=['GET'], strict_slashes=False)
def get_city (city_id):
    """ Retrieve a city object based on the city id """
    city_obj = (storage.get(city_id)).to_dict()

    if city_obj is None:
        abort (404)
    else:
        return jsonify(city_obj)


@app.route('/api/v1/cities/<int:city_id>', method=['DELETE'], strict_slashes=False)
def delete_city(city_id):
    """ Deletes a city object based on the city id """
    city_obj = (storage.get(city_id))

    if city_obj is None:
        abort (404)
    else:
        storage.delete(city_obj)
        return {}, 200


@app.route('/api/v1/states/<int:state_id>/cities', methods=['POST'], strict_slashes=False)
def post_city(state_id):
    """ Creates a new city object """
    attributes = request.get_json
    state = storage.get(state_id)

    if not attributes.is_json:
        abort(404, description="Not a JSON")
    if not attributes["name"]:
        abort(404, description="Missing name")
    if state is None:
        abort(404)
    else:
        attributes["state_id"] = state_id
        new_city = City(attributes)
        storage.new(new_city)
        return jsonify(new_city.to_dict()), 201


@app.route('/api/v1/cities/<int:city_id>', methods=["PUT"], strict_slashes=False)
def put_city(city_id):
    """ Updates a city object based on the city id """
    new_attributes = request.get_json
    city_obj = (storage.get(city_id))

    if not new_attributes.is_json:
        abort(404, description="Not a JSON")
    if city_obj is None:
        abort (404)

    new_attributes.pop('id', None)
    new_attributes.pop('updated_at', None)
    new_attributes.pop('created_at', None)

    setattr(city_obj, new_attributes)
    city_obj.save()
    return jsonify(city_obj.to_dict()), 200

if __name__ == "__main__":
    app.run(host=HBNB_API_HOST, port=HBNB_API_PORT, threaded=True)
