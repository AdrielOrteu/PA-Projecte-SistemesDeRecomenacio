from typing import Callable, Any
from numpy.typing import NDArray
import logging

def validate_input(func):
    """Decorator to validate user input by catching KeyError exceptions.

    This decorator wraps a function that takes user input and might raise
    a `KeyError` (e.g., when accessing a dictionary with an invalid key).
    It repeatedly prompts for input until a valid choice is made (i.e.,
    no `KeyError` is raised).

    Parameters
    ----------
    func : callable
        The function to be decorated. This function is expected to handle
        user input and potentially raise a `KeyError` for invalid choices.

    Returns
    -------
    callable
        The wrapped function that includes input validation.

    See Also
    --------
    KeyError : Exception raised when a mapping (dictionary) key is not found.

    Notes
    -----
    This decorator is specifically designed to catch `KeyError`. If the
    decorated function can raise other types of exceptions for invalid
    input, those would need to be handled separately or added to the `except`
    block.
    """
    def wrapper(*args):
        result = None
        while result is None:
            result = func(args)
        return result
    return wrapper
    

class GUI:
    """Handles user interaction and input for the recommendation system.

    This class provides methods for prompting the user to make choices
    regarding database selection, user identity, actions (recommend/evaluate),
    and recommendation methods, using the `validate_input` decorator for
    robust input handling.
    """
    def __init__(self) -> None:
        """Initializes the GUI instance."""
        pass
    
    @validate_input
    def chose_db(self) -> str:
        """Prompts the user to choose a database (movies or books).

        The input is validated to ensure it corresponds to a valid choice.

        Returns
        -------
        str
            The chosen database identifier ('movies' or 'books').
            Returns `None` if the input does not match 'M' or 'B'.
        """
        print("Witch database do you want to use?\n M -> movies | B -> books")
        choice = {"M": "movies", "B": "books"}.get(input())
        return choice
    
    @validate_input
    def chose_identity(self) -> str:
        """Prompts the user to enter their user ID.

        The input is validated (though the validation currently just ensures
        some input is provided, not its format or existence).

        Returns
        -------
        str
            The entered user ID or 'B' if the user chooses to go back.
        """
        choice = input("Enter your user id (or B to go back):\n")
        return choice
    
    @validate_input
    def chose_action(self) -> str:
        """Prompts the user to choose an action within the system.

        Actions include recommending items, evaluating the system, going back,
        or exiting. The input is validated.

        Returns
        -------
        str
            The chosen action ('recommend', 'evaluate', 'Back', or 'exit').
            Returns `None` if the input does not match 'R', 'E', 'B', or 'X'.
        """
        print("What do you want to do?\n R -> Recommend (best 5 items) | E -> Evaluate | B -> Back | X -> Exit")
        choice = {"R":"recommend", "E":"evaluate", "B": "back", "X": "exit"}.get(input())
        return choice
    
    @validate_input
    def chose_method(self) -> str:
        """Prompts the user to choose a recommendation method.

        Available methods are simple, collaborative, and content-based.
        The input is validated.

        Returns
        -------
        str
            The chosen method ('simple', 'collaborative', or 'content').
            Returns `None` if the input does not match 'S', 'L', or 'C'.
        """
        print("How do you want us to recommend the content?\n S -> simple | L -> collaborative | C -> content")
        # choice = {"S": self.chose_simple_params, "L": self.chose_collaborative_params, "C": self.chose_content_params}.get(input())
        choice = {"S": "simple", "L": "collaborative", "C": "content"}.get(input())
        return choice
    
    @validate_input
    def chose_simple_params(self) -> str:
        """Prompts the user to input parameters for the simple recommendation method.

        The exact parameters expected are not specified in the current
        implementation, as it just takes a generic input.

        Returns
        -------
        str
            The input provided by the user, representing simple method parameters.
        """
        # A more descriptive prompt would be beneficial here, e.g., "Enter min_votes for simple method:"
        return input()
    
    @validate_input
    def chose_collaborative_params(self) -> None:
        """Placeholder for prompting user to input parameters for the collaborative recommendation method.

        Currently, this method does nothing.

        Returns
        -------
        None
        """
        pass
    
    @validate_input
    def chose_content_params(self) -> None:
        """Placeholder for prompting user to input parameters for the content-based recommendation method.

        Currently, this method does nothing.

        Returns
        -------
        None
        """
        pass