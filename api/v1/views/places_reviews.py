#!/usr/bin/python3
""" a new view for Review """
from api.v1.views import app_views
from models.place import Place
from models.review import Review
from models.user import User
from models import storage
from flask import request, jsonify, abort


@app_views.route(
    "/places/<place_id>/reviews", methods=["GET"], strict_slashes=False)
def get_review(place_id):
    """ retrieve all Review objects """
    places = storage.get(Place, place_id)
    if not places:
        abort(404)
    all_reviews = storage.all(Review)
    place_list = []
    for value in all_reviews.values():
        if value.place_id == places.id:
            place_list.append(value.to_dict())
    return jsonify(place_list)


@app_views.route(
    "/reviews/<review_id>", methods=["GET"], strict_slashes=False)
def get_review_id(review_id):
    """ retrieve a single Review object """
    obj = storage.get(Review, review_id)
    if not obj:
        abort(404)
    return jsonify(obj.to_dict())


@app_views.route(
    "/reviews/<review_id>", methods=["DELETE"], strict_slashes=False)
def delete_review(review_id):
    """ delete a single Review object """
    obj = storage.get(Review, review_id)
    if not obj:
        abort(404)
    storage.delete(obj)
    storage.save()
    return jsonify({}), 200


@app_views.route(
    "/places/<place_id>/reviews", methods=["POST"], strict_slashes=False)
def new_review(place_id):
    """ add a new Review object """
    if not request.is_json:
        abort(400)
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    body = request.get_json()
    if not body:
        abort(400, "Not a JSON")
    if "user_id" not in body:
        abort(400, "Missing user_id")
    user = storage.get(User, body["user_id"])
    if not user:
        abort(404)
    if "text" not in body:
        abort(400, "Missing text")
    new_reviews = Review()
    for key, value in body.items():
        setattr(new_reviews, key, value)
    storage.new(new_reviews)
    storage.save()
    return jsonify(new_reviews.to_dict()), 201


@app_views.route(
    "/reviews/<review_id>", methods=["PUT"], strict_slashes=False)
def update_review(review_id):
    """ update a Review object """
    if not request.is_json:
        abort(400)
    obj = storage.get(Review, review_id)
    if not obj:
        abort(404)
    body = request.get_json()
    if not body:
        abort(400, "Not a JSON")
    for ke, value in body.items():
        if ke not in ["id", "user_id", "place_id", "created_at", "updated_at"]:
            setattr(obj, ke, value)
    storage.save()
    return jsonify(obj.to_dict()), 200
