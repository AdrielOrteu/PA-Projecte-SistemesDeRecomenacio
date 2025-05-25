import numpy as np
import pandas as pd
from numpy.typing import NDArray
from abc import ABC, abstractmethod
import typing
from typing import List, TypeVar, Any, NoReturn


class User:
    """
    Represents a user with an identifier and a dictionary of ratings.

    Attributes
    ----------
    identifier : str
        Unique string identifier for the user.
    ratings : dict[str, np.float64]
        Dictionary mapping content identifiers to user ratings.
    """

    def __init__(self, identifier: str):
        """
        Initialize a User instance.

        Parameters
        ----------
        identifier : str
            The unique identifier for the user.
        """
        self._identifier = identifier
        self._ratings: dict[str, np.float64] = {}

    @property
    def identifier(self) -> str:
        """
        Get the user's identifier.

        Returns
        -------
        str
            The identifier of the user.
        """
        return self._identifier

    @identifier.setter
    def identifier(self, new_identifier: str):
        """
        Set a new identifier for the user.

        Parameters
        ----------
        new_identifier : str
            The new identifier to assign to the user.
        """
        self._identifier = new_identifier

    @property
    def ratings(self) -> dict[str, np.float64]:
        """
        Get the user's ratings.

        Returns
        -------
        dict[str, np.float64]
            Dictionary of content identifiers mapped to their corresponding ratings.
        """
        # If you wish to enforce lazy initialization checking:
        # if self._ratings == {}:
        #     raise ValueError("ratings hasn't been loaded/filled yet")
        return self._ratings

    @ratings.setter
    def ratings(self, new_ratings: dict[str, np.float64]):
        """
        Set the user's ratings.

        Parameters
        ----------
        new_ratings : dict[str, np.float64]
            A dictionary mapping content identifiers to ratings.
        """
        self._ratings = new_ratings



class Users(ABC):
    """
    Abstract base class representing a collection of user objects.

    Attributes
    ----------
    users : dict[str, User]
        A dictionary mapping user identifiers to `User` instances.

    identifier : numpy.ndarray of str
        Numpy array of user identifiers.

    ratings : numpy.ndarray of dict[str, np.float64]
        Numpy array of ratings dictionaries from each user.

    Notes
    -----
    This class must be subclassed, and `load_users` must be implemented in a concrete subclass.
    """

    def __init__(self) -> None:
        """
        Initializes the Users collection with an empty user dictionary.

        The `_users` attribute is a dictionary where:
            - key: user identifier (str)
            - value: User object

        Example
        -------
        {
            "user1": User(...),
            "user2": User(...)
        }
        """
        self._users: dict[str, User] = {}

    @property
    def users(self) -> dict[str, 'User']:
        """
        Get the dictionary of user objects.

        Returns
        -------
        dict[str, User]
            A dictionary mapping user identifiers to User objects.

        Raises
        ------
        ValueError
            If users have not been loaded (i.e., `_users` is None).
        """
        if self._users is None:
            raise ValueError("users are not loaded")
        return self._users

    @property
    def identifier(self) -> NDArray[str]:
        """
        Get all user identifiers as a NumPy array.

        Returns
        -------
        numpy.ndarray of str
            Array of user identifiers.

        Raises
        ------
        ValueError
            If users have not been loaded.
        """
        if self._users is None:
            raise ValueError("users have not been loaded")
        return np.array([identifier for identifier in self._users])

    @property
    def ratings(self) -> NDArray[dict[str, np.float64]]:
        """
        Get all user ratings as a NumPy array.

        Returns
        -------
        numpy.ndarray of dict[str, np.float64]
            Array of rating dictionaries, one per user.

        Raises
        ------
        ValueError
            If users have not been loaded.
        """
        if self._users is None:
            raise ValueError("users have not been loaded")
        return np.array([self._users[identifier].ratings for identifier in self._users])

    @abstractmethod
    def load_users(self):
        """
        Load users into the `_users` dictionary.

        This method must be implemented by subclasses to populate the `_users` attribute.
        """
        pass



class BookUsers(Users):
    def load_users(self):
        pass #TODO



class MovieUsers(Users):
    """
    Concrete implementation of the `Users` abstract base class for loading movie user ratings.

    Loads user information and their corresponding ratings from a CSV file located at:
    `"movies/ratings.csv"`.

    The CSV is expected to contain at least three columns in the following order:
        1. `userId` (user identifier)
        2. `movieId` (content identifier)
        3. `rating` (float rating value)
    """

    def load_users(self) -> None:
        """
        Load users and their ratings from the "movies/ratings.csv" file.

        This method populates the `_users` dictionary with `User` instances.
        Each user is assigned a dictionary of ratings, where:
            - keys are movie identifiers (as strings)
            - values are float ratings

        Raises
        ------
        FileNotFoundError
            If the file "movies/ratings.csv" does not exist.

        Notes
        -----
        This method assumes that:
            - The first column contains `userId`
            - The second column contains `movieId`
            - The third column contains the `rating`
        """
        ratings_db = pd.read_csv("movies/ratings.csv")

        user_id = ratings_db.iloc[:, 0]
        for identifier in user_id:
            self._users[str(identifier)] = User(identifier=str(identifier))

        for i, identifier in enumerate(ratings_db["userId"]):
            for user_id in self._users:
                if user_id == str(identifier):
                    self._users[user_id].ratings[ratings_db.iloc[i, 1]] = ratings_db.iloc[i, 2]
