#!/usr/bin/python3
""" routes for Amenity """
from api.v1.views import app_views
from models.amenity import Amenity
from models import storage
from flask import request, jsonify, abort


@app_views.route(
    "/amenities", methods=["GET"], strict_slashes=False)
def get_amenities():
    """ retrieve list of all Amenity objects """
    amenities = storage.all(Amenity)
    objs = []
    for value in amenities.values():
        objs.append(value.to_dict())
    obj = jsonify(objs)
    return obj


@app_views.route(
    "/amenities/<amenity_id>", methods=["GET"], strict_slashes=False)
def get_amenity_id(amenity_id):
    """ retrieve object by ID """
    obj = storage.get(Amenity, amenity_id)
    if not obj:
        abort(404)
    obj = jsonify(obj.to_dict())
    return obj


@app_views.route(
    "/amenities/<amenity_id>", methods=["DELETE"], strict_slashes=False)
def delete_amenity(amenity_id):
    """ delete a specific amenity object """
    obj = storage.get(Amenity, amenity_id)
    if not obj:
        abort(404)
    storage.delete(obj)
    storage.save()
    obj = jsonify({})
    obj.status_code = 200
    return obj


@app_views.route(
    "/amenities", methods=["POST"], strict_slashes=False)
def new_amenity():
    """ add a new object """
    if request.is_json:
        abort(400)
    body = request.get_json()
    if not body:
        abort(400, "Not JSON")
    if "name" not in body:
        abort(400, "Missing name")
    obj = Amenity(name=body["name"])
    storage.new(obj)
    storage.save()
    obj = jsonify(obj.to_dict())
    obj.status_code = 201
    return obj


@app_views.route(
    "/amenities/<amenity_id>", methods=["PUT"], strict_slashes=False)
def update_amenity(amenity_id):
    """ update amenity object """
    if not request.is_json:
        abort(400)
    body = request.get_json()
    if not body:
        abort(400, "Not a JSON")
    obj = storage.get(Amenity, amenity_id)
    if not obj:
        abort(404)
    obj.name = body["name"]
    storage.save()
    obj = jsonify(obj.to_dict())
    obj.status_code = 200
    return obj
