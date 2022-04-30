from controller.selection import Selection
from model.generation import Generation
from model.individual import Individual
from dataclasses import dataclass
from random import randint


@dataclass
class TournamentSelection(Selection):

    k: int

    def select(self, generation: Generation) -> Individual:
        sample = [generation.individuals[randint(0, len(generation.individuals) - 1)]] * self.k
        return max(sample, key=lambda individual: individual.fitness)
