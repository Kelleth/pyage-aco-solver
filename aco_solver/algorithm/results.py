import numpy

from aco_solver.algorithm.ant import ClassicAnt, EgocentricAnt, AltercentricAnt, GoodConflictAnt, BadConflictAnt

fitness_separator = ';'
fitness_keys = sorted([ClassicAnt.__name__, EgocentricAnt.__name__, AltercentricAnt.__name__, GoodConflictAnt.__name__,
                       BadConflictAnt.__name__])


class Result(object):
    def __init__(self, fitness, diversity, attractiveness, computation_time, best_path, best_iteration, max_iterations,
                 name):
        self.fitness = fitness
        self.diversity = diversity
        self.attractiveness = attractiveness
        self.computation_time = computation_time
        self.best_path = best_path
        self.best_iteration = best_iteration
        self.max_iterations = max_iterations
        self.name = name;

    def __str__(self):
        output_string = 'Best distance: '
        output_string += str(self.best_path.distance) + '\n'
        output_string += 'Best path: '
        output_string += str([city.city_id for city in self.best_path.get_cities_list()]) + '\n'
        output_string += 'Best iteration: '
        output_string += str(self.best_iteration) + '\n'
        output_string += 'Computation time: '
        output_string += str(self.computation_time) + '\n'
        output_string += 'Diversity: '
        output_string += str(self.diversity) + '\n'

        output_string += str(self.fitness)

        return output_string

    def fitness_to_string(self):
        output_string = 'Best distance: '
        output_string += str(self.best_path.distance) + '\n'
        output_string += 'Best path: '
        output_string += str([city.city_id for city in self.best_path.get_cities_list()]) + '\n'
        output_string += 'Best iteration: '
        output_string += str(self.best_iteration) + '\n'
        output_string += 'Computation time: '
        output_string += str(self.computation_time) + '\n'
        output_string += 'Diversity: '
        output_string += str(self.diversity) + '\n'
        output_string += self.fitness.fitness_to_string()

        return output_string


class ResultConverter(object):
    def __init__(self, result_list):
        self.result_list = result_list

    def covert_to_avg_results(self):
        output_string = ''

        avg_distance, stdev_distance = self.__compute_avg_distance()
        output_string += 'Average distance: ' + str(avg_distance) + '\n'
        output_string += 'Standard deviation distance: ' + str(stdev_distance) + '\n'

        avg_time, stdev_time = self.__compute_avg_time()
        output_string += 'Average time: ' + str(avg_time) + '\n'
        output_string += 'Standard deviation time: ' + str(stdev_time) + '\n'

        output_string += "Iteration" + fitness_separator
        for fitness_key in fitness_keys:
            output_string += fitness_key + fitness_separator
            output_string += fitness_key + '_stdev' + fitness_separator
        output_string += '\n'

        avg_fitness_map = self.__compute_avg_fitness()
        for i in range(self.result_list[0].max_iterations):
            output_string += str(i)

            for key in fitness_keys:
                output_string += fitness_separator

                if avg_fitness_map[key]:
                    avg_fitness, stdev_fitness = avg_fitness_map[key][i]
                    output_string += str(avg_fitness) + fitness_separator + str(stdev_fitness)
                else:
                    output_string += fitness_separator

            output_string += '\n'

        return output_string

    def convert_diversity_results(self):
        output_string = ''
        for i in range(self.result_list[0].max_iterations):
            curr_iter_diversities = [result.diversity.get_diversity_value(i) for result in self.result_list]
            output_string += str(i) + ',' + str(numpy.mean(curr_iter_diversities)) + ',' + str(numpy.std(curr_iter_diversities)) + '\n'

        return output_string

    def convert_attractiveness_avg_std_results(self):
        output_string = ''
        for i in range(self.result_list[0].max_iterations):
            curr_iter_attractivenesses = [result.attractiveness.get_avg_attractiveness(i) for result in self.result_list]
            output_string += str(i) + ',' + str(numpy.mean(curr_iter_attractivenesses)) + ',' + str(numpy.std(curr_iter_attractivenesses)) \
                           + '\n'

        return output_string

    def convert_attractiveness_ratio_results(self):
        output_string = ''
        for i in range(self.result_list[0].max_iterations):
            curr_iter_attractiveness_ratios = [result.attractiveness.get_attractiveness_ratio(i) for result in self.result_list]
            output_string += str(i) + ',' + str(numpy.mean(curr_iter_attractiveness_ratios)) + ',' + str(numpy.std(curr_iter_attractiveness_ratios)) \
                           + '\n'

        return output_string


    def __compute_avg_distance(self):
        distances = [result.best_path.distance for result in self.result_list]
        mean = numpy.mean(distances)
        stdev = numpy.std(distances)

        return mean, stdev

    def __compute_avg_time(self):
        times = [result.computation_time for result in self.result_list]
        mean = numpy.mean(times)
        stdev = numpy.std(times)

        return mean, stdev

    def __compute_avg_fitness(self):
        avg_fitness_map = dict()
        for key in fitness_keys:
            avg_fitness_map[key] = []

        for fitness_iteration in range(self.result_list[0].max_iterations):

            for key in fitness_keys:
                if len(self.result_list[0].fitness.map[key]) == 0:
                    continue

                iteration_fitness = [result.fitness.map[key][fitness_iteration] for result in self.result_list]

                mean = numpy.mean(iteration_fitness)
                stdev = numpy.std(iteration_fitness)

                avg_fitness_map[key].append((mean, stdev, ))

        return avg_fitness_map


