import numpy as np
import typing
from actors import User

class Ratings:
    
    def __init__(self, users, contents):
        self._users = {user.id: user for user in users}
        self._contents = contents
#        self._ratings_table = "a"
    
    def simple_recommendation(self):
        pass
    
    def user_based_recommendation(self, my_id, k):
        def compute_vectors(user_1: User, user_2: User):
            if not isinstance(user_1, User) or not isinstance(user_2, User):
                raise TypeError("Both arguments must be instances of User")
            
            u1_ratings = user_1.ratings
            u2_ratings = user_2.ratings
            common_keys = sorted(u1_ratings.keys() & u2_ratings.keys())
            
            v1 = np.fromiter((u1_ratings[k] for k in common_keys), dtype=float)
            v2 = np.fromiter((u2_ratings[k] for k in common_keys), dtype=float)
            
            return v1, v2
        
        k_nearest = np.zeros((2,k))
        for user_id in self._users:
            if user_id != my_id:
                u1_vector, u2_vector = compute_vectors(self._users[my_id], self._users[user_id])
                s = np.dot(u1_vector, u2_vector)/(np.linalg.norm(u1_vector)*np.linalg.norm(u2_vector))
                
                if s > k_nearest[0, 0]:
                    k_nearest[0, 0] = s
                    k_nearest[0, 1] = user_id
                    k_nearest = k_nearest[np.argsort(k_nearest[:, 0])]
        
        
    
    def content_based_recommendation(self):
        pass


