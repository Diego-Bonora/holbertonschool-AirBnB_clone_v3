#!/usr/bin/python3
""" view for states """
from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.state import State


@app_views.route('/states/', methods=["GET"])
@app_views.route("/states/<state_id>", methods=["GET"])
def list_states(state_id=None):
    """ lists all the states or just one """
    if state_id:
        states = None
        all_states = storage.all(State)
        for value in all_states.values():
            if value.id == state_id:
                states = value.to_dict()
    else:
        states = []
        all_states = storage.all(State)
        for value in all_states.values():
            states.append(value.to_dict())
    if not states:
        abort(404)
    return states


@app_views.route("/states/<state_id>", methods=["DELETE"])
def delete_state(state_id):
    """ deletes a specific state """
    if state_id:
        states = None
        all_states = storage.all(State)
        for value in all_states.values():
            if value.id == state_id:
                states = value
    if not states or not state_id:
        abort(404)
    storage.delete(states)
    storage.save()
    return {}, 200


@app_views.route("/states/", methods=["POST"])
def create_state():
    """ creates a new state """
    json_data = request.get_json()
    if not json_data:
        return jsonify({"error": "Not a JSON"}), 400
    elif "name" in json_data:
        return jsonify({"error": "Missing name"}), 400
    new_state = State()
    new_state.name = json_data["name"]
    storage.new(new_state)
    storage.save()
    return jsonify(new_state.to_dict()), 201


@app_views.route("/states/<state_id>", methods=["PUT"])
def update_state(state_id):
    """ updates a state """
    json_data = request.get_json()
    if not json_data:
        return jsonify({"error": "Not a JSON"}), 400

    if state_id:
        state = None
        all_states = storage.all(State)
        for value in all_states.values():
            if value.id == state_id:
                state = value
    if not state or not state_id:
        abort(404)

    not_for_change = ["id", "created_at", "updated_at"]
    for key, value in json_data.items():
        if key not in not_for_change:
            setattr(state, key, value)
    storage.save()
    return jsonify(state.to_dict()), 200
