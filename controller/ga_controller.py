from controller.avaliator import Avaliator
from model.generation import Generation
from model.config import Configuration
from model.function import Function
from dataclasses import dataclass
from controller.god import God


@dataclass
class GAController:
    god: God
    function: Function
    generation = Generation

    def run(self, config: Configuration) -> None:

        avaliator = Avaliator(self.function)

        self.generation = self.god.generate_init_generation(self.function)
        avaliator.avaliate_fitness(self.generation)
        self.generation.set_best()
        print(self.generation.the_best)

        while not self.check_stop_criterion(config):
            self.generation = self.god.generate_next_generation(self.generation)
            avaliator.avaliate_fitness(self.generation)
            self.generation.set_best()
            print(self.generation.the_best)

    def check_stop_criterion(self, config: Configuration) -> bool:
        return self.generation.number == config.generation_amount
