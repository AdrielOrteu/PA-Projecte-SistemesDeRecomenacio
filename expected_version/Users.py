import numpy as np
import pandas as pd
from numpy.typing import NDArray
from abc import ABC, abstractmethod
import typing
from typing import List, TypeVar, Any, NoReturn

class User:
    def __init__(self, identifier:str):
        self._identifier = identifier
        self._ratings: dict[str, np.float64] = {}
    
    @property
    def identifier(self):
        return self._identifier
    
    @identifier.setter
    def identifier(self, new_identifier: str):
        self._identifier = new_identifier
    
    @property
    def ratings(self) -> dict[str, np.float64]:
        if self._ratings == {}:
            raise ValueError("ratings hasn't been loaded/filled yet")
        return self._ratings
    
    @ratings.setter
    def ratings(self, new_ratings: dict[str, np.float64]):
        self._ratings = new_ratings

class Users(ABC):
    def __init__(self) -> None:
        """
    Initializes the object with an empty user list.

    The `_users` attribute is set to `None` initially. Once populated, it should contain
    a list of tuples, where each tuple consists of:
        - a user ID (str)
        - a dictionary mapping content IDs (str) to rating values (int)
    
    Example structure:
        [("user1", {"contentA": 5, "contentB": 3}), ("user2", {"contentA": 4})] *WRONG STRUCTURE!*
    """
        self._users: dict[str, User] = {}
    
    @property
    def users(self) -> dict[str, User]:
        if self._users is None:
            raise ValueError("contents are not loaded")
        return self._users
    
    @property
    def identifier(self) -> NDArray[str]:
        if self._users in None:
            raise ValueError("users have not been loaded")
        return np.array([identifier for identifier in self._users])
    
    @property
    def ratings(self) -> NDArray[np.float64]:
        if self._users in None:
            raise ValueError("users have not been loaded")
        return np.array([self._users[identifier].ratings for identifier in self._users])
    
    @abstractmethod
    def load_users(self):
        pass
    
    @abstractmethod
    def save_users(self):
        pass


class BookUsers(Users):
    def load_users(self):
        pass #TODO
    
    def save_users(self):
        pass #TODO


class MovieUsers(Users):
    def load_users(self):
        ratings_db = pd.read_csv("movies/ratings.csv")
        user_id = ratings_db.iloc[:, 0]
        for identifier in user_id:
            self._users[str(identifier)] = User(identifier=str(identifier))
        print(self._users)
        for i, identifier in enumerate(ratings_db["userId"]):
                for user_id in self._users:
                    # noinspection SpellCheckingInspection
                    # print(user_id)
                    if user_id == str(identifier):
                        # user[1] is the dictionary of ratings
                        # [ratings_db.iloc[i, 1]] defines the key of the new rating to be the movie identifier
                        # ratings_db.iloc[i, 2] is the value of the rating
                        self._users[user_id].ratings[ratings_db.iloc[i, 1]] = ratings_db.iloc[i, 2]
    
    def save_users(self):
        pass