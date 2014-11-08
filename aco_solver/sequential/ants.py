import random

from aco_solver.sequential.commons import Path


class Ant(object):
    def __init__(self, alpha, beta, graph, path):
        self.alpha = alpha  # pheromone influence
        self.beta = beta  # distance influence

        self.graph = graph
        self.path = path

    def find_path(self):
        start_city = self.__choose_start_city()
        connection_list = []
        cities_visited = [start_city]

        present_city = start_city
        while len(connection_list) != len(self.path.connection_list):
            next_connection = self.choose_next_city(present_city, cities_visited)

            connection_list.append(next_connection)
            present_city = next_connection.destination_city

        self.path = Path(start_city, connection_list)
        return self.path

    def choose_next_city(self, present_city, new_path):
        pass

    def __choose_start_city(self):
        return random.choice(self.graph.cities)

    def __repr__(self):
        return 'Distance: %s Path: %s' % (self.path.distance, self.path)


class ClassicAnt(Ant):
    def __init__(self, alpha, beta, graph, path):
        super(ClassicAnt, self).__init__(alpha, beta, graph, path)

    def choose_next_city(self, present_city, visited_cities):
        paths_attractiveness = []

        for connection in present_city.connection_list:
            destination_city = connection.destination_city

            if destination_city == present_city or destination_city in visited_cities:
                paths_attractiveness.append(0.0)
            else:
                paths_attractiveness.append(
                    self.__calculate_path_attractiveness(connection))

        paths_probability = self.__calculate_path_probability(paths_attractiveness)
        value = random.random()

        # fixme
        for i in range(len(paths_probability) - 1):
            if paths_probability[i] <= value < paths_probability[i + 1]:
                return present_city.connection_list[i]

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

    def __calculate_path_attractiveness(self, connection):
        return connection.pheromone ** self.alpha * (1.0 / connection.distance) ** self.beta


class GreedyAnt(Ant):
    def __init__(self, alpha, beta, graph, path):
        super(GreedyAnt, self).__init__(alpha, beta, graph, init_path)

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