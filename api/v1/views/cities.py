#!/usr/bin/python3
""" view for Citys """
from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.city import City
from models.state import State


@app_views.route("states/<state_id>/cities", methods=["GET"])
def list_cities_by_state(state_id):
    """ lists all the Citys or just one """
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    cities = []
    for city in state.cities:
        cities.append(city.to_dict())
    return jsonify(cities)


@app_views.route("/cities/<city_id>", methods=["GET"])
def list_city(city_id):
    """ lists all the states or just one """
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route("/cities/<city_id>", methods=["DELETE"])
def delete_city(city_id):
    """ deletes a specific City """
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    storage.delete(city)
    storage.save()
    return jsonify({}), 200


@app_views.route("/states/<state_id>/cities", methods=["POST"])
def create_city(state_id):
    """ creates a new City """
    json_data = request.get_json()
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    if not json_data:
        return jsonify("Not a JSON"), 400
    elif "name" not in json_data:
        return jsonify("Missing name"), 400
    else:
        new_City = City()
        new_City.name = json_data["name"]
        new_City.state_id = state.id
        storage.new(new_City)
        storage.save()
        return jsonify(new_City.to_dict()), 201


@app_views.route("/cities/<city_id>", methods=["PUT"])
def update_city(city_id):
    """ updates a City """
    json_data = request.get_json()
    if not json_data:
        return jsonify({"error": "Not a JSON"}), 400

    city = storage.get(City, city_id)
    if not city or not city_id:
        abort(404)

    not_for_change = ["id", "created_at", "updated_at", "state_id"]
    for key, value in json_data.items():
        if key not in not_for_change:
            setattr(City, key, value)
    storage.save()
    return jsonify(City.to_dict()), 200
