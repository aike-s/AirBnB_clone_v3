#!/usr/bin/python3
"""

"""
HBNB_API_HOST = '0.0.0.0'
HBNB_API_PORT = '5000'

from flask.json import jsonify
from api.v1.views import app_views
from models import storage


@app_views.route('/status', strict_slashes=False)
def status():
    """  """
    status = jsonify({'status': ' '})

    return status

@app_views.route('/stats', strict_slashes=False)
def num_each_objs():
    """  """
    objs = {"amenities": 0, "cities": 0, "places": 0,
            "reviews": 0, "states": 0, "users": 0}

    for type_obj in objs.keys():
        num_objs = len(storage.all(type_obj).keys)
        objs[type_obj] = num_objs

    return jsonify(objs)

if __name__ == "__name__":
    app_views.run(host=HBNB_API_HOST, port=HBNB_API_PORT, threaded=True)
