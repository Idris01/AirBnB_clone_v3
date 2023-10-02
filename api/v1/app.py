#!/usr/bin/python3
"""This module starts a simple flask app
"""
import os
from flask import Flask
from models import storage
from api.v1.views import app_views

app = Flask(__name__)
app.register_blueprint(app_views)
HBNB_API_HOST = os.getenv(
        "HBNB_API_HOST",
        '0.0.0.0')
HBNB_API_PORT = int(
        os.getenv("HBNB_API_PORT", "5000"))


@app.teardown_appcontext
def teardown_app(e):
    """Close SQLAlchemy session or reload file storage session """
    storage.close()


if __name__ == "__main__":
    app.run(
            host=HBNB_API_HOST,
            port=HBNB_API_PORT,
            threaded=True)
