#!/usr/bin/env python3
"""this script contains the api endpoints"""

from flask import Blueprint, abort


app_views = Blueprint('app_views', __name__)


@app_views.route('/api/v1/unauthorized', methods=['GET'])
def unauthorized_route():
    """define a route that always returns a 401"""
    abort(401)
