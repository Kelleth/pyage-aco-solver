from random import Random
import sys

from aco_solver.newaco.ants import ClassicAnt


class AntColony:
    def __init__(self, graph, ants_count, iterations, alpha, beta):
        self.graph = graph
        self.ants_count = ants_count
        self.iterations = iterations
        self.best_path_distance = sys.maxint
        self.best_path = None
        self.ants = []
        self.random = Random()
        self.__initialize_ants(alpha, beta)

    def start_simulation(self):
        for i in range(self.iterations):
            found_new_best_solution = False

            # try to find better solution
            for ant in self.ants:
                (path, distance) = ant.find_path()

                if distance < self.best_path_distance:
                    found_new_best_solution = True
                    self.best_path_distance = distance
                    self.best_path = path

            # update pheromones
            self.graph.update_pheromones(self.ants)

            if found_new_best_solution:
                print 'Iteration: %s Best: %s' % (i + 1, self.best_path_distance)

        print 'Best: %s, %s' % (self.best_path, self.best_path_distance)

    def __initialize_ants(self, alpha, beta):
        for i in range(self.ants_count):
            ant = ClassicAnt(self.graph, self.__generate_random_path(self.graph.cities_count), alpha, beta)
            self.ants.append(ant)
            print '%s %s: init distance %s' % (type(ant).__name__, i + 1, ant.distance)

    def __generate_random_path(self, cities_count):
        result = range(cities_count)
        self.random.shuffle(result)
        return result