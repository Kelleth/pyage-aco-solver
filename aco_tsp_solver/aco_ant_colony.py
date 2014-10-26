import random
import sys
from aco_ant import ACOAnt


class ACOAntColony:
    def __init__(self, graph, ants_count, iterations):
        self.graph = graph
        self.ants_count = ants_count
        self.iterations = iterations
        self.best_path_cost = sys.maxint
        self.best_path = None
        self.ants = []

    def initialize_ants(self):
        for _ in range(0, self.ants_count):
            ant = ACOAnt(random.randint(0, self.graph.cities_count - 1), self)
            self.ants.append(ant)

    def start(self):
        self.initialize_ants()
        for _ in range(self.graph.cities_count-1):
            for ant in self.ants:
                ant.step()
        for ant in self.ants:
            if ant.path_cost < self.best_path_cost:
                self.best_path_cost = ant.path_cost
                self.best_path = ant.path
        print "Best: %s, %s" % (self.best_path, self.best_path_cost)

