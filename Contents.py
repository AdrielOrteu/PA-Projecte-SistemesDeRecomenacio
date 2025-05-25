import numpy as np
import pandas as pd
from numpy.typing import NDArray
from abc import ABC, abstractmethod
import typing
from typing import List, TypeVar, Any, NoReturn


class Content:
    """
    Represents a piece of content with an identifier, title, and additional characteristics.

    This class is intended to serve as a base or general-purpose content representation,
    such as movies, books, articles, etc.

    Attributes
    ----------
    identifier : str
        Unique identifier for the content (e.g., a stringified ID).
    title : str
        Human-readable title or name of the content.
    characteristics : dict[str, str]
        Dictionary of named characteristics (e.g., genre, author, year), where keys and values are strings.

    Examples
    --------
    >>> c = Content(identifier="42", title="The Hitchhiker's Guide", genre="Sci-Fi", author="Douglas Adams")
    >>> c.title
    "The Hitchhiker's Guide"
    >>> c.characteristics["genre"]
    "Sci-Fi"
    """

    def __init__(self, identifier: str, title: str, **characteristics) -> None:
        """
        Initialize a new Content instance.

        Parameters
        ----------
        identifier : str
            Unique identifier for the content.
        title : str
            Title or name of the content.
        **characteristics : dict[str, str]
            Additional keyword arguments representing content characteristics (e.g., genre, director, etc.).
        """
        self._identifier: str = identifier
        self._title: str = title
        self._characteristics: dict[str, str] = characteristics

    @property
    def identifier(self) -> str:
        """
        Get the identifier of the content.

        Returns
        -------
        str
            The content's unique identifier.
        """
        return self._identifier

    @identifier.setter
    def identifier(self, new_identifier: str) -> None:
        """
        Set a new identifier for the content.

        Parameters
        ----------
        new_identifier : str
            The new identifier to assign.
        """
        self._identifier = new_identifier

    @property
    def title(self) -> str:
        """
        Get the title of the content.

        Returns
        -------
        str
            The title of the content.
        """
        return self._title

    @title.setter
    def title(self, new_title: str) -> None:
        """
        Set a new title for the content.

        Parameters
        ----------
        new_title : str
            The new title to assign.
        """
        self._title = new_title

    @property
    def characteristics(self) -> dict[str, str]:
        """
        Get the dictionary of characteristics associated with the content.

        Returns
        -------
        dict[str, str]
            Dictionary mapping characteristic names to their values (as strings).
        """
        return self._characteristics
    
    def __str__(self):
        return f"{self.title}"



class Contents(ABC):
    """
    Abstract base class for managing a collection of `Content` objects.

    Provides properties for accessing metadata such as identifiers, titles,
    and characteristics of all content entries. Subclasses must implement
    the `load_contents` method to populate the internal storage.

    Attributes
    ----------
    contents : dict[str, Content]
        A dictionary mapping content identifiers to `Content` objects.
    identifiers : numpy.ndarray of str
        An array of all content identifiers.
    titles : numpy.ndarray of str
        An array of content titles.
    characteristics : numpy.ndarray of dict[str, str]
        An array of characteristic dictionaries for each content item.

    Raises
    ------
    ValueError
        If any property is accessed before contents are loaded.
    """

    def __init__(self) -> None:
        """
        Initialize the contents collection as an empty dictionary.
        """
        self._contents: dict[str, Content] = dict()

    @property
    def contents(self) -> dict[str, Content]:
        """
        Access the dictionary of loaded content.

        Returns
        -------
        dict[str, Content]
            A dictionary mapping content identifiers to `Content` instances.

        Raises
        ------
        ValueError
            If contents have not yet been loaded.
        """
        if self._contents == dict():
            raise ValueError("contents are not loaded")
        return self._contents

    @property
    def identifiers(self) -> NDArray[str]:
        """
        Get all content identifiers as a NumPy array.

        Returns
        -------
        numpy.ndarray of str
            An array of content identifiers.

        Raises
        ------
        ValueError
            If contents have not yet been loaded.
        """
        if self._contents == dict():
            raise ValueError("contents are not loaded")
        return np.array([identifier for identifier in self._contents.keys()])

    @property
    def titles(self) -> NDArray[str]:
        """
        Get all content titles as a NumPy array.

        Returns
        -------
        numpy.ndarray of str
            An array of titles corresponding to each content item.

        Raises
        ------
        ValueError
            If contents have not yet been loaded.
        """
        if self._contents == dict():
            raise ValueError("contents are not loaded")
        return np.array([self._contents[identifier].title for identifier in self._contents])

    @property
    def characteristics(self) -> NDArray[dict[str, str]]:
        """
        Get characteristics for all content items as a NumPy array.

        Returns
        -------
        numpy.ndarray of dict[str, str]
            An array where each element is a dictionary of characteristics.

        Raises
        ------
        ValueError
            If contents have not yet been loaded.
        """
        if self._contents == dict():
            raise ValueError("contents are not loaded")
        return np.array([self._contents[identifier].characteristics for identifier in self._contents])

    @abstractmethod
    def load_contents(self) -> None:
        """
        Abstract method to load content data into the `_contents` dictionary.

        This must be implemented by any subclass to define how content is loaded.
        """
        pass



