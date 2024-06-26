#!/usr/bin/env python3
"""BasicAuth class for basic HTTP authentication."""

from typing import TypeVar, List
from api.v1.auth.auth import Auth


class BasicAuth(Auth):
    """BasicAuth class that extends the Auth class for basic"""    
    def extract_base64_authorization_header(self, authorization_header: str) -> str:
        """Extract the Base64 part of the Authorization header.
        Args:
            authorization_header (str): The Authorization header.
        Returns:
            str: The Base64 part of the Authorization header, or None if invalid.
        """
        if authorization_header is None or not isinstance(authorization_header, str):
            return None

        if not authorization_header.startswith("Basic "):
            return None

        return authorization_header.split(" ")[1]

    def decode_base64_authorization_header(self, base64_authorization_header: str) -> str:
        """Decode a Base64 Authorization header  
        Args:
            base64_authorization_header (str).
        Returns:
            str: The decoded Authorization header, or None if invalid.
        """
        import base64

        if base64_authorization_header is None or not isinstance(base64_authorization_header, str):
            return None

        try:
            decoded_bytes = base64.b64decode(base64_authorization_header)
            return decoded_bytes.decode('utf-8')
        except Exception as e:
            return None

    def extract_user_credentials(self, decoded_base64_authorization_header: str) -> (str, str):
        """Extract user email and password from the decoded 
        Args:
            decoded_base64_authorization_header
        Returns:
            tuple: The user email and password, or (None, None) if invalid.
        """
        if decoded_base64_authorization_header is None or not isinstance(decoded_base64_authorization_header, str):
            return None, None
        parts = decoded_base64_authorization_header.split(':', 1)
        if len(parts) != 2:
            return None, None

        user_email, user_password = parts
        return user_email, user_password

    def user_object_from_credentials(self, user_email: str, user_pwd: str) -> TypeVar('User'):
        """Retrieve User instance based on email and password.
        Args:
            user_email (str): The user's email.
            user_pwd (str): The user's password.
        Returns:
            User: The User instance if valid, otherwise None.
        """
        if user_email is None or not isinstance(user_email, str):
            return None

        if user_pwd is None or not isinstance(user_pwd, str):
            return None

        users = User.search({'email': user_email})
        if not users:
            return None

        user = users[0]
        if not user.is_valid_password(user_pwd):
            return None

        return user

    def current_user(self, request=None) -> TypeVar('User'):
        """Retrieve the User instance for a request    
        Args:
            request: The request object
        Returns:
            User: The User instance if valid, otherwise None.
        """
        if request is None:
            return None

        auth_header = request.headers.get('Authorization')
        if auth_header is None:
            return None

        base64_auth_header = self.extract_base64_authorization_header(auth_header)
        if base64_auth_header is None:
            return None

        decoded_auth_header = self.decode_base64_authorization_header(base64_auth_header)
        if decoded_auth_header is None:
            return None

        user_email, user_pwd = self.extract_user_credentials(decoded_auth_header)
        if user_email is None or user_pwd is None:
            return None

        return self.user_object_from_credentials(user_email, user_pwd)

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Check if a path requires 
        Args:
            path (str): The path to check.
            excluded_paths (List[str]): A list of paths.
        Returns:
            bool: True if the path requires authentication.
        """
        if path is None or not isinstance(path, str) or excluded_paths is None or not all(isinstance(p, str) for p in excluded_paths):
            return True

        for excluded_path in excluded_paths:
            if excluded_path.endswith("*") and path.startswith(excluded_path[:-1]):
                return False
            elif path == excluded_path:
                return False

        return True
