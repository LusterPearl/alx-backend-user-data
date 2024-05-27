#!/usr/bin/env python3
"""
Auth module
"""

import bcrypt

def _hash_password(password: str) -> bytes:
    """Hashes a password with bcrypt and returns the hashed.

    Args:
        password (str): The password to hash.

    Returns:
        bytes: The hashed password.
    """
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode(), salt)
    return hashed
