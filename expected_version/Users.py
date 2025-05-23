import numpy as np
import pandas as pd
from numpy.typing import NDArray
from abc import ABC, abstractmethod
import typing
from typing import List, TypeVar, Any, NoReturn

class User:
    def __init__(self, identifier:int):
        self._identifier = identifier
        self._ratings: dict[int, np.float64] = {}
    
    @property
    def identifier(self):
        return self._identifier
    
    @identifier.setter
    def identifier(self, new_identifier: int):
        self._identifier = new_identifier
    
    @property
    def ratings(self):
        if self._ratings is None:
            raise ValueError("ratings hasn't been loaded/filled yet")
        return self._ratings
    
    @ratings.setter
    def ratings(self, new_ratings: dict[int, np.float64]):
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
        self._users: list[User] | None = None
        self.load_users()
    
    def users(self) -> list[tuple[int, dict[str, int]]]:
        if self._users is None:
            raise ValueError("contents are not loaded")
        return self._users
    
    @property
    def identifier(self) -> NDArray[int]:
        if self._users in None:
            raise ValueError("users have not been loaded")
        return np.array([user[0] for user in self._users])
    
    @property
    def ratings(self):
        if self._users in None:
            raise ValueError("users have not been loaded")
        return np.array([user[1] for user in self._users])
    
    @abstractmethod
    def load_users(self):
        pass
    
    @abstractmethod
    def save_users(self):
        pass


class MovieUsers(Users):
    def load_users(self):
        ratings_db = pd.read_csv("movies/ratings.csv")
        user_id = ratings_db.iloc[:, 0]
        for identifier in user_id:
            self._users.append(identifier)
        super().load_users()
    
    def load_rating(self):
        ratings_db = pd.read_csv("movies/ratings.csv")
        for i, identifier in enumerate(ratings_db["userId"]):
                for user in self._users:
                    # noinspection SpellCheckingInspection
                    if user[0] == identifier:
                        # user[1] is the dictionary of ratings
                        # [ratings_db.iloc[i, 1]] defines the key of the new rating to be the movie identifier
                        # ratings_db.iloc[i, 2] is the value of the rating
                        user[1][ratings_db.iloc[i, 1]] = ratings_db.iloc[i, 2]
                    
        
# .rate_content(content=ratings_db.iloc[i, 1], rating=ratings_db.iloc[i, 2])
