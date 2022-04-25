from dataclasses import dataclass
from model.config import Configuration
from model.generation import Generation
from model.individual import Individual
import random


@dataclass
class Multation:

    rate: float

    def generate_mutants(
        self, generation: Generation, config: Configuration
    ) -> Individual:
        qtd = (self.rate * len(generation.individuals)) / 100
        i = 0
        while i < qtd:
            self._modify(
                generation.individuals[random.randint(0, len(generation.individuals)-1)],
                config,
            )
            i += 1

    def _modify(self, individual: Individual, config: Configuration):
        a = random.randint(config.search_interval_min, config.search_interval_max)
        b = random.random()
        index = random.randint(0, len(individual.genes)-1)
        individual.genes[index].value = a + b
