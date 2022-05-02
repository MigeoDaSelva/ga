import sys
import re

sys.path.append("./")

import math
from controller.god import God
from model.function import Function
from controller.elitsm import Elitism
from model.config import Configuration
from controller.ga_controller import GAController
from controller.roulette_selection import RouletteSelection
from controller.one_point_crossover import OnePointCrossover
from controller.tournament_selection import TournamentSelection


def find_qtd(variables: list) -> int:
    el = []
    qtd = 0
    for e in variables:
        if e not in el:
            el.append(e)
            qtd += 1
    return qtd


if __name__ == "__main__":

    regex: re = re.compile(r"[x|y|z]")


    config = Configuration(
        # function="-x**4 + 4*x**3 + 30*x**2 - 50*x + 200",
        function="((x)**2+y-11)**2 + (x+(y)**2-7)**2",
        # function=("(math.sin(x-y/8)**2 + math.sin(y+x/8)**2)"
        # "/math.sqrt((x-8.6998)**2 + (y-6.7665)**2 + 1)"),
        mutation_rate=.2,
        intial_population=5,
        generation_amount=10,
        search_interval_max=6,
        search_interval_min=-6,
    )

    god = God(
        config=config, selection=TournamentSelection(10), crossover=OnePointCrossover(),
        elitism=Elitism(number_individuals=3)
    )

    variables = []
    for v in regex.findall(config.function):
        if v not in variables:
            variables.append(v)
    
    function = Function(
        function=config.function,
        qtd_variables=find_qtd(regex.findall(config.function)),
        variables=variables
    )

    ga = GAController(god, function).run(config)

