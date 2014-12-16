class Path(object):
    def __init__(self, start_city, connection_list):
        self.start_city = start_city
        self.connection_list = connection_list
        self.distance = self.calculate_distance(connection_list)

    def calculate_distance(self, connection_list):
        total_distance = 0.0
        for connection in connection_list:
            total_distance += connection.distance
        total_distance += connection_list[-1].destination_city.find_connection_to_city(self.start_city).distance
        return total_distance

    def get_cities_list(self):
        cities = [self.start_city]
        cities.extend(connection.destination_city for connection in self.connection_list)
        cities.append(self.start_city)
        return cities

    def __cmp__(self, other):
        if self.distance < other.distance:
            return -1
        elif self.distance > other.distance:
            return 1
        else:
            return 0

    def get_points(self):
        points = []
        for city in self.get_cities_list():
            points.append(city.get_position())
        return points

    def get_points_gnuplot(self):
        points = []
        for city in self.get_cities_list():
            points.append(city.get_position_string())

        return '\n'.join(points)

    def __str__(self):
        return 'Distance {}, path {}'.format(self.distance, [city.city_id for city in self.get_cities_list()])
