#!/usr/bin/python3
"""This module starts a simple flask app
"""
from flask import Flask
from models import Storage
from api.v1.views import app_views

app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown_app(e):
    """Close SQLAlchemy session or reload file storage session """


storage.close()


if __name__ == "__main__":
    app.run(HBNB_API_HOST='0.0.0.0', port=5000, threaded=True)
