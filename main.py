import sys


sys.path.append("./")

from controller.tournament_selection import TournamentSelection
from controller.one_point_crossover import OnePointCrossover
from controller.roulette_selection import RouletteSelection
from controller.ga_controller import GAController
from model.config import Configuration
from model.function import Function
from controller.god import God
import re


if __name__ == "__main__":
    
    regex: re = re.compile(r"x")

    config = Configuration(
        function="x**2+x",
        mutation_rate=0.5,
        intial_population=100,
        generation_amount=100,
        search_interval_max=100,
        search_interval_min=-100,
    )

    god = God(
        config=config, selection=TournamentSelection(5), crossover=OnePointCrossover()
    )

    function = Function(
            function=config.function,
            qtd_variables=len(regex.findall(config.function)),
            terms=config.function.split(";"),
        )

    ga = GAController(god, function).run(config)
