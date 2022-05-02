from dataclasses import dataclass
from model.config import Configuration
from model.gene import Gene
from model.generation import Generation
from model.individual import Individual
import random


@dataclass
class Multation:

    rate: float

    def generate_mutants_fixed_percentage(
        self, generation: Generation, config: Configuration
    ) -> Individual:
        qtd = self.rate * len(generation.individuals)
        i = 1
        
        while i < qtd:
            self._modify(
                generation.individuals[random.randint(0, len(generation.individuals)-1)],
                config,
            )
            i += 1
    
    def generate_mutants_probability( self, generation: Generation, config: Configuration
    ) -> Individual:
        for individual in generation.individuals:
            for gene in individual.genes:
                if random.random() < config.mutation_rate:
                    self._modify2(
                        gene,
                        config,
                    )

    def _modify(self, individual: Individual, config: Configuration):
        a = random.randint(config.search_interval_min, config.search_interval_max)
        b = random.random()
        value = a + b

        if value > config.search_interval_max:
            value = config.search_interval_max
        if value < config.search_interval_min:
            value = config.search_interval_min
                
        index = random.randint(0, len(individual.genes)-1)
        individual.genes[index].value = value
    
    def _modify2(self, gene: Gene, config: Configuration):
        a = random.randint(config.search_interval_min, config.search_interval_max)
        b = random.random()
        value = a + b

        if value > config.search_interval_max:
            value = config.search_interval_max
        if value < config.search_interval_min:
            value = config.search_interval_min

        gene.value = value
    