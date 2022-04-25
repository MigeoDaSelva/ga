from dataclasses import dataclass
from model.function import Function

from model.generation import Generation

@dataclass
class Avaliator:
    function: Function

    def avaliate_fitness(self, generation: Generation):
        for individual in generation.individuals:
            result = self.function.resolve([gene.value for gene in individual.genes])
            individual.__setattr__("fitness", result)