class Books(Contents):
    """
    Concrete subclass of `Contents` for handling book metadata.

    Loads book information from a CSV file and stores it in the `_contents` dictionary,
    mapping ISBNs to `Content` instances.

    Notes
    -----
    The CSV file `"books/Books.csv"` is expected to contain the following columns:
        - ISBN (used as identifier)
        - BookTitle
        - BookAuthor
        - YearOfPublication
        - Publisher

    Examples
    --------
    >>> books = Books()
    >>> books.load_contents()
    >>> books.contents["034545104X"].title
    'The Fellowship of the Ring'
    """

    def load_contents(self) -> None:
        """
        Load book metadata from a CSV file into the contents' collection.

        Loads the following fields for each book:
            - identifier: ISBN (as str)
            - title: BookTitle
            - characteristics:
                - BookAuthor
                - YearOfPublication
                - Publisher

        Populates the `_contents` dictionary with `Content` instances keyed by ISBN.

        Raises
        ------
        FileNotFoundError
            If "books/Books.csv" is not found.
        ValueError
            If required columns are missing from the CSV.
        """
        content_df = pd.read_csv("books/Books.csv")

        for book in content_df.itertuples(index=False, name='Pandas'):
            print(f"TITLE\nvalue={book.BookTitle} | type={type(book.BookTitle)}")
            print(f"IDENTIFIER\nvalue={book.ISBN} | type={type(book.ISBN)}\n")

            self._contents[book.ISBN] = Content(
                identifier=book.ISBN,
                title=book.BookTitle,
                BookAuthor=book.BookAuthor,
                YearOfPublication=book.YearOfPublication,
                Publisher=book.Publisher
            )
class Movies(Contents):
    """
    Concrete subclass of `Contents` for handling movie metadata.

    Loads movie information from a CSV file and stores it in the `_contents` dictionary,
    mapping movie IDs to `Content` instances.

    Notes
    -----
    The CSV file `"movies/movies.csv"` is expected to contain at least the following columns:
        - movieId (used as identifier)
        - title (movie title)
        - genres (pipe-separated string of genres)

    Examples
    --------
    >>> movies = Movies()
    >>> movies.load_contents()
    'Toy Story (1995)'
    """

    def load_contents(self) -> None:
        """
        Load movie metadata from a CSV file into the contents collection.

        Loads the following fields for each movie:
            - identifier: movieId (as str)
            - title: title (movie title)
            - characteristics:
                - genres (pipe-separated string of genres)

        Populates the `_contents` dictionary with `Content` instances keyed by movie ID.

        Raises
        ------
        FileNotFoundError
            If "movies/movies.csv" is not found.
        ValueError
            If required columns are missing from the CSV.
        """
        movies_df = pd.read_csv("movies/movies.csv")

        for movie in movies_df.itertuples(index=False, name='Pandas'):
            self._contents[movie.movieId] = Content(
                identifier=movie.movieId,
                title=movie.title,
                genres=movie.genres
            )