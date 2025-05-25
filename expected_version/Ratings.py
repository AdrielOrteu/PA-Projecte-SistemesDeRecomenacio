import numpy as np
import pandas as pd
from abc import ABC, abstractmethod
from typing import List, TypeVar, Any, NoReturn
from sklearn.feature_extraction.text import TfidfVectorizer

from Users import Users, User
from Contents import Contents
U = TypeVar('U', bound=Users)
C = TypeVar('C', bound=Contents)
from numpy.typing import NDArray
from sklearn.feature_extraction.text import TfidfVectorizer


class Ratings (ABC):
    
    def __init__(self, consumer: str, **parameters) -> None:
        self._consumer : str = consumer # declares the self._consumer type to be an int and sets it's value
        self._parameters : dict[str, Any] = parameters # declares the self._parameters type to be as described and sets it's value
        self._recommendations : NDArray[str] | None = None # we don't know it's size yet, so we just declare its type
        self._ratings : NDArray[np.float64] | None = None # we don't know it's size yet, so we just declare its type
    
    @property
    def consumer(self) -> str:
        return self._consumer
    
    @consumer.setter
    def consumer(self, new_consumer) -> None:
        self._consumer = new_consumer
    
    @property
    def recommendations(self) -> NDArray[str]:
        if self._recommendations is None:
            raise ValueError("recommendations have not been computed yet")
        return self._recommendations
    
    @property
    def ratings(self) -> NDArray[np.float64]:
        if self._ratings is None:
            raise ValueError("recommendations have not been computed yet")
        return self._ratings
    
    @abstractmethod
    def rate(self, users: U, contents: C) -> None:
        pass
   
    @abstractmethod
    def prediction_rate(self, user: U, content: C) -> tuple[NDArray[np.float64], NDArray[C]]:
        pass


class SimpleRatings(Ratings):
    def rate(self, users: U, contents: C) -> None:
        item_ratings = {}
        for content_id in contents.identifiers:
            item_ratings[content_id] = []
        
        for user in users.users.values():
            for content_id, rating in user.ratings.items():
                item_ratings[content_id].append(rating)
        avg_item = {}
        num_vots = {}
        ratings_global = []
        for content_id, rating in item_ratings.items():
            if len(rating) >= self._parameters["min_votes"]:
                avg_item[content_id] = np.mean(rating)
                num_vots[content_id] = len(rating)
                for value in rating:
                    ratings_global.append(value)
        
        avg_global = np.mean(ratings_global)
        final_rating = []
        for content_id in contents.identifiers:
            if content_id not in users.users[self._consumer].ratings and content_id in avg_item:
                calcul = ((num_vots[content_id] / (num_vots[content_id] + self._parameters["min_votes"]) * avg_item[content_id]) +
                          (self._parameters["min_votes"] / (num_vots[content_id] + self._parameters["min_votes"]) * avg_global))
                final_rating.append(calcul)
        
        self._ratings = np.array(final_rating.sort(reverse=True))
        
    def prediction_rate(self, users: U, contents: C) -> None:
        item_ratings = {}
        for content_id in contents.identifiers:
            item_ratings[content_id] = []
        
        for user in users.users.values():
            for content_id, rating in user.ratings.items():
                item_ratings[content_id].append(rating)
        avg_item = {}
        num_vots = {}
        ratings_global = []
        for content_id, rating in item_ratings.items():
            avg_item[content_id] = np.mean(rating)
            num_vots[content_id] = len(rating)
            for value in rating:
                ratings_global.append(value)
        
        avg_global = np.mean(ratings_global)
        final_rating = []
        for content_id in contents.identifiers:
            if content_id in users.users[self._consumer].ratings:
                calcul = ((num_vots[content_id] / (num_vots[content_id] + self._parameters["min_votes"]) * avg_item[content_id]) +
                          (self._parameters["min_votes"] / (num_vots[content_id] + self._parameters["min_votes"]) * avg_global))
                final_rating.append(calcul)
        
        self._ratings = np.array(final_rating.sort(reverse=True))
        
