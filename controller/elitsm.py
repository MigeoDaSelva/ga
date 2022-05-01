from operator import ge
from model.generation import Generation
from model.individual import Individual
from dataclasses import dataclass
from typing import List


@dataclass
class Elitism:

    number_individuals: int

    def get_elite(self, generation: Generation) -> List[Individual]:
        individuals_copy = generation.individuals.copy()
        individuals_copy.sort(
            key=lambda individual: individual.fitness, reverse=True)

        return individuals_copy[:self.number_individuals]
