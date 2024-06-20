#!/usr/bin/python3
""" routes for users """
from api.v1.views import app_views
from models.user import User
from models import storage
from flask import request, jsonify, abort


@app_views.route(
    "/users", methods=["GET"], strict_slashes=False)
def get_user():
    """ retrieve the list of all User objects """
    objs = storage.all(User)
    resp = []
    for value in objs.values():
        resp.append(value.to_dict())
    resp = jsonify(resp)
    return resp


@app_views.route(
    "/users/<user_id>", methods=["GET"], strict_slashes=False)
def get_user_id(user_id):
    """ retrieve a single User object """
    obj = storage.get(User, user_id)
    if not obj:
        abort(404)
    obj = jsonify(obj.to_dict())
    return obj


@app_views.route(
    "/users/<user_id>", methods=["DELETE"], strict_slashes=False)
def delete_user(user_id):
    """ delete a single User object """
    obj = storage.get(User, user_id)
    if not obj:
        abort(404)
    storage.delete(obj)
    storage.save()
    res = jsonify({})
    res.status_code = 200
    return res


@app_views.route(
    "/users", methods=["POST"], strict_slashes=False)
def new_user():
    """ add a new User object """
    if not request.is_json:
        abort(400)
    body = request.get_json()
    if not body:
        abort(400, "Not a JSON")
    if "email" not in body:
        abort(400, "Missing email")
    if "password" not in body:
        abort(400, "Missing password")
    new_obj = User()
    for key, value in body.items():
        setattr(new_obj, key, value)
    storage.new(new_obj)
    storage.save()
    new_obj = jsonify(new_obj.to_dict())
    new_obj.status_code = 201
    return new_obj


@app_views.route(
    "/users/<user_id>", methods=["PUT"], strict_slashes=False)
def update_user(user_id):
    """ update a User object """
    if not request.is_json:
        abort(400)
    body = request.get_json()
    if not body:
        abort(400, "Not a JSON")
    obj = storage.get(User, user_id)
    if not obj:
        abort(404)
    for key, value in body.items():
        if key not in ["id", "email", "created_at", "updated_at"]:
            setattr(obj, key, value)
    storage.save()
    obj = jsonify(obj.to_dict())
    obj.status_code = 200
    return obj
