class Graph(object):
    def __init__(self, distance_matrix, rho, q):
        number_of_cities = len(distance_matrix)

        cities = []
        for city_id in range(number_of_cities):
            cities.append(City(city_id))

        for i in range(number_of_cities):
            present_city = cities[i]
            for j in range(number_of_cities):
                if i == j:
                    continue

                present_city.create_and_add_connection(distance_matrix[i][j], cities[j])

        self.cities = cities
        self.number_of_cities = number_of_cities

        self.pheromone_evaporation = rho
        self.pheromone_deposit = q

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

    def compute_average_distance(self):

        total_distance = 0.0
        number_of_connections = 0

        connection_queue = []
        visited_cities = [self.cities[0]]
        connection_queue.extend(self.cities[0].connection_list)

        while connection_queue:
            connection = connection_queue.pop(0)
            total_distance += connection.distance
            number_of_connections += 1

            if connection.destination_city in visited_cities:
                continue
            else:
                connection_queue.extend(connection.destination_city.connection_list)
                visited_cities.append(connection.destination_city)

        return total_distance / number_of_connections


class City(object):
    def __init__(self, city_id, connection_list=None):
        if not connection_list:
            connection_list = []

        self.city_id = city_id
        self.connection_list = connection_list

    def add_connection(self, connection):
        if connection.destination_city.city_id == self.city_id:
            raise RuntimeError('Cannot add connection to itself')

        self.connection_list.append(connection)

    def create_and_add_connection(self, distance, destination_city):
        self.add_connection(Connection(distance, destination_city))

    def find_connection_to_city(self, city):
        for connection in self.connection_list:
            if connection.destination_city == city:
                return connection
        raise RuntimeError('Connection from city {} to city {} not found'.format(self.city_id, city.city_id))

    def __eq__(self, other):
        if isinstance(other, City):
            return self.city_id == other.city_id
        else:
            return False


class Connection(object):
    def __init__(self, distance, destination_city):
        self.distance = distance
        self.destination_city = destination_city
        self.pheromone = Pheromone()

    def accept_visitor(self, visitor, pheromone_value):
        visitor.visit(self, pheromone_value)


class Pheromone(object):
    def __init__(self, init_value=0.01):
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