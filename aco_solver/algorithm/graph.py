class Graph(object):
    def __init__(self, distance_matrix, positions, pheromone_evaporation, pheromone_deposit, init_pheromone_value, attractiveness_alpha, attractiveness_beta):
        number_of_cities = len(distance_matrix)

        cities = []
        for city_id in range(number_of_cities):
            cities.append(City(city_id, positions[city_id], init_pheromone_value))

        for i in range(number_of_cities):
            present_city = cities[i]
            for j in range(number_of_cities):
                if i == j:
                    continue

                present_city.create_and_add_connection(distance_matrix[i][j], cities[j])

        self.cities = cities
        self.number_of_cities = number_of_cities

        self.pheromone_evaporation = pheromone_evaporation
        self.pheromone_deposit = pheromone_deposit

        self.attractiveness_alpha = attractiveness_alpha
        self.attractiveness_beta = attractiveness_beta

    def update_pheromones(self, ant):
        # increase value for visited connections
        path = ant.path
        for connection in path.connection_list:
            connection.accept_visitor(ant, self.pheromone_deposit / path.distance)

    def evaporate_pheromones(self):
        # pheromone evaporation
        for city in self.cities:
            for connection in city.connection_list:
                connection.pheromone.evaporate(1.0 - self.pheromone_evaporation)

    def calculate_diversity_and_attractiveness(self):
        connections_with_pheromone = 0
        connections_number = 0
        attractiveness_list = []
        for city in self.cities:
            for connection in city.connection_list:
                connections_number += 1
                attractiveness = connection.pheromone.total_pheromone ** self.attractiveness_alpha * (1.0 / connection.distance) ** self.attractiveness_beta
                attractiveness_list.append(attractiveness)
                if connection.pheromone.total_pheromone > 0:
                    connections_with_pheromone += 1
        return (connections_with_pheromone / connections_number) * 100, attractiveness_list






class City(object):
    def __init__(self, city_id, position, init_pheromone_value, connection_list=None):
        if not connection_list:
            connection_list = []

        self.city_id = city_id
        self.connection_list = connection_list
        self.init_pheromone_value = init_pheromone_value
        self.position = position

    def add_connection(self, connection):
        if connection.destination_city.city_id == self.city_id:
            raise RuntimeError('Cannot add connection to itself')

        self.connection_list.append(connection)

    def create_and_add_connection(self, distance, destination_city):
        self.add_connection(Connection(distance, destination_city, self.init_pheromone_value))

    def find_connection_to_city(self, city):
        for connection in self.connection_list:
            if connection.destination_city == city:
                return connection
        raise RuntimeError('Connection from city {} to city {} not found'.format(self.city_id, city.city_id))

    def get_position(self):
        return self.position

    def get_position_string(self):
        return str(self.position[0]) + ";" + str(self.position[1])

    def __eq__(self, other):
        if isinstance(other, City):
            return self.city_id == other.city_id
        else:
            return False


class Connection(object):
    def __init__(self, distance, destination_city, init_pheromone_value):
        self.distance = distance
        self.destination_city = destination_city
        self.pheromone = Pheromone(init_pheromone_value)

    def accept_visitor(self, visitor, pheromone_value):
        visitor.visit(self, pheromone_value)


class Pheromone(object):
    def __init__(self, init_value):
        self.ac_pheromone = init_value
        self.ec_pheromone = init_value
        self.gc_pheromone = init_value
        self.bc_pheromone = init_value
        self.unknown_pheromone = init_value

        self.total_pheromone = self.ac_pheromone + self.ec_pheromone + self.gc_pheromone + self.bc_pheromone \
                               + self.unknown_pheromone

    def update_ac_pheromone(self, value):
        self.ac_pheromone += value
        self.__update_total_pheromone()

    def update_ec_pheromone(self, value):
        self.ec_pheromone += value
        self.__update_total_pheromone()

    def update_gc_pheromone(self, value):
        self.gc_pheromone += value
        self.__update_total_pheromone()

    def update_bc_pheromone(self, value):
        self.bc_pheromone += value
        self.__update_total_pheromone()

    def update_unknown_pheromone(self, value):
        self.unknown_pheromone += value
        self.__update_total_pheromone()

    def evaporate(self, factor):
        self.ac_pheromone *= factor
        self.ec_pheromone *= factor
        self.gc_pheromone *= factor
        self.bc_pheromone *= factor
        self.unknown_pheromone *= factor
        self.__update_total_pheromone()

    def __update_total_pheromone(self):
        self.total_pheromone = self.ac_pheromone + self.ec_pheromone + self.gc_pheromone + self.bc_pheromone \
                               + self.unknown_pheromone


# Average distance in graph is used to setup initial pheromone value
def compute_average_distance(distance_matrix):
    total_distance = 0.0
    number_of_connections = 0

    connection_queue = []
    visited_cities = [0]

    connection_queue.extend(get_connection_list(0, distance_matrix))

    while connection_queue:
        (source_id, destination_id) = connection_queue.pop(0)

        total_distance += distance_matrix[source_id][destination_id]
        number_of_connections += 1

        if destination_id in visited_cities:
            continue
        else:
            connection_queue.extend(get_connection_list(destination_id, distance_matrix))
            visited_cities.append(destination_id)

    return total_distance / number_of_connections


def get_connection_list(city_id, distance_matrix):
    connection_list = []

    for destination_id in range(len(distance_matrix[city_id])):
        if distance_matrix[city_id][destination_id] is not None:
            connection_list.append((city_id, destination_id))

    return connection_list
