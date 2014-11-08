class Path(object):
    def __init__(self, start_city, connection_list):
        self.start_city = start_city
        self.connection_list = connection_list
        self.distance = self.calculate_distance(connection_list)

    def calculate_distance(self, connection_list):
        total_distance = 0.0
        for connection in connection_list:
            total_distance += connection.distance
        return total_distance

    def get_cities_list(self):
        cities = [self.start_city]
        cities.extend(connection.destination_city for connection in self.connection_list)
        return cities

    def __cmp__(self, other):
        if self.distance < other.distance:
            return -1
        elif self.distance > other.distance:
            return 1
        else:
            return 0

    def __str__(self):
        return 'Cities {}, distance {}'.format(self.distance, [city.city_id for city in self.get_cities_list()])