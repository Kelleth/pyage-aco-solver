from random import Random


class Ant(object):
    def __init__(self, graph, init_path, alpha, beta):
        self.graph = graph
        self.path = init_path
        self.alpha = alpha  # pheromone influence
        self.beta = beta  # distance influence

        self.random = Random()
        self.cities_count = len(init_path)
        self.distance = self.graph.calculate_total_distance(self.path)

    def contains_connection(self, city_from, city_to):
        for i in range(len(self.path) - 1):
            if self.path[i] == city_from and self.path[i + 1] == city_to:
                return True
        return False

    def find_path(self):
        present_city = self.__choose_start_city()
        new_path = [present_city]

        while len(new_path) != self.cities_count:
            present_city = self.choose_next_city(present_city, new_path)
            new_path.append(present_city)

        self.path = new_path
        self.distance = self.graph.calculate_total_distance(new_path)

        return self.path, self.distance

    def choose_next_city(self, present_city, new_path):
        pass

    def __choose_start_city(self):
        return self.random.randint(0, self.cities_count - 1)

    def __repr__(self):
        return 'Distance: %s Path: %s' % (self.distance, self.path)


class ClassicAnt(Ant):
    def __init__(self, graph, init_path, alpha, beta):
        super(ClassicAnt, self).__init__(graph, init_path, alpha, beta)

    def choose_next_city(self, present_city, visited_cities):
        paths_attractiveness = []

        for city in range(self.cities_count):
            if city == present_city or city in visited_cities:
                paths_attractiveness.append(0.0)
            else:
                paths_attractiveness.append(
                    self.graph.calculate_path_attractiveness(self.alpha, self.beta, present_city, city))

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


class GreedyAnt(Ant):
    def __init__(self, graph, init_path, alpha, beta):
        super(GreedyAnt, self).__init__(graph, init_path, alpha, beta)

    def choose_next_city(self, present_city, visited_cities):
        chosen_city = None
        chosen_city_attractiveness = -1

        for city in range(self.cities_count):
            if city == present_city or city in visited_cities:
                continue
            else:
                path_attractiveness = self.graph.calculate_path_attractiveness(self.alpha, self.beta, present_city,
                                                                               city)
                if path_attractiveness > chosen_city_attractiveness:
                    chosen_city = city
                    chosen_city_attractiveness = path_attractiveness

        return chosen_city