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
    """Abstract base class for recommendation rating systems.

    This class provides a common interface for different recommendation
    rating methodologies, including properties for consumer, recommendations,
    and ratings, as well as abstract methods for rating and prediction.

    Attributes
    ----------
    _consumer : str
        The identifier of the consumer (e.g., user ID) for whom recommendations
        or ratings are being processed.
    _parameters : dict[str, Any]
        A dictionary containing parameters specific to the rating system
        implementation (e.g., number of neighbors, similarity metric).
    _recommendations : NDArray[str] or None
        An array of recommended item identifiers (strings). It is None until
        recommendations are computed.
    _ratings : NDArray[np.float64] or None
        An array of predicted ratings (float64) corresponding to the
        recommendations. It is None until recommendations are computed.

    Notes
    -----
    This is an abstract class and requires concrete implementations for
    `rate` and `prediction_rate` methods.
    """
    
    def __init__(self, consumer: str, **parameters) -> None:
        """Initializes the Ratings system for a specific consumer.

        Parameters
        ----------
        consumer : str
            The identifier of the consumer (e.g., user ID) for whom this
            rating system instance is being created.
        **parameters : dict[str, Any]
            Arbitrary keyword arguments representing specific parameters for
            the rating system's implementation (e.g., 'min_votes', 'top_n').
        """
        self._consumer : str = consumer 
        self._parameters : dict[str, Any] = parameters
        self._recommendations : NDArray[str] | None = None
        self._ratings : NDArray[np.float64] | None = None
    
    @property
    def consumer(self) -> str:
        """The identifier of the consumer.

        Returns
        -------
        str
            The current consumer identifier.
        """
        return self._consumer
    
    @consumer.setter
    def consumer(self, new_consumer: str) -> None:
        """Sets a new consumer identifier.

        Parameters
        ----------
        new_consumer : str
            The new consumer identifier to set.
        """
        self._consumer = new_consumer
    
    @property
    def recommendations(self) -> NDArray[str]:
        """Array of recommended item identifiers.

        Returns
        -------
        numpy.typing.NDArray[str]
            A NumPy array containing string identifiers of the recommended items.

        Raises
        ------
        ValueError
            If recommendations have not yet been computed.
        """
        if self._recommendations is None:
            raise ValueError("recommendations have not been computed yet")
        return self._recommendations
    
    @property
    def ratings(self) -> NDArray[np.float64]:
        """Array of predicted ratings corresponding to the recommendations.

        Returns
        -------
        numpy.typing.NDArray[numpy.float64]
            A NumPy array containing float64 predicted ratings.

        Raises
        ------
        ValueError
            If recommendations (and thus ratings) have not yet been computed.
        """
        if self._ratings is None:
            raise ValueError("recommendations have not been computed yet")
        return self._ratings
    
    @abstractmethod
    def rate(self, users: U, contents: C) -> None:
        """Abstract method to compute and store recommendations and their ratings.

        This method must be implemented by concrete subclasses to perform the
        actual rating calculation logic based on the specific recommendation
        methodology. It should typically update `_recommendations` and `_ratings`
        attributes.

        Parameters
        ----------
        users : U
            Data representing users (e.g., user ID, user profiles, or user-item matrix).
            The specific type `U` depends on the implementation.
        contents : C
            Data representing content items (e.g., item ID, item features, or
            item-user matrix). The specific type `C` depends on the implementation.

        Returns
        -------
        None

        Notes
        -----
        Implementations should handle updating the `_recommendations` and `_ratings`
        attributes.
        """
        pass
    
    @abstractmethod
    def prediction_rate(self, user: U, content: C) -> tuple[NDArray[np.float64], NDArray[C]]:
        """Abstract method to predict ratings for specific users and contents.

        This method should be implemented by concrete subclasses to provide
        predictions for given user(s) and content item(s), primarily used
        for evaluation purposes.

        Parameters
        ----------
        user : U
            The user(s) for whom to predict ratings. Can be a single user ID
            or an array of user IDs, depending on the implementation.
        content : C
            The content item(s) for which to predict ratings. Can be a single
            item ID or an array of item IDs, depending on the implementation.

        Returns
        -------
        tuple[numpy.typing.NDArray[numpy.float64], numpy.typing.NDArray[C]]
            A tuple containing:
            - A NumPy array of predicted ratings (float64) for the given user(s)
              and content(s).
            - A NumPy array of the content identifiers for which predictions
              were made.

        Notes
        -----
        This method is particularly useful for evaluation metrics like MAE and RMSE,
        where predictions for items already rated by a user are needed.
        """
        pass

