#!/usr/bin/python3
""" the api flask app"""
from os import getenv, environ
from flask import Flask
from models import storage
from api.v1.views import app_views


app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def close_session(exception):
    storage.close()


if __name__ == "__main__":
    host = getenv("HBNB_API_HOST") if "HBNB_API_HOST" in environ else "0.0.0.0"
    port = getenv("HBNB_API_PORT") if "HBNB_API_PORT" in environ else 5000
    app.run(host=host, port=port, threaded=True)
