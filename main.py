import pandas as pd
from rating_sistem import Ratings
from actors import User, Content
import numpy as np

users = []
content = []

def load_users(u):
    ratings = pd.read_csv("movies/ratings.csv")
    user_id = ratings.iloc[:, 0]
    tmp_lst = []
    for identifier in user_id:
        n=0
        if identifier not in tmp_lst:
            u.append( User(identifier) )
            tmp_lst.append(identifier)

def load_user_ratings(u):
    print(u)
    ratings = pd.read_csv("movies/ratings.csv")
    for i, id in enumerate(ratings["userId"]):
        for user in u:
            #print(id, user.id)
            if user.id == id:
                user.rate_content(content=ratings.iloc[i, 1], rating=ratings.iloc[i, 2])
                print(user.ratings)


def load_movies(m):
    movies = pd.read_csv("movies/movies.csv")
    for row in movies.itertuples(index=False, name='Pandas'):
        m.append(Content(id=row.movieId, title=row.title, genres=row.genres))

load_users(users)
load_user_ratings(users)
print(np.int64(170875))
