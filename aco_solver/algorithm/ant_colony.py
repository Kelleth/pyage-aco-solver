import random
import time
import math

from aco_solver.algorithm.ant import ClassicAnt, ECAnt, ACAnt, GCAnt, BCAnt
from aco_solver.algorithm.commons import Path


def get_population_fullname(abbreviation):
    if abbreviation == 'ca':
        return 'Classic Ants'
    elif abbreviation == 'cs':
        return 'Control Sample'
    elif abbreviation == 'gc':
        return 'Guilt Condition'
    elif abbreviation == 'ac':
        return 'Anger Condition'
    else:
        raise RuntimeError('Unknown population: ' + abbreviation)


class Result(object):
    def __init__(self, fitness, computation_time, best_path, iteration):
        self.fitness = fitness
        self.computation_time = computation_time
        self.best_path = best_path
        self.iteration = iteration

    def __str__(self):
        output_string = 'Best distance: '
        output_string += str(self.best_path.distance) + '\n'
        output_string += 'Best path: '
        output_string += str([city.city_id for city in self.best_path.get_cities_list()]) + '\n'
        output_string += 'Best iteration:'
        output_string += str(self.iteration) + '\n'
        output_string += 'Computation time:'
        output_string += str(self.computation_time) + '\n'

        output_string += str(self.fitness)

        return output_string


class Fitness(object):
    def __init__(self):
        self.separator = ';'
        self.best_key = 'Best'
        self.current_iteration = 0

        self.map = dict()
        self.map[ClassicAnt.__name__] = []
        self.map[ECAnt.__name__] = []
        self.map[ACAnt.__name__] = []
        self.map[GCAnt.__name__] = []
        self.map[BCAnt.__name__] = []
        self.map[self.best_key] = []

    def increase_iteration(self):
        iteration_best = None

        for key in self.map:
            if key == self.best_key or not self.map[key]:
                continue

            if iteration_best is None or self.map[key][-1] < iteration_best:
                iteration_best = self.map[key][-1]

        self.map[self.best_key].append(iteration_best)
        self.current_iteration += 1

    def update_fitness(self, ant):
        fitness_list = self.map[ant.__class__.__name__]

        current_best = None
        if len(fitness_list) > self.current_iteration:
            current_best = fitness_list[self.current_iteration]

        ant_distance = ant.path.distance
        if current_best is None:
            fitness_list.append(ant_distance)
        elif ant_distance < current_best:
            fitness_list[self.current_iteration] = ant_distance

    def __str__(self):
        output_string = 'Iteration'
        for key in sorted(self.map):
            output_string += self.separator + key
        output_string += '\n'

        for i in range(self.current_iteration):
            output_string += str(i + 1)

            for key in sorted(self.map):
                fitness = ''
                if self.map[key]:
                    fitness = str(self.map[key][i])

                output_string += self.separator + fitness

            output_string += '\n'

        return output_string


class AntColony:
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

            # verts = iteration_best_path.get_points()
            # verts.append((0, 0))
            # path = ph.Path(verts)
            # x, y = zip(*path.vertices[:-1])
            # fig, ax = plt.subplots()
            # ax.plot(x, y, 'go', ms=10)
            # ax.plot(x, y, '-k')
            # plt.savefig("path_" + ("0" if iteration < 9 else "") + str(iteration + 1) + ".png")
            # plt.close()
        # print fitness
        return Result(fitness, time.time() - start_time, self.best_path, self.best_path_iteration)

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
