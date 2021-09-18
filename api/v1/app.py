#!/usr/bin/python3
"""

"""
from api.v1.views import app_views
from models import storage
from flask import Flask, make_response
from flask.json import jsonify

HBNB_API_HOST = '0.0.0.0'
HBNB_API_PORT = '5000'

app = Flask(__name__)
app.register_blueprint(app_views, url_prefix="/api/v1")

@app.teardown_appcontext
def teardown():
    """  """
    storage.close()

@app.errorhandler(404)
def page_not_found(error):
    """ handler for 404 errors """
    return make_response(jsonify({"error": "Not found"}), 404)


if __name__ == "__name__":
    app.run(host=HBNB_API_HOST, port=HBNB_API_PORT, threaded=True)
