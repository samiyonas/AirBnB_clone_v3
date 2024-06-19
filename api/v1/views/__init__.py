#!/usr/bin/python3
"""one of the blueprints of our flask api"""
from flask import Blueprint


app_views = Blueprint("app_views", __name__, url_prefix="/api/v1")
