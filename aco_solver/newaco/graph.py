from random import Random


class Graph:
    initial_pheromone = 0.01

    def __init__(self, cities_distances, rho, q):
        self.rho = rho  # pheromone evaporation coefficient
        self.q = q  # pheromone deposit factor

        self.random_generator = Random()
        self.cities_distances = cities_distances
        self.cities_count = len(cities_distances)
        self.pheromone_matrix = [[self.initial_pheromone for _ in range(self.cities_count)] for _ in
                                 range(self.cities_count)]

    def calculate_total_distance(self, cities):
        total_distance = 0

        for i in range(len(cities) - 1):
            city_from = cities[i]
            city_to = cities[i + 1]

            total_distance += self.__distance(city_from, city_to)

        return total_distance

    def update_pheromones(self, ants):

        for i in range(self.cities_count):
            for j in range(self.cities_count):
                for ant in ants:
                    increase = 0.0
                    decrease = (1.0 - self.rho) * self.__pheromone(i, j)
                    if ant.contains_connection(i, j):
                        increase = (self.q / ant.distance)

                    self.__update_pheromone(i, j, increase + decrease)

    def calculate_path_attractiveness(self, alpha, beta, city_from, city_to):
        distance = self.__distance(city_from, city_to)
        pheromone = self.__pheromone(city_from, city_to)

        return (pheromone ** alpha) * ((1.0 / distance) ** beta)

    def __distance(self, city_from, city_to):
        return self.cities_distances[city_from][city_to]

    def __pheromone(self, city_from, city_to):
        return self.pheromone_matrix[city_from][city_to]

    def __update_pheromone(self, city_from, city_to, val):
        self.pheromone_matrix[city_from][city_to] = val
