#!/usr/bin/python3
"""
All default RESTFul API actions for review objects
"""
from api.v1.views import app_views
from flask import request, abort
from flask.json import jsonify
from models import storage
from models.place import Place
from models.review import Review


@app_views.route('/places/<place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def get_all_place_reviews(place_id):
    """ Retrieves a list of all place objects based on the place id"""
    all_place_reviews = []
    review_objs = storage.all("Review")

    for obj in review_objs.values():
        obj = obj.to_dict()
        if obj['place_id'] is place_id:
            all_place_reviews.append(obj)

    if len[all_place_reviews] < 1:
        abort(404)
    else:
        return jsonify(all_place_reviews)


@app_views.route('/reviews/<review_id>', methods=['GET'],
                 strict_slashes=False)
def get_place_review(review_id):
    """ Retrieve a place object based on the review id """
    review_obj = storage.get(Review, review_id)

    if review_obj is None:
        abort(404)
    else:
        review_obj.to_dict()
        return jsonify(review_obj)


@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place_review(review_id):
    """ Deletes a review object based on the review id """
    review_obj = storage.get(Review, review_id)

    if review_obj is None:
        abort(404)
    else:
        storage.delete(review_obj)
        return jsonify({}), 200


@app_views.route('/places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def post_place_review(place_id):
    """ Creates a new place object """
    attributes = request.get_json(silent=True)
    place = storage.get(Place, place_id)

    if not attributes:
        abort(404, description="Not a JSON")
    if not attributes["name"]:
        abort(404, description="Missing name")
    if place is None:
        abort(404)
    else:
        attributes["place_id"] = place_id
        new_review = Review(**attributes)
        new_review.save()
        return jsonify(new_review.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=["PUT"],
                 strict_slashes=False)
def put_place_review(review_id):
    """ Updates a review object based on the review id """
    new_attributes = request.get_json(silent=True)
    review_obj = storage.get(Review, review_id)

    if not new_attributes:
        abort(404, description="Not a JSON")
    if review_obj is None:
        abort(404)

    new_attributes.pop('id', None)
    new_attributes.pop('updated_at', None)
    new_attributes.pop('created_at', None)

    for key, value in new_attributes.items():
        setattr(review_obj, key, value)
    review_obj.save()
    return jsonify(review_obj.to_dict()), 200
