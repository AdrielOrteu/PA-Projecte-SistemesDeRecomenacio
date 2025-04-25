class User:
    
    def __init__(self, id):
        self._id = id
        self._movie_ratings = dict()
    
    def rate_content(self, content, rating):
        self._movie_ratings[content] = rating



class Content:
    
    def __init__(self):
        pass