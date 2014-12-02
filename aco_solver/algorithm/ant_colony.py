import random
import time
import math

from aco_solver.algorithm.ant import ClassicAnt, ECAnt, ACAnt, GCAnt, BCAnt
from aco_solver.algorithm.commons import Path


class AntColony:
    def __init__(self, graph, ants, iterations):
        self.graph = graph
        self.ants = ants
        self.iterations = iterations
        self.best_path = None
        self.best_path_iteration = None

    def start_simulation(self, print_fitness=True):

        output_string = ''
        start_time = time.time()

        for iteration in range(self.iterations):
            # shuffle ants
            random.shuffle(self.ants)

            iteration_best_ant = None
            iteration_best_path = None

            for ant in self.ants:
                new_path = ant.find_path()

                if iteration_best_path is None or new_path < iteration_best_path:
                    iteration_best_path = new_path
                    iteration_best_ant = ant

                    if self.best_path is None or new_path < self.best_path:
                        self.best_path = new_path
                        self.best_path_iteration = iteration + 1

                self.graph.update_pheromones(ant)

            self.graph.evaporate_pheromones()

            if print_fitness:
                output_string += '{};{:.3f};{}\n'.format(iteration + 1, iteration_best_path.distance,
                                                         iteration_best_ant)

        output_string += 'Time: {:.2f}s\tbest: {:.3f}\titeration: {}\n'.format(time.time() - start_time,
                                                                               self.best_path.distance,
                                                                               self.best_path_iteration)
        return output_string, self.best_path.distance

    def __repr__(self):
        output = 'Colony population:\n'
        population = {}

        for ant in self.ants:
            previous_value = 0
            name = str(ant)

            if name in population.keys():
                previous_value = population[name]

            population[name] = previous_value + 1

        for k, v in population.iteritems():
            output += "{}:\t{}\n".format(k, v)

        return output


# only classic ants
class ClassicAntColony(AntColony):
    def __init__(self, number_of_ants, graph, alpha, beta, iterations):
        ants = self.__generate_population(number_of_ants, graph, alpha, beta)
        AntColony.__init__(self, graph, ants, iterations)

    def __generate_population(self, number_of_ants, city_graph, alpha, beta):
        generated_ants = []
        for _ in range(number_of_ants):
            generated_ants.append(ClassicAnt(city_graph, generate_random_path(city_graph.cities), alpha, beta))
        return generated_ants


# 22% egocentric, 15% altercentric, 45% flexible, 18% bad conflict handlers
class ControlSampleColony(AntColony):
    def __init__(self, number_of_ants, graph, iterations):
        ants = self.__generate_population(number_of_ants, graph)
        AntColony.__init__(self, graph, ants, iterations)

    def __generate_population(self, number_of_ants, city_graph):
        return create_sample(number_of_ants, 0.22, 0.15, 0.45, 0.18, city_graph)


# 3% egocentric, 46% altercentric, 23% flexible, 28% bad conflict handlers
class GuiltConditionColony(AntColony):
    def __init__(self, number_of_ants, graph, iterations):
        ants = self.__generate_population(number_of_ants, graph)
        AntColony.__init__(self, graph, ants, iterations)

    def __generate_population(self, number_of_ants, city_graph):
        return create_sample(number_of_ants, 0.03, 0.46, 0.23, 0.28, city_graph)


# 6% egocentric, 6% altercentric, 63% flexible, 25% bad conflict handlers
class AngerConditionColony(AntColony):
    def __init__(self, number_of_ants, graph, iterations):
        ants = self.__generate_population(number_of_ants, graph)
        AntColony.__init__(self, graph, ants, iterations)

    def __generate_population(self, number_of_ants, city_graph):
        return create_sample(number_of_ants, 0.06, 0.06, 0.63, 0.25, city_graph)


def create_sample(total_number_of_ants, ec_fraction, ac_fraction, gc_fraction, bc_fraction, city_graph):
    generated_ants = []

    for _ in range(int(math.ceil(total_number_of_ants * ec_fraction))):
        generated_ants.append(ECAnt(city_graph, generate_random_path(city_graph.cities)))

    for _ in range(int(math.ceil(total_number_of_ants * ac_fraction))):
        generated_ants.append(ACAnt(city_graph, generate_random_path(city_graph.cities)))

    for _ in range(int(math.ceil(total_number_of_ants * gc_fraction))):
        generated_ants.append(GCAnt(city_graph, generate_random_path(city_graph.cities)))

    for _ in range(total_number_of_ants - len(generated_ants)):
        generated_ants.append(BCAnt(city_graph, generate_random_path(city_graph.cities)))

    random.shuffle(generated_ants)
    return generated_ants


def generate_random_path(available_cities):
    shuffled_cities = list(available_cities)
    random.shuffle(shuffled_cities)

    start_city = shuffled_cities.pop(0)

    connection_list = []
    present_city = start_city

    while shuffled_cities:
        next_city = shuffled_cities.pop(0)
        connection_list.append(present_city.find_connection_to_city(next_city))

        present_city = next_city

    return Path(start_city, connection_list)
