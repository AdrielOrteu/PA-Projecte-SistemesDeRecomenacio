from abc import ABC, abstractmethod

class User:
    
    def __init__(self, id):
        self._id = id
        self._ratings = dict()
    
    def rate_content(self, content, rating):
        self.ratings[content] = rating
    
    def __str__(self):
        return f"{self._id}"
    
    @property
    def id(self):
        return self._id
    
    @property
    def ratings(self):
        return self._ratings

class Content:
    
    def __init__(self, id, title, characteristics, rating=0):
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
    
    @property
    def characteristics(self):
        return self._characteristics


