import random


class AntColony:
    def __init__(self, graph, ants, iterations):
        self.graph = graph
        self.ants = ants
        self.iterations = iterations
        self.best_path = None

    def start_simulation(self):
        for iteration in range(self.iterations):
            # shuffle ants
            random.shuffle(self.ants)
            found_new_best_solution = False

            # try to find better solution
            for ant in self.ants:
                new_path = ant.find_path()

                if self.best_path is None or new_path < self.best_path:
                    found_new_best_solution = True
                    self.best_path = new_path

                self.graph.update_pheromones(ant)

            self.graph.evaporate_pheromones()

            if found_new_best_solution:
                print 'Iteration: %s Best: %s' % (iteration + 1, self.best_path.distance)

        print 'Best: {}'.format(str(self.best_path))

    def __repr__(self):
        output = 'Colony population:\n'
        population = {}

        for ant in self.ants:
            previous_value = 0
            name = ant.__class__.__name__

            if name in population.keys():
                previous_value = population[name]

            population[name] = previous_value + 1

        for k, v in population.iteritems():
            output += "{}: {}\n".format(k, v)

        return output