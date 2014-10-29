from random import Random


class Ant(object):
    def __init__(self, graph, init_path):
        self.graph = graph
        self.random = Random()
        self.path = init_path
        self.cities_count = len(init_path)
        self.distance = self.graph.calculate_total_distance(self.path)

    def find_path(self):
        present_city = self.__choose_start_city()
        new_path = [present_city]

        while len(new_path) != self.cities_count:
            present_city = self.__choose_next_city(present_city, new_path)
            new_path.append(present_city)

        self.path = new_path
        self.distance = self.graph.calculate_total_distance(new_path)

        return self.path, self.distance

    def contains_connection(self, city_from, city_to):
        for i in range(len(self.path) - 1):
            if self.path[i] == city_from and self.path[i + 1] == city_to:
                return True
        return False

    def __choose_next_city(self, present_city, visited_cities):
        paths_attractiveness = []

        for city in range(self.cities_count):
            if city == present_city or city in visited_cities:
                paths_attractiveness.append(0.0)
            else:
                paths_attractiveness.append(self.graph.calculate_path_attractiveness(present_city, city))

        paths_probability = self.__calculate_path_probability(paths_attractiveness)
        value = self.random.random()

        for city in range(self.cities_count):
            if paths_probability[city] <= value < paths_probability[city + 1]:
                return city

        raise RuntimeError("City not found")

    @staticmethod
    def __calculate_path_probability(paths_attractiveness):
        attractiveness_sum = sum(paths_attractiveness)

        paths_probability = []
        for i in range(len(paths_attractiveness)):
            paths_probability.append(paths_attractiveness[i] / attractiveness_sum)

        converted_form = [0.0]
        for probability in paths_probability:
            converted_form.append(converted_form[-1] + probability)

        return converted_form

    def __choose_start_city(self):
        return self.random.randint(0, self.cities_count - 1)

    def __repr__(self):
        return 'Distance: %s Path: %s' % (self.distance, self.path)
