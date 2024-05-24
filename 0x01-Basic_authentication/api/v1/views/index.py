#!/usr/bin/env python3
""" Module of Index views
"""
from flask import abort, Blueprint


app_views = Blueprint('app_views', __name__)


@app_views.route('/api/v1/unauthorized', methods=['GET'])
def unauthorized_endpoint():
    """Raise a 401 error to test the unauthorized handler."""
    abort(401)


@app_views.route('/stats/', strict_slashes=False)
def stats() -> str:
    """ GET /api/v1/stats
    Return:
      - the number of each objects
    """
    from models.user import User
    stats = {}
    stats['users'] = User.count()
    return jsonify(stats)
