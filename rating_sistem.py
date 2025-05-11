import numpy as np
import typing
import tkinter as tk
from actors import User

class Ratings:
    
    def __init__(self, users, contents):
        self._users = {user.id: user for user in users}
        self._contents = {content.id: content for content in contents}
#        self._ratings_table = "a"
    
    def simple_recommendation(self):
        pass
    
    def user_based_recommendation(self, my_id, k, num_recommendations=1):
        def compute_restricted_u_vectors(user_1: User, user_2: User):
            if not isinstance(user_1, User) or not isinstance(user_2, User):
                raise TypeError("Both arguments must be instances of User")
            
            u1_ratings = user_1.ratings
            u2_ratings = user_2.ratings
            common_keys = sorted(u1_ratings.keys() & u2_ratings.keys())
            
            v1 = np.fromiter((u1_ratings[k] for k in common_keys), dtype=float)
            v2 = np.fromiter((u2_ratings[k] for k in common_keys), dtype=float)
            
            return v1, v2
        
        def compute_full_u_vector(user_1: User):
            if not isinstance(user_1, User):
                raise TypeError("Both arguments must be instances of User")
            return np.array([user_1.ratings.get(key,0) for key in self._contents])
        
        k_nearest = np.zeros((k, 2))
        for user_id in self._users:
            if user_id != my_id:
                u1_vector, u2_vector = compute_restricted_u_vectors(self._users[my_id], self._users[user_id])
                
                norm1 = np.linalg.norm(u1_vector)
                norm2 = np.linalg.norm(u2_vector)
                if norm1 == 0 or norm2 == 0:
                    continue  # skip this user
                s = np.dot(u1_vector, u2_vector) / (norm1 * norm2)
                
                if s > k_nearest[0, 0]:
                    #print(f"#########\n##### {user_id} #####")
                    #print(k_nearest)
                    #print(u2_vector)
                    k_nearest[0, 0] = s
                    k_nearest[0, 1] = user_id
                    k_nearest = k_nearest[np.argsort(k_nearest[:, 0])]
                    #print(k_nearest)
        
        k_nearest_ratings = np.stack([compute_full_u_vector(self._users[u[1]]) for u in k_nearest]) # THIS
        
        best_content = np.zeros((2,num_recommendations))
        
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
        
        print(f"{u_mean}+{best_content[:, 0]}/{denominator}\n{best_content[:, 1]}  {self._contents[best_content[0, 1]]}\n{self._contents[best_content[0, 1]].id}\n")
        print(np.full(len(best_content), u_mean) + best_content[:, 0] / denominator)
        print("\n\n")
        return np.full(len(best_content), u_mean) + best_content[:, 0] / denominator
    
    def content_based_recommendation(self):
        pass


class WindowManager:
    
    def __init__(self, root_window):
        self._root_window = root_window
    
    def clear(self):
        for frame in self._root_window.winfo_children():
            frame.destroy()
