#!/usr/bin/python3
from flask import jsonify
from flask import Blueprint

app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')


@app_views.route("/status", strict_slashes=False)
def status():
    """ Returns JSON """
    return jsonify(status="OK")
