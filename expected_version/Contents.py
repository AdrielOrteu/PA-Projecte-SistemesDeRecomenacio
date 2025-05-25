import numpy as np
import pandas as pd
from numpy.typing import NDArray
from abc import ABC, abstractmethod
import typing
from typing import List, TypeVar, Any, NoReturn


class Content:
    
    def __init__(self, identifier: str, title: str, **characteristics) -> None:
        self._identifier : str = identifier
        self._title : str = title
        self._characteristics : dict[str, Any] = characteristics
    
    @property
    def identifier(self) -> str:
        return self._identifier
    @identifier.setter
    def identifier(self, new_identifier: str) -> None:
        self._identifier = new_identifier
    
    @property
    def title(self) -> str:
        return self._title
    @title.setter
    def title(self, new_title: str) -> None:
        self._title = new_title
    
    @property
    def characteristics(self) -> dict[str, Any]:
        return self._characteristics


class Contents(ABC):
    def __init__(self) -> None:
        self._contents: dict[str, Content] = dict()
    
    @property
    def contents(self) -> dict[str, Content]:
        if self._contents == dict():
            raise ValueError("contents are not loaded")
        return self._contents
    
    @property
    def identifiers(self) -> NDArray[str]:
        if self._contents == dict():
            raise ValueError("contents are not loaded")
        return np.array(self._contents.keys())
    
    @property
    def titles(self) -> NDArray[str]:
        if self._contents == dict():
            raise ValueError("contents are not loaded")
        return np.array([self._contents[identifier].title for identifier in self._contents])
    
    @property
    def characteristics(self) -> NDArray[dict[str, Any]]:
        if self._contents == dict():
            raise ValueError("contents are not loaded")
        return np.array([self._contents[identifier].characteristics for identifier in self._contents])
    
    @abstractmethod
    def load_contents(self) -> None:
        pass
    
    @abstractmethod
    def save_contents(self):
        pass


class Books(Contents):
    def load_contents(self) -> None:
        """
        Loads the books into the contents attribute
        Loads the id, title, author, YearOfPublication, publisher
        """
        content_df = pd.read_csv("books/Books.csv")
        for book in content_df.itertuples(index=False, name='Pandas'):
            print(f"TITLE\nvalue={book.BookTitle} | type={type(book.BookTitle)}")
            print(f"IDENTIFIER\nvalue={book.ISBN} | type={type(book.ISBN)}")
            print()
            self._contents[book.ISBN] = Content(identifier=book.ISBN, title=book.BookTitle, BookAuthor=book.BookAuthor,
                                                YearOfPublication=book.YearOfPublication, Publisher=book.Publisher)
        #print(self._contents)
    def save_contents(self):
        pass #TODO


class Movies(Contents):
    def load_contents(self) -> None:
        """
        Loads the movies into the contents attribute
        Loads the id, title, genres
        """
        movies_df = pd.read_csv("movies/movies.csv")
        for movie in movies_df.itertuples(index=False, name='Pandas'):
            print(movie)
            self._contents[movie.movieId]= Content(identifier=movie.movieId,title=movie.title, genres=movie.genres)
    
    def save_contents(self):
        pass #TODO
