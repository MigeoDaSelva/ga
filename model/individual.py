from typing import List
from model.gene import Gene
from dataclasses import dataclass


@dataclass
class Individual:

    genes: List[Gene]
