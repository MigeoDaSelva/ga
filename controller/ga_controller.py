from controller.avaliator import Avaliator
from model.generation import Generation
from model.config import Configuration
from model.function import Function
from dataclasses import dataclass
from controller.god import God
import pandas as pd
import csv


@dataclass
class GAController:
    god: God
    function: Function
    generation = Generation

    def run(self, config: Configuration) -> None:
        line = {
            "fitness": 0.0,
            "generation": 0.0,
        }

        avaliator = Avaliator(self.function)

        self.generation = self.god.generate_init_generation(self.function)

        avaliator.avaliate_fitness(self.generation)

        print(self.generation.get_best())

        line["fitness"] = self.generation.get_best().fitness
        line["generation"] = self.generation.number

        self._to_csv(line)

        while not self.check_stop_criterion(config):

            self.generation = self.god.generate_next_generation(self.generation)
            avaliator.avaliate_fitness(self.generation)

            print(self.generation.get_best())

            line["fitness"] = self.generation.get_best().fitness
            line["generation"] = self.generation.number
            self._to_csv(line)

    def check_stop_criterion(self, config: Configuration) -> bool:
        return self.generation.number == config.generation_amount

    def _to_csv(self, line: dict):
        path = "./files/results.csv"
        try:
            open(path, "r")
            with open(path, "a") as arq:
                writer = csv.writer(arq)
                writer.writerow(line.values())
        except IOError:
            dataF = pd.DataFrame(columns=line.keys())
            dataF = dataF.append(line, ignore_index=True)
            dataF.to_csv(path, index=False)
