#!/usr/bin/python3
""" view for states """
from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.state import State


@app_views.route('/states/', methods=["GET"], strict_slashes=False)
@app_views.route("/states/<state_id>", methods=["GET"], strict_slashes=False)
def list_states(state_id=None):
    """ lists all the states or just one """
    if state_id:
        states = storage.get(State, state_id)
        if not states:
            abort(404)
        else:
            states = states.to_dict()
    else:
        states = []
        all_states = storage.all(State)
        for value in all_states.values():
            states.append(value.to_dict())
    return jsonify(states)


@app_views.route("/states/<state_id>", methods=["DELETE"],
                 strict_slashes=False)
def delete_state(state_id):
    """ deletes a specific state """
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    storage.delete(state)
    storage.save()
    return jsonify({}), 200


@app_views.route("/states/", methods=["POST"], strict_slashes=False)
def create_state():
    """ creates a new state """
    json_data = request.get_json()
    if not json_data:
        return jsonify("Not a JSON"), 400
    elif "name" not in json_data:
        return jsonify("Missing name"), 400
    else:
        new_state = State()
        new_state.name = json_data["name"]
        storage.new(new_state)
        storage.save()
        return jsonify(new_state.to_dict()), 201


@app_views.route("/states/<state_id>", methods=["PUT"], strict_slashes=False)
def update_state(state_id):
    """ updates a state """
    json_data = request.get_json()
    if not json_data:
        return jsonify({"error": "Not a JSON"}), 400

    state = storage.get(State, state_id)
    if not state:
        abort(404)

    not_for_change = ["id", "created_at", "updated_at"]
    for key, value in json_data.items():
        if key not in not_for_change:
            setattr(state, key, value)
    storage.save()
    return jsonify(state.to_dict()), 200
