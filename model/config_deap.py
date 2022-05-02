from ast import FunctionDef
from dataclasses import dataclass
from deap import tools


@dataclass
class ConfigurationDeap:

    mate: str
    mutate: str
    select: str
    qtd_variables: int
    tournsize: int
    population_size: int
    no_of_generations: int
    probabilityCrossed: float
    probabilityMutating: float

    def get_mate(self):
        if self.mate == "two_point":
            return tools.cxTwoPoint 
        elif self.mate == "one_point":
            return tools.cxOnePoint
        else:
            return tools.cxUniform

    def get_mutate(self):
        return tools.mutFlipBit
    
    def get_select(self):
        return tools.selTournament