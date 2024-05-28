#!/usr/bin/env python3
"""
Basic Flask app
"""

from flask import Flask, request, jsonify, make_response, abort, redirect
from auth import Auth
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound
from werkzeug.security import check_password_hash
import uuid
import logging


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

    logging.debug(f"Attempting login for email: {email}")

    try:
        if not AUTH.valid_login(email, password):
            logging.debug(f"Invalid login for email: {email}")
            abort(401)

        session_id = AUTH.create_session(email)
        if not session_id:
            logging.debug(f"Failed to create session for email: {email}")
            abort(401)

        logging.debug(f"Login successful for email: {email}, session_id: {session_id}")
        response = make_response(jsonify({"email": email, "message": "logged in"}))
        response.set_cookie('session_id', session_id)
        return response
    except Exception as e:
        logging.error(f"Error during login for email: {email}: {e}")
        abort(500)


@app.route("/sessions", methods=["DELETE"])
def logout():
    """Endpoint to log out a user and destroy the session."""
    session_id = request.cookies.get('session_id')

    user = AUTH.get_user_from_session_id(session_id)
    if user:
        AUTH.destroy_session(user.id)
        response = make_response(redirect("/"))
        response.delete_cookie('session_id')
        return response
    else:
        abort(403)


@app.route("/profile", methods=["GET"])
def profile():
    """Endpoint to retrieve user profile."""
    session_id = request.cookies.get('session_id')

    user = AUTH.get_user_from_session_id(session_id)
    if user:
        return jsonify({"email": user.email}), 200
    else:
        abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
