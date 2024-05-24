#!/usr/bin/env python3
"""
Route module for the API
"""
from os import getenv
from api.v1.views import app_views
from flask import Flask, jsonify
from flask_cors import CORS


app = Flask(__name__)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})


@app.errorhandler(401)
def unauthorized(error):
    """Handle unauthorized errors."""
    return jsonify({"error": "Unauthorized"}), 401

app.register_blueprint(app_views)

if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=port)
