#!/usr/bin/env python3
"""
Basic Flask app
"""

from flask import Flask, request, jsonify
from auth import Auth
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound

app = Flask(__name__)

AUTH = Auth()


@app.route("/", methods=["GET"])
def home():
    """Home route that returns a welcome message."""
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=["POST"])
def users():
    """Endpoint to register a user."""
    email = request.form.get("email")
    password = request.form.get("password")

    if not email or not password:
        return jsonify({"message": "email and password required"}), 400

    try:
        user = AUTH.register_user(email, password)
        return jsonify({"email": user.email, "message": "user created"}), 200
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
