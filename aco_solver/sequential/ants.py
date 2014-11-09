import random

from aco_solver.sequential.commons import Path


class Ant(object):
    def __init__(self, graph, path):
        self.graph = graph
        self.path = path

    def find_path(self):
        start_city = self.__choose_start_city()
        connection_list = []
        cities_visited = [start_city]

        present_city = start_city
        while len(connection_list) != len(self.path.connection_list):
            next_connection = self.chose_next_connection(present_city, cities_visited)

            connection_list.append(next_connection)
            cities_visited.append(next_connection.destination_city)
            present_city = next_connection.destination_city

        self.path = Path(start_city, connection_list)
        return self.path

    def chose_next_connection(self, present_city, visited_cities):
        chosen_connection = None
        chosen_connection_attractiveness = -1

        for connection in present_city.connection_list:
            destination_city = connection.destination_city

            if destination_city == present_city or destination_city in visited_cities:
                continue
            else:
                path_attractiveness = self.calculate_connection_attractiveness(connection)

                if path_attractiveness > chosen_connection_attractiveness:
                    chosen_connection = connection
                    chosen_connection_attractiveness = path_attractiveness

        return chosen_connection

    def calculate_connection_attractiveness(self, connection):
        return 0

    def __choose_start_city(self):
        return random.choice(self.graph.cities)

    def __repr__(self):
        return 'Distance: %s Path: %s' % (self.path.distance, self.path)


class ShuffleAnt(Ant):
    def __init__(self, graph, path):
        super(ShuffleAnt, self).__init__(graph, path)

    def chose_next_connection(self, present_city, visited_cities):
        connections_attractiveness = []

        for connection in present_city.connection_list:
            destination_city = connection.destination_city

            if destination_city == present_city or destination_city in visited_cities:
                connections_attractiveness.append(0.0)
            else:
                connections_attractiveness.append(
                    self.calculate_connection_attractiveness(connection))

        connection_probabilities = self.calculate_connection_probability(connections_attractiveness)
        value = random.random()

        for i in range(len(connection_probabilities) - 1):
            if connection_probabilities[i] <= value < connection_probabilities[i + 1]:
                return present_city.connection_list[i]

        raise RuntimeError("City not found")

    @staticmethod
    def calculate_connection_probability(connections_attractiveness):
        attractiveness_sum = sum(connections_attractiveness)

        connections_probability = []

        for i in range(len(connections_attractiveness)):
            connections_probability.append(connections_attractiveness[i] / attractiveness_sum)

        converted_form = [0.0]
        for probability in connections_probability:
            converted_form.append(converted_form[-1] + probability)

        return converted_form


# ClassicAnt which computes attractiveness like pheromone^alpha * (1/distance)^beta
class ClassicAnt(ShuffleAnt):
    def __init__(self, graph, path, alpha, beta):
        super(ClassicAnt, self).__init__(graph, path)
        self.alpha = alpha
        self.beta = beta

    def calculate_connection_attractiveness(self, connection):
        return connection.pheromone ** self.alpha * (1.0 / connection.distance) ** self.beta


# The individuals who are "altercentric" would follow the mass
class ACAnt(Ant):
    def __init__(self, graph, path):
        super(ACAnt, self).__init__(graph, path)

    def calculate_connection_attractiveness(self, connection):
        return connection.pheromone


# The individuals who are "egocentric" would be more creative to try to find a new solution,
# finding their own way, less caring for others and for pheromone trail.
class ECAnt(Ant):
    def __init__(self, graph, path):
        super(ECAnt, self).__init__(graph, path)

    def calculate_connection_attractiveness(self, connection):
        return 1.0 / connection.distance


# Those bad at conflict handling will behave impulsively (in effect randomly)
class BCAnt(Ant):
    def __init__(self, graph, path):
        super(BCAnt, self).__init__(graph, path)

    def chose_next_connection(self, present_city, visited_cities):
        next_connection = None

        while not next_connection:
            random_connection = random.choice(present_city.connection_list)
            destination_city = random_connection.destination_city

            if destination_city == present_city or destination_city in visited_cities:
                continue
            else:
                next_connection = random_connection

        return next_connection
