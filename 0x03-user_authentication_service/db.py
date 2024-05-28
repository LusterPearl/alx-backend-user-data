#!/usr/bin/env python3
"""
DB module
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from user import Base, User
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=False) 
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """Add a user to the database.
        Args:
            email (str): The user's email address.
            hashed_password (str): The user's hashed password.
        Returns:
            User: The created user object.
        """
        new_user = User(email=email, hashed_password=hashed_password)
        session = self._session
        session.add(new_user)
        session.commit()
        return new_user

    def find_user_by(self, **kwargs) -> User:
        """Find a user by arbitrary keyword arguments.
        Args:
            **kwargs: Arbitrary keyword arguments to filter users.
        Returns:
            User: The first user found.
        Raises:
            NoResultFound: If no user is found.
            InvalidRequestError: If the query is invalid.
        """
        session = self._session
        try:
            user = session.query(User).filter_by(**kwargs).one()
            return user
        except NoResultFound:
            raise NoResultFound("No user found for the given criteria.")
        except InvalidRequestError:
            raise InvalidRequestError("Invalid query arguments.")

    def update_user(self, user_id: int, **kwargs) -> None:
        """Update a user's attributes.
        Args:
            user_id (int): The user's ID.
            **kwargs: Arbitrary keyword arguments to update the user.
        Returns:
            None
        Raises:
            ValueError: If an argument does not correspond to a user.
        """
        session = self._session
        user = self.find_user_by(id=user_id)

        for key, value in kwargs.items():
            if not hasattr(user, key):
                raise ValueError(f"Invalid attribute: {key}")
            setattr(user, key, value)

        session.commit()
