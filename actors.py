from abc import ABC, abstractmethod

class User:
    
    def __init__(self, id):
        self._id = id
        self._movie_ratings = dict()
    
    def rate_content(self, content, rating):
        self._movie_ratings[content] = rating
    
    def __str__(self):
        return f"{self._id}"
    
    @property
    def id(self):
        return self._id

class Content:
    
    def __init__(self, id, title, rating=0, **characteristics):
        self._id = id
        self._title = title
        self._characteristics = characteristics
        self._rating = rating
    
    def actualize_rating(self):
        pass
    
    @property
    def id(self):
        return self._id
    
    @property
    def rating(self):
        return self._rating
    
    @property
    def title(self):
        return self._title
    
    def get_characteristic(self, characteristic):
        try:
            return self._characteristics[characteristic]
        except KeyError:
            return None


