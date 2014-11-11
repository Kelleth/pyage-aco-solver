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

    def update_pheromones(self, ants):
        # pheromone evaporation
        for city in self.cities:
            for connection in city.connection_list:
                connection.pheromone *= (1.0 - self.pheromone_evaporation)

        # increase value for visited connections
        for path in [ant.path for ant in ants]:
            for connection in path.connection_list:
                connection.pheromone += self.pheromone_deposit / path.distance

    def clean_connections_statistics(self):
        for city in self.cities:
            for connection in city.connection_list:
                connection.number_of_visits = 0


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
        self.pheromone = 0.01
        self.number_of_visits = 0

    def update_pheromone(self, value):
        self.pheromone += value

    def visit_connection(self):
        self.number_of_visits += 1