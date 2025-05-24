import numpy as np
from numpy.typing import NDArray
from abc import ABC, abstractmethod
from typing import List, TypeVar, Any, NoReturn



class Ratings (ABC):
    
    def __init__(self, consumer: int, **parameters) -> None:
        self._consumer : int = consumer # declares the self._consumer type to be an int and sets it's value
        self._parameters : dict[str, Any] = parameters # declares the self._parameters type to be as described and sets it's value
        self._recommendations : NDArray[int] | None = None # we don't know it's size yet, so we just declare its type
        self._ratings : NDArray[np.float64] | None = None # we don't know it's size yet, so we just declare its type
    
    @property
    def consumer(self) -> int:
        return self._consumer
    
    @consumer.setter
    def consumer(self, new_consumer) -> None:
        self._consumer = new_consumer
    
    @property
    def recommendations(self) -> NDArray[int]:
        if self._recommendations is None:
            raise ValueError("recommendations have not been computed yet")
        return self._recommendations
    
    @property
    def ratings(self) -> NDArray[int]:
        if self._ratings is None:
            raise ValueError("recommendations have not been computed yet")
        return self._ratings
    
    @abstractmethod
    def rate(self) -> None:
        pass


class SimpleRatings(Ratings):
    def rate(self) -> None:
        pass #TODO

class CollaborativeRatings(Ratings):
    def rate(self) -> None:
        pass #TODO

class ContentRatings(Ratings):
    def rate(self):
        pass #TODO