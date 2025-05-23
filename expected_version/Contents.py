import numpy as np
import pandas as pd
from numpy.typing import NDArray
from abc import ABC, abstractmethod
import typing
from typing import List, TypeVar, Any, NoReturn

class Contents(ABC):
    def __init__(self) -> None:
        self._contents: dict[str, tuple[str, dict[str, Any]]] | None = None # { "id":("title", {characteristics}), ...}
    
    @property
    def contents(self) -> list[tuple[str, str, dict[str, Any]]]:
        if self._contents is None:
            raise ValueError("contents are not loaded")
        return self._contents
    
    @property
    def identifiers(self) -> NDArray[str]:
        if self._contents is None:
            raise ValueError("contents are not loaded")
        return np.array([content[0] for content in self._contents])
    
    @property
    def titles(self) -> NDArray[str]:
        if self._contents is None:
            raise ValueError("contents are not loaded")
        return np.array([content[1] for content in self._contents])
    
    @property
    def characteristics(self) -> NDArray[dict[str, Any]]:
        if self._contents is None:
            raise ValueError("contents are not loaded")
        return np.array([content[2] for content in self._contents])
    
    @abstractmethod
    def load_content(self) -> None:
        pass


C = TypeVar('C', bound=Contents)


class Books(Contents):
    def load_content(self) -> None:
        """Loads the books into the contents attribute"""
        content_df = pd.read_csv("books/Books.csv")
        for book in content_df.iterables(index=False, name='Pandas'):
            self._contents.append((book.ISBN,
                                   book.BookTitle,
                                   {"BookAuthor":book.BookAuthor,
                                    "YearOfPublication":book.YearOfPublication,
                                    "Publisher":book.Publisher}))


class Movies(Contents):
    def load_content(self) -> None:
        """Loads the movies into the contents attribute"""
        movies_df = pd.read_csv("movies/movies.csv")
        for movie in movies_df.iterables(index=False, name='Pandas'):
            self._contents.append((movie.movieId, movie.title, {"genres":movie.genres}))
