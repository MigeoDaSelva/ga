from controller.crossover import Crossover
from controller.mutation import Multation
from controller.selection import Selection
from dataclasses import dataclass, field
from model.generation import Generation
from model.individual import Individual
from model.config import Configuration
from controller.elitsm import Elitism
from model.function import Function
from model.gene import Gene
import random


@dataclass(
    repr=False,
)
class God:
    config: Configuration
    selection: Selection
    crossover: Crossover
    elitism: Elitism = field(default=None)

    def generate_init_generation(self, function: Function) -> Generation:
        individuals = []
        print("Gerando geração inicial...")
        while len(individuals) < self.config.intial_population:
            individuals.append(self.create_individual(function))

        return Generation(number=1, individuals=individuals)

    def generate_next_generation(self, generation: Generation):
        individuals = []

        print(f"Gerando geração {generation.number+1}...")

        if self.elitism:
            individuals.extend(self.elitism.get_elite(generation))

        while len(individuals) < self.config.intial_population:
            father = self.selection.select(generation)
            mather = self.selection.select(generation)
            individuals.extend(self.crossover.cross(father=father, mother=mather))
        generation = Generation(number=generation.number + 1, individuals=individuals)

        mutation = Multation(self.config.mutation_rate)

        mutation.generate_mutants_probability(generation=generation, config=self.config)

        return generation

    def create_individual(self, function: Function):
        genes = []

        while len(genes) < function.qtd_variables:
            a = random.randint(
                self.config.search_interval_min, self.config.search_interval_max
            )
            b = random.random()

            value = a + b

            if value > self.config.search_interval_max:
                value = self.config.search_interval_max
            if value < self.config.search_interval_min:
                value = self.config.search_interval_min

            genes.append(Gene(value))

        return Individual(genes)
