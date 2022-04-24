from typing import List
from dataclasses import dataclass
from model.individual import Individual


@dataclass
class Generation:
    
    number: int
    individuals: List[Individual]
