#!/usr/bin/env python3
"""
Auth module
"""

from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound
import bcrypt
import uuid
import logging


def _hash_password(password: str) -> bytes:
    """Hashes a password with bcrypt and returns the hashed password as bytes.

    Args:
        password (str): The password to hash.

    Returns:
        bytes: The hashed password.
    """
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode(), salt)
    return hashed


def _generate_uuid() -> str:
    """Generates a new UUID and returns it as a string.

    Returns:
        str: The string representation of the UUID.
    """
    return str(uuid.uuid4())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

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
            hashed_password = _hash_password(password)
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

    def create_session(self, email: str) -> str:
        """Creates a new session for the user with the given email.

        Args:
            email (str): The user's email.

        Returns:
            str: The session ID if the user is found, None otherwise.
        """
        try:
            user = self._db.find_user_by(email=email)
            session_id = _generate_uuid()
            self._db.update_user(user.id, session_id=session_id)
            return session_id
        except NoResultFound:
            return None

    def get_user(self, email: str) -> User:
        """Retrieves a user by email.

        Args:
            email (str): The user's email.

        Returns:
            User: The user object if found, None otherwise.
        """
        try:
            return self._db.find_user_by(email=email)
        except NoResultFound:
            return None
        
    def get_user_from_session_id(self, session_id: str) -> User:
        """Get user from session ID.
       Args:
        session_id (str): The session ID.
       Returns:
        User: The user if session ID is valid, None otherwise.
        """
        if not session_id:
            return None
        
        try:
            return self._db.find_user_by(session_id=session_id)
        except NoResultFound:
            return None
