#!/usr/bin/python3
""" view for users """
from flask import jsonify, abort, request, Flask
from api.v1.views import app_views
from models import storage
from models.place import Place
from models.city import City
from models.user import User


@app_views.route("/cities/<city_id>/places", methods=["GET"],
                 strict_slashes=False)
def list_place_from_city(city_id):
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    places = []
    all_places = storage.all(Place)
    for value in all_places.values():
        if value.city_id == city.id:
            places.append(value.to_dict())
    return jsonify(places)


@app_views.route("/places/<place_id>", methods=["GET"],
                 strict_slashes=False)
def get_place(place_id):
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route("places/<place_id>", methods=["DELETE"],
                 strict_slashes=False)
def delete_place(place_id):
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    storage.delete(place)
    storage.save()
    return jsonify({}), 200


@app_views.route("cities/<city_id>/places", methods=["POST"],
                 strict_slashes=False)
def create_place(city_id):
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    json_data = request.get_json()
    if not json_data:
        return jsonify("Not a JSON"), 400
    elif "user_id" not in json_data:
        return jsonify("Missing user_id"), 400
    elif "name" not in json_data:
        return jsonify("Missing name"), 400
    else:
        user = storage.get(User, json_data["user_id"])
        if not user:
            abort(404)
        new_place = Place()
        new_place.city_id = city.id
        new_place.user_id = user.id
        new_place.name = json_data["name"]
        storage.new(new_place)
        storage.save()
        return jsonify(new_place.to_dict()), 201


@app_views.route("/places/<place_id>", methods=["PUT"],
                 strict_slashes=False)
def update_user(place_id):
    """ updates a user """
    json_data = request.get_json()
    if not json_data:
        return jsonify({"error": "Not a JSON"}), 400

    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    not_for_change = ["id", "created_at", "updated_at", "user_id", "city_id"]
    for key, value in json_data.items():
        if key not in not_for_change:
            setattr(place, key, value)
    storage.save()
    return jsonify(place.to_dict()), 200
