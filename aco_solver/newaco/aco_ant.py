from random import Random


class Ant(object):
    def __init__(self, graph, init_path):
        self.graph = graph
        self.random = Random()
        self.path = init_path
        self.distance = self.graph.calculate_total_distance(self.path)

    def find_path(self):
        present_city = self.random.randint(0, len(self.path) - 1)
        new_path = [present_city]

        while len(new_path) != len(self.path):
            present_city = self.graph.choose_city(present_city, new_path)
            new_path.append(present_city)

        self.path = new_path
        self.distance = self.graph.calculate_total_distance(new_path)

        return self.path, self.distance

    def contains_connection(self, city_from, city_to):
        for i in range(len(self.path) - 1):
            if self.path[i] == city_from and self.path[i + 1] == city_to:
                return True
        return False

    def __repr__(self):
        return 'Distance: %s Path: %s' % (self.distance, self.path)
