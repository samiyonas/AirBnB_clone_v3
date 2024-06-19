#!/usr/bin/python3
""" route for the blueprint app_views """
from api.v1.views import app_views
from flask import jsonify


@app_views.route("/status")
def index():
    """ status route """
    return jsonify({"status": "OK"})
