import random


class AntColony:
    def __init__(self, graph, ants, iterations):
        self.graph = graph
        self.ants = ants
        self.iterations = iterations
        self.best_path = None

    def start_simulation(self):
        for iteration in range(self.iterations):
            #iteration_best = 1000000000
            #iteration_bests = {"ClassicAnt":1000000000, "ACAnt":1000000000, "ECAnt":1000000000, "GCAnt":1000000000, "BCAnt":1000000000}
            iteration_best_ant = None
            # shuffle ants
            random.shuffle(self.ants)
            found_new_best_solution = False

            # try to find better solution
            for ant in self.ants:
                new_path = ant.find_path()

                if self.best_path is None or new_path < self.best_path:
                #    found_new_best_solution = True
                    self.best_path = new_path
                #    iteration_best_ant = ant
                #if new_path.distance < iteration_best:
                #    iteration_best = new_path.distance
                #    iteration_best_ant = ant
                #if new_path.distance < iteration_bests[ant.__class__.__name__]:
                #    iteration_bests[ant.__class__.__name__] = new_path.distance

                self.graph.update_pheromones(ant)

            self.graph.evaporate_pheromones()
            #for key, value in iteration_bests.iteritems():
            #    print 'Iteration: %s Best: %s Ant: %s' % (iteration + 1, value, key)
            #if found_new_best_solution:
            #    print '!!!!!!!!!!!!!!!!Iteration: %s Best: %s Ant: %s' % (iteration + 1, self.best_path.distance, iteration_best_ant.__class__.__name__)
            #else:
            #    print '!!!!!!!!!!!!!!!!Iteration: %s Best: %s Ant: %s' % (iteration + 1, iteration_best, iteration_best_ant.__class__.__name__)

        return self.best_path.distance

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