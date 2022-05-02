import sys


sys.path.append("./")

from controller.tournament_selection import TournamentSelection
from controller.one_point_crossover import OnePointCrossover
from controller.roulette_selection import RouletteSelection
from controller.ga_deap_controller import GADeapController
from controller.ga_controller import GAController
from model.config_deap import ConfigurationDeap
from model.function_deap import FunctionDeap
from controller.god_deap import GodDeap
from model.config import Configuration
from controller.elitsm import Elitism
from model.function import Function
import plotly.graph_objects as go
from controller.god import God
import plotly.express as px
import pandas as pd
import re


def find_qtd(variables: list) -> int:
    el = []
    qtd = 0
    for e in variables:
        if e not in el:
            el.append(e)
            qtd += 1
    return qtd


def run_ga():

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

def run_ga_deap():
    
    config = ConfigurationDeap(
        mate= "two_point",
        mutate="flip_bit",
        select= "tournament",
        tournsize = 5,
        qtd_variables=2,
        population_size=500,
        no_of_generations=1000,
        probabilityCrossed=0.5,
        probabilityMutating=0.30
    )
     
    function = FunctionDeap(
        qtd_variables=config.qtd_variables,
        bounds=[(-10, 10)] * config.qtd_variables,
        function_name="gradient descent" # himmelblau or h1 or five_variables
    )

    god = GodDeap(
        config=config,
        function=function
    )

    ga = GADeapController(god=god, config=config)
    ga.run()
    ga.plot_result()


def export_csv():
    
    df_log = pd.read_csv("./files/result.csv")
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df_log['Generation'], y=df_log['Min'],
                        mode='lines',
                        name='Min'))
    fig.add_trace(go.Scatter(x=df_log['Generation'], y=df_log['Max'],
                        mode='lines',
                        name='Max'))
    fig.add_trace(go.Scatter(x=df_log['Generation'], y=df_log['Avg'],
                        mode='lines',
                        name='Avg'))
    fig.show()
    fig.write_image("./files/fig1.jpeg")

if __name__ == "__main__":
    run_ga_deap()
    export_csv()