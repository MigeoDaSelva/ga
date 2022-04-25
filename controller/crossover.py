from model.individual import Individual
from abc import ABC, abstractmethod


class Crossover(ABC):
    @abstractmethod
    def cross(self, father: Individual, mother: Individual):
        pass