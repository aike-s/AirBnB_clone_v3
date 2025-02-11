#!/usr/bin/python3
"""
All default RESTFul API actions for review objects
"""
from api.v1.views import app_views
from flask import abort, jsonify
from models import storage
from models.place import Place
from models.amenity import Amenity


@app_views.route('/places/<place_id>/amenities', methods=['GET'],
                 strict_slashes=False)
def get_all_place_amenities(place_id):
    """ Retrieves a list of all amenity objects based on the place id"""
    all_place_amenities = []
    place_obj = storage.get(Place, place_id)

    if place_obj is None:
        abort(404)

    else:
        for amenity in place_obj.amenities:
            all_place_amenities.append(amenity.to_dict())

        return jsonify(all_place_amenities)


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_place_amenity(place_id, amenity_id):
    """ Deletes a review object based on the review id """
    amenity_obj = storage.get(Amenity, amenity_id)
    place_obj = storage.get(Place, place_id)

    if amenity_obj is None:
        abort(404)
    if place_obj is None:
        abort(404)
    if amenity_obj.to_dict()["place_id"] is not place_id:
        abort(404)
    else:
        storage.delete(amenity_obj)
        storage.save()
        return jsonify({}), 200


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['POST'], strict_slashes=False)
def post_place_amenity(place_id, amenity_id):
    """ Creates a new amenity """
    place_obj = storage.get(Place, place_id)
    amenity_obj = storage.get(Amenity, amenity_id)

    if place_obj is None:
        abort(404)
    if amenity_obj is None:
        abort(404)

    amenity_dict = amenity_obj.to_dict()

    if amenity_dict["place_id"] is place_id:
        return jsonify(amenity_dict), 200
    else:
        amenity_dict["place_id"] = place_id
        return jsonify(amenity_dict), 201
