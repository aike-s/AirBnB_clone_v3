#!/usr/bin/python3
"""
Route functions
"""
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from flask import jsonify
from api.v1.views import app_views
from models import storage

@app_views.route('/status', strict_slashes=False)
def status():
    """ Return the status """
    status = jsonify({'status': 'OK'})

    return status


@app_views.route('/stats', strict_slashes=False)
def num_each_dict_num_objs():
    """ Return a dict with the num of objects in a class """

    dict_num_objs = {"amenities": storage.count(Amenity),
                     "cities": storage.count(City),
                     "reviews": storage.count(Review),
                     "states": storage.count(State),
                     "users": storage.count(User),
                     "places": storage.count(Place)}

    return jsonify(dict_num_objs)
