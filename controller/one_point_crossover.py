from controller.crossover import Crossover
from model.individual import Individual
from random import randint

class OnePointCrossover(Crossover):

    def cross(self, father: Individual, mother: Individual):
        children_one = []
        children_two = []
        point = randint(0, len(father.genes)-1)
        
        for i in range(point):
            children_one.append(father.genes[i])
            children_two.append(mother.genes[i])

        for i in range(point, len(mother.genes)):
            children_one.append(mother.genes[i])
            children_two.append(father.genes[i])
        
        return Individual(genes=children_one), Individual(genes=children_two)