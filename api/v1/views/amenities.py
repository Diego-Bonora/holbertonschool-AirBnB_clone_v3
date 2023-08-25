#!/usr/bin/python3
""" view for amenities """
from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities/', methods=["GET"])
@app_views.route("/amenities/<amenity_id>", methods=["GET"])
def list_amenities(amenity_id=None):
    """ lists all the amenities or just one """
    if amenity_id:
        amenities = storage.get(Amenity, amenity_id)
        if not amenities:
            abort(404)
    else:
        amenities = []
        all_amenities = storage.all(Amenity)
        for value in all_amenities.values():
            amenities.append(value.to_dict())
    return jsonify(amenities)


@app_views.route("/amenities/<amenity_id>", methods=["DELETE"])
def delete_amenity(amenity_id):
    """ deletes a specific amenity """
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    storage.delete(amenity)
    storage.save()
    return jsonify({}), 200


@app_views.route("/amenities/", methods=["POST"])
def create_amenity():
    """ creates a new amenity """
    json_data = request.get_json()
    if not json_data:
        return jsonify("Not a JSON"), 400
    elif "name" not in json_data:
        return jsonify("Missing name"), 400
    else:
        new_amenity = Amenity()
        new_amenity.name = json_data["name"]
        storage.new(new_amenity)
        storage.save()
        return jsonify(new_amenity.to_dict()), 201


@app_views.route("/amenities/<amenity_id>", methods=["PUT"])
def update_amenity(amenity_id):
    """ updates a amenity """
    json_data = request.get_json()
    if not json_data:
        return jsonify({"error": "Not a JSON"}), 400

    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)

    not_for_change = ["id", "created_at", "updated_at"]
    for key, value in json_data.items():
        if key not in not_for_change:
            setattr(amenity, key, value)
    storage.save()
    return jsonify(amenity.to_dict()), 200
