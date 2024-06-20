#!/usr/bin/python3
""" crud operations on cities """
from flask import request, jsonify, abort
from api.v1.views import app_views
from models import storage
from models.state import State
from models.city import City


@app_views.route(
    "/states/<state_id>/cities", methods=["GET"], strict_slashes=False)
def get_city(state_id):
    """ retrieve the list of all City objects of a state """
    obj = storage.get(State, state_id)
    if not obj:
        abort(404)
    match = []
    cities = storage.all(City)
    for value in cities.values():
        if value.state_id == obj.id:
            match.append(value.to_dict())
    match = jsonify(match)
    return match


@app_views.route(
    "/cities/<city_id>", methods=["GET"], strict_slashes=False)
def get_city_id(city_id):
    """ retrieve a city object by city id"""
    obj = storage.get(City, city_id)
    if not obj:
        abort(404)
    obj = jsonify(obj.to_dict())
    return obj


@app_views.route(
    "/cities/<city_id>", methods=["DELETE"], strict_slashes=False)
def delete_city(city_id):
    """ delete a city object """
    obj = storage.get(City, city_id)
    if not obj:
        abort(404)
    storage.delete(obj)
    storage.save()
    res = jsonify({})
    res.status_code = 200
    return res


@app_views.route(
    "/states/<state_id>/cities", methods=["POST"], strict_slashes=False)
def new_obj(state_id):
    """ add a new object through a post request """
    if not request.is_json:
        abort(400)
    body = request.get_json()
    if not body:
        abort(400, "Not a JSON")
    if "name" not in body:
        abort(400, "Missing name")
    obj = storage.get(State, state_id)
    if not obj:
        abort(404)
    new_city = City(name=body["name"])
    new_city.state_id = state_id
    storage.new(new_city)
    storage.save()
    new_city = jsonify(new_city.to_dict())
    new_city.status_code = 200
    return new_city


@app_views.route(
    "/cities/<city_id>", methods=["PUT"], strict_slashes=False)
def update_obj(city_id):
    """ update existing City object """
    if not request.is_json:
        abort(400)
    body = request.get_json()
    if not body:
        abort(400, "Not a JSON")
    obj = storage.get(City, city_id)
    if not obj:
        abort(404)
    obj.name = body["name"]
    storage.save()
    obj = jsonify(obj.to_dict())
    obj.status_code = 200
    return obj
