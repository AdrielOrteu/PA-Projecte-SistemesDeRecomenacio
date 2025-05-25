from typing import Callable, Any
from numpy.typing import NDArray

def validate_input(func):
    def wrapper():
        valid = False
        while not valid:
            try:
                result = func()
            except KeyError:
                print("Your choice isn't valid")
            else:
                valid = True
        return result
    return wrapper
    

class GUI:
    def __init__(self) -> None:
        pass
    
    @validate_input
    def chose_db(self) -> str:
        print("Witch database do you want to use?\n M -> movies | B -> books")
        choice = {"M": "movies", "B": "books"}.get(input())
        return choice # after the
    
    @validate_input
    def chose_identity(self) -> str:
        choice = input("Enter your user id (or B to go back):\n")
        return choice
    
    @validate_input
    def chose_action(self) -> str:
        print("What do you want to do?\n R -> Recommend (best 5 items) | E -> Evaluate | B -> Back | X -> Exit")
        choice = {"R":"recommend", "E":"evaluate", "B": "Back", "X": "exit"}.get(input())
        return choice
    
    @validate_input
    def chose_method(self) -> str:
        print("How do you want us to recommend the content?\n S -> simple | L -> collaborative | C -> content")
        # choice = {"S": self.chose_simple_params, "L": self.chose_collaborative_params, "C": self.chose_content_params}.get(input())
        choice = {"S": "simple", "L": "collaborative", "C": "content"}.get(input())
        return choice
    
    @validate_input
    def chose_simple_params(self):
        
        return input()
    
    @validate_input
    def chose_collaborative_params(self):
        pass
    
    @validate_input
    def chose_content_params(self):
        pass