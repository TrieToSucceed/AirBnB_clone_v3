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
    obj = storage.get("Place", place_id)
    if not obj:
        abort(404)
    amenity_objs = obj.amenities
    return jsonify([amenity.to_dict() for amenity in amenity_objs])


@app_views.route("/places/<place_id>/amenities/<amenity_id>",
                 strict_slashes=False,
                 methods=['DELETE'])
def delete_place_amenity(place_id, amenity_id):
    """delete amenity object by place"""
    place_obj = storage.get("Place", place_id)
    if not place_obj:
        abort(404)
    amenity_obj = storage.get("Amenity", amenity_id)
    if not amenity_obj:
        abort(404)
    if getenv("HBNB_TYPE_STORAGE") == "db":
        if amenity_obj not in place_obj.amenities:
            abort(404)
        else:
            place_obj.amenities.remove(amenity_obj)
            storage.save()
            return jsonify({}), 200
    else:
        if amenity_obj not in place_obj.amenity_ids:
            abort(404)
        else:
            place_obj.amenity_ids.remove(amenity_id)
            storage.save()
            return jsonify({}), 200


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
            place_obj.amenity_ids.append(amenity_id)
            storage.save()
            return jsonify(amenity_obj.to_dict()), 201
