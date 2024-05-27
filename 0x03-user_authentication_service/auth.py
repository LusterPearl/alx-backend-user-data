#!/usr/bin/env python3
"""
Auth module
"""

from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound
import bcrypt


class Auth:
    """Auth class to interact with the authentication database."""

    def __init__(self):
        self._db = DB()

    def _hash_password(self, password: str) -> bytes:
        """Hashes a password with bcrypt and returns the hashed password.
        Args:
            password (str): The password to hash.
        Returns:
            bytes: The hashed password.
        """
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password.encode(), salt)
        return hashed

    def register_user(self, email: str, password: str) -> User:
        """Registers a new user with the given email and password.
        Args:
            email (str): The user's email.
            password (str): The user's password.
        Returns:
            User: The newly created user.
        Raises:
            ValueError: If the user already exists.
        """
        try:
            self._db.find_user_by(email=email)
            raise ValueError(f"User {email} already exists")
        except NoResultFound:
            hashed_password = self._hash_password(password)
            user = self._db.add_user(email, hashed_password)
            return user
        
    def valid_login(self, email: str, password: str) -> bool:
        """Validates a user's login credentials.
        Args:
            email (str): The user's email.
            password (str): The user's password.
        Returns:
            bool: True if the credentials are valid, False otherwise.
        """
        try:
            user = self._db.find_user_by(email=email)
            return bcrypt.checkpw(password.encode(), user.hashed_password)
        except NoResultFound:
            return False
