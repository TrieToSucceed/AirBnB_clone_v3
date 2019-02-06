#!/usr/bin/python3
""" module that handles all default RestFul API actions
"""

from models.amenity import Amenity
from models import storage
from api.v1.views import app_views
from flask import jsonify, abort, request


@app_views.route("/amenities", strict_slashes=False)
def get_amenities():
    """ get all amenities objects """
    objs = storage.all("Amenity")
    return jsonify([obj.to_dict() for obj in objs.values()])


@app_views.route("/amenities/<amenity_id>",
                 strict_slashes=False,
                 methods=['GET'])
def get_amenity(amenity_id):
    """ get amenity object """
    obj = storage.get("Amenity", amenity_id)
    if obj:
        return jsonify(obj.to_dict())
    abort(404)


@app_views.route("/amenities/<amenity_id>",
                 strict_slashes=False,
                 methods=['DELETE'])
def delete_amenity(amenity_id):
    """delete amenity object"""
    obj = storage.get("Amenity", amenity_id)
    if obj:
        obj.delete()
        return jsonify({}), 200
    abort(404)


@app_views.route("/amenities", strict_slashes=False, methods=['POST'])
def post_amenity():
    """create amenity instance"""
    request_dict = request.get_json()
    if not request_dict:
        abort(400, jsonify({"message": "Not a JSON"}))
    if "name" not in request_dict:
        abort(400, jsonify({"message": "Missing name"}))
    obj = Amenity(**request_dict)
    obj.save()
    return jsonify(obj.to_dict()), 201


@app_views.route("/amenities/<amenity_id>",
                 strict_slashes=False,
                 methods=['PUT'])
def put_amenity(amenity_id):
    """update amenity object"""
    obj = storage.get("Amenity", amenity_id)
    if not obj:
        abort(404)
    request_dict = request.get_json()
    if not request_dict:
        abort(400, jsonify({"message": "Not a JSON"}))
    for key, value in request_dict.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(obj, key, value)
    obj.save()
    return jsonify(obj.to_dict()), 200
