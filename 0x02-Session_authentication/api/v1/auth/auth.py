#!/usr/bin/env python3
""" class to manage the API authentication"""

from typing import List, TypeVar
from flask import request


class Auth:
    """BasicAuth class that extends the Auth class for basic"""
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Check if a path requires authentication."""
        if not path:
            return True

        if not excluded_paths or not isinstance(excluded_paths, list):
            return True

        for excluded_path in excluded_paths:
            if path.rstrip('/') == excluded_path.rstrip('/'):
                return False

        return True

    def authorization_header(self, request=None) -> str:
        """Get the authorization header from the request."""
        if request is None or 'Authorization' not in request.headers:
            return None
        return request.headers['Authorization']

    def current_user(self, request=None) -> TypeVar('User'):
        """Get the current user from the request."""
        return None
    
    def session_cookie(self, request=None):
        """Return a cookie value from a request"""
        if request is None:
            return None

        session_name = os.getenv('SESSION_NAME', '_my_session_id')
        return request.cookies.get(session_name)
