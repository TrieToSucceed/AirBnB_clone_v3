#!/usr/bin/python3
"""
Index file of app
"""
from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route("/status", strict_slashes=False)
def status():
    """returns a JSON: "status": "OK"""
    return jsonify({"status": "OK"})


@app_views.route("/stats", strict_slashes=False)
def stats():
    """retrieves the number of each objects by type
    """
    cls_list = ["Amenity", "City", "Place",
                "Review", "State", "User"]
    cls_output = ["amenities", "cities", "places",
                  "reviews", "states", "users"]
    cls_count = {}
    for index in range(len(cls_list)):
        cls_count[cls_output[index]] = storage.count(cls_list[index])
    return jsonify(cls_count)