class CollaborativeRatings(Ratings):
    def compute_restricted_u_vector(self, user_1: User, user_2: User):
        if not isinstance(user_1, User) or not isinstance(user_2, User):
            raise TypeError("Both arguments must be instances of User")
        
        u1_ratings = user_1.ratings
        u2_ratings = user_2.ratings
        common_keys = sorted(u1_ratings.keys() & u2_ratings.keys())
        
        v1 = np.fromiter((u1_ratings[k] for k in common_keys), dtype=np.float64)
        v2 = np.fromiter((u2_ratings[k] for k in common_keys), dtype=np.float64)
        
        return v1, v2
    def compute_full_u_vector(self, user: User, contents: C):
        if not isinstance(user, User):
            raise TypeError("Argument needs to be instance of User")
        return np.array([user.ratings.get(key, np.float64(0)) for key in contents.contents], dtype=np.float64)
    
    def rate(self, users: U, contents: C) -> None:
        k = self._parameters["k"]
        n = len(contents.contents)
        k_nearest_u = np.zeros(k, dtype=str)
        k_nearest_s = np.zeros(k, dtype=np.float64)
        k_nearest_v = np.zeros((k,n), dtype=np.float64)
        
        u1_vector = self.compute_full_u_vector(user=users.users[self.consumer], contents=contents)
        norm1 = np.linalg.norm(u1_vector)
        for user_id  in users.identifier:
            if user_id != self.consumer:
                # u1_vector, u2_vector = self.compute_restricted_u_vector(users.users[self.consumer], users.users[user_id])
                
                u2_vector = self.compute_full_u_vector(user=users.users[user_id], contents=contents)
                norm2 = np.linalg.norm(u2_vector)
                
                if norm1 == 0 or norm2 == 0: # guarantee no division by zero
                    continue # skip this user
                s = np.dot(u1_vector, u2_vector) / (norm1*norm2)
                if s > k_nearest_s[0]:
                    k_nearest_s[0] = s
                    k_nearest_u[0] = user_id
                    k_nearest_v[0] = u2_vector
                    sorting = np.argsort(k_nearest_s)
                    k_nearest_s = k_nearest_s[sorting]
                    k_nearest_u = k_nearest_u[sorting]
                    k_nearest_v = k_nearest_v[sorting]
            
            denominator = np.linalg.norm(k_nearest_s, ord=1)
            mu = np.mean(u1_vector)
            
            means_u = np.mean(k_nearest_v, axis=1)
            self._ratings = np.array([mu + np.dot(k_nearest_s, k_nearest_v[:,i]-means_u)/denominator for i in range(n)], dtype=np.float64)
            self._recommendations = contents.identifiers
            sorting = np.argsort(self._ratings)
            self._ratings = self._ratings[sorting]
            self._recommendations = self._recommendations[sorting]

    
    def prediction_rate(self, users: U, contents: C) -> None:
        k = self._parameters["k"]
        n = len(contents.contents)
        k_nearest_u = np.zeros(k, dtype=str)
        k_nearest_s = np.zeros(k, dtype=np.float64)
        k_nearest_v = np.zeros((k,n), dtype=np.float64)
        
        u1_vector = self.compute_full_u_vector(user=users.users[self.consumer], contents=contents)
        norm1 = np.linalg.norm(u1_vector)
        for user_id  in users.identifier:
            if user_id != self.consumer:
                # u1_vector, u2_vector = self.compute_restricted_u_vector(users.users[self.consumer], users.users[user_id])
                
                u2_vector = self.compute_full_u_vector(user=users.users[user_id], contents=contents)
                norm2 = np.linalg.norm(u2_vector)
                
                s = np.dot(u1_vector, u2_vector) / (norm1*norm2)
                if s > k_nearest_s[0]:
                    k_nearest_s[0] = s
                    k_nearest_u[0] = user_id
                    k_nearest_v[0] = u2_vector
                    sorting = np.argsort(k_nearest_s)
                    k_nearest_s = k_nearest_s[sorting]
                    k_nearest_u = k_nearest_u[sorting]
                    k_nearest_v = k_nearest_v[sorting]
            
            denominator = np.linalg.norm(k_nearest_s, ord=1)
            mu = np.mean(u1_vector)
            
            means_u = np.mean(k_nearest_v, axis=1)
            self._ratings = np.array([mu + np.dot(k_nearest_s, k_nearest_v[:,i]-means_u)/denominator for i in range(n)], dtype=np.float64)
            self._recommendations = contents.identifiers
            sorting = np.argsort(self._ratings)
            self._ratings = self._ratings[sorting]
            self._recommendations = self._recommendations[sorting]


class ContentRatings(Ratings):
    def compute_full_u_vector(self, user: User, contents: C):
        if not isinstance(user, User):
            raise TypeError("Argument needs to be instance of User")
        return np.array([user.ratings.get(key, np.float64(0)) for key in contents.contents], dtype=np.float64)
    def cos_similarity(self, u: NDArray, v: NDArray) -> np.float64:
        numerator = np.dot(u, v)
        denominator = np.linalg.norm(u) * np.linalg.norm(v)
        if denominator == 0:
            return np.float64(0)
        return np.float64(numerator/denominator)
    def rate(self, users: U, contents: C) -> None:
        
        # === Build TF-IDF matrix ===
        item_features = [
            ' '.join(content_characteristics.values())
            for content_characteristics in contents.characteristics
        ]
        tfidf = TfidfVectorizer(stop_words='english')
        tfidf_matrix = tfidf.fit_transform(item_features).toarray()
        p_u = self.compute_full_u_vector(user=users.users[self.consumer], contents=contents)
        profile = p_u[:, np.newaxis] * tfidf_matrix
        profile = profile.sum(axis=0)
        profile = profile / p_u.sum()

        
        similarities = tfidf_matrix @ profile

        similarities = similarities * self._parameters["max"]
        self._recommendations = contents.identifiers
        self._ratings = similarities
        sorting = np.argsort(similarities)
        self._ratings = self._ratings[sorting]
        self._recommendations = self._recommendations[sorting]
    
    def prediction_rate(self, user: U, content: C) -> tuple[NDArray[np.float64], NDArray[C]]:
        pass
