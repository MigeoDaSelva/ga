import os
from model.config_deap import ConfigurationDeap
from model.function_deap import FunctionDeap
from model.generation import Generation
from dataclasses import dataclass
import plotly.graph_objects as go
import plotly.express as px
import random, numpy as np
from deap import creator
from deap import tools
from deap import base
import pandas as pd
import random


@dataclass(
    repr=False,
)
class GodDeap:
    
    def __init__(self, config: ConfigurationDeap, function: FunctionDeap):
        self.config = config
        self.function = function
        self.stats = tools.Statistics()
        self.logbook = tools.Logbook()
        self.hall_of_fame = tools.HallOfFame(1)
        self.toolbox = base.Toolbox()

    def init(self) -> Generation:
        creator.create("FitnessMin", base.Fitness, weights=(1.0,))

        # an Individual is a list with one more attribute called fitness
        creator.create("Individual", list, fitness=creator.FitnessMin)
        
        self.toolbox.register("attr_bool", random.randint, 0, 1)       
        self.toolbox.register("individual", tools.initRepeat, creator.Individual, self.toolbox.attr_bool, self.config.qtd_variables * 50)
        self.toolbox.register("population", tools.initRepeat, list, self.toolbox.individual)
        
        # registering objetive function with constraint
        self.toolbox.register("evaluate", self.function.objective_fxn) # privide the objective function here
        self.toolbox.decorate("evaluate", tools.DeltaPenalty(self.function.check_feasiblity, 1000, self.function.penalty_fxn)) # constraint on our objective function

        # registering basic processes using bulit in functions in DEAP
        self.toolbox.register("mate", self.config.get_mate())
        self.toolbox.register("mutate", self.config.get_mutate(), indpb=self.config.probabilityMutating)
        self.toolbox.register("select", self.config.get_select(), tournsize=self.config.tournsize)
        
        self.stats.register('Min', np.min)
        self.stats.register('Max', np.max)
        self.stats.register('Avg', np.mean)
        self.stats.register('Std', np.std)

        pop = self.toolbox.population(n=self.config.population_size)
        
        return pop

    def generateES(self, ind_cls, strg_cls, size):
        ind = ind_cls(np.random.normal() for _ in range(size))
        ind.strategy = strg_cls(np.random.normal() for _ in range(size))
        return ind

    def generate_next_generation(self, population, g):
        #The evolution itself will be performed by selecting, mating, and mutating the individuals in our population.
    
        # the first step is to select the next generation.
        offspring = self.toolbox.select(population, len(population))
        
        # Clone the selected individuals, this needs to be done to create copy and avoid problem of inplace operations
        # This is of utter importance since the genetic operators in toolbox will modify the provided objects in-place.
        offspring = list(map(self.toolbox.clone, offspring))
        
        # Apply crossover and mutation on the offspring
        # note, that since we are not cloning, the changes in child1, child2 and mutant are happening inplace in offspring
        for child1, child2 in zip(offspring[::2], offspring[1::2]):
            if random.random() < self.config.probabilityCrossed:
                    self.toolbox.mate(child1, child2)
                    del child1.fitness.values
                    del child2.fitness.values

            for mutant in offspring:
                if random.random() < self.config.probabilityMutating:
                    self.toolbox.mutate(mutant)
                    del mutant.fitness.values 
                        
        # Evaluate the individuals with an invalid fitness (after we use del to make them invalid)
        # again note, that since we did not use clone, each change happening is happening inplace in offspring
        invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
        fitnesses = map(self.toolbox.evaluate, invalid_ind)
        for ind, fit in zip(invalid_ind, fitnesses):
            ind.fitness.values = fit
        
        # To check the performance of the evolution, we will calculate and print the 
        # minimal, maximal, and mean values of the fitnesses of all individuals in our population 
        this_gen_fitness = [] # this list will have fitness value of all the offspring
        for ind in offspring:
            this_gen_fitness.append(ind.fitness.values[0])            
        
        # will update the HallOfFame object with the best individual 
        #   according to fitness value and weight (while creating base.Fitness class)
        self.hall_of_fame.update(offspring)
        
        # pass a list of fitnesses 
        # (basically an object on which we want to perform registered functions)
        # will return a dictionary with key = name of registered function and value is return of the registered function
        stats_of_this_gen = self.stats.compile(this_gen_fitness)
        
        # creating a key with generation number
        stats_of_this_gen['Generation'] = g
        
        # printing for each generation
        print(stats_of_this_gen)
        
        # recording everything in a logbook object
        # logbook is essentially a list of dictionaries
        self.logbook.append(stats_of_this_gen)
        
        # now one generation is over and we have offspring from that generation
        population[:] = offspring
    
    def plot_result(self):
        # print the best solution using HallOfFame object
        for best_indi in self.hall_of_fame:
            # using values to return the value and
            # not a deap.creator.FitnessMin object
            best_obj_val_overall = best_indi.fitness.values[0]
            print('Max value for function: ',best_obj_val_overall)
            print('Optimum Solution: ',self.function.decode_all_x(best_indi))

    def export_csv(self):
        os.remove('./files/result.csv')
        df_log = pd.DataFrame(self.logbook)
        df_log.to_csv('./files/result.csv', index=False)
        