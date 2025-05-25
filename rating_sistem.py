import numpy as np
from typing import Callable, Any
from tkinter import *
from tkinter import ttk
import pandas as pd
from actors import User, Content
from sklearn.feature_extraction.text import TfidfVectorizer




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
                raise TypeError("Both arguments must be instances of Users")
            
            u1_ratings = user_1.ratings
            u2_ratings = user_2.ratings
            common_keys = sorted(u1_ratings.keys() & u2_ratings.keys())
            
            v1 = np.fromiter((u1_ratings[k] for k in common_keys), dtype=float)
            v2 = np.fromiter((u2_ratings[k] for k in common_keys), dtype=float)
            
            return v1, v2
        
        def compute_full_u_vector(user_1: User):
            if not isinstance(user_1, User):
                raise TypeError("Both arguments must be instances of Users")
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
        return np.full(len(best_content), u_mean) + best_content[:, 0] / denominator, self._contents[best_content[0, 1]].title
    
    def content_based_recommendation(self):
        item_features = [self._contents[key].get_characteristic("genre") for key in self._contents]
        tfidf = TfidfVectorizer(stop_words='english')
        tfidf_matrix = tfidf.fit_transform(item_features).toarray()
        print(tfidf_matrix)
        


class WindowManager:

    def __init__(self, root_window:Tk):
        self._root_window = root_window
        self._frames = dict()
    
    def clear(self):
        for frame in self._root_window.winfo_children():
            frame.destroy()
    
    def switch_working_window(self):
        pass
    
    def create_start_screen(self, databases: list, combo_command: Callable[[object], str], button_command: Callable[[], Any]):
        self._frames["start"] = Frame(self._root_window, width=100, height=100, bg='#65A8E1')
        self._frames["start"].grid(row=0, column=0, padx=5, pady=5)
        
        settings_button = Button(self._frames["start"], text="SETTINGS", font=("bold", 12), bg="#88d1b9", width=20, command=button_command)
        settings_button.grid(row=0, column=1)
        
        database_combo = ttk.Combobox(self._frames["start"], values=databases, width=40)
        database_combo.set("SELECT THE CONTENT YOU WANT")
        database_combo.grid(row=0, column=0)
        
        database_combo.bind("<<ComboboxSelected>>", combo_command)
    
    def login_toolbar(self, intro_command: Callable[[], Any]):
        self._frames["login"] = Frame(self._root_window, width=100, height=100, bg='#65A8E1')
        self._frames["login"].grid(row=1, column=0, padx=5, pady=5)
        identity_entry = Entry(self._frames["login"], width=15, fg='blue', font=('Arial', 16, 'bold'))
        password_entry = Entry(self._frames["login"], width=15, fg='blue', font=('Arial', 16, 'bold'))
        intro_button = Button(self._frames["login"], text="ENTER", font=("bold", 12), bg="#88d1b9", width=20, command=intro_command)
    
    def create_settings_screen(self):
        pass
    
    def create_rating_method_screen(self, combo_command: Callable[[object], str]):
        self._frames["rating_method"] = Frame(self._root_window, width=100, height=100, bg='#65A8E1')
        self._frames["rating_method"].grid(row=0, column=0, padx=5, pady=5)
        
        rating_method_combo = ttk.Combobox(self._frames["rating_method"], values=["SIMPLE", "COLLABORATIVE", "SIMILAR CONTENT"], width=40)
        rating_method_combo.set("SELECT THE RECOMMENDATION METHOD")
        rating_method_combo.grid(row=0, column=0)
        
        rating_method_combo.bind("<<ComboboxSelected>>", combo_command)
    
    def create_recommendation_display(self):
        self._frames["recommendation_display"] = Frame(self._root_window, width=100, height=100, bg='#65A8E1')
        self._frames["recommendation_display"].grid(row=1, column=0, padx=5, pady=5)
        
        title_label = Label(self._frames["recommendation_display"], text="title_label", bg="#65A8E1", font=("bold", 24))
        id_label = Label(self._frames["recommendation_display"], text="id_label", bg="#65A8E1", font=("bold", 24))
        description_label = Label(self._frames["recommendation_display"], text="description_label", bg="#65A8E1", font=("bold", 24))
        
        title_label.grid(row=0, column=0, padx=5, pady=5)
        id_label.grid(row=0, column=1, padx=5, pady=5)
        description_label.grid(row=1, column=0, padx=5, pady=5)
        
        

#class MainClass:
#
#    def __init__(self, window_manager: WindowManager):
#        self._users = []
#        self._content = []
#        self._window_manager = window_manager
#
#
#
#    def main_function(self):
#        with open("databases.csv", "r") as db_storage:
#            databases = [db for db in db_storage]
#        self._window_manager.create_start_screen(databases=databases, combo_command=self.db_combo_command, button_command=self.settings)
#
#    def db_combo_command (self, event):
#        selected_item = event.widget.get()
#        self.load_movie_users()
#        self._window_manager.
#        return selected_item
#
#    def login(self, user, database):
#        self.load_movie_users()
#
#    def settings(self):
#        print("opening settings...")
#
#    def load_movie_users(self):
#        ratings = pd.read_csv("movies/Ratings.csv")
#        user_id = ratings.iloc[:, 0]
#        tmp_lst = []
#        for identifier in user_id:
#            n = 0
#            if identifier not in tmp_lst:
#                self._users.append(Users(identifier))
#                tmp_lst.append(identifier)
#
#    def load_movie_user_ratings(self):
#        ratings = pd.read_csv("movies/Ratings.csv")
#        for i, id in enumerate(ratings["userId"]):
#            for user in self._users:
#                if user.id == id:
#                    user.rate_content(content=ratings.iloc[i, 1], rating=ratings.iloc[i, 2])
#
#    def load_movies(self):
#        movies = pd.read_csv("movies/movies.csv")
#        for row in movies.iterables(index=False, name='Pandas'):
#            self._content.append(Contents(id=row.movieId, title=row.title, genres=row.genres))

