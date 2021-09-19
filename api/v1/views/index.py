#!/usr/bin/python3
"""

"""
HBNB_API_HOST = '0.0.0.0'
HBNB_API_PORT = '5000'

""" Every class """
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User

""" Necesary tools """
from flask.json import jsonify
from api.v1.views import app_views
from models import storage


@app_views.route('/status', strict_slashes=False)
def status():
    """  """
    status = jsonify({'status': 'OK'})

    return status

@app_views.route('/stats', strict_slashes=False)
def num_each_dict_num_objs():
    """  """

    classes = {"Amenity": Amenity, "City": City, "Place": Place,
               "Review": Review, "State": State, "User": User}

    dict_num_objs = {}

    for key, value in classes.items():
        num_objs = storage.count(value)
        class_name = key.lower()
        dict_num_objs[class_name] = num_objs

    return jsonify(dict_num_objs)
