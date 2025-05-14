import numpy as np
from abc import ABC, abstractmethod
from typing import List, TypeVar, Any


class Content (ABC):
    def __init__(self):
        self._identifier: str | None = None
        self._title: str | None = None
        self._characteristics: dict[str, Any] = {}
    @property
    def identifier(self) -> str:
        if self._identifier is None:
            raise ValueError("identifier not loaded")
        return self._identifier

    @property
    def title(self) -> str:
        if self._title is None:
            raise ValueError("title not loaded")
        return self._title
    
    @property
    def characteristics(self) -> dict[str, Any]:
        return self._characteristics
    
    @abstractmethod
    def load_content(self):
        pass
C = TypeVar('C', bound=Content)


class Book (Content):
    def load_content(self):
        pass
    

class Movie (Content):
    pass

class User (ABC):
    def __init__(self, identifier):
        self._identifier = identifier
        self._ratings = dict()
    
    @property
    def identifier(self):
        return self._identifier

class MovieUser(User):
    
    
    @property
    def identifier(self):
        return self._identifier
    
    @property
    def ratings(self):
        return self._ratings


class Rating (ABC):
    def __init__(self, users: List[User], contents: List[C]):
        self._users = {user.identifier: user for user in users}
        self._contents = {content.identifier: content for content in contents}
    
    @abstractmethod
    def rate(self, user_id):
        pass
    
R = TypeVar('R', bound=Rating)

class SimpleRating (Rating):
    pass

class CollaborativeRating (Rating):
    def compute_restricted_u_vectors(self, user_1: User, user_2: User):
        if not isinstance(user_1, User) or not isinstance(user_2, User):
            raise TypeError("Both arguments must be instances of User")
        
        u1_ratings = user_1.ratings
        u2_ratings = user_2.ratings
        common_keys = sorted(u1_ratings.keys() & u2_ratings.keys())
        
        v1 = np.fromiter((u1_ratings[k] for k in common_keys), dtype=float)
        v2 = np.fromiter((u2_ratings[k] for k in common_keys), dtype=float)
        
        return v1, v2
    
    def compute_full_u_vector(self, user_1: User):
        if not isinstance(user_1, User):
            raise TypeError("Both arguments must be instances of User")
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
        
        k_nearest_ratings = np.stack([compute_full_u_vector(self._users[u[1]]) for u in k_nearest])  # THIS
        
        best_content = np.zeros((2, num_recommendations))
        
        # Get mean rating vector of each nearest user
        means = np.mean(k_nearest_ratings, axis=1)  # shape: (k,)
        
        # Now compute the predicted score for each item (content)
        best_content = np.zeros((num_recommendations, 2))  # shape (n_recommendations, [score, content_id])
        
        denominator = np.linalg.norm(k_nearest[:, 0], ord=1)
        
        u_mean = np.mean(compute_full_u_vector(self._users[my_id]))
        
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
        return np.full(len(best_content), u_mean) + best_content[:, 0] / denominator, self._contents[
            best_content[0, 1]].title

class ContentRating (Rating):
    pass

