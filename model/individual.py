from typing import List
from model.gene import Gene
from dataclasses import dataclass


@dataclass
class Individual:

    genes: List[Gene]
    fitness: float = None

    def __eq__(self, __o: object) -> bool:
        return self.fitness == __o.fitness

    def __lt__(self, __o: object) -> bool:
        return self.fitness < __o.fitness
