from typing import List
from dataclasses import dataclass
from model.individual import Individual


@dataclass
class Generation:

    number: int
    individuals: List[Individual]
    the_best: Individual = None

    def total_fitness(self) -> float:
        return abs(sum([individual.fitness for individual in self.individuals]))

    def set_best(self):
        for individual in self.individuals:
            if self.the_best:
                if individual.fitness > self.the_best.fitness:
                    self.the_best = individual
            else:
                self.the_best = individual

    def get_best(self):
        return max(self.individuals, key=lambda individual: individual.fitness)
