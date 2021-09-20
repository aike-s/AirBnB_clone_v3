#!/usr/bin/python3
"""
All default RESTFul API actions for City objects
"""
from api.v1.views import app_views
from flask import request, abort, make_response, jsonify
from models import storage
from models.city import City
from models.state import State


@app_views.route('/states/<state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def get_all_cities(state_id):
    """ Retrieves a list of all City objects based on the state id"""
    all_state_cities = []
    state_obj = storage.get(State, state_id)

    if state_obj is None:
        abort(404)

    else:
        for city in state_obj.cities:
            all_state_cities.append(city.to_dict())

        return jsonify(all_state_cities)


@app_views.route('/cities/<city_id>', methods=['GET'],
                 strict_slashes=False)
def get_city(city_id):
    """ Retrieve a city object based on the city id """
    city_obj = storage.get(City, city_id)

    if city_obj is None:
        abort(404)
    else:
        city_obj = city_obj.to_dict()
        return jsonify(city_obj)


@app_views.route('/cities/<city_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_city(city_id):
    """ Deletes a city object based on the city id """
    city_obj = storage.get(City, city_id)

    if city_obj is None:
        abort(404)
    else:
        storage.delete(city_obj)
        storage.save()
        return jsonify({}), 200


@app_views.route('/states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def post_city(state_id):
    """ Creates a new city object """
    attributes = request.get_json(silent=True)
    state = storage.get(State, state_id)

    if not attributes:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    if not attributes["name"]:
        return make_response(jsonify({"error": "Missing name"}), 400)
    if state is None:
        abort(404)
    else:
        attributes["state_id"] = state_id
        new_city = City(**attributes)
        new_city.save()
        return jsonify(new_city.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=["PUT"],
                 strict_slashes=False)
def put_city(city_id):
    """ Updates a city object based on the city id """
    new_attributes = request.get_json(silent=True)
    city_obj = storage.get(City, city_id)

    if not new_attributes:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    if city_obj is None:
        abort(404)

    new_attributes.pop('id', None)
    new_attributes.pop('updated_at', None)
    new_attributes.pop('created_at', None)

    for key, value in new_attributes.items():
        setattr(city_obj, key, value)
    storage.save()
    return jsonify(city_obj.to_dict()), 200
