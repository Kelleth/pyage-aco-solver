import random
import time
import math

from aco_solver.algorithm.ant import ClassicAnt, EgocentricAnt, AltercentricAnt, GoodConflictAnt, BadConflictAnt
from aco_solver.algorithm.commons import Path
from aco_solver.algorithm.results import Result, Fitness



# Template class for different populations/colonies
# Subclass only has to provide ants list
class AntColony(object):
    def __init__(self, graph, ants, iterations):
        self.graph = graph
        self.ants = ants
        self.iterations = iterations
        self.best_path = None
        self.best_path_iteration = None

    def start_simulation(self):
        start_time = time.time()
        fitness = Fitness()

        for iteration in range(self.iterations):
            # shuffle ants
            random.shuffle(self.ants)

            for ant in self.ants:
                new_path = ant.find_path()

                if self.best_path is None or new_path < self.best_path:
                    self.best_path = new_path
                    self.best_path_iteration = iteration + 1

                self.graph.update_pheromones(ant)
                fitness.update_fitness(ant)

            self.graph.evaporate_pheromones()
            fitness.increase_iteration()

        return Result(fitness, time.time() - start_time, self.best_path, self.best_path_iteration, self.iterations)

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


# Only classic ants
class ClassicAntColony(AntColony):
    def __init__(self, number_of_ants, graph, alpha, beta, iterations):
        ants = self.__generate_population(number_of_ants, graph, alpha, beta)
        AntColony.__init__(self, graph, ants, iterations)

    def __generate_population(self, number_of_ants, city_graph, alpha, beta):
        generated_ants = []
        for _ in range(number_of_ants):
            generated_ants.append(ClassicAnt(city_graph, generate_random_path(city_graph.cities), alpha, beta))
        return generated_ants


# 22% egocentric, 15% altercentric, 45% flexible, 18% bad conflict
class ControlSampleColony(AntColony):
    def __init__(self, number_of_ants, graph, iterations):
        ants = self.__generate_population(number_of_ants, graph)
        AntColony.__init__(self, graph, ants, iterations)

    def __generate_population(self, number_of_ants, city_graph):
        return create_sample(number_of_ants, 0.22, 0.15, 0.45, 0.18, city_graph)


# 3% egocentric, 46% altercentric, 23% good conflict, 28% bad conflict
class HighAltercentricityCondition(AntColony):
    def __init__(self, number_of_ants, graph, iterations):
        ants = self.__generate_population(number_of_ants, graph)
        AntColony.__init__(self, graph, ants, iterations)

    def __generate_population(self, number_of_ants, city_graph):
        return create_sample(number_of_ants, 0.03, 0.46, 0.23, 0.28, city_graph)


# 6% egocentric, 6% altercentric, 63% good conflict, 25% bad conflict
class LowAltercentricityCondition(AntColony):
    def __init__(self, number_of_ants, graph, iterations):
        ants = self.__generate_population(number_of_ants, graph)
        AntColony.__init__(self, graph, ants, iterations)

    def __generate_population(self, number_of_ants, city_graph):
        return create_sample(number_of_ants, 0.06, 0.06, 0.63, 0.25, city_graph)


def get_population_fullname(abbreviation):
    if abbreviation == 'ca':
        return 'Classic Ants'
    elif abbreviation == 'cs':
        return 'Control Sample'
    elif abbreviation == 'ha':
        return 'High Altercentricity Condition'
    elif abbreviation == 'la':
        return 'Low Altercentricity Condition'
    else:
        raise RuntimeError('Unknown population: ' + abbreviation)


def create_sample(total_number_of_ants, ec_fraction, ac_fraction, gc_fraction, bc_fraction, city_graph):
    generated_ants = []

    for _ in range(int(math.ceil(total_number_of_ants * ec_fraction))):
        generated_ants.append(EgocentricAnt(city_graph, generate_random_path(city_graph.cities)))

    for _ in range(int(math.ceil(total_number_of_ants * ac_fraction))):
        generated_ants.append(AltercentricAnt(city_graph, generate_random_path(city_graph.cities)))

    for _ in range(int(math.ceil(total_number_of_ants * gc_fraction))):
        generated_ants.append(GoodConflictAnt(city_graph, generate_random_path(city_graph.cities)))

    # BCAnts really sucks so we ignore bc_fraction coefficient
    # For low total number of ants population might not contain any BCAnts
    for _ in range(total_number_of_ants - len(generated_ants)):
        generated_ants.append(BadConflictAnt(city_graph, generate_random_path(city_graph.cities)))

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
