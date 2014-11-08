from random import Random

from aco_solver.sequential.ants import ClassicAnt
from aco_solver.sequential.commons import Path


class AntColony:
    def __init__(self, graph, ants_count, iterations, alpha, beta):
        self.graph = graph
        self.ants_count = ants_count
        self.iterations = iterations
        self.best_path = None
        self.ants = []
        self.random = Random()
        self.initialize_ants(alpha, beta)

    def start_simulation(self):
        for i in range(self.iterations):
            pass

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

    def initialize_ants(self, alpha, beta):
        for i in range(self.ants_count):
            path = self.__generate_random_path(self.graph.cities)

            ant = ClassicAnt(alpha, beta, self.graph, path)
            self.ants.append(ant)
            print '%s %s: init distance %s' % (type(ant).__name__, i + 1, ant.path.distance)

    def __generate_random_path(self, available_cities):
        shuffled_cities = list(available_cities)
        self.random.shuffle(shuffled_cities)

        start_city = shuffled_cities.pop(0)

        connection_list = []
        present_city = start_city

        while shuffled_cities:
            next_city = shuffled_cities.pop(0)
            connection_list.append(present_city.find_connection_to_city(next_city))

            present_city = next_city

        return Path(start_city, connection_list)
