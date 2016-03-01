# Represents ant path
class Path(object):
    def __init__(self, item_list, graph):
        self.item_list = item_list
        self.fitness = self.calculate_knapsacks_fitness(graph, item_list)

    def calculate_knapsacks_fitness(self, graph, assignment_list):
        total_fitness = 0.0
        for item_id, item_taken in enumerate(self.item_list):
            total_fitness += item_taken * graph.items[item_id].profit
        return total_fitness

    def get_items(self):
        return self.item_list

    # Comparing by distance
    def __cmp__(self, other):
        if self.fitness < other.fitness:
            return -1
        elif self.fitness > other.fitness:
            return 1
        else:
            return 0

    def contains_item(self, item):
        return self.item_list[item.id] == 1

    def __str__(self):
        return 'Fitness {}, items {}'.format(self.fitness, self.item_list)
