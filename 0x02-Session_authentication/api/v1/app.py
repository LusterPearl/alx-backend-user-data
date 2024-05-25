#!/usr/bin/env python3
"""
Route module for the API
"""
from os import getenv
from api.v1.views import app_views
from flask import Flask, jsonify, request, abort
from flask_cors import CORS
from api.v1.auth.auth import Auth
from api.v1.auth.basic_auth import BasicAuth
from api.v1.auth.session_auth import SessionAuth


app = Flask(__name__)

CORS(app, resources={r"/api/v1/*": {"origins": "*"}})
app.register_blueprint(app_views)


auth = None
auth_type = getenv("AUTH_TYPE")
if auth_type == "basic_auth":
    auth = BasicAuth()
elif auth_type == "session_auth":
    auth = SessionAuth()
else:
    auth = Auth()


@app.errorhandler(401)
def unauthorized(error):
    """Return a JSON response for 401 unauthorized errors."""
    return jsonify({"error": "Unauthorized"}), 401


@app.errorhandler(403)
def forbidden(error):
    """Return a JSON response for 403 forbidden errors."""
    return jsonify({"error": "Forbidden"}), 403


@app.before_request
def before_request():
    """Handle requests before they are processed."""
    if auth is None:
        return
    excluded_paths = ['/api/v1/status/',
                      '/api/v1/unauthorized/',
                      '/api/v1/forbidden/']
    if request.path in excluded_paths:
        return
    if not auth.require_auth(request.path, excluded_paths):
        return
    if auth.authorization_header(request) is None:
        abort(401)
    request.current_user = auth.current_user(request)
    if request.current_user is None:
        abort(403)


@app.route('/api/v1/status')
@app.route('/api/v1/status/')
def status():
    """Return the status of the API."""
    return jsonify({"status": "OK"})


if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=port)
