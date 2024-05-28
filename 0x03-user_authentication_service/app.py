#!/usr/bin/env python3
"""
Basic Flask app
"""

from flask import Flask, request, jsonify, make_response, abort
from auth import Auth
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound
from werkzeug.security import check_password_hash
import uuid


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
    

@app.route("/sessions", methods=["POST"])
def login():
    """Endpoint to log in a user and create a new session."""
    email = request.form.get('email')
    password = request.form.get('password')

    if not email or not password:
        abort(401)

    try:
        user = AUTH.get_user(email)
    except NoResultFound:
        abort(401)

    if not check_password_hash(user.hashed_password, password):
        abort(401)

    session_id = str(uuid.uuid4())
    user.session_id = session_id
    AUTH.update_user(user.id, session_id=session_id)

    response = make_response(jsonify({"email": email, "message": "logged in"}))
    response.set_cookie('session_id', session_id)
    return response


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
