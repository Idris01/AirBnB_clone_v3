#!/usr/bin/python3
from api.v1.views import app_views
from models import storage

@app_views.route("/status", strict_slashes=False)
  def status():
      """ Returns JSON """
      return jsonify(status: "OK")
