class ACOGraph:
    def __init__(self, cities_distances):
        self.cities_distances = cities_distances
        self.cities_count = len(cities_distances)
        self.pheromone_matrix = [[0.001 for _ in range(self.cities_count)] for _ in range(self.cities_count)]

    def distance(self, city_from, city_to):
        return self.cities_distances[city_from][city_to]

    def pheromone(self, city_from, city_to):
        return self.pheromone_matrix[city_from][city_to]

    def distance_attractiveness(self, city_from, city_to):
        return 1.0 / self.cities_distances[city_from][city_to]

    def set_pheromone(self, city_from, city_to, val):
        self.pheromone_matrix[city_from][city_to] = val

    def add_pheromone(self, city_from, city_to, val):
        self.pheromone_matrix[city_from][city_to] += val
