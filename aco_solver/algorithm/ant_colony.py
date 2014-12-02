import random
import time


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