class SimpleRatings(Ratings):
    """Concrete implementation of a simple recommendation rating system.

    This system recommends items based on a smoothed average rating,
    considering a minimum number of votes. It extends the abstract
    `Ratings` class.
    """
    def rate(self, users: U, contents: C) -> None:
        """Computes and stores recommendations for unseen items based on smoothed average ratings.

        This method calculates a weighted average rating for each content item,
        considering a 'min_votes' parameter (from `self._parameters`) to smooth ratings.
        It then identifies the top-rated items that the current consumer
        (`self._consumer`) has not yet rated, and updates the `_ratings` attribute
        with these predicted scores.

        Parameters
        ----------
        users : U
            An object containing user data. Expected to have a `users` attribute
            which is a dictionary mapping user IDs to user objects. Each user object
            is expected to have a `ratings` attribute (a dictionary of content_id: rating).
        contents : C
            An object containing content data. Expected to have an `identifiers`
            attribute which is an iterable of all content IDs.

        Returns
        -------
        None

        Notes
        -----
        - The `_ratings` attribute of the class instance is updated with the
          computed predicted ratings for unseen items.
        - The calculation uses a "smoothed" average formula incorporating `min_votes`
          and a global average rating.
        - **Important**: The line `self._ratings = np.array(final_rating.sort(reverse=True))`
          is problematic. `list.sort()` sorts the list in-place and returns `None`,
          so `self._ratings` will be assigned `np.array(None)`. It should likely
          be `final_rating.sort(reverse=True)` followed by `self._ratings = np.array(final_rating)`
          or `self._ratings = np.array(sorted(final_rating, reverse=True))`.
        - This method currently only updates `self._ratings`. If `_recommendations`
          is also meant to be updated by this method (e.g., with the content IDs
          corresponding to the predicted ratings), that functionality is missing.
        """
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
        """Predicts ratings for items that have been seen by the current consumer.

        This method calculates a smoothed average rating for each content item,
        similar to the `rate` method, but specifically targets items that the
        current consumer (`self._consumer`) has already rated. The primary purpose
        is to provide predicted ratings for evaluation against actual ratings
        (e.g., for MAE or RMSE calculation).

        Parameters
        ----------
        users : U
            An object containing user data. Expected to have a `users` attribute
            which is a dictionary mapping user IDs to user objects. Each user object
            is expected to have a `ratings` attribute (a dictionary of content_id: rating).
        contents : C
            An object containing content data. Expected to have an `identifiers`
            attribute which is an iterable of all content IDs.

        Returns
        -------
        None
            (Note: The abstract base class `Ratings` defines `prediction_rate`
            to return `tuple[NDArray[np.float64], NDArray[C]]`. The current
            implementation updates `self._ratings` but does not return
            the predicted ratings and content IDs as required by the signature.)

        Notes
        -----
        - The `_ratings` attribute of the class instance is updated with the
          computed predicted ratings for items seen by the consumer.
        - The `min_votes` parameter (from `self._parameters`) is used in the
          smoothing formula. Unlike the `rate` method, items are not filtered
          by `min_votes` when calculating their average for prediction.
        - **Important**: The line `self._ratings = np.array(final_rating.sort(reverse=True))`
          is problematic. `list.sort()` sorts the list in-place and returns `None`,
          so `self._ratings` will be assigned `np.array(None)`. It should likely
          be `final_rating.sort(reverse=True)` followed by `self._ratings = np.array(final_rating)`
          or `self._ratings = np.array(sorted(final_rating, reverse=True))`.
        - This method needs to be modified to return a tuple of `(predicted_ratings, content_ids)`
          to match the abstract method signature in the base class `Ratings`.
        """
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
            if content_id in users.users[self._consumer].ratings: # Check if consumer has rated this item
                calcul = ((num_vots[content_id] / (num_vots[content_id] + self._parameters["min_votes"]) * avg_item[content_id]) +
                                  (self._parameters["min_votes"] / (num_vots[content_id] + self._parameters["min_votes"]) * avg_global))
                final_rating.append(calcul)
        
        self._ratings = np.array(final_rating.sort(reverse=True))
        
