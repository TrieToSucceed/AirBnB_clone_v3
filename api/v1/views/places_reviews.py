#!/usr/bin/python3
""" module that handles all default RestFul API actions
"""

from models.review import Review
from models import storage
from api.v1.views import app_views
from flask import jsonify, abort, request


@app_views.route("/reviews", strict_slashes=False, methods=['GET'])
def get_reviews():
    """ get all review objects """
    objs = storage.all("Review")
    return jsonify([obj.to_dict() for obj in objs.values()])


@app_views.route("/places/<place_id>/reviews",
                 strict_slashes=False,
                 methods=['GET'])
def get_review_by_place(place_id):
    """ get all place objects given a state"""
    obj = storage.get("Place", place_id)
    if not obj:
        abort(404)
    review_objs = obj.reviews
    return jsonify([review.to_dict() for review in review_objs])


@app_views.route("/reviews/<review_id>", strict_slashes=False, methods=['GET'])
def get_review(review_id):
    """ get review object """
    obj = storage.get("Review", review_id)
    if obj:
        return jsonify(obj.to_dict())
    abort(404)


@app_views.route("/reviews/<review_id>",
                 strict_slashes=False,
                 methods=['DELETE'])
def delete_review(review_id):
    """delete review object"""
    obj = storage.get("Review", review_id)
    if obj:
        obj.delete()
        return jsonify({}), 200
    abort(404)


@app_views.route("/places/<place_id>/reviews",
                 strict_slashes=False,
                 methods=['POST'])
def post_review(place_id):
    """create review instance"""
    if not storage.get("Place", place_id):
        abort(404)
    request_dict = request.get_json()
    if not request_dict:
        abort(400, jsonify({'message': 'Not a JSON'}))
    if 'user_id' not in request_dict:
        abort(400, jsonify({'message': 'Missing user_id'}))
    if not storage.get("User", request_dict['user_id']):
        abort(404)
    if 'text' not in request_dict:
        abort(400, jsonify({'message': 'Missing text'}))
    obj = Review(**request_dict)
    obj.place_id = place_id
    obj.save()
    return jsonify(obj.to_dict()), 201


@app_views.route("/reviews/<review_id>", strict_slashes=False, methods=['PUT'])
def put_review(review_id):
    """update review object"""
    obj = storage.get("Review", review_id)
    if not obj:
        abort(404)
    request_dict = request.get_json()
    if not request_dict:
        abort(400, jsonify({'message': 'Not a JSON'}))
    for key, value in request_dict.items():
        if key not in ['id', 'user_id', 'place_id',
                       'created_at', 'updated_at']:
            setattr(obj, key, value)
    obj.save()
    return jsonify(obj.to_dict()), 200
