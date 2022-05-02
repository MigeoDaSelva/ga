from controller.god_deap import GodDeap
from model.config_deap import ConfigurationDeap
from dataclasses import dataclass
from deap import tools


@dataclass
class GADeapController:
    god: GodDeap
    config: ConfigurationDeap

    def run(self) -> None:
        
        self.god.hall_of_fame = tools.HallOfFame(1)

        pop = self.god.init()
        
        fitnesses = list(map(self.god.toolbox.evaluate, pop)) 
        
        # individual class in deap has fitness.values attribute which is used to store fitness value
        for individual, fit in zip(pop, fitnesses):
            individual.fitness.values = fit
        
        g = 0
        
        # clearing hall_of_fame object as precaution before every run
        self.god.hall_of_fame.clear()

        # Begin the evolution
        while g < self.config.no_of_generations:
            g = g + 1
            self.god.generate_next_generation(pop, g)
            
            
    def plot_result(self):
        self.god.plot_result()
        self.god.export_csv()
        
        
