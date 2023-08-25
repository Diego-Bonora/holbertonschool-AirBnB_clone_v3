#!/usr/bin/python3
""" view for reviews """
from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.review import Review
from models.place import Place
from models.user import User


@app_views.route("/places/<place_id>/reviews", methods=["GET"])
def list_reviews_by_place(place_id):
    """ lists all the reviews or just one """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    reviews = []
    for review in place.reviews:
        reviews.append(review.to_dict())
    return jsonify(reviews)


@app_views.route("/reviews/<review_id>", methods=["GET"])
def list_review(review_id):
    """ lists all the places or just one """
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route("/reviews/<review_id>", methods=["DELETE"])
def delete_review(review_id):
    """ deletes a specific review """
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    storage.delete(review)
    storage.save()
    return jsonify({}), 200


@app_views.route("/places/<place_id>/reviews", methods=["POST"],
                 strict_slashes=False)
def create_review(place_id):
    """ creates a new review """
    json_data = request.get_json()
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    if not json_data:
        return jsonify("Not a JSON"), 400
    elif "user_id" not in json_data:
        return jsonify("Missing user_id"), 400
    elif "text" not in json_data:
        return jsonify("Missing text"), 400
    else:
        user = storage(User, json_data["user_id"])
        if not user:
            abort(404)
        new_review = Review()
        new_review.user_id = user.id
        new_review.text = json_data["text"]
        new_review.place_id = place.id
        storage.new(new_review)
        storage.save()
        return jsonify(new_review.to_dict()), 201


@app_views.route("/reviews/<review_id>", methods=["PUT"])
def update_review(review_id):
    """ updates a review """
    json_data = request.get_json()
    if not json_data:
        return jsonify({"error": "Not a JSON"}), 400

    review = storage.get(Review, review_id)
    if not review or not review_id:
        abort(404)

    not_for_change = ["id", "created_at", "updated_at", "place_id", "user_id"]
    for key, value in json_data.items():
        if key not in not_for_change:
            setattr(review, key, value)
    storage.save()
    return jsonify(review.to_dict()), 200
