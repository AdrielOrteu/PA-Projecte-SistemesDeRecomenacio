import pandas as pd
from rating_sistem import Ratings
from actors import User, Content

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
########################################################
    for line in ratings["userId"]:
        
        print(ratings.iloc[line, :])
        print("#######")

def load_movies(m):
    movies = pd.read_csv("movies/movies.csv")
    for row in movies.itertuples(index=False, name='Pandas'):
        print(f"id: {row.movieId}, title: {row.title}, genres:{row.genres}")
        print("#####")
    # m.append(Content(id=identifier, title=titol, genres=generes) )

load_movies(users)
