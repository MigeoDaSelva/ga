from distutils.command.config import config
from model.function import Function
from model.generation import Generation
from model.individual import Individual
from model.config import Configuration
from dataclasses import dataclass
from model.gene import Gene
import random


@dataclass(
    repr=False,
)
class God:
    config: Configuration

    def generate_init_generation(self, function: Function):
        individuals = []

        while len(individuals) < self.config.intial_population:
            individuals.append(self.create_individual(function))

        return Generation(number=1, individuals=individuals)

    def create_individual(self, function: Function):
        genes = []

        while len(genes) < len(function.terms):
            a = random.randint(config.search_interval_min,
                               config.search_interval_max)
            b = random.random()
            genes.append(Gene(a + b))

        return Individual(genes)
