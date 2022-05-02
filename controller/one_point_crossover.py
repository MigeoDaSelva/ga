from controller.crossover import Crossover
from model.individual import Individual
from random import randint

class OnePointCrossover(Crossover):

    def cross(self, father: Individual, mother: Individual):
        point = randint(0, len(father.genes)-1)
        mother.genes[point:], father.genes[point:] = father.genes[point:], mother.genes[point:]
        return Individual(genes=father.genes), Individual(genes=mother.genes)