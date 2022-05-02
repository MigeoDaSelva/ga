from dataclasses import dataclass
from typing import List
import math


@dataclass
class Function:

    function: str
    qtd_variables: int
    variables: list

    def resolve(self, values: List[float]) -> float:
        func = self.function
        
        for v, vl in zip(self.variables, values):
            func = func.replace(v, str(vl), -1)

        return eval(func)
