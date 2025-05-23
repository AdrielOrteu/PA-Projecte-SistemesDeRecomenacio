import numpy as np
import pandas as pd
from abc import ABC, abstractmethod
from typing import List, TypeVar, Any, NoReturn
from numpy.typing import NDArray


class GraphicalUserInterface:
    def __init__(self) -> None:
        pass
    
    def chose_db(self) -> str:
        print("Witch database do you want to use?\n M -> movies | B -> books")
        choice = {"M":"movies", "B":"books"}.get(input())
        return choice
    
    def chose_method(self):
        print("How do you want us to recommend the content?\n S -> simple | L -> collaborative | C -> content")
        choice = {"S": "simple", "L": "collaborative", "C": "content"}.get(input())
        return choice
    
    # Anabel

class Contents (ABC):
    def __init__(self) -> None:
        self._contents: list[ tuple [str,str, dict[str, Any] ] ] | None = None
    
    @property
    def contents(self) -> list[ tuple [str,str, dict[str, Any] ] ]:
        if self._contents is None:
            raise ValueError("contents are not loaded")
        return self._contents
    
    @property
    def identifiers(self) -> NDArray[str]:
        if self._contents is None:
            raise ValueError("contents are not loaded")
        return np.array([content[0] for content in self._contents])
    @property
    def titles(self) -> NDArray[str]:
        if self._contents is None:
            raise ValueError("contents are not loaded")
        return np.array([content[1] for content in self._contents])
    
    @property
    def characteristics(self) -> NDArray[dict[str, Any]]:
        if self._contents is None:
            raise ValueError("contents are not loaded")
        return np.array([content[2] for content in self._contents])
    
    @abstractmethod
    def load_content(self) -> None:
        pass
C = TypeVar('C', bound=Contents)


class Books (Contents):
    def load_content(self) -> None:
        pass
    

class Movies (Contents):
    def load_content(self) -> None:
        pass

class Users (ABC):
    def __init__(self) -> None:
        self._users: list[ NDArray[int]] | None = None


    def users(self) -> list[ NDArray[int] ]:
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

class MovieUsers(Users):
    def load_users(self):
        a = pd.read_csv("")


class Rating (ABC):
    def __init__(self, users: List[Users], contents: List[C]) -> None:
        self._users = {user.identifier: user for user in users}
        self._contents = {content.identifier: content for content in contents}
    
    @abstractmethod
    def rate(self, user_id) -> tuple[NDArray[np.float64], NDArray[C]]:
        pass
    
R = TypeVar('R', bound=Rating)

class SimpleRating (Rating):
    pass

class CollaborativeRating (Rating):
    def compute_restricted_u_vectors(self, user_1: Users, user_2: Users):
        if not isinstance(user_1, Users) or not isinstance(user_2, Users):
            raise TypeError("Both arguments must be instances of Users")
        
        u1_ratings = user_1.ratings
        u2_ratings = user_2.ratings
        common_keys = sorted(u1_ratings.keys() & u2_ratings.keys())
        
        v1 = np.fromiter((u1_ratings[k] for k in common_keys), dtype=float)
        v2 = np.fromiter((u2_ratings[k] for k in common_keys), dtype=float)
        
        return v1, v2
    
    def compute_full_u_vector(self, user_1: Users) -> NDArray[np.float64]:
        if not isinstance(user_1, Users):
            raise TypeError("Both arguments must be instances of Users")
        return np.array([user_1.ratings.get(key, 0) for key in self._contents])
    def rate(self, my_id):
        k_nearest = np.zeros((k, 2))
        for user_id in self._users:
            if user_id != my_id:
                u1_vector, u2_vector = self.compute_restricted_u_vectors(self._users[my_id], self._users[user_id])
                
                norm1 = np.linalg.norm(u1_vector)
                norm2 = np.linalg.norm(u2_vector)
                if norm1 == 0 or norm2 == 0:
                    continue  # skip this user
                s = np.dot(u1_vector, u2_vector) / (norm1 * norm2)
                
                if s > k_nearest[0, 0]:
                    # print(f"#########\n##### {user_id} #####")
                    # print(k_nearest)
                    # print(u2_vector)
                    k_nearest[0, 0] = s
                    k_nearest[0, 1] = user_id
                    k_nearest = k_nearest[np.argsort(k_nearest[:, 0])]
                    # print(k_nearest)
        
        k_nearest_ratings = np.stack([self.compute_full_u_vector(self._users[u[1]]) for u in k_nearest])  # THIS
        
        best_content = np.zeros((2, num_recommendations))
        
        # Get mean rating vector of each nearest user
        means = np.mean(k_nearest_ratings, axis=1)  # shape: (k,)
        
        # Now compute the predicted score for each item (content)
        best_content = np.zeros((num_recommendations, 2))  # shape (n_recommendations, [score, content_id])
        
        denominator = np.linalg.norm(k_nearest[:, 0], ord=1)
        
        u_mean = np.mean(self.compute_full_u_vector(self._users[my_id]))
        
        for pos, content_id in enumerate(self._contents):
            y = means  # shape (k,)
            values = k_nearest_ratings[:, pos]  # shape (k,)
            weighted_diff = k_nearest[:, 0] * (values - y)  # shape (k,)
            numerator = np.sum(weighted_diff)
            
            if numerator > best_content[0, 0]:
                best_content[0, 0] = numerator
                best_content[0, 1] = content_id
        
        print(
            f"{u_mean}+{best_content[:, 0]}/{denominator}\n{best_content[:, 1]}  {self._contents[best_content[0, 1]]}\n{self._contents[best_content[0, 1]].id}\n")
        print(np.full(len(best_content), u_mean) + best_content[:, 0] / denominator)
        print("\n\n")
        return np.full(len(best_content), u_mean) + best_content[:, 0] / denominator, self._contents[best_content[0, 1]].title

class ContentRating (Rating):
    pass

