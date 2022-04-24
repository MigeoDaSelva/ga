from dataclasses import dataclass


@dataclass
class Configuration:

    function: str
    function_terms: int
    mutation_rate: float
    intial_population: int
    generation_amount: int
    search_interval_min: float
    search_interval_min: float