class Attractiveness(object):
    def __init__(self):
        self.attractiveness_lists = []
        self.attractiveness_ratios = []
        self.avg_attractiveness_list = []
        self.std_attractiveness_list = []

    def update_attractiveness_data(self, attractiveness_list, attractiveness_ratio):
        self.attractiveness_lists.append(attractiveness_list)
        self.avg_attractiveness_list.append(numpy.mean(attractiveness_list))
        self.std_attractiveness_list.append(numpy.std(attractiveness_list))
        self.attractiveness_ratios.append(attractiveness_ratio)

    def get_attractiveness_list(self, iteration):
        return self.attractiveness_lists[iteration]

    def get_avg_attractiveness(self, iteration):
        return self.avg_attractiveness_list[iteration]

    def get_std_attractiveness(self, iteration):
        return self.std_attractiveness_list[iteration]

    def get_attractiveness_ratio(self, iteration):
        return self.attractiveness_ratios[iteration]

    def __str__(self):
        return str(self.attractiveness_lists) + '\n' + str(self.attractiveness_ratios)


class Diversity(object):
    def __init__(self):
        self.list = list()

    def update_diversity_list(self, value):
        self.list.append(value)

    def get_diversity_value(self, iteration):
        return self.list[iteration]

    def __str__(self):
        return str(self.list)


class Fitness(object):
    def __init__(self):
        self.current_iteration = 0

        self.map = dict()
        for key in fitness_keys:
            self.map[key] = []

    def get_iteration(self):
        return self.current_iteration

    def increase_iteration(self):
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

    def update_fitness_stats(self, ant_name, ant_distance):
        fitness_list = self.map[ant_name]

        current_best = None
        if len(fitness_list) > self.current_iteration:
            current_best = fitness_list[self.current_iteration]

        if current_best is None:
            fitness_list.append(ant_distance)
        elif ant_distance < current_best:
            fitness_list[self.current_iteration] = ant_distance

    def fitness_to_string(self):
        output_string = 'Iteration'
        for key in sorted(self.map):
            output_string += fitness_separator + key
        output_string += '\n'

        current_best = dict()
        current_best[ClassicAnt.__name__] = None
        current_best[EgocentricAnt.__name__] = None
        current_best[AltercentricAnt.__name__] = None
        current_best[GoodConflictAnt.__name__] = None
        current_best[BadConflictAnt.__name__] = None

        for i in range(self.current_iteration):
            output_string += str(i + 1)

            for key in sorted(self.map):
                fitness = ''
                if self.map[key]:
                    if current_best[key] is None or self.map[key][i] < current_best[key]:
                        current_best[key] = self.map[key][i]
                    fitness = str(current_best[key])

                output_string += fitness_separator + fitness

            output_string += '\n'

        return output_string

    def __str__(self):
        output_string = 'Iteration' + fitness_separator + fitness_separator.join(fitness_keys) + '\n'

        for i in range(self.current_iteration):
            output_string += str(i + 1)

            for key in sorted(self.map):
                fitness = ''
                if self.map[key]:
                    fitness = str(self.map[key][i])

                output_string += fitness_separator + fitness

            output_string += '\n'

        return output_string