#!/usr/bin/python3
""" a new view for State objects """
from api.v1.views import app_views
from models.state import State
from models import storage
from flask import jsonify, abort, request


@app_views.route("/states", methods=["GET"], strict_slashes=False)
def get_states():
    """ retrieve the list of all State object"""
    response = storage.all(State)
    res = []
    for value in response.values():
        res.append(value.to_dict())
    return jsonify(res)


@app_views.route("/states/<state_id>", methods=["GET"], strict_slashes=False)
def get_states_id(state_id):
    """ get a state with the specific ID """
    response = storage.get(State, state_id)
    try:
        response = response.to_dict()
    except Exception:
        abort(404)
    return jsonify(response)


@app_views.route(
    "/states/<state_id>", methods=["DELETE"], strict_slashes=False)
def delete_states(state_id):
    """ delete a state object """
    response = storage.get(State, state_id)
    if not response:
        abort(404)
    storage.delete(response)
    storage.save()
    res = jsonify({})
    res.status_code = 200
    return res


@app_views.route("/states", methods=["POST"], strict_slashes=False)
def new_state():
    """ adding a new object to our database """
    if not request.is_json:
        abort(400)
    post = request.get_json()
    if not post:
        abort(400, "Not a JSON")
    if "name" not in post:
        abort(400, "Missing name")
    newObj = State(name=post["name"])
    storage.new(newObj)
    storage.save()
    newObj = jsonify(newObj.to_dict())
    newObj.status_code = 201
    return newObj


@app_views.route("/states/<state_id>", methods=["PUT"])
def update_state(state_id):
    """ update a state object """
    if not request.is_json:
        abort(400)
    put = request.get_json()
    if not put:
        abort(400, "Not a JSON")
    obj = storage.get(State, state_id)
    if not obj:
        abort(404)
    obj.name = put["name"]
    storage.save()
    res = jsonify(obj.to_dict())
    res.status_code = 200
    return res
