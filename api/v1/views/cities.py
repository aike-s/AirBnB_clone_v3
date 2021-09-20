#!/usr/bin/python3
"""
All default RESTFul API actions for City objects
"""
from api.v1.views import app_views
from flask import request, abort
from flask.json import jsonify
from models import storage
from models.city import City
from models.state import State


@app_views.route('/api/v1/states/<int:state_id>/cities', method=['GET'],
                 strict_slashes=False)
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


@app_views.route('/api/v1/cities/<int:city_id>', methods=['GET'],
                 strict_slashes=False)
def get_city(city_id):
    """ Retrieve a city object based on the city id """
    city_obj = storage.get(City, city_id)

    if city_obj is None:
        abort(404)
    else:
        city_obj.to_dict()
        return jsonify(city_obj)


@app_views.route('/api/v1/cities/<int:city_id>', method=['DELETE'],
                 strict_slashes=False)
def delete_city(city_id):
    """ Deletes a city object based on the city id """
    city_obj = storage.get(City, city_id)

    if city_obj is None:
        abort(404)
    else:
        storage.delete(city_obj)
        return jsonify({}), 200


@app_views.route('/api/v1/states/<int:state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def post_city(state_id):
    """ Creates a new city object """
    attributes = request.get_json(silent=True)
    state = storage.get(State, state_id)

    if not attributes:
        abort(404, description="Not a JSON")
    if not attributes["name"]:
        abort(404, description="Missing name")
    if state is None:
        abort(404)
    else:
        attributes["state_id"] = state_id
        new_city = City(**attributes)
        new_city.save()
        return jsonify(new_city.to_dict()), 201


@app_views.route('/api/v1/cities/<int:city_id>', methods=["PUT"],
                 strict_slashes=False)
def put_city(city_id):
    """ Updates a city object based on the city id """
    new_attributes = request.get_json(silent=True)
    city_obj = storage.get(City, city_id)

    if not new_attributes:
        abort(404, description="Not a JSON")
    if city_obj is None:
        abort(404)

    new_attributes.pop('id', None)
    new_attributes.pop('updated_at', None)
    new_attributes.pop('created_at', None)

    for key, value in new_attributes.items():
        setattr(city_obj, key, value)
    city_obj.save()
    return jsonify(city_obj.to_dict()), 200
