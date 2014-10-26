class ACOAnt():
    def __init__(self, start_node, colony):
        self.start_node = start_node
        self.colony = colony
        self.pheromone = 0.01

        self.curr_node = self.start_node
        self.graph = self.colony.graph
        self.path = [self.start_node]
        self.path_cost = 0

        self.nodes_to_visit = {}

        for i in range(0, self.graph.cities_count):
            if i != self.start_node:
                self.nodes_to_visit[i] = i

    def step(self):
        new_node = self.state_transition_rule(self.curr_node)
        self.path_cost += self.graph.distance(self.curr_node, new_node)

        self.path.append(new_node)

        self.update_pheromone(self.curr_node, new_node)

        self.curr_node = new_node

    def state_transition_rule(self, curr_node):
        graph = self.colony.graph
        max_node = -1
        max_val = -1
        for node in self.nodes_to_visit.values():
            val = graph.pheromone(curr_node, node) * graph.distance_attractiveness(curr_node, node)
            if val > max_val:
                max_val = val
                max_node = node

        del self.nodes_to_visit[max_node]
        return max_node

    def update_pheromone(self, curr_node, next_node):
        self.graph.add_pheromone(curr_node, next_node, self.pheromone)

