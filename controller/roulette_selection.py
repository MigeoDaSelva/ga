from controller.selection import Selection
from model.generation import Generation
from model.individual import Individual
from random import randint
from typing import List


class RouletteSelection(Selection):
    def select(self, generation: Generation) -> Individual:
        roulette = self._generate_roulette(generation)
        # print("###########################")
        # print(len(roulette))
        # print("****************************")
        # print(len(generation.individuals))
        # print("----------------------------")
        number = randint(0, len(roulette)-1)
        # print(number)
        return roulette[number]

    def _get_percentage(self, total: float, fitness: float) -> int:
        return int((100 * fitness) / total)

    def _generate_roulette(self, generation: Generation) -> List[Individual]:
        roulette = []
        total = generation.total_fitness()
        for individual in generation.individuals:
            qtd = self._get_percentage(total, individual.fitness)
            roulette.extend([individual] * qtd)
        return roulette
