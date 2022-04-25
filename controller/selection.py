from model.generation import Generation
from model.individual import Individual
from abc import ABC, abstractmethod


class Selection(ABC):
    @abstractmethod
    def select(self, generatio: Generation) -> Individual:
        pass
