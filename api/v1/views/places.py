#!/usr/bin/python3
"""
All default RESTFul API actions for Place objects
"""
from api.v1.views import app_views
from flask import request, abort, make_response
from flask.json import jsonify
from models import storage
from models.place import Place
from models.city import City


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def get_all_places(city_id):
    """ Retrieves a list of all place objects based on the place id"""
    all_city_places = []
    place_objs = storage.all("Place")

    for obj in place_objs.values():
        obj = obj.to_dict()
        if obj['city_id'] is city_id:
            all_city_places.append(obj)

    if len[all_city_places] < 1:
        abort(404)
    else:
        return jsonify(all_city_places)


@app_views.route('/places/<place_id>', methods=['GET'],
                 strict_slashes=False)
def get_place(place_id):
    """ Retrieve a place object based on the place id """
    place_obj = storage.get(Place, place_id)

    if place_obj is None:
        abort(404)
    else:
        place_obj = place_obj.to_dict()
        return jsonify(place_obj)


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id):
    """ Deletes a place object based on the place id """
    place_obj = storage.get(Place, place_id)

    if place_obj is None:
        abort(404)
    else:
        storage.delete(place_obj)
        storage.save()
        return jsonify({}), 200


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def post_place(city_id):
    """ Creates a new place object """
    attributes = request.get_json(silent=True)
    city = storage.get(City, city_id)

    if not attributes:
        return make_response(jsonify({"error": "Not a JSON"}), 404)
    if not attributes["name"]:
        return make_response(jsonify({"error": "Missing name"}), 404)
    if city is None:
        abort(404)
    else:
        attributes["city_id"] = city_id
        new_place = Place(**attributes)
        new_place.save()
        return jsonify(new_place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=["PUT"],
                 strict_slashes=False)
def put_place(place_id):
    """ Updates a place object based on the place id """
    new_attributes = request.get_json(silent=True)
    place_obj = storage.get(Place, place_id)

    if not new_attributes:
        return make_response(jsonify({"error": "Not a JSON"}), 404)
    if place_obj is None:
        abort(404)

    new_attributes.pop('id', None)
    new_attributes.pop('updated_at', None)
    new_attributes.pop('created_at', None)

    for key, value in new_attributes.items():
        setattr(place_obj, key, value)
    place_obj.save()
    return jsonify(place_obj.to_dict()), 200
