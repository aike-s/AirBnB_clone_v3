#!/usr/bin/python3
"""
Here runs app with all routes and RESTful API services
"""
from api.v1.views import app_views
from models import storage
from flask import Flask, make_response, jsonify
from os import getenv
from flask_cors import CORS

app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
app.register_blueprint(app_views)
CORS(app, resources={r"/*": {"origins": ["0.0.0.0"]}})


@app.errorhandler(404)
def page_not_found(error):
    """ Handler for 404 errors """
    error_response = {"error": "Not found"}
    return make_response(jsonify(error_response), 404)


@app.teardown_appcontext
def teardown(exception):
    """ Teardown context """
    storage.close()


if __name__ == "__main__":
    """ Runs the app """
    Host = getenv('HBNB_API_HOST', default='0.0.0.0')
    Port = getenv('HBNB_API_PORT', default='5000')

    app.run(host=Host, port=int(Port), threaded=True)
