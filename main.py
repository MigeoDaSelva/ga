import sys
import re

sys.path.append("./")

from controller.god import God
from model.function import Function
from controller.elitsm import Elitism
from model.config import Configuration
from controller.ga_controller import GAController
from controller.roulette_selection import RouletteSelection
from controller.one_point_crossover import OnePointCrossover
from controller.tournament_selection import TournamentSelection


if __name__ == "__main__":

    regex: re = re.compile(r"x")  # TODO: ajustar para pegar letras diferentes

    config = Configuration(
        function="-x**4 + 4*x**3 + 30*x**2 - 50*x + 200",
        mutation_rate=10,
        intial_population=50,
        generation_amount=500,
        search_interval_max=1000,
        search_interval_min=-1000,
    )

    god = God(
        config=config, selection=TournamentSelection(5), crossover=OnePointCrossover(),
        elitism=Elitism(number_individuals=3)
    )

    function = Function(
        function=config.function,
        qtd_variables=len(regex.findall(config.function)),
    )

    ga = GAController(god, function).run(config)
