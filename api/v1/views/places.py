#!/usr/bin/python3
""" routes for places """
from api.v1.views import app_views
from models.place import Place
from models.city import City
from models.user import User
from models import storage
from flask import request, jsonify, abort


@app_views.route(
    "/cities/<city_id>/places", methods=["GET"], strict_slashes=False)
def get_place(city_id):
    """ retrieve the list of all place objects """
    city_obj = storage.get(City, city_id)
    if not city_obj:
        abort(404)
    place_obj = storage.all(Place)
    places = []
    for value in place_obj.values():
        if value.city_id == city_obj.id:
            places.append(value.to_dict())
    places = jsonify(places)
    return places


@app_views.route(
    "/places/<place_id>", methods=["GET"], strict_slashes=False)
def get_place_id(place_id):
    """ retrieve a single Place object """
    obj = storage.get(Place, place_id)
    if not obj:
        abort(404)
    obj = jsonify(obj.to_dict())
    return obj


@app_views.route(
    "/places/<place_id>", methods=["DELETE"], strict_slashes=False)
def delete_place(place_id):
    """ delete a Place object """
    obj = storage.get(Place, place_id)
    if not obj:
        abort(404)
    storage.delete(obj)
    storage.save()
    return jsonify({}), 200


@app_views.route(
    "/cities/<city_id>/places", methods=["POST"], strict_slashes=False)
def new_place(city_id):
    """ new Place object """
    if not request.is_json:
        abort(400)
    city_obj = storage.get(City, city_id)
    if not city_obj:
        abort(404)
    body = request.get_json()
    if not body:
        abort(400, "Not a JSON")
    if "user_id" not in body:
        abort(400, "Missing user_id")
    user_obj = storage.get(User, body["user_id"])
    if not user_obj:
        abort(404)
    if "name" not in body:
        abort(400, "Missing name")
    place = Place()
    for key, value in body.items():
        setattr(place, key, value)
    return jsonify(place.to_dict()), 201


@app_views.route(
    "/places/<place_id>", methods=["PUT"], strict_slashes=False)
def update_place(place_id):
    """ update Place object """
    if not request.is_json:
        abort(400)
    obj = storage.get(Place, place_id)
    if not obj:
        abort(404)
    body = request.get_json()
    if not body:
        abort(400, "Not a JSON")
    for key, value in body.items():
        if key not in ["id", "user_id", "city_id", "created_at", "updated_at"]:
            setattr(obj, key, value)
    storage.save()
    return jsonify(obj.to_dict()), 200
