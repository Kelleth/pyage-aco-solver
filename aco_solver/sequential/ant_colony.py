class AntColony:
    def __init__(self, graph, ants, iterations):
        self.graph = graph
        self.ants = ants
        self.iterations = iterations
        self.best_path = None

    def start_simulation(self):
        for iteration in range(self.iterations):
            found_new_best_solution = False

            # try to find better solution
            for ant in self.ants:
                new_path = ant.find_path()

                if self.best_path is None or new_path < self.best_path:
                    found_new_best_solution = True
                    self.best_path = new_path

            self.graph.update_pheromones(self.ants)
            self.graph.clean_connections_statistics()

            if found_new_best_solution:
                print 'Iteration: %s Best: %s' % (iteration + 1, self.best_path.distance)

        print 'Best: {}'.format(str(self.best_path))
