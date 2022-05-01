from dataclasses import dataclass
from typing import List


@dataclass
class Function:

    function: str
    qtd_variables: int

    def resolve(self, values: List[float]) -> float:
        func = self.function
        for value in values:
            func = func.replace("x", str(value), 1)
        return eval(func)
