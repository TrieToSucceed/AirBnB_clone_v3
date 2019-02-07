#!/usr/bin/python3
""" module that handles all default RestFul API actions
"""

from models.amenity import Amenity
from models import storage
from api.v1.views import app_views
from flask import jsonify, abort, request
from os import getenv


@app_views.route("/places/<place_id>/amenities",
                   strict_slashes=False,
                   methods=['GET'])
def get_place_amenity(place_id):
    """list all amenity objects of a place"""
    objs = storage.get("Place", place_id)
    if not obj:
        abort(404)
    amenity_objs = obj.amenities
    return jsonify([amenity.to_dict() for amenity in amenity_obj])

'''
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
'''

@app_views.route("/places/<place_id>/amenities/<amenity_id>",
                 strict_slashes=False,
                 methods=['POST'])
def post_place_amenity(place_id, amenity_id):
    """create amenity instance"""
    place_obj = storage.get("Place", place_id)
    if not place_obj:
        abort(404)
    amenity_obj = storage.get("Amenity", amenity_id)
    if not amenity_obj:
        abort(404)
    if getenv("HBNB_TYPE_STORAGE") == "db":
        if amenity_obj in place_obj.amenities:
            return jsonify(amenity_obj.to_dict()), 200
        else:
            place_obj.amenities.append(amenity_obj)
            storage.save()
            return jsonify(amenity_obj.to_dict()), 201
    else:
        if amenity_id in place_obj.amenity_ids:
            return jsonify(amenity_obj.to_dict()), 200
        else:
            place_obj.amenity_ids.append(amenity_obj)
            storage.save()
            return jsonify(amenity_obj.to_dict()), 201

'''
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
'''