class CollaborativeRatings(Ratings):
    """Concrete implementation of a collaborative filtering recommendation rating system.

    This system utilizes a user-based K-Nearest Neighbors (KNN) approach to
    predict ratings and generate recommendations for the current consumer.
    It extends the abstract `Ratings` class.
    """
    def compute_restricted_u_vector(self, user_1: User, user_2: User) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
        """Computes rating vectors for two users based only on their commonly rated items.

        Parameters
        ----------
        user_1 : User
            The first user object, expected to have a `ratings` attribute (dict of content_id: rating).
        user_2 : User
            The second user object, expected to have a `ratings` attribute (dict of content_id: rating).

        Returns
        -------
        tuple[numpy.typing.NDArray[numpy.float64], numpy.typing.NDArray[numpy.float64]]
            A tuple containing two NumPy arrays (v1, v2), where each array holds the
            ratings of the respective user for the items they both have rated,
            in a consistent order.

        Raises
        ------
        TypeError
            If either `user_1` or `user_2` is not an instance of the `User` class.
        """
        if not isinstance(user_1, User) or not isinstance(user_2, User):
            raise TypeError("Both arguments must be instances of User")
        
        u1_ratings = user_1.ratings
        u2_ratings = user_2.ratings
        common_keys = sorted(u1_ratings.keys() & u2_ratings.keys())
        
        v1 = np.fromiter((u1_ratings[k] for k in common_keys), dtype=np.float64)
        v2 = np.fromiter((u2_ratings[k] for k in common_keys), dtype=np.float64)
        
        return v1, v2

    def compute_full_u_vector(self, user: User, contents: C) -> NDArray[np.float64]:
        """Computes a full rating vector for a given user across all provided content items.

        For items not rated by the user, a rating of 0 is assigned. The order of
        ratings in the vector corresponds to the order of content identifiers.

        Parameters
        ----------
        user : User
            The user object, expected to have a `ratings` attribute (dict of content_id: rating).
        contents : C
            An object containing content data. Expected to have a `contents`
            attribute which is an iterable of all content IDs (e.g., `contents.contents`).

        Returns
        -------
        numpy.typing.NDArray[numpy.float64]
            A NumPy array of float64 representing the user's ratings for all
            content items. Unrated items are represented by 0.

        Raises
        ------
        TypeError
            If `user` is not an instance of the `User` class.
        """
        if not isinstance(user, User):
            raise TypeError("Argument needs to be instance of User")
        return np.array([user.ratings.get(key, np.float64(0)) for key in contents.contents], dtype=np.float64)
    
    def rate(self, users: U, contents: C) -> None:
        """Computes and stores recommendations for the current consumer using user-based collaborative filtering.

        This method identifies the k-nearest neighbors (users with highest
        cosine similarity) to the current consumer (`self._consumer`). It then
        predicts ratings for all content items based on the weighted average
        of ratings from these neighbors, and updates the `_ratings` and
        `_recommendations` attributes.

        Parameters
        ----------
        users : U
            An object containing user data. Expected to have a `users` attribute
            (a dictionary mapping user IDs to `User` objects) and an `identifier`
            attribute (an iterable of all user IDs).
        contents : C
            An object containing content data. Expected to have a `contents`
            attribute (an iterable of all content IDs) and an `identifiers`
            attribute (an iterable of all content IDs).

        Returns
        -------
        None

        Notes
        -----
        - The `k` parameter for the number of nearest neighbors is retrieved from
          `self._parameters["k"]`.
        - Cosine similarity is used to find similar users.
        - The prediction formula involves the mean rating of the current user
          and a weighted sum of the deviations of neighbors' ratings from their means.
        - **Potential issue**: The logic to maintain `k_nearest_s`, `k_nearest_u`,
          and `k_nearest_v` only inserts if similarity `s` is greater than `k_nearest_s[0]`,
          and then re-sorts. This only works correctly if `k_nearest_s` is always
          kept sorted in ascending order (smallest similarity at index 0).
        - **Potential issue**: The final sorting of `self._ratings` and
          `self._recommendations` uses `np.argsort(self._ratings)`, which by default
          returns indices that would sort in *ascending* order. For recommendations,
          a descending order (highest ratings first) is typically desired.
        - This method updates the `_ratings` and `_recommendations` attributes of
          the class instance with the calculated predictions and corresponding content IDs.
        """
        k = self._parameters["k"]
        n = len(contents.contents)
        k_nearest_u = np.zeros(k, dtype=str)
        k_nearest_s = np.zeros(k, dtype=np.float64)
        k_nearest_v = np.zeros((k,n), dtype=np.float64)
        
        u1_vector = self.compute_full_u_vector(user=users.users[self.consumer], contents=contents)
        norm1 = np.linalg.norm(u1_vector)
        for user_id in users.identifier:
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

    
    def prediction_rate(self, users: U, contents: C) -> None: # Should be -> tuple[NDArray[np.float64], NDArray[C]] based on Ratings abstract method
        """Predicts ratings for all content items for the current consumer using user-based collaborative filtering.

        This method identifies the k-nearest neighbors to the current consumer
        (`self._consumer`) and uses their ratings to predict ratings for all
        content items. This is typically used for evaluating the system's
        accuracy against known ratings.

        Parameters
        ----------
        users : U
            An object containing user data. Expected to have a `users` attribute
            (a dictionary mapping user IDs to `User` objects) and an `identifier`
            attribute (an iterable of all user IDs).
        contents : C
            An object containing content data. Expected to have a `contents`
            attribute (an iterable of all content IDs) and an `identifiers`
            attribute (an iterable of all content IDs).

        Returns
        -------
        None
            (Note: The abstract base class `Ratings` defines `prediction_rate`
            to return `tuple[NDArray[np.float64], NDArray[C]]`. The current
            implementation updates `self._ratings` and `_recommendations`
            internally but does not return the predicted ratings and content IDs
            as required by the signature for external use.)

        Notes
        -----
        - The `k` parameter for the number of nearest neighbors is retrieved from
          `self._parameters["k"]`.
        - Cosine similarity is used to find similar users.
        - The prediction formula involves the mean rating of the current user
          and a weighted sum of the deviations of neighbors' ratings from their means.
        - **Potential issue**: The logic to maintain `k_nearest_s`, `k_nearest_u`,
          and `k_nearest_v` only inserts if similarity `s` is greater than `k_nearest_s[0]`,
          and then re-sorts. This only works correctly if `k_nearest_s` is always
          kept sorted in ascending order (smallest similarity at index 0).
        - **Potential issue**: The final sorting of `self._ratings` and
          `self._recommendations` uses `np.argsort(self._ratings)`, which by default
          returns indices that would sort in *ascending* order. For evaluation
          purposes, the order of predictions might not be critical, but if it
          implies an order of recommendations, descending is typically desired.
        - This method is missing the `if norm1 == 0 or norm2 == 0:` check
          that is present in the `rate` method's loop, which could lead to
          division by zero if a user has no ratings.
        """
        k = self._parameters["k"]
        n = len(contents.contents)
        k_nearest_u = np.zeros(k, dtype=str)
        k_nearest_s = np.zeros(k, dtype=np.float64)
        k_nearest_v = np.zeros((k,n), dtype=np.float64)
        
        u1_vector = self.compute_full_u_vector(user=users.users[self.consumer], contents=contents)
        norm1 = np.linalg.norm(u1_vector)
        for user_id in users.identifier:
            if user_id != self.consumer:
                # u1_vector, u2_vector = self.compute_restricted_u_vector(users.users[self.consumer], users.users[user_id])
                
                u2_vector = self.compute_full_u_vector(user=users.users[user_id], contents=contents)
                norm2 = np.linalg.norm(u2_vector)
                
                # if norm1 == 0 or norm2 == 0: # This check is present in rate, but missing here.
                #    continue # skip this user
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
    """Concrete implementation of a content-based recommendation rating system.

    This system builds a user profile based on the consumer's past ratings
    and the TF-IDF representation of content features. It then predicts
    ratings for items based on the similarity between the user profile
    and the item features. It extends the abstract `Ratings` class.
    """
    def compute_full_u_vector(self, user: User, contents: C) -> NDArray[np.float64]:
        """Computes a full rating vector for a given user across all provided content items.

        For items not rated by the user, a rating of 0 is assigned. The order of
        ratings in the vector corresponds to the order of content identifiers.

        Parameters
        ----------
        user : User
            The user object, expected to have a `ratings` attribute (dict of content_id: rating).
        contents : C
            An object containing content data. Expected to have a `contents`
            attribute which is an iterable of all content IDs (e.g., `contents.contents`).

        Returns
        -------
        numpy.typing.NDArray[numpy.float64]
            A NumPy array of float64 representing the user's ratings for all
            content items. Unrated items are represented by 0.

        Raises
        ------
        TypeError
            If `user` is not an instance of the `User` class.
        """
        if not isinstance(user, User):
            raise TypeError("Argument needs to be instance of User")
        return np.array([user.ratings.get(key, np.float64(0)) for key in contents.contents], dtype=np.float64)

    def cos_similarity(self, u: NDArray[np.float64], v: NDArray[np.float64]) -> np.float64:
        """Calculates the cosine similarity between two NumPy vectors.

        Parameters
        ----------
        u : numpy.typing.NDArray[numpy.float64]
            The first vector.
        v : numpy.typing.NDArray[numpy.float64]
            The second vector.

        Returns
        -------
        numpy.float64
            The cosine similarity between the two vectors. Returns 0.0 if
            the denominator (product of norms) is zero to prevent division by zero.
        """
        numerator = np.dot(u, v)
        denominator = np.linalg.norm(u) * np.linalg.norm(v)
        if denominator == 0:
            return np.float64(0)
        return np.float64(numerator/denominator)

    def rate(self, users: U, contents: C) -> None:
        """Computes and stores recommendations for the current consumer using content-based filtering.

        This method builds a TF-IDF matrix from content characteristics,
        constructs a user profile based on the consumer's past ratings,
        calculates the similarity between the user profile and all content items,
        and then updates the `_ratings` and `_recommendations` attributes.

        Parameters
        ----------
        users : U
            An object containing user data. Expected to have a `users` attribute
            which is a dictionary mapping user IDs to `User` objects.
        contents : C
            An object containing content data. Expected to have a `characteristics`
            attribute (a list of dictionaries, where each dictionary represents
            the characteristics of a content item) and an `identifiers` attribute
            (an iterable of all content IDs).

        Returns
        -------
        None

        Notes
        -----
        - The `TfidfVectorizer` from `sklearn.feature_extraction.text` is used
          to convert content features into a numerical TF-IDF matrix.
        - The user profile is calculated as a weighted sum of TF-IDF vectors
          of items rated by the consumer, weighted by their ratings.
        - Item scores are derived from the dot product of the TF-IDF matrix
          and the user profile, scaled by `self._parameters["max"]`.
        - The `_ratings` and `_recommendations` attributes are updated and
          sorted in ascending order of predicted ratings. For typical recommendations,
          a descending order (highest ratings first) is usually desired.
        """
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
        sorting = np.argsort(similarities) # Sorts in ascending order by default
        self._ratings = self._ratings[sorting]
        self._recommendations = self._recommendations[sorting]
    
    def prediction_rate(self, user: U, content: C) -> tuple[NDArray[np.float64], NDArray[C]]:
        """Abstract method to predict ratings for specific users and contents.

        This method must be implemented by concrete subclasses to provide
        predictions for given user(s) and content item(s), primarily used
        for evaluation purposes.

        Parameters
        ----------
        user : U
            The user(s) for whom to predict ratings. Can be a single user ID
            or an array of user IDs, depending on the implementation.
        content : C
            The content item(s) for which to predict ratings. Can be a single
            item ID or an array of item IDs, depending on the implementation.

        Returns
        -------
        tuple[numpy.typing.NDArray[numpy.float64], numpy.typing.NDArray[C]]
            A tuple containing:
            - A NumPy array of predicted ratings (float64) for the given user(s)
              and content(s).
            - A NumPy array of the content identifiers for which predictions
              were made.

        Notes
        -----
        This method is particularly useful for evaluation metrics like MAE and RMSE,
        where predictions for items already rated by a user are needed.
        """
        pass